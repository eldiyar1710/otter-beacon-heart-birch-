/** Бесплатный AI Backend client + fallback */
window.TNVED_API = "http://127.0.0.1:8000";

async function apiHealth() {
  try {
    const r = await fetch(window.TNVED_API + "/api/health", { signal: AbortSignal.timeout(1500) });
    return r.ok ? await r.json() : null;
  } catch { return null; }
}

async function apiClassify(text) {
  try {
    const r = await fetch(window.TNVED_API + "/api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
      signal: AbortSignal.timeout(5000),
    });
    if (r.ok) return await r.json();
  } catch {}
  return null;
}

async function apiCalculate(payload) {
  try {
    const r = await fetch(window.TNVED_API + "/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(5000),
    });
    if (r.ok) return await r.json();
  } catch {}
  return null;
}
