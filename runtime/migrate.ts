import pg from 'pg';
import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
export async function migrate(pool: pg.Pool) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN'); await client.query("SELECT pg_advisory_xact_lock(hashtext('project-genesis-schema'))");
    await client.query('CREATE TABLE IF NOT EXISTS genesis_migrations (version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW())');
    for (const file of ['001_genesis.sql','002_observations.sql']) {
      const version=file.split('_')[0];
      const applied=await client.query('SELECT version FROM genesis_migrations WHERE version=$1',[version]);
      if(!applied.rowCount) {
        await client.query(await readFile(new URL('./migrations/'+file,import.meta.url),'utf8'));
        await client.query('INSERT INTO genesis_migrations(version) VALUES($1)',[version]);
      }
    }
    await client.query('COMMIT');
  } catch (e) { await client.query('ROLLBACK'); throw e; } finally { client.release(); }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (!process.env.DATABASE_URL) throw new Error('DATABASE_URL is required');
  const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
  try { await migrate(pool); console.log('Project Genesis migrations applied.'); } finally { await pool.end(); }
}
