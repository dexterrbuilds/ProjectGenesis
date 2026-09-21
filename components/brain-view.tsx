'use client';
import { useEffect, useMemo, useRef, useState } from 'react';
import type { BrainState, Edge, Node } from '@/core/contracts';
import { Input } from '@/components/ui/input';
export function BrainView({ nodes, edges, frame, large = false }: { nodes: Node[]; edges: Edge[]; frame?: BrainState; large?: boolean }) {
  const canvas = useRef<HTMLCanvasElement>(null), [selection, setSelected] = useState(''), [query, setQuery] = useState('');
  const selected = nodes.some(n => n.id === selection) ? selection : nodes[0]?.id ?? '';
  const positions = useMemo(() => {
    const groups = [...new Set(nodes.map(n => n.role))];
    const index = new Map(nodes.map((n, i) => [n.id, i]));
    const points = nodes.map(n => {
      const g = groups.indexOf(n.role), peers = nodes.filter(x => x.role === n.role), i = peers.findIndex(x => x.id === n.id);
      // Schematic deterministic coordinates, never invented neural activity.
      const a = i * 2.399963229728653, r = Math.sqrt((i + 1) / peers.length) * (g === 2 ? 114 : 104);
      const columns = Math.min(3, groups.length), rows = Math.ceil(groups.length / columns);
      const cx = 140 + (g % columns) * (500 / Math.max(1, columns - 1)), cy = rows === 1 ? 230 : 140 + Math.floor(g / columns) * (180 / Math.max(1, rows - 1));
      return { id: n.id, x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r * .92 };
    }); return { points, index };
  }, [nodes]);
  useEffect(() => {
    const el = canvas.current; if (!el) return;
    const draw = () => {
      const ctx = el.getContext('2d'); if (!ctx) return;
      const width = el.clientWidth, height = el.clientHeight, ratio = window.devicePixelRatio || 1;
      el.width = width * ratio; el.height = height * ratio; ctx.scale(ratio * width / 780, ratio * height / 460); ctx.clearRect(0, 0, 780, 460);
      const activity = frame?.activity ?? [];
      for (const edge of edges) {
        const i = positions.index.get(edge.source)!, j = positions.index.get(edge.target)!;
        const a = positions.points[i], b = positions.points[j], value = Math.min(1, (activity[i] ?? 0) * 2), hi = a.id === selected || b.id === selected;
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = hi ? `rgba(196,231,131,${.09 + value * .32})` : `rgba(164,187,146,${.018 + value * .09})`;
        ctx.lineWidth = hi ? .85 : .5; ctx.stroke();
      }
      positions.points.forEach((p, i) => {
        const v = activity[i] ?? 0, strength = Math.min(1, v * 3), sensory = frame?.stimulated.includes(p.id);
        if (v > .035) { ctx.beginPath(); ctx.arc(p.x, p.y, 4 + strength * 6, 0, Math.PI * 2); ctx.fillStyle = `rgba(190,235,112,${strength * .13})`; ctx.fill(); }
        ctx.beginPath(); ctx.arc(p.x, p.y, p.id === selected ? 4.5 : 1.5 + strength * 2.3, 0, Math.PI * 2);
        ctx.fillStyle = sensory ? `rgba(231,239,208,${.4 + strength * .6})` : `rgba(${Math.round(96 + strength * 101)},${Math.round(113 + strength * 124)},${Math.round(87 + strength * 54)},${.45 + strength * .55})`; ctx.fill();
        if (p.id === selected) { ctx.strokeStyle = '#d3f49a'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(p.x, p.y, 9, 0, Math.PI * 2); ctx.stroke(); ctx.fillStyle = '#e2efce'; ctx.font = '12px monospace'; ctx.fillText(p.id, p.x + 13, p.y + 4); }
      });
    }; draw(); const observer = new ResizeObserver(draw); observer.observe(el); return () => observer.disconnect();
  }, [frame, edges, positions, selected]);
  const selectedIndex = positions.index.get(selected)!;
  return <div className={`brain-visual ${large ? 'large' : ''}`}>
    <div className="network-label"><span>CONNECTOME / {nodes.length}</span><span>SCHEMATIC LAYOUT</span></div>
    <canvas ref={canvas} role="img" aria-label={`Biological network of ${nodes.length} neurons. ${frame ? `Recorded simulation tick ${frame.tick}.` : 'No activity supplied; current neural state unknown.'}`} onPointerDown={e => {
      const r = e.currentTarget.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * 780, y = (e.clientY - r.top) / r.height * 460;
      if (positions.points.length) setSelected(positions.points.reduce((a, p) => Math.hypot(p.x - x, p.y - y) < Math.hypot(a.x - x, a.y - y) ? p : a).id);
    }} />
    <div className="network-legend">{[...new Set(nodes.map(n => n.role))].map(role => <span key={role}>{role}</span>)}</div>
    <div className="neuron-inspector"><div><span className="mono accent">{selected}</span><span className="muted"> {nodes[selectedIndex]?.role}</span></div><span className="mono">{frame ? frame.activity[selectedIndex]?.toFixed(5) ?? 'Unknown' : 'Unknown'} <small className="muted">activation</small></span><Input aria-label="Find neuron by biological name" list="neuron-names" placeholder="Find a neuron…" value={query} onChange={e => { setQuery(e.target.value.toUpperCase()); if (positions.index.has(e.target.value.toUpperCase())) setSelected(e.target.value.toUpperCase()); }} /><datalist id="neuron-names">{nodes.map(n => <option key={n.id} value={n.id} />)}</datalist></div>
  </div>;
}
