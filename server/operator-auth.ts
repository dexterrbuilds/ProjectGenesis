/** Private server/CLI authentication. Attribution strings never authenticate a caller. */
import {createHash,timingSafeEqual} from 'node:crypto';
import {z} from 'zod';
export const CAPABILITIES=['VIEW_PRIVATE_STATE','REVIEW_DISCLOSURE','MANAGE_ONE_SHOT','MANAGE_CONTINUOUS','RECORD_HUMAN_RESPONSE','INSPECT_RECOVERY','RESOLVE_RECOVERY','MANAGE_PROVIDER_ADMISSION'] as const;
export type Capability=typeof CAPABILITIES[number];
const key=z.object({id:z.string().min(1).max(100),actorId:z.string().min(1).max(100),sha256:z.string().regex(/^[a-f0-9]{64}$/),expiresAt:z.string().datetime()}).strict();
const configSchema=z.object({enabled:z.literal(true),mode:z.enum(['production','test']),keys:z.array(key).min(1).max(20)}).strict();
export type Principal={readonly actorId:string;readonly mode:'production'|'test'};
export class OperatorAuthentication{
 private config:z.infer<typeof configSchema>;private issued=new WeakMap<object,{until:number;keyId:string}>();
 constructor(raw:unknown){const c=configSchema.safeParse(raw);if(!c.success)throw Error('OPERATOR_AUTH_UNAVAILABLE');if(new Set(c.data.keys.map(k=>k.id)).size!==c.data.keys.length||new Set(c.data.keys.map(k=>k.sha256)).size!==c.data.keys.length)throw Error('OPERATOR_AUTH_UNAVAILABLE');this.config=c.data;}
 authenticate(credential:string):Principal{
  if(typeof credential!=='string'||credential.length<32||credential.length>500)throw Error('OPERATOR_AUTH_FAILED');
  const hash=createHash('sha256').update(credential).digest();let found:typeof this.config.keys[number]|undefined;
  for(const k of this.config.keys){const equal=timingSafeEqual(hash,Buffer.from(k.sha256,'hex'));if(equal&&Date.parse(k.expiresAt)>Date.now())found=k;}
  if(!found)throw Error('OPERATOR_AUTH_FAILED');const p=Object.freeze({actorId:found.actorId,mode:this.config.mode});this.issued.set(p,{keyId:found.id,until:Math.min(Date.now()+300000,Date.parse(found.expiresAt))});return p;
 }
 assert(p:Principal){const issued=this.issued.get(p);if(!issued||issued.until<=Date.now()||!this.config.keys.some(k=>k.id===issued.keyId&&k.actorId===p.actorId&&Date.parse(k.expiresAt)>Date.now()))throw Error('OPERATOR_AUTH_FAILED');}
 /** Replacing the external configuration revokes removed keys, including cached principals. */
 rotate(raw:unknown){const replacement=new OperatorAuthentication(raw);if(replacement.config.mode!==this.config.mode)throw Error('OPERATOR_AUTH_UNAVAILABLE');this.config=replacement.config;this.issued=new WeakMap();}
}
