import type pg from 'pg';
import type {Organism} from '../core/contracts.ts';
import type {SnapshotRef} from '../core/v2/contracts.ts';
import {serializedDigest} from '../core/v2/identity.ts';
/** Match the saved bytes to a real legacy brainAfter, never to a computational event.
 * Earliest exact historical recording is stable even if later records repeat that snapshot.
 * No match means no timestamp/observation is invented. No canonical rows are changed.
 */
export async function savedSnapshotReference(db:Pick<pg.PoolClient,'query'>,snapshot:Organism['brain']):Promise<SnapshotRef|null>{
 if(!snapshot)return null;
 const row=(await db.query("SELECT id,at,record->>'at' AS recorded_at FROM genesis_decisions WHERE NOT (record ? 'schemaVersion') AND record->'brainAfter'=$1::jsonb ORDER BY cycle ASC LIMIT 1",[JSON.stringify(snapshot)])).rows[0];
 if(!row||!Number.isFinite(Date.parse(row.recorded_at))||new Date(row.at).getTime()!==Date.parse(row.recorded_at))return null;
 const bytes=JSON.stringify(snapshot);
 return {bytes,sha256:serializedDigest(snapshot),recordedAt:row.recorded_at,sourceDecisionId:row.id,parent:null};
}
