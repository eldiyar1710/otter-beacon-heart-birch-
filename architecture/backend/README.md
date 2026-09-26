# AI Backend — ТН ВЭД Classifier

## API

### POST /api/classify
```json
Request: { "text": "картофельные чипсы из Китая 500 кг", "lang": "ru" }
Response: {
  "candidates": [{ "code": "2005202000", "name": "...", "confidence": 0.92, "rate": "15%" }],
  "questions": ["Укажите таможенную стоимость"]
}
```

### POST /api/calculate
```json
Request: {
  "code": "2005202000",
  "value": 3500000,
  "weight": 500,
  "currency": "KZT",
  "country": "OTHER",
  "vat": 10
}
Response: {
  "duty": 525000,
  "fee": 25950,
  "vat": 717192,
  "total": 743142,
  "measures": "Режим третьей страны..."
}
```

### GET /api/tnved/:code
Информация по коду (ставка, ОПИ, сертификация)

## Стек
- Node.js / FastAPI
- LLM (Grok / OpenAI) для классификации
- PostgreSQL (Supabase) для кэша кодов

## ENV
```
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
GROK_API_KEY=
TNVED_DB_PATH=./data/tnved.json
```
