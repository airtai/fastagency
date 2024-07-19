import React, { useState } from 'react';
import TerminalDisplay from './TerminalDisplay';

interface AgentConversationHistoryProps {
  agentConversationHistory: string;
  initialState?: boolean;
  isAgentWindow?: boolean;
  isDeploymentInstructions?: boolean;
  containerTitle?: string;
}

const AgentConversationHistory: React.FC<AgentConversationHistoryProps> = ({
  agentConversationHistory,
  initialState = false,
  isAgentWindow = false,
  isDeploymentInstructions = false,
  containerTitle,
}) => {
  const [showHistory, setShowHistory] = useState(initialState);

  const toggleHistory = () => {
    setShowHistory(!showHistory);
  };

  const bg = isDeploymentInstructions ? '' : 'bg-airt-primary';
  const maxH = isDeploymentInstructions ? 700 : 400;

  return (
    <div data-testid='agent-loader' className={`flex items-center group flex-col ${isDeploymentInstructions} pb-3`}>
      <div
        style={{
          ...(isDeploymentInstructions ? {} : { maxWidth: `${isAgentWindow ? '745px' : '800px'}` }),
          ...(isDeploymentInstructions ? {} : { left: `${isAgentWindow ? '15px' : '0px'}` }),
          margin: '0 auto 20',
        }}
        className={`relative block w-full`}
      >
        <TerminalDisplay
          messages={agentConversationHistory}
          maxHeight={maxH}
          isOpenOnLoad={isDeploymentInstructions ? isDeploymentInstructions : isAgentWindow}
          theme={isDeploymentInstructions ? 'modelDeployment' : null}
          containerTitle={containerTitle}
        />
      </div>
    </div>
  );
};

export default AgentConversationHistory;
