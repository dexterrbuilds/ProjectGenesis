/** External chain amounts stay separate from the simulated USD-cent wallet. */
export type Asset = { chain: 'solana'; network: 'devnet' | 'mainnet-beta'; mint: 'native' | string; symbol: string; decimals: number };
export type AssetAmount = { asset: Asset; atomicUnits: string };
export type WalletAccount = { address: string; balances: AssetAmount[]; observedAt: string };
export type IncomeReceipt = { id: string; source: 'clawpump_fee' | 'business'; transaction: string; recipient: string; amount: AssetAmount; finalized: true; at: string };
export interface ExternalWalletReader { readAccount(): Promise<WalletAccount> }
export interface IncomeAdapter { poll(cursor?: string): Promise<{ receipts: IncomeReceipt[]; cursor?: string }> }
export type ApprovalIntent = { id: string; status: 'pending'; kind: 'transfer' | 'investment'; recipient: string; amount: AssetAmount; rationale: string };
export interface ApprovedTransactionExecutor {
  // Deliberately not implemented or supplied to Genesis. Requires an external
  // human approval service, idempotency, durable outbox and reconciliation.
  executeApproved(intent: ApprovalIntent, approvalId: string): Promise<{ transaction: string }>;
}
export function validateAmount(amount: AssetAmount) {
  if (!/^\d+$/.test(amount.atomicUnits) || !Number.isInteger(amount.asset.decimals) || amount.asset.decimals < 0 || amount.asset.decimals > 18) throw new Error('Invalid asset amount');
  if (BigInt(amount.atomicUnits) < 0n) throw new Error('Negative amount');
}
export function sameAsset(a: Asset, b: Asset) { return a.chain === b.chain && a.network === b.network && a.mint === b.mint && a.decimals === b.decimals; }
export function requestFinancialAction(intent: Omit<ApprovalIntent, 'status'>, cap: AssetAmount): ApprovalIntent {
  validateAmount(intent.amount); validateAmount(cap);
  if (!sameAsset(intent.amount.asset, cap.asset)) throw new Error('Asset mismatch; no implicit exchange rate conversion');
  if (BigInt(intent.amount.atomicUnits) > BigInt(cap.atomicUnits)) throw new Error('Financial approval-request limit exceeded');
  if (!intent.recipient || !intent.rationale || !intent.id) throw new Error('Incomplete approval request');
  return { ...structuredClone(intent), status: 'pending' };
}
export class SolanaReadOnlyWallet implements ExternalWalletReader {
  private rpcUrl: string; private address: string; private network: Asset['network']; private fetcher: typeof fetch;
  constructor(rpcUrl: string, address: string, network: Asset['network'], fetcher: typeof fetch = fetch) {
    if (new URL(rpcUrl).protocol !== 'https:' || !/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(address)) throw new Error('Configure an HTTPS Solana RPC and valid base58 address');
    this.rpcUrl = rpcUrl; this.address = address; this.network = network; this.fetcher = fetcher;
  }
  async readAccount(): Promise<WalletAccount> {
    const r = await this.fetcher(this.rpcUrl, { method: 'POST', redirect: 'error', signal: AbortSignal.timeout(8000), headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'getBalance', params: [this.address, { commitment: 'finalized' }] }) });
    if (!r.ok) throw new Error(`Solana RPC HTTP ${r.status}`);
    const data = await r.json() as { error?: unknown; result?: { value: number } };
    const lamports = data.result?.value;
    if (data.error || !Number.isSafeInteger(lamports) || lamports! < 0) throw new Error('Invalid or inexact Solana balance');
    return { address: this.address, observedAt: new Date().toISOString(), balances: [{ asset: { chain: 'solana', network: this.network, mint: 'native', symbol: 'SOL', decimals: 9 }, atomicUnits: String(lamports) }] };
  }
}
/** ClawPump API/receipt verification is injected after its actual integration is agreed.
 * No endpoint, credential, fees or income is fabricated. No signing method exists. */
export class ClawPumpFeeIncomeAdapter implements IncomeAdapter {
  private reader: IncomeAdapter; private recipient: string;
  constructor(verifiedReader: IncomeAdapter, recipient: string) { this.reader = verifiedReader; this.recipient = recipient; }
  async poll(cursor?: string) {
    const page = await this.reader.poll(cursor);
    const ids = new Set<string>();
    for (const r of page.receipts) {
      validateAmount(r.amount);
      if (!r.finalized || r.source !== 'clawpump_fee' || r.recipient !== this.recipient || !r.transaction || !r.id || ids.has(r.id)) throw new Error('Unverified, duplicate or mismatched fee receipt');
      ids.add(r.id);
    }
    return structuredClone(page);
  }
}
