'use client';
import {memo,useEffect,useMemo,useRef} from 'react';
import type {BrainState,Node,Edge} from '@/core/contracts';
export type RecordedActivity={kind:'historical';frame:Pick<BrainState,'tick'|'activity'>;at:string|null};
/** Static anatomical schematic. Only explicitly supplied saved measurements affect activity brightness. */
export const ObserverNetwork=memo(function ObserverNetwork({nodes,edges,recording}:{nodes:Node[];edges:Edge[];recording?:RecordedActivity}){
 const canvas=useRef<HTMLCanvasElement>(null);
 const geometry=useMemo(()=>{const roles=[...new Set(nodes.map(n=>n.role))];const index=new Map(nodes.map((n,i)=>[n.id,i]));const points=nodes.map(n=>{const g=roles.indexOf(n.role),peers=nodes.filter(x=>x.role===n.role),i=peers.indexOf(n),angle=i*2.399963229728653,r=Math.sqrt((i+1)/peers.length);return {x:450+Math.cos(angle)*r*(125+g*31)+(g-2)*74,y:228+Math.sin(angle)*r*(95+g*9)+(g%2?22:-20)};});return {points,lines:edges.map(e=>[index.get(e.source)!,index.get(e.target)!])};},[nodes,edges]);
 useEffect(()=>{const el=canvas.current;if(!el)return;const draw=()=>{const c=el.getContext('2d');if(!c){el.setAttribute('data-unavailable','true');return;}const d=Math.min(window.devicePixelRatio||1,2),w=el.clientWidth,h=el.clientHeight;el.width=w*d;el.height=h*d;c.scale(w*d/900,h*d/460);c.clearRect(0,0,900,460);
  for(const [i,j] of geometry.lines){const a=geometry.points[i],b=geometry.points[j];if(!a||!b)continue;const strength=recording?Math.min(1,Math.max(0,recording.frame.activity[i]??0)*2):0;c.strokeStyle=`rgba(170,200,151,${.035+strength*.13})`;c.lineWidth=.45;c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.stroke();}
  geometry.points.forEach((p,i)=>{const v=recording?Math.min(1,Math.max(0,recording.frame.activity[i]??0)*3):0;c.fillStyle=`rgba(202,222,184,${.42+v*.58})`;c.beginPath();c.arc(p.x,p.y,1.8+v*2,0,Math.PI*2);c.fill();});};draw();const resize=new ResizeObserver(draw);resize.observe(el);return()=>resize.disconnect();},[geometry,recording]);
 return <div className="observer-network"><canvas ref={canvas} role="img" aria-label={`C. elegans, ${nodes.length} named neurons connected by genuine anatomical data. ${recording?'Historical saved activity, not live.':'Static structure only; no new neural activity.'} Positions are schematic.`}>A structural map of the C. elegans connectome. No current neural activity is shown.</canvas><p className="canvas-fallback">The visual map is unavailable. C. elegans has 302 named neurons in this dataset; no current neural activity is shown.</p></div>;
});
