import { notFound } from 'next/navigation';
import { developmentPreviewEnabled } from '@/lib/awakening';

export const dynamic = 'force-dynamic';

export default async function Preview() {
  if (!developmentPreviewEnabled(process.env)) notFound();
  const { default: LiveObservation } = await import('@/components/live-observation');
  const {observerFixtures}=await import('@/lib/observer-fixtures');
  return <LiveObservation fixtures={observerFixtures()} />;
}
