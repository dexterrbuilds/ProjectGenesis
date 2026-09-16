import connectome from '@/data/connectome.json';
import styles from './dormant.module.css';

/** Real connectivity, static schematic coordinates. No simulation state or activity is supplied. */
export function DormantConnectome() {
  const groups = [...new Set(connectome.neurons.map(node => node.role))];
  const points = new Map(connectome.neurons.map(node => {
    const group = groups.indexOf(node.role);
    const peers = connectome.neurons.filter(peer => peer.role === node.role);
    const index = peers.findIndex(peer => peer.id === node.id);
    const angle = index * 2.399963229728653;
    const radius = Math.sqrt((index + 1) / peers.length) * (group === 2 ? 114 : 104);
    const columns = Math.min(3, groups.length), rows = Math.ceil(groups.length / columns);
    return [node.id, {
      x: 140 + (group % columns) * (500 / Math.max(1, columns - 1)) + Math.cos(angle) * radius,
      y: (rows === 1 ? 230 : 140 + Math.floor(group / columns) * (180 / Math.max(1, rows - 1))) + Math.sin(angle) * radius * .92,
    }];
  }));
  const paths = connectome.edges.map(edge => {
    const a = points.get(edge.source)!, b = points.get(edge.target)!;
    return `M${a.x.toFixed(2)},${a.y.toFixed(2)}L${b.x.toFixed(2)},${b.y.toFixed(2)}`;
  }).join('');
  return <figure className={styles.specimen}>
    <svg viewBox="0 0 780 460" role="img" aria-labelledby="dormant-connectome-title">
      <title id="dormant-connectome-title">C. elegans: 302 named neurons and their real connectivity. Static schematic, no neural activity displayed.</title>
      <path d={paths} fill="none" stroke="currentColor" strokeWidth=".6" opacity=".11" />
      {[...points].map(([id, point]) => <circle key={id} cx={point.x} cy={point.y} r="1.7" fill="currentColor" opacity=".55"><title>{id}</title></circle>)}
    </svg>
    <figcaption>CONNECTOME 001 <span>STRUCTURAL MAP · NO ACTIVITY</span></figcaption>
  </figure>;
}
