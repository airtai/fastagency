import { test, expect, describe } from 'vitest';

import { generateNatsUrl } from '../utils/commonUtils';

describe('commonUtils', () => {
  test('generateNatsUrl - local undefined', () => {
    const natsUrl = undefined;
    const fastAgencyServerUrl = undefined;
    const expected = undefined;
    const actual = generateNatsUrl(natsUrl, fastAgencyServerUrl);
    expect(actual).toEqual(expected);
  });

  test('generateNatsUrl - local', () => {
    const natsUrl = 'nats://localhost:4222';
    const fastAgencyServerUrl = 'https://api.staging.fastagency.ai';
    const expected = 'nats://localhost:4222';
    const actual = generateNatsUrl(natsUrl, fastAgencyServerUrl);
    expect(actual).toEqual(expected);
  });

  test('generateNatsUrl - staging', () => {
    const natsUrl = undefined;
    const fastAgencyServerUrl = 'https://api.staging.fastagency.ai';
    const expected = 'tls://api.staging.fastagency.ai:4222';
    const actual = generateNatsUrl(natsUrl, fastAgencyServerUrl);
    expect(actual).toEqual(expected);
  });

  test('generateNatsUrl - production', () => {
    const natsUrl = undefined;
    const fastAgencyServerUrl = 'https://api.fastagency.ai';
    const expected = 'tls://api.fastagency.ai:4222';
    const actual = generateNatsUrl(natsUrl, fastAgencyServerUrl);
    expect(actual).toEqual(expected);
  });
});
