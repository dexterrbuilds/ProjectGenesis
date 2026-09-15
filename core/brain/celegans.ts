import data from '../../data/connectome.json' with { type: 'json' };
import { CHANNELS } from '../contracts.ts';
import type { BrainAdapter, BrainSnapshot, BrainState, Stimulus, Channel, BehavioralOutput, Edge } from '../contracts.ts';

// These are documented product analogies, not a biologically validated event encoder.
export const SENSORY_MAP: Record<Channel, [string, number][]> = {
  rewardOpportunity: [['AWAL', 1], ['AWAR', 1], ['ASEL', .5], ['ASER', .5]],
  danger: [['ASHL', 1.6], ['ASHR', 1.6]],
  novelty: [['AWCL', 1], ['AWCR', 1]],
  scarcity: [['AWCL', .7], ['AWCR', .7], ['ASKL', .5], ['ASKR', .5]],
  acquisition: [['AWAL', .8], ['AWAR', .8], ['CEPDL', .4], ['CEPDR', .4], ['CEPVL', .4], ['CEPVR', .4]],
  uncertainty: [['AWCL', .3], ['AWCR', .3], ['ASHL', .15], ['ASHR', .15]],
  social: [['ASKL', .7], ['ASKR', .7], ['URXL', .4], ['URXR', .4]],
};
const POOLS: Record<string, string[]> = {
  forward: ['AVBL', 'AVBR', 'PVCL', 'PVCR'],
  reverse: ['AVAL', 'AVAR', 'AVDL', 'AVDR', 'AVEL', 'AVER'],
  forwardMotor: data.neurons.filter(n => /^(DB|VB)\d+$/.test(n.id)).map(n => n.id),
  reverseMotor: data.neurons.filter(n => /^(DA|VA)\d+$/.test(n.id)).map(n => n.id),
  search: ['AIBL', 'AIBR'], navigation: ['AIYL', 'AIYR'],
};
const clamp = (x: number) => Math.max(0, Math.min(1, x));

