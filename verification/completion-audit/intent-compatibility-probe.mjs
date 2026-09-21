// Audit-only, pure in-memory reproduction of the record shape written by
// OneShotController.journal. No database, transport, model or runtime execution.
import {ProductFallback} from '../../core/v2/planner.ts';
import {digest} from '../../core/v2/identity.ts';
import {transitionIntent} from '../../core/v2/policy.ts';
import {writeFileSync} from 'node:fs';
const proposal=await new ProductFallback().propose({hash:'a'.repeat(64)});
const journalRecord={id:'audit:fixture:intent',payloadHash:digest(proposal),proposal,status:'proposed',receipt:null,attempts:0};
let error=null;try{transitionIntent(journalRecord,'denied','2026-09-20T00:00:00Z');}catch(e){error={name:e.name,message:e.message};}
const result={scope:'PURE AUDIT FIXTURE; NOT CANONICAL',recordSource:'server/one-shot.ts OneShotController.journal',consumer:'core/v2/policy.ts transitionIntent (used by LifeExtensionStore.recordIntentTransition)',missingCanonicalIntentFields:['organismId','policy','reservedMicros','approval'],transition:'proposed -> denied',result:error?'REJECTED':'ACCEPTED',error};
writeFileSync('verification/completion-audit/intent-compatibility.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
