/** Stateless Next.js proxy. This module never imports the brain, scheduler or database. */
import { observationEnabled } from '../lib/awakening.ts';

export async function proxyRuntime(request: Request, endpoint: string) {
  if (!observationEnabled(process.env)) return Response.json({ error: 'Not found' }, { status: 404, headers: { 'Cache-Control': 'no-store' } });
  const base = process.env.GENESIS_API_URL;
  if (!base) return Response.json({ error: 'Genesis runtime is not connected. Configure GENESIS_API_URL.' }, { status: 503 });
  let destination:URL;try{destination=new URL(base);if(destination.username||destination.password||destination.search||destination.hash||!['https:','http:'].includes(destination.protocol)||(process.env.NODE_ENV==='production'&&destination.protocol!=='https:'&&!['127.0.0.1','localhost','[::1]'].includes(destination.hostname)))throw Error();}catch{return Response.json({error:'Observer connection unavailable'},{status:503});}
  const origin = request.headers.get('origin');
  if (request.method !== 'GET' && origin && origin !== new URL(request.url).origin) return Response.json({ error: 'Cross-origin request rejected' }, { status: 403 });
  const url = new URL(endpoint, base); url.search = new URL(request.url).search;
  const headers = new Headers({ 'Content-Type': 'application/json' });
  // Production public projection never forwards browser credentials. Private CLI is separate.
  if (process.env.NODE_ENV!=='production' && request.headers.has('authorization')) headers.set('authorization', request.headers.get('authorization')!);
  else if (process.env.NODE_ENV === 'development' && process.env.GENESIS_DEV_OPERATOR === 'true' && ['localhost','127.0.0.1'].includes(new URL(request.url).hostname) && process.env.GENESIS_OPERATOR_TOKEN) headers.set('authorization','Bearer '+process.env.GENESIS_OPERATOR_TOKEN);
  if (origin) headers.set('origin', origin);
  try {
    const body = request.method === 'GET' ? undefined : await request.text();
    if (body && body.length > 2000) return Response.json({ error: 'Request too large' }, { status: 413 });
    const response = await fetch(url, { method: request.method, headers, body, cache: 'no-store', redirect: 'error', signal: AbortSignal.timeout(50000) });
    return new Response(response.body, { status: response.status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
  } catch { return Response.json({ error: 'Genesis runtime is temporarily unreachable. Its saved life remains in Postgres.' }, { status: 503 }); }
}
