/**
 * Пример AI Backend API (Node.js / Express)
 * Схема: classify → calculate → result
 */

async function classify(req, res) {
  const { text, lang = "ru" } = req.body;
  // 1. LLM / keyword → кандидаты из ТН ВЭД базы
  // 2. Правила ОПИ
  // 3. Вернуть candidates + questions
  res.json({ candidates: [], questions: [] });
}

async function calculate(req, res) {
  const { code, value, weight, currency, country, vat } = req.body;
  // 1. Ставка по коду
  // 2. Пошлина
  // 3. Сбор (РФ / KZ)
  // 4. НДС
  // 5. Тарифные меры / преференции
  res.json({ duty: 0, fee: 0, vat: 0, total: 0, measures: "" });
}

module.exports = { classify, calculate };
