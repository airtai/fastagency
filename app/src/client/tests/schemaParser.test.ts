import { test, expect, describe } from 'vitest';

import { JsonSchema } from '../interfaces/BuildPageInterfaces';
import { flattenSchema } from '../utils/schemaParser';

describe('schemaParser', () => {
  test('flattenSchema without reference', () => {
    const input: JsonSchema = {
      properties: {
        api_key: {
          description: 'The API Key from OpenAI',
          title: 'Api Key',
          type: 'string',
        },
      },
      required: ['api_key'],
      title: 'AzureOAIAPIKey',
      type: 'object',
    };
    const expected = {
      properties: {
        api_key: {
          description: 'The API Key from OpenAI',
          title: 'Api Key',
          type: 'string',
        },
      },
      required: ['api_key'],
      title: 'AzureOAIAPIKey',
      type: 'object',
    };
    const actual = flattenSchema(input);
    expect(actual).toEqual(expected);
  });
  // test('flattenSchema with reference', () => {
  //   const input: JsonSchema = {
  //     $defs: {
  //       AzureOAIAPIKeyRef: {
  //         properties: {
  //           type: {
  //             const: 'secret',
  //             default: 'secret',
  //             description: 'The name of the type of the data',
  //             enum: ['secret'],
  //             title: 'Type',
  //             type: 'string',
  //           },
  //           name: {
  //             const: 'AzureOAIAPIKey',
  //             default: 'AzureOAIAPIKey',
  //             description: 'The name of the data',
  //             enum: ['AzureOAIAPIKey'],
  //             title: 'Name',
  //             type: 'string',
  //           },
  //           uuid: {
  //             description: 'The unique identifier',
  //             format: 'uuid',
  //             title: 'UUID',
  //             type: 'string',
  //           },
  //         },
  //         required: ['uuid'],
  //         title: 'AzureOAIAPIKeyRef',
  //         type: 'object',
  //       },
  //     },
  //     properties: {
  //       model: {
  //         default: 'gpt-3.5-turbo',
  //         description: "The model to use for the Azure OpenAI API, e.g. 'gpt-3.5-turbo'",
  //         title: 'Model',
  //         type: 'string',
  //       },
  //       api_key: {
  //         $ref: '#/$defs/AzureOAIAPIKeyRef',
  //       },
  //       base_url: {
  //         default: 'https://api.openai.com/v1',
  //         description: 'The base URL of the Azure OpenAI API',
  //         format: 'uri',
  //         maxLength: 2083,
  //         minLength: 1,
  //         title: 'Base Url',
  //         type: 'string',
  //       },
  //       api_type: {
  //         const: 'azure',
  //         default: 'azure',
  //         description: "The type of the API, must be 'azure'",
  //         enum: ['azure'],
  //         title: 'API type',
  //         type: 'string',
  //       },
  //       api_version: {
  //         default: 'latest',
  //         description: "The version of the Azure OpenAI API, e.g. '2024-02-15-preview' or 'latest",
  //         enum: ['2024-02-15-preview', 'latest'],
  //         title: 'Api Version',
  //         type: 'string',
  //       },
  //     },
  //     required: ['api_key'],
  //     title: 'AzureOAI',
  //     type: 'object',
  //   };
  //   const expected = {
  //     properties: {
  //       model: {
  //         default: 'gpt-3.5-turbo',
  //         description: "The model to use for the Azure OpenAI API, e.g. 'gpt-3.5-turbo'",
  //         title: 'Model',
  //         type: 'string',
  //       },
  //       api_key: {
  //         $ref: '#/$defs/AzureOAIAPIKeyRef',
  //       },
  //       base_url: {
  //         default: 'https://api.openai.com/v1',
  //         description: 'The base URL of the Azure OpenAI API',
  //         format: 'uri',
  //         maxLength: 2083,
  //         minLength: 1,
  //         title: 'Base Url',
  //         type: 'string',
  //       },
  //       api_type: {
  //         const: 'azure',
  //         default: 'azure',
  //         description: "The type of the API, must be 'azure'",
  //         enum: ['azure'],
  //         title: 'API type',
  //         type: 'string',
  //       },
  //       api_version: {
  //         default: 'latest',
  //         description: "The version of the Azure OpenAI API, e.g. '2024-02-15-preview' or 'latest",
  //         enum: ['2024-02-15-preview', 'latest'],
  //         title: 'Api Version',
  //         type: 'string',
  //       },
  //     },
  //     required: ['api_key'],
  //     title: 'AzureOAI',
  //     type: 'object',
  //   };
  //   const actual = flattenSchema(input);
  //   expect(actual).toEqual(expected);
  // });
});
