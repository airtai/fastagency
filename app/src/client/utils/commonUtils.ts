export function generateNatsUrl(
  natsUrl: string | undefined,
  fastAgencyServerUrl: string | undefined
): string | undefined {
  if (natsUrl) return natsUrl;
  return fastAgencyServerUrl ? `${fastAgencyServerUrl.replace('https://', 'tls://')}:4222` : fastAgencyServerUrl;
}
