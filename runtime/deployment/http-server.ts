import {createServer,type Server} from 'node:http';
import type pg from 'pg';
import type {GenesisService} from '../service.ts';
import {handleRequest} from '../http.ts';
import {inspectReadiness} from './readiness.ts';
/** Only health is available without a matching release. No private/control surface here. */
export function observationServer(service:GenesisService,pool:pg.Pool,expected:{organismId:string;bornAt:string}){
 let active=0,tokens=120,refill=Date.now();
 const server=createServer(async(req,res)=>{
 let counted=false;try{
 const path=new URL(req.url??'/','http://runtime').pathname;
 if(req.method!=='GET'){res.writeHead(405);res.end();return;}
 if(path==='/health'||path==='/healthz'){res.writeHead(200,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end('{"alive":true}');return;}
 const now=Date.now();if(now-refill>=60000){tokens=120;refill=now;}if(active>=8||tokens<=0){res.writeHead(429,{'Retry-After':'5'});res.end();return;}tokens--;active++;counted=true;
 const readiness=await inspectReadiness(pool,expected,'reader');
 if(path==='/readiness'||!readiness.ready){res.writeHead(readiness.ready?200:503,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(readiness));return;}
 // Ignore user authorization entirely: this process serves public DTOs only.
 const r=await handleRequest(new Request(new URL(req.url??'/','http://runtime')),service);
 res.writeHead(r.status,Object.fromEntries(r.headers));res.end(await r.text());
 }catch{res.writeHead(503,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end('{"ready":false}');}finally{if(counted)active--;}
 });server.maxConnections=64;server.requestTimeout=20000;server.headersTimeout=10000;server.keepAliveTimeout=5000;return server;
}
export async function stopObservation(server:Server,pool:pg.Pool,deadlineMs=10000){
 const timer=setTimeout(()=>server.closeAllConnections(),Math.floor(deadlineMs/2));
 const deadline=setTimeout(()=>{process.exitCode=1;server.closeAllConnections();},deadlineMs);deadline.unref();
 try{await new Promise<void>(resolve=>{server.close(()=>resolve());server.closeIdleConnections();});await pool.end();}finally{clearTimeout(timer);clearTimeout(deadline);}
}
