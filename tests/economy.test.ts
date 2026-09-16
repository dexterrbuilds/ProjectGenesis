import test from 'node:test';
import assert from 'node:assert/strict';
import { SolanaReadOnlyWallet } from '../core/economy/adapters.ts';
import { readConfig } from '../runtime/config.ts';

test('Solana observer requests finalized balances and rejects inexact or failed RPC responses', async()=>{
  const address='11111111111111111111111111111111';
  const fetcher=(async (_url:string,init:RequestInit)=>{
    const request=JSON.parse(init.body as string);
    assert.equal(request.method,'getBalance');assert.deepEqual(request.params,[address,{commitment:'finalized'}]);
    assert.equal(init.redirect,'error');
    return Response.json({jsonrpc:'2.0',id:1,result:{value:1500000001}});
  }) as typeof fetch;
  const account=await new SolanaReadOnlyWallet('https://rpc.example',address,'devnet',fetcher).readAccount();
  assert.equal(account.balances[0].atomicUnits,'1500000001');assert.equal(account.balances[0].asset.network,'devnet');
  for(const payload of [{result:{value:9007199254740992}},{error:{message:'RPC unavailable'}},{result:{value:-1}}]) {
    await assert.rejects(new SolanaReadOnlyWallet('https://rpc.example',address,'devnet',(async()=>Response.json(payload)) as typeof fetch).readAccount(),/Invalid/);
  }
});
test('partial live-wallet configuration fails closed',()=>{
  const base={DATABASE_URL:'postgresql://localhost/test',GENESIS_OPERATOR_TOKEN:'test-token-at-least-24-characters'};
  assert.throws(()=>readConfig({...base,SOLANA_RPC_URL:'https://rpc.example'}),/Supply/);
  assert.throws(()=>readConfig({...base,SOLANA_RPC_URL:'http://rpc.example',SOLANA_WALLET_ADDRESS:'11111111111111111111111111111111',SOLANA_NETWORK:'devnet'}),/Invalid/);
  assert.equal(readConfig(base).solana,undefined);
});
