import { test, expect, vi, describe } from 'vitest';
import { renderInContext } from 'wasp/client/test';
import { screen, render, fireEvent, act } from '@testing-library/react';

import AgentConversationHistory from '../components/AgentConversationHistory';

const agentConversationHistory = 'Test History';

describe('AgentConversationHistory', () => {
  test('renders AgentConversationHistory component with isAgentWindow prop', async () => {
    renderInContext(
      <AgentConversationHistory
        agentConversationHistory={agentConversationHistory}
        isAgentWindow={true}
      />
    );
    const historyItems = await screen.findAllByText('Test History');
    expect(historyItems).toHaveLength(1);
    screen.debug();
  });
});
