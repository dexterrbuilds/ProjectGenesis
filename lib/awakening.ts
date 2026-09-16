/** Presentation only. None of these settings can start or stop the organism. */
type ReleaseEnvironment = { NODE_ENV?: string; GENESIS_PUBLIC_MODE?: string; GENESIS_DEV_PREVIEW?: string };

export function developmentPreviewEnabled(env: ReleaseEnvironment) {
  return env.NODE_ENV === 'development' && env.GENESIS_DEV_PREVIEW === 'true';
}

export function observationEnabled(env: ReleaseEnvironment) {
  return env.GENESIS_PUBLIC_MODE === 'live' || developmentPreviewEnabled(env);
}

/** Require an absolute ISO timestamp, including Z or an explicit UTC offset. */
export function awakeningTimestamp(value: string | undefined): number | null {
  if (!value?.trim()) return null;
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,3})?(Z|[+-](\d{2}):(\d{2}))$/.exec(value);
  const epoch = Date.parse(value);
  if (!match || !Number.isFinite(epoch)) throw new Error('GENESIS_AWAKENS_AT must be an absolute ISO timestamp, for example 2026-10-01T18:00:00Z.');
  const [, year, month, day, hour, minute, second, , offsetHour, offsetMinute] = match;
  const daysInMonth = new Date(Date.UTC(Number(year), Number(month), 0)).getUTCDate();
  if (+month < 1 || +month > 12 || +day < 1 || +day > daysInMonth || +hour > 23 || +minute > 59 || +second > 59 || +(offsetHour ?? 0) > 23 || +(offsetMinute ?? 0) > 59) {
    throw new Error('GENESIS_AWAKENS_AT contains an invalid calendar date or time.');
  }
  return epoch;
}

export function countdownParts(target: number | null, now: number) {
  if (target === null) return null;
  const seconds = Math.max(0, Math.ceil((target - now) / 1000));
  return [Math.floor(seconds / 86400), Math.floor(seconds / 3600) % 24, Math.floor(seconds / 60) % 60, seconds % 60];
}
