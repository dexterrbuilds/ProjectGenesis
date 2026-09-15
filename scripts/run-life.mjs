// Browser-independent bounded runner. Ctrl-C stops after the current request.
const origin = process.env.GENESIS_ORIGIN ?? 'http://localhost:3001';
const cycles = Number(process.env.GENESIS_CYCLES ?? 12);
const interval = Number(process.env.GENESIS_INTERVAL_MS ?? 10000);
if (!Number.isInteger(cycles) || cycles < 1 || cycles > 100 || !Number.isFinite(interval) || interval < 1000 || interval > 3600000) throw new Error('Use 1–100 cycles and a 1s–1h interval');
let stopped = false; process.on('SIGINT', () => { stopped = true; });
for (let i = 0; i < cycles && !stopped; i++) {
  const r = await fetch(new URL('/api/cycle', origin), { method: 'POST', headers: { 'Content-Type': 'application/json', ...(process.env.GENESIS_OPERATOR_TOKEN ? { Authorization: `Bearer ${process.env.GENESIS_OPERATOR_TOKEN}` } : {}) }, body: JSON.stringify({ requestId: crypto.randomUUID() }), signal: AbortSignal.timeout(55000) });
  const data = await r.json(); if (!r.ok) throw new Error(data.error ?? `HTTP ${r.status}`);
  console.log(data.decision.cycle, data.decision.neural.behavior, data.decision.outcome.title);
  if (!data.decision.outcome.ok) break;
  if (i < cycles - 1 && !stopped) await new Promise(resolve => setTimeout(resolve, interval));
}
