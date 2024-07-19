import { describe, it, expect } from 'vitest';
import { parseValidationErrors } from '../app/utils/formHelpers';

describe('parseValidationErrors', () => {
  it('converts a list of Pydantic validation errors to a simplified error object', () => {
    const input = [
      {
        type: 'string_type',
        loc: ['body', 'api_key'],
        msg: 'Input should be a valid string',
        input: 4,
        url: 'https://errors.pydantic.dev/2.7/v/string_type',
      },
      {
        type: 'url_parsing',
        loc: ['body', 'base_url'],
        msg: 'Input should be a valid URL, relative URL without a base',
        input: '1',
        ctx: {
          error: 'relative URL without a base',
        },
        url: 'https://errors.pydantic.dev/2.7/v/url_parsing',
      },
    ];

    const expectedOutput = {
      api_key: 'Input should be a valid string', // pragma: allowlist secret
      base_url: 'Input should be a valid URL, relative URL without a base',
    };

    const result = parseValidationErrors(input);
    expect(result).toEqual(expectedOutput);
  });

  it('converts a list of Pydantic validation errors to a simplified error object', () => {
    const input = [
      {
        type: 'url_parsing',
        loc: ['body', 'base_url'],
        msg: 'Input should be a valid URL, relative URL without a base',
        input: '1',
        ctx: {
          error: 'relative URL without a base',
        },
        url: 'https://errors.pydantic.dev/2.7/v/url_parsing',
      },
    ];

    const expectedOutput = {
      base_url: 'Input should be a valid URL, relative URL without a base',
    };

    const result = parseValidationErrors(input);
    expect(result).toEqual(expectedOutput);
  });
});
