import { createHash, timingSafeEqual } from 'node:crypto';
import { DEMO_EVENTS } from '../core/sensory.ts';
import type { GenesisService } from './service.ts';
export function isOperator(request: Request, secret: string) {
  const token = request.headers.get('authorization')?.replace(/^Bearer /, '') ?? '';
  return token.length <= 500 && timingSafeEqual(createHash('sha256').update(token).digest(), createHash('sha256').update(secret).digest());
}
const json = (value: unknown, status = 200) => Response.json(value, { status, headers: { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' } });
export async function handleRequest(request: Request, service: GenesisService): Promise<Response> {
  const url = new URL(request.url), operator = isOperator(request, service.config.operatorToken);
  try {
    if (request.method === 'GET') {
      if (url.pathname === '/healthz') { await service.store.read(); return json({ ok: true, service: 'project-genesis-runtime' }); }
      if (url.pathname === '/api/state') return json(await service.observe(operator));
      if (url.pathname === '/api/brain') return json(service.graph());
      if (url.pathname === '/api/history') {
        const id = url.searchParams.get('id'); if (id) { const decision = await service.store.decision(id); return json({ decision }, decision ? 200 : 404); }
        const before = Number(url.searchParams.get('before') ?? Number.MAX_SAFE_INTEGER);
        if (!Number.isSafeInteger(before) || before < 1) return json({ error: 'Invalid history cursor' }, 400);
        return json({ decisions: await service.store.history(before) });
      }
      return json({ error: 'Not found' }, 404);
    }
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
    if (!operator) return json({ error: 'Operator authorization required' }, 401);
    const origin = request.headers.get('origin');
    if (origin && !service.config.allowedOrigins.includes(origin)) return json({ error: 'Origin not allowed' }, 403);
    const raw = await request.text(); if (raw.length > 2000) return json({ error: 'Request too large' }, 413);
    let body: Record<string, unknown>; try { body = JSON.parse(raw || '{}'); } catch { return json({ error: 'Invalid JSON' }, 400); }
    if (!body || typeof body !== 'object' || Array.isArray(body)) return json({ error: 'Expected an object' }, 400);
    if (url.pathname === '/api/cycle') {
      const id = body.requestId ?? crypto.randomUUID(), event = body.event;
      if (typeof id !== 'string' || !/^[a-zA-Z0-9-]{8,80}$/.test(id)) return json({ error: 'Invalid request ID' }, 400);
      if (event !== undefined && (typeof event !== 'string' || !Object.hasOwn(DEMO_EVENTS, event))) return json({ error: 'Unknown event' }, 400);
      const result = await service.advance(id, event ? { id: id + ':event', ...DEMO_EVENTS[event as string] } : undefined);
      return result ? json(result) : json({ error: 'Cycle paused, busy, or daily budget reached' }, 409);
    }
    if (url.pathname === '/api/control') {
      if (Object.keys(body).some(k => !['paused','enabled','remainingCycles'].includes(k))) return json({ error: 'Unknown control' }, 400);
      if (body.paused !== undefined && typeof body.paused !== 'boolean') return json({ error: 'paused must be boolean' }, 400);
      if (body.enabled !== undefined && typeof body.enabled !== 'boolean') return json({ error: 'enabled must be boolean' }, 400);
      if (body.enabled === true && !service.config.autonomous) return json({ error: 'Enable GENESIS_AUTONOMY_ENABLED on the runtime first' }, 409);
      if (body.remainingCycles !== undefined && body.remainingCycles !== null && (!Number.isInteger(body.remainingCycles) || Number(body.remainingCycles) < 1 || Number(body.remainingCycles) > 100)) return json({ error: 'Run must contain 1–100 cycles' }, 400);
      if (body.paused === undefined && body.enabled === undefined) return json({ error: 'No control supplied' }, 400);
      await service.store.control(body as { paused?: boolean; enabled?: boolean; remainingCycles?: number | null }); return json({ ok: true });
    }
    return json({ error: 'Not found' }, 404);
  } catch (e) { console.error('Genesis request failed:', e instanceof Error ? e.message : 'Unknown error'); return json({ error: 'Runtime unavailable. Your committed life state is preserved; check runtime logs.' }, 503); }
}
