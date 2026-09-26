# Архитектура ТН ВЭД AI Classifier

```
USER
  │
  ▼
┌─────────────────┐
│  WEB / MOBILE   │  ← React / HTML / PWA
│   APPLICATION   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    SUPABASE     │  ← Auth + Database + Storage
│ Auth + Database │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI BACKEND    │  ← API: classify, calc, rates
│  AI Classifier  │
└────────┬────────┘
         │
 ┌───────┼────────────┐
 ▼       ▼            ▼
ТН ВЭД  Правила ОПИ  Ставки
 база
 │       │            │
 └───────┼────────────┘
         ▼
   AI анализирует товар
         │
         ▼
   Код ТН ВЭД
         │
         ▼
  Расчёт платежей
         │
         ▼
      RESULT
```

## Слои

### 1. WEB / MOBILE APPLICATION
- UI: калькулятор, AI-чат, поиск, загрузка Excel
- Клиент: HTML/JS (MVP) или React/Next.js
- Авторизация через Supabase Auth
- Запросы к AI Backend API

### 2. SUPABASE
- **Auth** — email / phone / OAuth
- **Database** — users, history, favorites, custom rates
- **Storage** — загруженные Excel, отчёты

### 3. AI BACKEND
- `POST /api/classify` — текст товара → кандидаты кодов
- `POST /api/calculate` — код + стоимость → платежи
- `GET /api/rates/:code` — ставка, НДС, меры
- Логика: NLP/LLM + правила ОПИ + база ТН ВЭД

### 4. Данные
| Источник | Содержание |
|----------|------------|
| ТН ВЭД база | 13 000+ кодов, наименования |
| Правила ОПИ | Основные правила интерпретации |
| Ставки | Пошлина, НДС, сборы, преференции |

### 5. RESULT
- Таможенный сбор
- Импортная пошлина
- НДС
- ИТОГО*
- Тарифные меры и преференции
