/** Pure fixture-only review tool. It cannot reserve, resolve secrets or send. */
import {validateAdmission,implementationHashes} from './factory.ts';
import {buildRequest} from './request.ts';
import {digest} from '../../core/v2/identity.ts';
import type {WorkingContext} from '../../core/v2/contracts.ts';
import type {CycleFence} from '../commit-v2.ts';
export function inspectFixtureAdmission(raw:unknown,context:WorkingContext,fence:CycleFence,at:string){
 const a=validateAdmission(raw);if(a.provider!=='fixture')throw Error('FIXTURE_ONLY');const r=buildRequest(a,context,fence,at);
 return {admissionHash:digest(a),requestHash:r.hash,wireHash:r.wireHash,completeRequestBytes:r.accounting.bytes,inputBound:r.accounting.inputBound,reservationMicros:r.reservationMicros,categories:a.rateCard.categories,secretReference:a.secretReference,implementation:implementationHashes(),audience:a.audience,knownAssumptions:['Injected deterministic fixture; no transport or secret resolved','Complete instructions/schema/context/wrapper accounted together','Rational microunit costs rounded upward per category'],unverifiedAssumptions:['No production tokenizer calibration','No production model, tariff, vendor protocol or endpoint admitted','Fixture prices and response usage are not biological or production measurements'],networkCalls:0};
}
