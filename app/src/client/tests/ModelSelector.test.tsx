import React from 'react';

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';

import { renderInContext } from 'wasp/client/test';
import selectEvent from 'react-select-event';

import { ModelSelector } from '../components/buildPage/ModelSelector';
import { PropertySchemaParser, SetActiveModelType } from '../components/buildPage/PropertySchemaParser';

const mockSchemas = [
  {
    name: 'AnthropicAPIKey',
    json_schema: {
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
    },
  },
  {
    name: 'AzureOAIAPIKey',
    json_schema: {
      properties: {
        name: {
          description: 'The name of the item',
          minLength: 1,
          title: 'Name',
          type: 'string',
        },
        api_key: {
          description: 'The API Key from Azure OpenAI',
          title: 'Api Key',
          type: 'string',
        },
      },
      required: ['name', 'api_key'],
      title: 'AzureOAIAPIKey',
      type: 'object',
    },
  },
];

const mockPropertySchemasList = {
  name: 'secret',
  schemas: mockSchemas,
};

const parser = new PropertySchemaParser(mockPropertySchemasList);
const mockSetActiveModel: SetActiveModelType = vi.fn();

describe('ModelSelector', () => {
  it('renders correct number of options', () => {
    const { getByRole } = renderInContext(<ModelSelector parser={parser} setActiveModel={mockSetActiveModel} />);

    expect(screen.getByText('Select Secret')).toBeInTheDocument();

    // Open the select dropdown
    const selectElement = getByRole('combobox');
    fireEvent.mouseDown(selectElement);

    const options = screen.getAllByRole('option');
    expect(options).toHaveLength(mockPropertySchemasList.schemas.length);
  });

  it('renders correct number of options', () => {
    const { getByRole } = renderInContext(<ModelSelector parser={parser} setActiveModel={mockSetActiveModel} />);

    expect(screen.getByText('Select Secret')).toBeInTheDocument();

    // Open the select dropdown
    const selectElement = getByRole('combobox');
    fireEvent.mouseDown(selectElement);

    const options = screen.getAllByRole('option');
    expect(options).toHaveLength(mockSchemas.length);
  });

  it('calls setActiveModel with correct value when option is selected', async () => {
    const { getByRole, getByText } = renderInContext(
      <ModelSelector parser={parser} setActiveModel={mockSetActiveModel} />
    );

    expect(getByText('AnthropicAPIKey')).toBeInTheDocument();

    // Open the select dropdown
    const selectElement = getByRole('combobox');
    fireEvent.mouseDown(selectElement);

    // Select an option
    await selectEvent.select(selectElement, 'AzureOAIAPIKey');

    expect(mockSetActiveModel).toHaveBeenCalledWith('AzureOAIAPIKey');
  });
});
