'use client';

import { useEffect, useState } from 'react';
import { countdownParts } from '@/lib/awakening';
import styles from './dormant.module.css';

const labels = ['Days', 'Hours', 'Minutes', 'Seconds'];

export function Countdown({ awakeningAt, serverNow }: { awakeningAt: number | null; serverNow: number }) {
  const [now, setNow] = useState(serverNow);
  useEffect(() => {
    if (awakeningAt === null) return;
    // Every tick recalculates from an absolute deadline; background tabs do not accumulate drift.
    const update = () => setNow(Date.now());
    const timer = window.setInterval(update, 1000);
    document.addEventListener('visibilitychange', update);
    return () => { window.clearInterval(timer); document.removeEventListener('visibilitychange', update); };
  }, [awakeningAt]);
  const parts = countdownParts(awakeningAt, now);
  const reached = parts?.every(value => value === 0);
  return <section className={styles.countdown} aria-label="Countdown to Genesis">
    <div className={styles.digits} role="timer" aria-live="off" aria-label={parts ? parts.map((value, i) => `${value} ${labels[i].toLowerCase()}`).join(', ') : 'Awakening time unannounced'}>
      {labels.map((label, i) => <div className={styles.unit} key={label}>
        <span className={styles.number}>{parts ? String(parts[i]).padStart(2, '0') : 'XX'}</span>
        <span className={styles.unitLabel}>{label}</span>
      </div>)}
    </div>
    <p className={styles.until}>UNTIL GENESIS</p>
    <p className={styles.countdownNote} role="status">{reached ? 'The threshold is here. Awaiting awakening.' : awakeningAt === null ? 'Awakening time to be announced.' : <time dateTime={new Date(awakeningAt).toISOString()}>{new Date(awakeningAt).toISOString().slice(0, 16).replace('T', ' · ')} UTC</time>}</p>
  </section>;
}
