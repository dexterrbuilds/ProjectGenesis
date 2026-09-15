import { createServer } from 'node:http';
import pg from 'pg';
import { readConfig } from './config.ts';
import { migrate } from './migrate.ts';
import { LifeStore } from '../server/store.ts';
import { CElegansBrain } from '../core/brain/celegans.ts';
import { LocalPlanner, OpenAIPlanner } from '../core/planner.ts';
import { GenesisService } from './service.ts';
import { LifeScheduler } from './scheduler.ts';
import { handleRequest } from './http.ts';
const config = readConfig();
const pool = new pg.Pool({ connectionString: config.databaseUrl, max: 8, connectionTimeoutMillis: 10000, statement_timeout: 15000 });
pool.on('error', e => console.error('Database pool error:', e.message));
await migrate(pool);
const store = new LifeStore(pool); await store.initialize(config.startingCents);
const planner = config.plannerMode !== 'local' && config.apiKey && config.model ? new OpenAIPlanner(config.apiKey, config.model) : new LocalPlanner();
const service = new GenesisService(store, config, () => new CElegansBrain(), planner);
const scheduler = new LifeScheduler(service);
const server = createServer(async (req, res) => {
  try {
    let bytes = 0; const chunks = [];
    for await (const chunk of req) { bytes += chunk.length; if (bytes > 8192) { res.writeHead(413); res.end('Request too large'); return; } chunks.push(chunk); }
    const headers = new Headers(); for (const [key, value] of Object.entries(req.headers)) if (typeof value === 'string') headers.set(key, value);
    const method = req.method ?? 'GET';
    const request = new Request(new URL(req.url ?? '/', 'http://genesis-runtime'), { method, headers, ...(method !== 'GET' && method !== 'HEAD' ? { body: Buffer.concat(chunks) } : {}) });
    const response = await handleRequest(request, service); res.writeHead(response.status, Object.fromEntries(response.headers)); res.end(await response.text());
  } catch { res.writeHead(500); res.end('Runtime request failed'); }
});
server.requestTimeout = 55000; server.headersTimeout = 10000;
server.listen(config.port, config.host, () => { console.log(`Project Genesis runtime listening on ${config.host}:${config.port}; planner=${planner instanceof OpenAIPlanner ? 'openai' : 'local'}; scheduler=${config.autonomous}`); scheduler.start(); });
let stopping = false;
async function shutdown() { if (stopping) return; stopping = true; const closed = new Promise<void>(resolve => server.close(() => resolve())); await scheduler.stop(); await closed; await pool.end(); }
process.on('SIGTERM', () => void shutdown()); process.on('SIGINT', () => void shutdown());
