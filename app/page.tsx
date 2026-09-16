import { awakeningTimestamp } from '@/lib/awakening';
import { DormantExperience } from '@/components/dormant/experience';

export const dynamic = 'force-dynamic';

export default async function Home() {
  if (process.env.GENESIS_PUBLIC_MODE === 'live') {
    const { default: LiveObservation } = await import('@/components/live-observation');
    return <LiveObservation />;
  }
  // This dynamic server page captures request time once for hydration-safe initial HTML.
  // eslint-disable-next-line react-hooks/purity
  const requestTime = Date.now();
  return <DormantExperience awakeningAt={awakeningTimestamp(process.env.GENESIS_AWAKENS_AT)} now={requestTime} />;
}
