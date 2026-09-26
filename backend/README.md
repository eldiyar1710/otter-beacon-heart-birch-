# AI Backend — бесплатно

Локальный сервер без платных API.

## Запуск

```bash
cd backend
python3 server.py
```

http://127.0.0.1:8000

## API

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/health` | Статус |
| POST | `/api/classify` | Текст → коды ТН ВЭД |
| POST | `/api/calculate` | Код + стоимость → платежи |
| GET | `/api/tnved/:code` | Инфо по коду |
| GET | `/api/search?q=` | Поиск |

## Полная база (бесплатно)

1. Excel: https://www.tws.by/tws/tnved/download/excel
2. `python convert_tnved.py`
3. JSON → `backend/data/tnved.json`
4. Перезапуск server.py

Без OpenAI / Grok / облака.
