import { renderHook, waitFor } from '@testing-library/react';
import { test, expect, describe, it } from 'vitest';
import { usePropertyReferenceValues } from '../hooks/usePropertyReferenceValues';

describe('usePropertyReferenceValues', () => {
  it('should return an empty object when jsonSchema is null', async () => {
    const jsonSchema = null;
    const allUserProperties = [
      {
        uuid: 'df194dd3-097e-412e-928b-3b04210f0ac2',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'FlyToken',
        json_str: {
          name: 'Fly Token D',
          fly_token: 'FlyToken',
        },
        created_at: '2024-06-19T09:47:19.132000Z',
        updated_at: '2024-07-07T07:35:08.019000Z',
      },
    ];
    const updateExistingModel = null;

    const { result } = renderHook(() =>
      usePropertyReferenceValues({ jsonSchema, allUserProperties, updateExistingModel })
    );

    // Initial state should be an empty object
    expect(result.current).toEqual({});

    // Wait for any asynchronous updates
    await waitFor(
      () => {
        // After any potential updates, the result should still be an empty object
        expect(result.current).toEqual({});
      },
      { timeout: 1000 }
    );
  });
  it('should return an empty object when jsonSchema has no $ref or anyOf/allOf properties', async () => {
    const jsonSchema = {
      properties: {
        name: {
          description: 'The name of the item',
          minLength: 1,
          title: 'Name',
          type: 'string',
        },
        api_key: {
          description: 'The API Key from Anthropic',
          title: 'Api Key',
          type: 'string',
        },
      },
      required: ['name', 'api_key'],
      title: 'AnthropicAPIKey',
      type: 'object',
    };

    const allUserProperties = [
      {
        uuid: 'df194dd3-097e-412e-928b-3b04210f0ac2',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'FlyToken',
        json_str: {
          name: 'Fly Token D',
          fly_token: 'FlyToken',
        },
        created_at: '2024-06-19T09:47:19.132000Z',
        updated_at: '2024-07-07T07:35:08.019000Z',
      },
    ];

    const updateExistingModel = null;

    const { result } = renderHook(() =>
      usePropertyReferenceValues({ jsonSchema, allUserProperties, updateExistingModel })
    );

    // Initial state should be an empty object
    expect(result.current).toEqual({});

    // Wait for any asynchronous updates
    await waitFor(
      () => {
        // After any potential updates, the result should still be an empty object
        expect(result.current).toEqual({});
      },
      { timeout: 1000 }
    );
  });
  it('should process $ref properties and return appropriate refValues', async () => {
    const jsonSchema = {
      $defs: {
        AnthropicAPIKeyRef: {
          properties: {
            type: {
              const: 'secret',
              default: 'secret',
              description: 'The name of the type of the data',
              enum: ['secret'],
              title: 'Type',
              type: 'string',
            },
            name: {
              const: 'AnthropicAPIKey',
              default: 'AnthropicAPIKey',
              description: 'The name of the data',
              enum: ['AnthropicAPIKey'],
              title: 'Name',
              type: 'string',
            },
            uuid: {
              description: 'The unique identifier',
              format: 'uuid',
              title: 'UUID',
              type: 'string',
            },
          },
          required: ['uuid'],
          title: 'AnthropicAPIKeyRef',
          type: 'object',
        },
      },
      properties: {
        name: {
          description: 'The name of the item',
          minLength: 1,
          title: 'Name',
          type: 'string',
        },
        model: {
          default: 'claude-3-5-sonnet-20240620',
          description: "The model to use for the Anthropic API, e.g. 'claude-3-5-sonnet-20240620'",
          enum: [
            'claude-3-5-sonnet-20240620',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
          ],
          title: 'Model',
          type: 'string',
        },
        api_key: {
          $ref: '#/$defs/AnthropicAPIKeyRef',
        },
        base_url: {
          default: 'https://api.anthropic.com/v1',
          description: 'The base URL of the Anthropic API',
          format: 'uri',
          maxLength: 2083,
          minLength: 1,
          title: 'Base Url',
          type: 'string',
        },
        api_type: {
          const: 'anthropic',
          default: 'anthropic',
          description: "The type of the API, must be 'anthropic'",
          enum: ['anthropic'],
          title: 'API Type',
          type: 'string',
        },
        temperature: {
          default: 0.8,
          description: 'The temperature to use for the model, must be between 0 and 2',
          maximum: 2,
          minimum: 0,
          title: 'Temperature',
          type: 'number',
        },
      },
      required: ['name', 'api_key'],
      title: 'Anthropic',
      type: 'object',
    };

    const allUserProperties = [
      {
        uuid: 'df194dd3-097e-412e-928b-3b04210f0ac2',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'FlyToken',
        json_str: {
          name: 'Fly Token D',
          fly_token: 'FlyToken',
        },
        created_at: '2024-06-19T09:47:19.132000Z',
        updated_at: '2024-07-07T07:35:08.019000Z',
      },
    ];

    const updateExistingModel = null;

    const { result } = renderHook(() =>
      usePropertyReferenceValues({ jsonSchema, allUserProperties, updateExistingModel })
    );

    // Wait for asynchronous updates
    await waitFor(
      () => {
        expect(result.current).toHaveProperty('api_key');
      },
      { timeout: 1000 }
    );

    const expected = {
      api_key: {
        htmlSchema: { default: '', description: '', enum: ['None'], title: 'Api Key' },
        matchedProperties: [],
        propertyTypes: ['secret'],
        isRequired: true,
      },
    };
    // Check the structure of the returned refValues
    expect(result.current).toEqual(expected);
  });
  it('should process $ref properties and return appropriate refValues with matching user property', async () => {
    const jsonSchema = {
      $defs: {
        AzureOAIAPIKeyRef: {
          properties: {
            type: {
              const: 'secret',
              default: 'secret',
              description: 'The name of the type of the data',
              enum: ['secret'],
              title: 'Type',
              type: 'string',
            },
            name: {
              const: 'AzureOAIAPIKey',
              default: 'AzureOAIAPIKey',
              description: 'The name of the data',
              enum: ['AzureOAIAPIKey'],
              title: 'Name',
              type: 'string',
            },
            uuid: {
              description: 'The unique identifier',
              format: 'uuid',
              title: 'UUID',
              type: 'string',
            },
          },
          required: ['uuid'],
          title: 'AzureOAIAPIKeyRef',
          type: 'object',
        },
      },
      properties: {
        name: {
          description: 'The name of the item',
          minLength: 1,
          title: 'Name',
          type: 'string',
        },
        model: {
          default: 'gpt-3.5-turbo',
          description: "The model to use for the Azure OpenAI API, e.g. 'gpt-3.5-turbo'",
          title: 'Model',
          type: 'string',
        },
        api_key: {
          $ref: '#/$defs/AzureOAIAPIKeyRef',
        },
        base_url: {
          default: 'https://api.openai.com/v1',
          description: 'The base URL of the Azure OpenAI API',
          format: 'uri',
          maxLength: 2083,
          minLength: 1,
          title: 'Base Url',
          type: 'string',
        },
        api_type: {
          const: 'azure',
          default: 'azure',
          description: "The type of the API, must be 'azure'",
          enum: ['azure'],
          title: 'API type',
          type: 'string',
        },
        api_version: {
          default: '2024-02-01',
          description: "The version of the Azure OpenAI API, e.g. '2024-02-01'",
          enum: [
            '2023-05-15',
            '2023-06-01-preview',
            '2023-10-01-preview',
            '2024-02-15-preview',
            '2024-03-01-preview',
            '2024-04-01-preview',
            '2024-05-01-preview',
            '2024-02-01',
          ],
          title: 'Api Version',
          type: 'string',
        },
        temperature: {
          default: 0.8,
          description: 'The temperature to use for the model, must be between 0 and 2',
          maximum: 2,
          minimum: 0,
          title: 'Temperature',
          type: 'number',
        },
      },
      required: ['name', 'api_key'],
      title: 'AzureOAI',
      type: 'object',
    };

    const allUserProperties = [
      {
        uuid: '367d2944-fe36-4223-82e6-f532c58afe32',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'AzureOAIAPIKey',
        json_str: {
          name: 'Azure Key',
          api_key: 'api_key', // pragma: allowlist secret
        },
        created_at: '2024-07-04T10:50:12.705000Z',
        updated_at: '2024-07-04T10:50:12.705000Z',
      },
    ];

    const updateExistingModel = null;

    const { result } = renderHook(() =>
      usePropertyReferenceValues({ jsonSchema, allUserProperties, updateExistingModel })
    );

    // Wait for asynchronous updates
    await waitFor(
      () => {
        expect(result.current).toHaveProperty('api_key');
      },
      { timeout: 1000 }
    );

    // Check the structure of the returned refValues
    expect(result.current).toHaveProperty('api_key');

    const apiKeyResult = result.current.api_key;

    // Check htmlSchema
    expect(apiKeyResult.htmlSchema).toEqual({
      default: 'Azure Key',
      description: '',
      enum: ['Azure Key'],
      title: 'Api Key',
    });

    // Check missingDependency
    expect(apiKeyResult.matchedProperties).toEqual([
      {
        uuid: '367d2944-fe36-4223-82e6-f532c58afe32',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'AzureOAIAPIKey',
        json_str: {
          name: 'Azure Key',
          api_key: 'api_key', // pragma: allowlist secret
        },
        created_at: '2024-07-04T10:50:12.705000Z',
        updated_at: '2024-07-04T10:50:12.705000Z',
      },
    ]);

    // Check missingDependency
    expect(apiKeyResult.propertyTypes).toEqual(['secret']);

    // Additional checks
    expect(Object.keys(result.current)).toHaveLength(1); // Only api_key should be processed
  });
  it('should process anyOf properties with $ref and null options', async () => {
    const jsonSchema = {
      $defs: {
        OpenAPIAuthRef: {
          properties: {
            type: {
              const: 'secret',
              default: 'secret',
              description: 'The name of the type of the data',
              enum: ['secret'],
              title: 'Type',
              type: 'string',
            },
            name: {
              const: 'OpenAPIAuth',
              default: 'OpenAPIAuth',
              description: 'The name of the data',
              enum: ['OpenAPIAuth'],
              title: 'Name',
              type: 'string',
            },
            uuid: {
              description: 'The unique identifier',
              format: 'uuid',
              title: 'UUID',
              type: 'string',
            },
          },
          required: ['uuid'],
          title: 'OpenAPIAuthRef',
          type: 'object',
        },
      },
      properties: {
        name: {
          description: 'The name of the item',
          minLength: 1,
          title: 'Name',
          type: 'string',
        },
        openapi_url: {
          description: 'The URL of OpenAPI specification file',
          format: 'uri',
          maxLength: 2083,
          minLength: 1,
          title: 'OpenAPI URL',
          type: 'string',
        },
        openapi_auth: {
          anyOf: [{ $ref: '#/$defs/OpenAPIAuthRef' }, { type: 'null' }],
          default: null,
          description: 'Authentication information for the API mentioned in the OpenAPI specification',
          title: 'OpenAPI Auth',
        },
      },
      required: ['name', 'openapi_url'],
      title: 'Toolbox',
      type: 'object',
    };

    const allUserProperties = [
      {
        uuid: '367d2944-fe36-4223-82e6-f532c58afe32',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'AzureOAIAPIKey',
        json_str: {
          name: 'Azure Key',
          api_key: 'api_key', // pragma: allowlist secret
        },
        created_at: '2024-07-04T10:50:12.705000Z',
        updated_at: '2024-07-04T10:50:12.705000Z',
      },
    ];

    const updateExistingModel = null;

    const { result } = renderHook(() =>
      usePropertyReferenceValues({ jsonSchema, allUserProperties, updateExistingModel })
    );

    // Wait for asynchronous updates
    await waitFor(
      () => {
        expect(result.current).toHaveProperty('openapi_auth');
      },
      { timeout: 1000 }
    );

    // Check the structure of the returned refValues
    expect(result.current).toHaveProperty('openapi_auth');

    const openapiAuthResult = result.current.openapi_auth;

    // Check htmlSchema
    expect(openapiAuthResult.htmlSchema).toEqual({
      default: 'None',
      description: '',
      enum: ['None'],
      title: 'OpenAPI Auth',
    });

    // Check missingDependency
    expect(openapiAuthResult.matchedProperties).toEqual([]);

    // Check missingDependency
    expect(openapiAuthResult.propertyTypes).toEqual(['secret']);

    // Additional checks
    // expect(Object.keys(result.current)).toHaveLength(1); // Only openapi_auth should be processed
  });
  it('should process anyOf properties with $ref and null options, with a matching user property', async () => {
    const jsonSchema = {
      $defs: {
        OpenAPIAuthRef: {
          properties: {
            type: {
              const: 'secret',
              default: 'secret',
              description: 'The name of the type of the data',
              enum: ['secret'],
              title: 'Type',
              type: 'string',
            },
            name: {
              const: 'OpenAPIAuth',
              default: 'OpenAPIAuth',
              description: 'The name of the data',
              enum: ['OpenAPIAuth'],
              title: 'Name',
              type: 'string',
            },
            uuid: {
              description: 'The unique identifier',
              format: 'uuid',
              title: 'UUID',
              type: 'string',
            },
          },
          required: ['uuid'],
          title: 'OpenAPIAuthRef',
          type: 'object',
        },
      },
      properties: {
        name: {
          description: 'The name of the item',
          minLength: 1,
          title: 'Name',
          type: 'string',
        },
        openapi_url: {
          description: 'The URL of OpenAPI specification file',
          format: 'uri',
          maxLength: 2083,
          minLength: 1,
          title: 'OpenAPI URL',
          type: 'string',
        },
        openapi_auth: {
          anyOf: [{ $ref: '#/$defs/OpenAPIAuthRef' }, { type: 'null' }],
          default: null,
          description: 'Authentication information for the API mentioned in the OpenAPI specification',
          title: 'OpenAPI Auth',
        },
      },
      required: ['name', 'openapi_url'],
      title: 'Toolbox',
      type: 'object',
    };

    const allUserProperties = [
      {
        uuid: 'd72e6782-a849-45c3-bac8-7e9605fb73b3',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'OpenAPIAuth',
        json_str: {
          name: 'OpenAPIAuth',
          password: 'OpenAPIAuth', // pragma: allowlist secret
          username: 'OpenAPIAuth',
        },
        created_at: '2024-07-08T01:07:13.877000Z',
        updated_at: '2024-07-08T01:07:13.877000Z',
      },
    ];

    const updateExistingModel = null;

    const { result } = renderHook(() =>
      usePropertyReferenceValues({ jsonSchema, allUserProperties, updateExistingModel })
    );

    // Wait for asynchronous updates
    await waitFor(
      () => {
        expect(result.current).toHaveProperty('openapi_auth');
      },
      { timeout: 1000 }
    );

    // Check the structure of the returned refValues
    expect(result.current).toHaveProperty('openapi_auth');

    const openapiAuthResult = result.current.openapi_auth;

    // Check htmlSchema
    expect(openapiAuthResult.htmlSchema).toEqual({
      default: 'None',
      description: '',
      enum: ['None', 'OpenAPIAuth'],
      title: 'OpenAPI Auth',
    });

    // Check matchedProperties
    expect(openapiAuthResult.matchedProperties).toEqual([
      {
        uuid: 'd72e6782-a849-45c3-bac8-7e9605fb73b3',
        user_uuid: 'dae81928-8e99-48c2-be5d-61a5b422cf47',
        type_name: 'secret',
        model_name: 'OpenAPIAuth',
        json_str: {
          name: 'OpenAPIAuth',
          password: 'OpenAPIAuth', // pragma: allowlist secret
          username: 'OpenAPIAuth',
        },
        created_at: '2024-07-08T01:07:13.877000Z',
        updated_at: '2024-07-08T01:07:13.877000Z',
      },
    ]);

    // Check missingDependency
    expect(openapiAuthResult.propertyTypes).toEqual(['secret']);

    // Additional checks
    expect(Object.keys(result.current)).toHaveLength(1); // Only openapi_auth should be processed
  });
});
