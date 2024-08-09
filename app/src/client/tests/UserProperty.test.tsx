import React from 'react';
import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { screen, fireEvent, waitFor } from '@testing-library/react';

import { UserProperty } from '../components/buildPage/UserProperty';
import { renderInContext } from 'wasp/client/test';
import { useQuery } from 'wasp/client/operations';

// Mock the wasp/client/operations
vi.mock('wasp/client/operations', () => ({
  useQuery: vi.fn(() => ({
    // todo: fix the data strucure. pass the user added models
    data: [
      { uuid: '1', type_name: 'testProperty', model_name: 'Model1', json_str: {} },
      { uuid: '2', type_name: 'testProperty', model_name: 'Model2', json_str: {} },
    ],
    isLoading: false,
    refetch: vi.fn(),
  })),
  getModels: vi.fn(),
}));

describe('UserProperty', () => {
  const mockProps = {
    activeProperty: 'secret',
    propertiesSchema: {
      list_of_schemas: [
        {
          name: 'secret',
          schemas: [
            {
              name: 'AnthropicAPIKey',
              json_schema: {
                properties: {
                  name: { description: 'The name of the item', minLength: 1, title: 'Name', type: 'string' },
                  api_key: { description: 'The API Key from Anthropic', title: 'Api Key', type: 'string' },
                },
                required: ['name', 'api_key'],
                title: 'AnthropicAPIKey',
                type: 'object',
              },
            },
            {
              name: 'AzureOAIAPIKey',
              json_schema: {
                properties: {
                  name: { description: 'The name of the item', minLength: 1, title: 'Name', type: 'string' },
                  api_key: { description: 'The API Key from Azure OpenAI', title: 'Api Key', type: 'string' },
                },
                required: ['name', 'api_key'],
                title: 'AzureOAIAPIKey',
                type: 'object',
              },
            },
          ],
        },
        {
          name: 'llm',
          schemas: [
            {
              name: 'Anthropic',
              json_schema: {
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
                      uuid: { description: 'The unique identifier', format: 'uuid', title: 'UUID', type: 'string' },
                    },
                    required: ['uuid'],
                    title: 'AnthropicAPIKeyRef',
                    type: 'object',
                  },
                },
                properties: {
                  name: { description: 'The name of the item', minLength: 1, title: 'Name', type: 'string' },
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
                  api_key: { $ref: '#/$defs/AnthropicAPIKeyRef' },
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
              },
            },
          ],
        },
      ],
    },
    sideNavItemClickCount: 0,
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders UserProperty component with add button when no models exist', () => {
    renderInContext(<UserProperty {...mockProps} />);

    // Check for the presence of the "Add TestProperty" button
    expect(screen.getByText('Add Secret')).toBeInTheDocument();

    // Check for the "No TestProperty found" message
    expect(screen.getByText('No Secrets found. Please add one.')).toBeInTheDocument();
  });

  it('renders loading component when data is being fetched', () => {
    (useQuery as Mock).mockReturnValue({ data: undefined, refetch: vi.fn(), isLoading: true });

    const { getByText, container } = renderInContext(<UserProperty {...mockProps} />);
    console.log(container.innerHTML);

    expect(getByText('Loading...')).toBeInTheDocument();
  });

  it('renders ModelsList when models exist', () => {
    (useQuery as Mock).mockReturnValue({
      data: [
        { uuid: '1', type_name: 'secret', model_name: 'Secret1', json_str: {} },
        { uuid: '2', type_name: 'secret', model_name: 'Secret2', json_str: {} },
      ],
      isLoading: false,
      refetch: vi.fn(),
    });

    renderInContext(<UserProperty {...mockProps} />);

    expect(screen.getByText('Secret1')).toBeInTheDocument();
    expect(screen.getByText('Secret2')).toBeInTheDocument();
    expect(screen.queryByText('No Secrets found. Please add one.')).not.toBeInTheDocument();
  });

  it('opens form to add new model when Add Secret button is clicked', async () => {
    (useQuery as Mock).mockReturnValue({
      data: [],
      isLoading: false,
      refetch: vi.fn(),
    });

    const { getByText, getAllByTestId } = renderInContext(<UserProperty {...mockProps} />);

    const addButton = getByText('Add Secret');
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(screen.getByText('Add a new Secret')).toBeInTheDocument();
      expect(screen.getByText('Select Secret')).toBeInTheDocument();
    });
  });
  it('renders correct property name for LLM', () => {
    (useQuery as Mock).mockReturnValue({
      data: [],
      isLoading: false,
      refetch: vi.fn(),
    });

    const llmProps = {
      ...mockProps,
      activeProperty: 'llm',
    };

    renderInContext(<UserProperty {...llmProps} />);

    expect(screen.getByText('Add LLM')).toBeInTheDocument();
    expect(screen.getByText('No LLMs found. Please add one.')).toBeInTheDocument();
  });
  it('filters models by activeProperty type', () => {
    (useQuery as Mock).mockReturnValue({
      data: [
        { uuid: '1', type_name: 'secret', model_name: 'Secret1', json_str: {} },
        { uuid: '2', type_name: 'llm', model_name: 'LLM1', json_str: {} },
      ],
      isLoading: false,
      refetch: vi.fn(),
    });

    renderInContext(<UserProperty {...mockProps} />);

    expect(screen.getByText('Secret1')).toBeInTheDocument();
    expect(screen.queryByText('LLM1')).not.toBeInTheDocument();
  });
  it('uses correct schema when adding a new model', async () => {
    (useQuery as Mock).mockReturnValue({
      data: [],
      isLoading: false,
      refetch: vi.fn(),
    });

    const { getByText, getByRole } = renderInContext(<UserProperty {...mockProps} />);

    fireEvent.click(screen.getByText('Add Secret'));

    await waitFor(() => {
      expect(getByText('AnthropicAPIKey')).toBeInTheDocument();
    });

    // Open the select dropdown
    const selectElement = getByRole('combobox');
    fireEvent.mouseDown(selectElement);

    await waitFor(() => {
      expect(getByText('AzureOAIAPIKey')).toBeInTheDocument();
    });

    // on cancel button click, the form should be closed
    const cancelButton = getByText('Cancel');
    fireEvent.click(cancelButton);

    expect(screen.getByText('Add Secret')).toBeInTheDocument();
    expect(screen.getByText('No Secrets found. Please add one.')).toBeInTheDocument();
  });
});
