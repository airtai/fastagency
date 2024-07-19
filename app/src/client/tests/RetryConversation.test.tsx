import { test, expect, vi, describe } from 'vitest';
import { renderInContext } from 'wasp/client/test';
import { fireEvent, screen, waitFor } from '@testing-library/react';
import * as operations from 'wasp/client/operations';

import { type Chat } from 'wasp/entities';
import RetryConversation from '../components/RetryConversation';

vi.mock('wasp/client/operations', async (importOriginal) => {
  const mod = await importOriginal<typeof import('wasp/client/operations')>();
  return {
    ...mod,
    retryTeamChat: vi.fn().mockResolvedValue([{ uuid: '123' }, 'Sample user message']),
  };
});

describe('RetryConversation', () => {
  test('Renders the component', async () => {
    const mockOnClick = vi.fn();
    const currentChatDetails: Partial<Chat> = {
      team_name: 'Team Name',
      isExceptionOccured: true,
      id: 1,
    };

    renderInContext(
      <RetryConversation
        // @ts-ignore
        currentChatDetails={currentChatDetails}
        retryOnClick={mockOnClick}
      />
    );

    fireEvent.click(screen.getByText("Let's try again"));

    expect(mockOnClick).toHaveBeenCalledWith(null, false, true);
  });
});
