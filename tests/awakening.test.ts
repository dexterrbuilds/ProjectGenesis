import test from 'node:test';
import assert from 'node:assert/strict';
import { awakeningTimestamp, countdownParts, developmentPreviewEnabled, observationEnabled } from '../lib/awakening.ts';
import { proxyRuntime } from '../server/runtime.ts';

test('absolute awakening time is independent of timezone notation and deployment time', () => {
  const target = awakeningTimestamp('2026-10-01T18:00:00Z');
  assert.equal(target, awakeningTimestamp('2026-10-01T11:00:00-07:00'));
  assert.deepEqual(countdownParts(target, target! - 90061000), [1, 1, 1, 1]);
  assert.deepEqual(countdownParts(target, target! - 1000), [0, 0, 0, 1]);
  assert.deepEqual(countdownParts(target, target! - 1), [0, 0, 0, 1]);
  assert.deepEqual(countdownParts(target, target!), [0, 0, 0, 0]);
  assert.deepEqual(countdownParts(target, target! + 100000), [0, 0, 0, 0]);
  assert.deepEqual(countdownParts(target, target! - 100 * 86400000), [100, 0, 0, 0]);
});

test('unannounced dates stay unannounced; ambiguous or invalid dates fail clearly', () => {
  assert.equal(awakeningTimestamp(undefined), null);
  assert.equal(awakeningTimestamp(''), null);
  assert.equal(countdownParts(null, Date.now()), null);
  for (const value of ['tomorrow', '2026-10-01', '2026-10-01T18:00:00', '2026-02-30T12:00:00Z', '2026-10-01T24:00:00Z']) {
    assert.throws(() => awakeningTimestamp(value), /GENESIS_AWAKENS_AT/);
  }
});

test('public access requires explicit live release; preview cannot be enabled in production', () => {
  assert.equal(observationEnabled({}), false);
  assert.equal(observationEnabled({ GENESIS_PUBLIC_MODE: 'LIVE' }), false);
  assert.equal(observationEnabled({ GENESIS_PUBLIC_MODE: 'live' }), true);
  for (const mode of ['production', 'test', undefined]) {
    assert.equal(developmentPreviewEnabled({ NODE_ENV: mode, GENESIS_DEV_PREVIEW: 'true' }), false);
    assert.equal(observationEnabled({ NODE_ENV: mode, GENESIS_DEV_PREVIEW: 'true' }), false);
  }
  assert.equal(developmentPreviewEnabled({ NODE_ENV: 'development' }), false);
  assert.equal(developmentPreviewEnabled({ NODE_ENV: 'development', GENESIS_DEV_PREVIEW: 'true' }), true);
});

test('dormant proxy blocks reads and mutations before contacting the runtime, even after the deadline', async t => {
  const original = { ...process.env };
  t.after(() => { process.env = original; });
  process.env = { ...process.env, NODE_ENV: 'production' };
  process.env.GENESIS_PUBLIC_MODE = 'dormant';
  process.env.GENESIS_DEV_PREVIEW = 'true';
  process.env.GENESIS_AWAKENS_AT = '2020-01-01T00:00:00Z';
  process.env.GENESIS_API_URL = 'http://runtime.invalid';
  const fetchMock = t.mock.method(globalThis, 'fetch', () => { throw new Error('Dormant page must not contact the runtime'); });
  for (const [path, method] of [['state', 'GET'], ['brain', 'GET'], ['history', 'GET'], ['cycle', 'POST'], ['control', 'POST']]) {
    const response = await proxyRuntime(new Request(`https://genesis.example/api/${path}?preview=true`, { method, headers: { authorization: 'Bearer anything' } }), `/api/${path}`);
    assert.equal(response.status, 404);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
  }
  assert.equal(fetchMock.mock.callCount(), 0);
});

test('explicit live release preserves the existing proxy behavior', async t => {
  const original = { ...process.env };
  t.after(() => { process.env = original; });
  process.env = { ...process.env, NODE_ENV: 'production' };
  process.env.GENESIS_PUBLIC_MODE = 'live';
  process.env.GENESIS_API_URL = 'https://runtime.example';
  const fetchMock = t.mock.method(globalThis, 'fetch', async (url: URL | RequestInfo, init?: RequestInit) => {
    assert.equal(String(url), 'https://runtime.example/api/state');
    assert.equal(new Headers(init?.headers).get('authorization'), null);
    return Response.json({ organism: { cycles: 7 } });
  });
  const response = await proxyRuntime(new Request('https://genesis.example/api/state'), '/api/state');
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { organism: { cycles: 7 } });
  assert.equal(fetchMock.mock.callCount(), 1);
});
