# Запуск всего бесплатно

## Вариант A — только браузер (уже работает)

Откройте `frontend/index.html` или `tnved_kalkulyator.html`  
AI и расчёт работают **офлайн**, без сервера.

## Вариант B — Frontend + бесплатный Backend

```bash
# 1. Backend
cd backend
python3 server.py

# 2. Frontend (другой терминал)
cd frontend
python3 -m http.server 3000
```

Frontend ходит на `http://127.0.0.1:8000` если backend запущен,  
иначе — встроенный локальный AI.

## Вариант C — полная база кодов (бесплатно)

1. https://www.tws.by/tws/tnved/download/excel  
2. Загрузить Excel во вкладке «Загрузка Excel»  
   **или**  
3. `python convert_tnved.py` → `backend/data/tnved.json`

## Supabase (опционально, free tier)

Не обязателен. Schema: `architecture/supabase/schema.sql`

## Итог

| Компонент | Платно? |
|-----------|---------|
| Frontend | Нет |
| AI Backend | Нет (локально) |
| База ТН ВЭД | Нет (tws.by) |
| Supabase | Нет (free tier, опционально) |
| LLM API | Не используется |
