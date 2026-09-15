import type { LedgerEntry, WalletAdapter, WalletState } from './contracts.ts';
import { LIMITS } from './policy.ts';
export class SimulatedWallet implements WalletAdapter {
  private state: WalletState;
  constructor(state: WalletState) {
    this.state = structuredClone(state);
    if (!Number.isSafeInteger(state.startingCents) || state.startingCents < 0 || state.startingCents > 100000000) throw new Error('Invalid starting capital');
    const ids = new Set();
    for (const entry of state.entries) { this.validate(entry); if (ids.has(entry.id)) throw new Error('Duplicate ledger id'); ids.add(entry.id); }
    if (!Number.isSafeInteger(this.balance()) || this.balance() < 0) throw new Error('Invalid wallet balance');
  }
  private validate(entry: LedgerEntry) {
    if (!entry.id || !Number.isSafeInteger(entry.cents) || !['business_income', 'trading_fee_income', 'expense', 'investment_pnl'].includes(entry.kind)) throw new Error('Invalid ledger entry');
    if (entry.kind === 'expense' ? entry.cents >= 0 : entry.kind !== 'investment_pnl' && entry.cents < 0) throw new Error('Invalid ledger sign');
  }
  balance() { return this.state.startingCents + this.state.entries.reduce((sum, e) => sum + e.cents, 0); }
  post(entry: LedgerEntry) {
    this.validate(entry);
    const existing = this.state.entries.find(e => e.id === entry.id);
    if (existing) { if (JSON.stringify(existing) !== JSON.stringify(entry)) throw new Error('Ledger idempotency conflict'); return; }
    if (entry.cents < 0 && (-entry.cents > LIMITS.maxExpenseCents || this.balance() + entry.cents < LIMITS.reserveCents)) throw new Error('Expense limit or capital reserve reached');
    if (!Number.isSafeInteger(this.balance() + entry.cents)) throw new Error('Balance overflow');
    this.state.entries.push(structuredClone(entry));
  }
  getState() { return structuredClone(this.state); }
}
export function economics(state: WalletState, businesses = 0) {
  const sum = (kind: LedgerEntry['kind']) => state.entries.filter(e => e.kind === kind).reduce((s, e) => s + e.cents, 0);
  const cash = state.startingCents + state.entries.reduce((s, e) => s + e.cents, 0);
  return { cash, netWorth: cash, totalEarned: sum('business_income') + sum('trading_fee_income'), totalSpent: -sum('expense'), tradingFeeIncome: sum('trading_fee_income'), businessIncome: sum('business_income'), investmentPnl: sum('investment_pnl'), businessesCreated: businesses, humansHired: 0 };
}
