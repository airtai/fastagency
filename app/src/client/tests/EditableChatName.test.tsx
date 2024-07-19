import { test, expect, vi } from 'vitest';
import { renderInContext } from 'wasp/client/test';
import { screen, render, fireEvent, act } from '@testing-library/react';

import EditableChatName from '../components/EditableChatName';

const mockOnValueChange = vi.fn();
const chatId = 1;
const chatName = 'Test Chat';

test('renders EditableChatName component', async () => {
  renderInContext(
    <EditableChatName
      chatId={chatId}
      chatName={chatName}
      onValueChange={mockOnValueChange}
    />
  );
  const signInItems = await screen.findAllByText('Test Chat');
  expect(signInItems).toHaveLength(1);
  screen.debug();
});

test('shows input box when edit button is clicked', async () => {
  const { getByRole, getByTestId } = renderInContext(
    <EditableChatName
      chatId={chatId}
      chatName={chatName}
      onValueChange={mockOnValueChange}
    />
  );
  fireEvent.click(getByTestId('edit-button'));
  expect(getByRole('textbox')).toBeInTheDocument();
});

test('calls onValueChange when input is blurred', async () => {
  const { getByRole, getByTestId } = renderInContext(
    <EditableChatName
      chatId={chatId}
      chatName={chatName}
      onValueChange={mockOnValueChange}
    />
  );
  fireEvent.click(getByTestId('edit-button'));
  const input = getByRole('textbox');
  fireEvent.change(input, { target: { value: 'New Chat Name' } });
  await act(async () => {
    fireEvent.blur(input);
  });
  expect(mockOnValueChange).toHaveBeenCalledWith(chatId, 'New Chat Name');
});

test('calls onValueChange when form is submitted', async () => {
  const { getByRole, getByTestId } = render(
    <EditableChatName
      chatId={chatId}
      chatName={chatName}
      onValueChange={mockOnValueChange}
    />
  );
  fireEvent.click(getByTestId('edit-button'));
  const input = getByRole('textbox');
  fireEvent.change(input, { target: { value: 'New Chat Name' } });
  await act(async () => {
    const form = getByTestId('edit-form');
    fireEvent.submit(form);
  });
  expect(mockOnValueChange).toHaveBeenCalledWith(chatId, 'New Chat Name');
});
