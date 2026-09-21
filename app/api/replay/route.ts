import {proxyRuntime} from '@/server/runtime';
export const runtime='nodejs';
export const dynamic='force-dynamic';
export async function GET(request:Request){return proxyRuntime(request,'/api/replay');}
