# ТН ВЭД AI System

Полная архитектура по схеме:

**USER → WEB/MOBILE → SUPABASE → AI BACKEND → (ТН ВЭД / ОПИ / Ставки) → RESULT**

## Структура

```
architecture/
├── ARCHITECTURE.md      # Схема слоёв
├── README.md
├── docs/FLOW.md         # Поток данных
├── frontend/            # WEB / MOBILE APPLICATION
│   └── index.html
├── backend/             # AI BACKEND
│   ├── README.md
│   └── api.example.js
└── supabase/
    └── schema.sql       # Auth + Database
```

## MVP сейчас

- `frontend/index.html` — работает офлайн (локальный AI + Excel)
- Backend и Supabase — заготовки под production

## Roadmap

1. ✅ Frontend калькулятор + AI-чат + карточка RESULT
2. ⬜ Supabase Auth + история расчётов
3. ⬜ AI Backend API (classify + calculate)
4. ⬜ Подключение LLM для классификации
5. ⬜ Mobile (PWA / React Native)