export class CElegansBrain implements BrainAdapter {
  readonly id = 'celegans-cook2019-rate-v1';
  readonly nodes = data.neurons;
  readonly edges: Edge[];
  private index = new Map(this.nodes.map((n, i) => [n.id, i]));
  private activity = new Float64Array(this.nodes.length);
  private adaptation = new Float64Array(this.nodes.length);
  private input = new Float64Array(this.nodes.length);
  private tick = 0;
  private chemical: [number, number, number][] = [];
  private gaps: [number, number, number][] = [];
  constructor(edges: Edge[] = data.edges) {
    this.edges = edges;
    const incoming = new Float64Array(this.nodes.length);
    const gapTotal = new Float64Array(this.nodes.length);
    for (const e of edges) {
      const i = this.index.get(e.source), j = this.index.get(e.target);
      if (i === undefined || j === undefined || !Number.isFinite(e.weight) || e.weight <= 0) throw new Error('Invalid biological edge');
      const w = Math.log1p(e.weight);
      if (e.kind === 'chemical') incoming[j] += w;
      else { gapTotal[i] += w; gapTotal[j] += w; }
    }
    for (const e of edges) {
      const i = this.index.get(e.source)!, j = this.index.get(e.target)!;
      const w = Math.log1p(e.weight);
      if (e.kind === 'chemical') {
        const inhibitory = /^(DD|VD)\d+$/.test(e.source) || (/^AWC/.test(e.source) && /^(AIY|AIA)/.test(e.target));
        this.chemical.push([i, j, (inhibitory ? -1 : 1) * w / Math.max(1, incoming[j])]);
      } else this.gaps.push([i, j, w / Math.max(1, gapTotal[i], gapTotal[j])]);
    }
    this.initialize();
  }
  initialize(snapshot?: BrainSnapshot) {
    this.activity.fill(0); this.adaptation.fill(0); this.input.fill(0); this.tick = 0;
    if (!snapshot) return;
    if (snapshot.adapter !== this.id || snapshot.version !== 1) throw new Error('Incompatible brain snapshot');
    const s = snapshot.payload as { activity: number[]; adaptation: number[]; input: number[]; tick: number; dataset: string };
    if (s.dataset !== data.provenance.commit || !Number.isSafeInteger(s.tick) || s.tick < 0) throw new Error('Invalid brain provenance/tick');
    for (const key of ['activity', 'adaptation', 'input'] as const) {
      if (!Array.isArray(s[key]) || s[key].length !== this.nodes.length || s[key].some(x => !Number.isFinite(x) || x < 0 || x > (key === 'input' ? 3 : 1))) throw new Error('Invalid snapshot vector');
      this[key].set(s[key]);
    }
    this.tick = s.tick;
  }
  stimulate(stimulus: Stimulus) {
    this.input.fill(0);
    const contributions = new Map<string, Channel[]>();
    for (const channel of CHANNELS) {
      const value = stimulus[channel];
      if (!Number.isFinite(value) || value < 0 || value > 1) throw new Error('Stimulus must be finite within [0,1]');
      if (!value) continue;
      for (const [name, gain] of SENSORY_MAP[channel]) {
        this.input[this.index.get(name)!] += value * gain;
        contributions.set(name, [...(contributions.get(name) ?? []), channel]);
      }
    }
    this.input.forEach((x, i) => { this.input[i] = Math.min(3, x); });
    return [...contributions].map(([neuron, channels]) => ({ neuron, current: this.input[this.index.get(neuron)!], channels }));
  }
  step(count = 1): BrainState {
    if (!Number.isInteger(count) || count < 1 || count > 1000) throw new Error('Invalid integration step count');
    for (let t = 0; t < count; t++) {
      const drive = new Float64Array(this.nodes.length);
      for (const [i, j, w] of this.chemical) drive[j] += .85 * w * this.activity[i];
      for (const [i, j, w] of this.gaps) {
        const flow = .25 * w * (this.activity[i] - this.activity[j]);
        drive[j] += flow; drive[i] -= flow;
      }
      const next = new Float64Array(this.nodes.length);
      for (let i = 0; i < next.length; i++) {
        const target = clamp(Math.tanh(this.input[i] + drive[i] - .12 * this.adaptation[i]));
        next[i] = clamp(this.activity[i] + .15 * (target - this.activity[i]));
        this.adaptation[i] += .008 * (this.activity[i] - this.adaptation[i]);
        this.input[i] *= .995;
      }
      this.activity = next; this.tick++;
    }
    return this.getState();
  }
  decodeBehavior(): BehavioralOutput {
    const avg = (ids: string[]) => ids.reduce((s, n) => s + this.activity[this.index.get(n)!], 0) / ids.length;
    const p = Object.fromEntries(Object.entries(POOLS).map(([k, ids]) => [k, avg(ids)]));
    const forward = p.forward + .4 * p.forwardMotor + .3 * p.navigation;
    const reverse = p.reverse + .4 * p.reverseMotor;
    const search = .8 * p.search;
    const max = Math.max(forward, reverse, search);
    const behavior = max < .008 ? 'WAIT' : reverse > forward * 1.02 && reverse > search ? (reverse > .07 ? 'RETREAT' : 'AVOID') : search > forward ? 'EXPLORE' : 'APPROACH';
    return { behavior, scores: { forward, reverse, search, ...Object.fromEntries(Object.entries(p).map(([k, v]) => ['pool_' + k, v])) }, evidence: Object.entries(POOLS).flatMap(([pool, ids]) => ids.map(id => ({ id, pool, activity: this.activity[this.index.get(id)!] }))), policy: 'readout-v1; dimensionless engineering thresholds' };
  }
  getState() { return { tick: this.tick, activity: Array.from(this.activity), stimulated: this.nodes.filter((_, i) => this.input[i] > .001).map(n => n.id) }; }
  snapshot(): BrainSnapshot { return { adapter: this.id, version: 1, payload: { dataset: data.provenance.commit, tick: this.tick, activity: Array.from(this.activity), adaptation: Array.from(this.adaptation), input: Array.from(this.input) } }; }
}
