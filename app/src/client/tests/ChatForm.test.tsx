import { test, expect, describe, vi } from 'vitest';
import { fireEvent, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import { renderInContext } from 'wasp/client/test';

import ChatForm from '../components/ChatForm';
import { Chat } from 'wasp/entities';

describe('ChatForm', () => {
  const defaultChatDetails: Chat = {
    id: 1,
    uuid: '1312312312321313',
    createdAt: new Date(),
    updatedAt: new Date(),
    team_id: 1,
    team_name: '',
    team_status: '',
    userRespondedWithNextAction: false,
    agentChatHistory: '',
    isExceptionOccured: false,
    showLoader: false,
    streamAgentResponse: false,
    customerBrief: '',
    userId: 1,
    name: '',
    isChatNameUpdated: false,
    selectedTeam: '',
    isChatTerminated: false,
  };

  test('renders ChatForm and auto submits the form', async () => {
    const handleFormSubmit = vi.fn();
    const currentChatDetails: Chat = {
      id: 1,
      uuid: '1312312312321313',
      createdAt: new Date(),
      updatedAt: new Date(),
      team_id: 1,
      team_name: '',
      team_status: '',
      userRespondedWithNextAction: false,
      agentChatHistory: '',
      isExceptionOccured: false,
      showLoader: false,
      streamAgentResponse: false,
      customerBrief: '',
      userId: 1,
      name: '',
      isChatNameUpdated: false,
      selectedTeam: '',
      isChatTerminated: false,
    };
    const triggerChatFormSubmitMsg = 'Test message';

    const { getByTestId, getByPlaceholderText } = renderInContext(
      <ChatForm
        handleFormSubmit={handleFormSubmit}
        currentChatDetails={currentChatDetails}
        triggerChatFormSubmitMsg={triggerChatFormSubmitMsg}
      />
    );
    expect(getByTestId('chat-form')).toBeInTheDocument();
    expect(handleFormSubmit).toHaveBeenCalledWith(triggerChatFormSubmitMsg, true);
  });
  test('renders ChatForm and submits the form', async () => {
    const handleFormSubmit = vi.fn();
    const currentChatDetails: Chat = {
      id: 1,
      uuid: '1312312312321313',
      createdAt: new Date(),
      updatedAt: new Date(),
      team_id: 1,
      team_name: '',
      team_status: '',
      userRespondedWithNextAction: false,
      agentChatHistory: '',
      isExceptionOccured: false,
      showLoader: false,
      streamAgentResponse: false,
      customerBrief: '',
      userId: 1,
      name: '',
      isChatNameUpdated: false,
      selectedTeam: '',
      isChatTerminated: false,
    };

    renderInContext(
      <ChatForm
        handleFormSubmit={handleFormSubmit}
        currentChatDetails={currentChatDetails}
        triggerChatFormSubmitMsg={null}
      />
    );
    expect(screen.getByTestId('chat-form')).toBeInTheDocument();

    const formInputValue = 'Hello World!';
    const input = screen.getByPlaceholderText('Enter your message...');
    fireEvent.change(input, { target: { value: formInputValue } });
    // @ts-ignore
    expect(input.value).toBe(formInputValue);

    // Simulate form submission
    const form = screen.getByTestId('chat-form');
    fireEvent.submit(form);

    await waitFor(() => expect(handleFormSubmit).toHaveBeenCalledWith(formInputValue));
  });

  test('submits the form only once when submitted multiple times quickly', async () => {
    const handleFormSubmit = vi.fn();
    const currentChatDetails: Chat = {
      id: 1,
      uuid: '1312312312321313',
      createdAt: new Date(),
      updatedAt: new Date(),
      team_id: 1,
      team_name: '',
      team_status: '',
      userRespondedWithNextAction: false,
      agentChatHistory: '',
      isExceptionOccured: false,
      showLoader: false,
      streamAgentResponse: false,
      customerBrief: '',
      userId: 1,
      name: '',
      isChatNameUpdated: false,
      selectedTeam: '',
      isChatTerminated: false,
    };

    renderInContext(
      <ChatForm
        handleFormSubmit={handleFormSubmit}
        currentChatDetails={currentChatDetails}
        triggerChatFormSubmitMsg={null}
      />
    );
    expect(screen.getByTestId('chat-form')).toBeInTheDocument();

    const formInputValue = 'Hello World!';
    const input = screen.getByPlaceholderText('Enter your message...');
    fireEvent.change(input, { target: { value: formInputValue } });
    // @ts-ignore
    expect(input.value).toBe(formInputValue);
    const form = screen.getByTestId('chat-form');

    // Simulate multiple form submissions within 500 ms
    for (let i = 0; i < 10; i++) {
      fireEvent.submit(form);
    }

    await waitFor(() => expect(handleFormSubmit).toHaveBeenCalledTimes(1));
  });

  test('does not submit when the chat message is empty', async () => {
    const handleFormSubmit = vi.fn();
    const currentChatDetails: Chat = {
      id: 1,
      uuid: '1312312312321313',
      createdAt: new Date(),
      updatedAt: new Date(),
      team_id: 1,
      team_name: '',
      team_status: '',
      userRespondedWithNextAction: false,
      agentChatHistory: '',
      isExceptionOccured: false,
      showLoader: false,
      streamAgentResponse: false,
      customerBrief: '',
      userId: 1,
      name: '',
      isChatNameUpdated: false,
      selectedTeam: '',
      isChatTerminated: false,
    };

    renderInContext(
      <ChatForm
        handleFormSubmit={handleFormSubmit}
        currentChatDetails={currentChatDetails}
        triggerChatFormSubmitMsg={null}
      />
    );
    expect(screen.getByTestId('chat-form')).toBeInTheDocument();

    const input = screen.getByPlaceholderText('Enter your message...');
    fireEvent.change(input, { target: { value: '' } });
    // @ts-ignore
    expect(input.value).toBe('');

    // Simulate form submission
    const form = screen.getByTestId('chat-form');
    fireEvent.submit(form);

    await waitFor(() => expect(handleFormSubmit).not.toHaveBeenCalled());
  });

  test('disables form when team_status is inprogress', () => {
    const handleFormSubmit = vi.fn();
    const currentChatDetails = {
      ...defaultChatDetails,
      team_status: 'inprogress',
    };

    renderInContext(<ChatForm handleFormSubmit={handleFormSubmit} currentChatDetails={currentChatDetails} />);

    const input = screen.getByPlaceholderText('Enter your message...');
    const submitButton = screen.getByRole('button');

    expect(input).toBeDisabled();
    expect(submitButton).toBeDisabled();
  });

  test('submits form on Enter key press without Shift', async () => {
    const handleFormSubmit = vi.fn();
    renderInContext(<ChatForm handleFormSubmit={handleFormSubmit} currentChatDetails={defaultChatDetails} />);

    const input = screen.getByPlaceholderText('Enter your message...');
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Test message' } });
    });

    await act(async () => {
      fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    });

    await waitFor(() => {
      expect(handleFormSubmit).toHaveBeenCalledWith('Test message');
    });
  });

  test('does not submit form on Shift+Enter key press', () => {
    const handleFormSubmit = vi.fn();
    renderInContext(<ChatForm handleFormSubmit={handleFormSubmit} currentChatDetails={defaultChatDetails} />);

    const input = screen.getByPlaceholderText('Enter your message...');
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter', shiftKey: true });

    expect(handleFormSubmit).not.toHaveBeenCalled();
  });

  test('submits form on button click', async () => {
    const handleFormSubmit = vi.fn();
    renderInContext(<ChatForm handleFormSubmit={handleFormSubmit} currentChatDetails={defaultChatDetails} />);

    const input = screen.getByPlaceholderText('Enter your message...');
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Test message' } });
    });

    const submitButton = screen.getByRole('button');
    await act(async () => {
      fireEvent.click(submitButton);
    });

    await waitFor(() => {
      expect(handleFormSubmit).toHaveBeenCalledWith('Test message');
    });
  });

  test('handles error during form submission', async () => {
    const handleFormSubmit = vi.fn().mockRejectedValue(new Error('Submission failed'));
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    renderInContext(<ChatForm handleFormSubmit={handleFormSubmit} currentChatDetails={defaultChatDetails} />);

    const input = screen.getByPlaceholderText('Enter your message...');
    fireEvent.change(input, { target: { value: 'Test message' } });

    const form = screen.getByTestId('chat-form');
    fireEvent.submit(form);

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('Error submitting form:', expect.any(Error));
    });

    consoleSpy.mockRestore();
  });
});
