#!/usr/bin/env python3
"""
ТН ВЭД AI Backend — бесплатно, локально
Запуск: python3 server.py
API: http://127.0.0.1:8000
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8000
DATA = Path(__file__).parent / "data"
DEMO_DB = [
    {"code": "2005202000", "name": "Картофель нарезанный тонкими ломтиками (чипсы/криспы)", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 10},
    {"code": "1905905500", "name": "Экструдированные продукты острые/солёные", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 10},
    {"code": "1905100000", "name": "Хрустящие хлебцы (crispbread)", "rate": "15%, не менее 0.15 евро/кг", "rateType": "combined", "rateValue": 15, "specific": 0.15, "vat": 10},
    {"code": "2104100000", "name": "Супы и бульоны и заготовки для них", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 10},
    {"code": "2104200000", "name": "Гомогенизированные составные пищевые продукты", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 10},
    {"code": "2005201000", "name": "Картофель в виде муки, хлопьев", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 10},
    {"code": "0901210000", "name": "Кофе жареный с кофеином", "rate": "10%", "rateType": "advalorem", "rateValue": 10, "vat": 20},
    {"code": "8470100000", "name": "Калькуляторы электронные", "rate": "0%", "rateType": "advalorem", "rateValue": 0, "vat": 20},
    {"code": "1704909900", "name": "Прочие кондитерские изделия из сахара", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 20},
    {"code": "2202100000", "name": "Воды газированные с сахаром", "rate": "15%", "rateType": "advalorem", "rateValue": 15, "vat": 20},
]

def load_db():
    p = DATA / "tnved.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return list(DEMO_DB)

DB = load_db()

def classify(text: str) -> dict:
    t = (text or "").lower()
    keys = []
    if re.search(r"чип|крисп|chips|crisp|снек", t):
        keys += ["чип", "ломтик", "экструд", "2005", "1905"]
    if re.search(r"бульон|суп|broth|soup", t):
        keys += ["бульон", "суп", "2104"]
    if re.search(r"хлебц|crispbread", t):
        keys += ["хлебц", "1905"]
    if re.search(r"кофе", t):
        keys += ["кофе", "0901"]
    if re.search(r"калькулятор", t):
        keys += ["калькулятор", "8470"]
    if not keys:
        keys = [w for w in re.split(r"\s+", t) if len(w) > 3][:5]
    scored = []
    for item in DB:
        name = (item.get("name") or "").lower()
        code = item.get("code") or ""
        score = sum(2 for k in keys if k in name or k in code)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    candidates = []
    for score, item in scored[:5]:
        candidates.append({
            "code": item["code"],
            "name": item.get("name", ""),
            "rate": item.get("rate", ""),
            "confidence": min(0.95, 0.5 + score * 0.08),
            "vat": item.get("vat", 20),
            "rateType": item.get("rateType", "advalorem"),
            "rateValue": item.get("rateValue", 15),
            "specific": item.get("specific"),
        })
    questions = []
    if not re.search(r"\d+\s*(тенге|тг|руб|₸|₽|kg|кг)", t, re.I):
        questions.append("Укажите таможенную стоимость и вес (кг)")
    if not candidates:
        questions.append("Уточните название товара или загрузите полную базу")
    return {"candidates": candidates, "questions": questions, "product": text}

def customs_fee(value: float, currency: str) -> float:
    if currency == "RUB":
        if value <= 200000: return 1231
        if value <= 450000: return 2462
        if value <= 1200000: return 4924
        if value <= 2700000: return 13541
        if value <= 4200000: return 18465
        if value <= 5500000: return 21344
        if value <= 10000000: return 49240
        return 73860
    if value <= 500000: return 5000
    if value <= 2000000: return 15000
    if value <= 5000000: return 25950
    if value <= 10000000: return 45000
    return 75000

def calculate(body: dict) -> dict:
    code = str(body.get("code", "")).replace(" ", "")
    value = float(body.get("value") or 0)
    weight = float(body.get("weight") or 0)
    currency = body.get("currency") or "KZT"
    country = body.get("country") or "OTHER"
    vat_rate = float(body.get("vat") or 20)
    eur = float(body.get("eur") or 500)
    item = next((x for x in DB if x["code"] == code or x["code"].startswith(code)), None)
    if item and not body.get("vat"):
        vat_rate = float(item.get("vat") or 20)
    duty = 0.0
    duty_text = ""
    if country == "EAEU":
        duty = 0.0
        duty_text = "0 (ЕАЭС)"
    elif item:
        rt = item.get("rateType", "advalorem")
        rv = float(item.get("rateValue") or 15)
        if rt == "advalorem":
            duty = value * (rv / 100)
            duty_text = f"{duty:.2f} ({rv}%)"
        elif rt == "combined":
            adv = value * (rv / 100)
            spec = float(item.get("specific") or 0) * weight * eur
            duty = max(adv, spec)
            duty_text = f"{duty:.2f} (комб.)"
        else:
            duty = value * 0.15
            duty_text = f"{duty:.2f}"
    else:
        duty = value * 0.15
        duty_text = f"{duty:.2f} (~15%)"
    fee = customs_fee(value, currency)
    vat = (value + duty + fee) * (vat_rate / 100)
    total = duty + fee + vat
    if country == "EAEU":
        measures = "Тарифные меры: пошлина 0% (ЕАЭС). Преференции ЕАЭС."
    elif country == "CIS":
        measures = "Возможны преференции СНГ (сертификат СТ-1)."
    else:
        measures = "Режим третьей страны (ЕТТ). Преференции возможны при сертификате происхождения / ЗСТ / НРС."
    return {
        "code": code,
        "name": (item or {}).get("name", ""),
        "duty": round(duty, 2),
        "dutyText": duty_text,
        "fee": round(fee, 2),
        "vat": round(vat, 2),
        "vatRate": vat_rate,
        "total": round(total, 2),
        "currency": currency,
        "measures": measures,
        "note": "Приведённый расчёт является базовым. Товар может попадать под дополнительные тарифные меры и преференции.",
    }

class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/api/health"):
            return self._json(200, {"ok": True, "service": "tnved-ai-free", "codes": len(DB)})
        if path.startswith("/api/tnved/"):
            code = path.split("/api/tnved/")[-1].strip()
            item = next((x for x in DB if x["code"] == code), None)
            if not item:
                return self._json(404, {"error": "not found"})
            return self._json(200, item)
        if path == "/api/search":
            qs = parse_qs(urlparse(self.path).query)
            q = (qs.get("q") or [""])[0].lower()
            found = [x for x in DB if q in x["code"] or q in (x.get("name") or "").lower()][:50]
            return self._json(200, {"results": found})
        self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            return self._json(400, {"error": "invalid json"})
        path = urlparse(self.path).path
        if path == "/api/classify":
            return self._json(200, classify(body.get("text") or ""))
        if path == "/api/calculate":
            if not body.get("code") or not body.get("value"):
                return self._json(400, {"error": "code and value required"})
            return self._json(200, calculate(body))
        self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

def main():
    DATA.mkdir(parents=True, exist_ok=True)
    print(f"ТН ВЭД AI Backend (FREE) → http://127.0.0.1:{PORT}")
    print(f"Кодов в базе: {len(DB)}")
    print("POST /api/classify  |  POST /api/calculate  |  GET /api/health")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

if __name__ == "__main__":
    main()
