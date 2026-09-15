export type RuntimeConfig = {
  databaseUrl: string; operatorToken: string; port: number; host: string; intervalMs: number;
  maxDailyCycles: number; autonomous: boolean; internet: boolean; startingCents: number;
  apiKey?: string; model?: string; plannerMode: 'auto' | 'local' | 'openai'; allowedOrigins: string[];
};
export function readConfig(env: Record<string, string | undefined> = process.env): RuntimeConfig {
  const integer = (name: string, fallback: number, min: number, max: number) => { const v = Number(env[name] || fallback); if (!Number.isSafeInteger(v) || v < min || v > max) throw new Error(`Invalid ${name}`); return v; };
  if (!env.DATABASE_URL) throw new Error('DATABASE_URL is required. Persistence never falls back to memory or filesystem.');
  if (!env.GENESIS_OPERATOR_TOKEN || env.GENESIS_OPERATOR_TOKEN.length < 24) throw new Error('GENESIS_OPERATOR_TOKEN must have at least 24 characters.');
  const mode = env.GENESIS_PLANNER_MODE ?? 'auto';
  if (!['auto', 'local', 'openai'].includes(mode)) throw new Error('Invalid GENESIS_PLANNER_MODE');
  if (mode !== 'local' && (!!env.OPENAI_API_KEY !== !!env.OPENAI_MODEL || (mode === 'openai' && !env.OPENAI_API_KEY))) throw new Error('Supply both OPENAI_API_KEY and OPENAI_MODEL for the language planner.');
  return { databaseUrl: env.DATABASE_URL, operatorToken: env.GENESIS_OPERATOR_TOKEN, port: integer('PORT', 3001, 1, 65535), host: env.HOST || '0.0.0.0', intervalMs: integer('GENESIS_INTERVAL_MS', 30000, 1000, 3600000), maxDailyCycles: integer('GENESIS_MAX_DAILY_CYCLES', 200, 1, 10000), autonomous: env.GENESIS_AUTONOMY_ENABLED === 'true', internet: env.GENESIS_INTERNET === 'true', startingCents: integer('GENESIS_STARTING_CENTS', 10000, 0, 100000000), apiKey: env.OPENAI_API_KEY || undefined, model: env.OPENAI_MODEL || undefined, plannerMode: mode as RuntimeConfig['plannerMode'], allowedOrigins: (env.GENESIS_ALLOWED_ORIGINS ?? 'http://localhost:5173,http://127.0.0.1:5173').split(',').map(x => x.trim()).filter(Boolean) };
}
