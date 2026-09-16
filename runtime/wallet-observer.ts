import type pg from 'pg';
import type { ExternalWalletReader, WalletAccount } from '../core/economy/adapters.ts';
export type WalletObservation = { account: WalletAccount | null; checkedAt: string; error: string | null };
/** No signing or transfers. A failed read retains its last good value with a visible error. */
export class WalletObserver {
  private pool: pg.Pool; private reader: ExternalWalletReader; private key: string; private pending?: Promise<void>;
  constructor(pool: pg.Pool, reader: ExternalWalletReader, key: string) { this.pool=pool;this.reader=reader;this.key=key; }
  async get(): Promise<WalletObservation | null> { return (await this.pool.query('SELECT record FROM genesis_external_observations WHERE id=$1',[this.key])).rows[0]?.record ?? null; }
  async refresh() {
    if(this.pending) return this.pending;
    this.pending=this.poll().finally(()=>{this.pending=undefined;});return this.pending;
  }
  private async poll() {
    const previous=await this.get();
    if(previous&&Date.now()-Date.parse(previous.checkedAt)<60000) return;
    const checkedAt=new Date().toISOString();
    let observation:WalletObservation;
    try {observation={account:await this.reader.readAccount(),checkedAt,error:null};}
    catch {observation={account:previous?.account ?? null,checkedAt,error:'Wallet observation failed. Last successful balance may be stale.'};}
    await this.pool.query('INSERT INTO genesis_external_observations(id,checked_at,record) VALUES($1,$2,$3) ON CONFLICT(id) DO UPDATE SET checked_at=EXCLUDED.checked_at,record=EXCLUDED.record WHERE genesis_external_observations.checked_at<EXCLUDED.checked_at',[this.key,checkedAt,observation]);
  }
}
