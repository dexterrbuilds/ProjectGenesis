import { Countdown } from './countdown';
import { DormantConnectome } from './connectome';
import styles from './dormant.module.css';

export function DormantExperience({ awakeningAt, now }: { awakeningAt: number | null; now: number }) {
  return <main className={styles.page}>
    <header className={styles.header}>
      <div className={styles.brand}><span className={styles.mark} aria-hidden="true">g</span><span>PROJECT GENESIS</span></div>
      <span className={styles.edition}>EXPERIMENT 001</span>
    </header>
    <div className={styles.observation}>
      <div className={styles.specimenFrame}><DormantConnectome /></div>
      <div className={styles.intro}>
        <p className={styles.eyebrow}><span aria-hidden="true" /> PRE-AWAKENING</p>
        <h1>AN ARTIFICIAL LIFE,<br /><span>IN PROGRESS.</span></h1>
        <p className={styles.whisper}>Every life has a beginning.<br />This one is approaching its own.</p>
      </div>
      <Countdown awakeningAt={awakeningAt} serverNow={now} />
    </div>
    <footer className={styles.footer}>
      <div className={styles.science}><span>C. ELEGANS</span><span>302 NEURONS</span></div>
      <div className={styles.state}><span aria-hidden="true" /> STATE: DORMANT</div>
    </footer>
  </main>;
}
