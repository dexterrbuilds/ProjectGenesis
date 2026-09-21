/** Deliberately accepts no free-form text, error object, URL, request or context. */
export function logRecord(service:'runtime'|'consumer'|'migration',status:'STARTED'|'STOPPING'|'STOPPED'|'READY'|'NOT_READY'|'REFUSED'|'COMPLETED',runtimeHash?:string){
 return JSON.stringify({at:new Date().toISOString(),service,status,...(runtimeHash&&/^[a-f0-9]{64}$/.test(runtimeHash)?{runtimeHash}:{})});
}
