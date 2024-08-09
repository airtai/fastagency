import React from 'react';

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, fireEvent, waitFor } from '@testing-library/react';

import { renderInContext } from 'wasp/client/test';

import ModelsList from '../components/ModelsList';
import { ItemProps } from '../components/ModelItem'; // Make sure this path is correct

// Mock the ModelItem component
vi.mock('./ModelItem', () => {
  return {
    default: vi.fn(({ model, onClick }: { model: ItemProps; onClick: () => void }) => (
      <div data-testid={`model-item-${model.model_uuid}`} onClick={onClick}>
        {model.model_name}
      </div>
    )),
  };
});

// Mock the ModelItem component
vi.mock('./ModelItem', () => ({
  default: ({ model, onClick }: { model: any; onClick: any }) => (
    <div data-testid={`model-item-${model.model_uuid}`} onClick={onClick}>
      {model.model_name}
    </div>
  ),
}));

describe('ModelsList', () => {
  const mockModels = [
    {
      uuid: 'uuid1',
      user_uuid: 'user1',
      type_name: 'secret',
      model_name: 'Model 1',
      model_uuid: 'model_uuid1',
      json_str: {
        name: 'Model 1 Name',
        api_key: 'api_key_1', // pragma: allowlist secret
      },
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-02T00:00:00Z',
    },
    {
      uuid: 'uuid2',
      user_uuid: 'user1',
      type_name: 'secret',
      model_name: 'Model 2',
      model_uuid: 'model_uuid2',
      json_str: {
        name: 'Model 2 Name',
        api_key: 'api_key_2', // pragma: allowlist secret
      },
      created_at: '2023-01-03T00:00:00Z',
      updated_at: '2023-01-04T00:00:00Z',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the list of models when models are provided', () => {
    const { getByText, getAllByTestId } = renderInContext(
      <ModelsList models={mockModels} onSelectModel={() => {}} type_name='Test' />
    );

    expect(getByText('Model 1 Name')).toBeInTheDocument();
    expect(getByText('Model 2 Name')).toBeInTheDocument();

    const modelItems = getAllByTestId(/model-item-/);
    expect(modelItems).toHaveLength(2);
  });

  it('calls onSelectModel with the correct index when a model is clicked', () => {
    const mockOnSelectModel = vi.fn();
    const { getByRole, getByText } = renderInContext(
      <ModelsList models={mockModels} onSelectModel={mockOnSelectModel} type_name='Test' />
    );

    const selectElement = getByText('Model 2 Name');
    fireEvent.click(selectElement);
    expect(mockOnSelectModel).toHaveBeenCalledWith(1);
  });

  it('displays a message when no models are found', () => {
    renderInContext(<ModelsList models={[]} onSelectModel={() => {}} type_name='Test' />);

    expect(screen.getByText('No Tests found. Please add one.')).toBeInTheDocument();
  });
});
