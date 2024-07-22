import {
  updateCurrentChat,
  updateCurrentConversation,
  createNewAndReturnAllConversations,
  createNewAndReturnLastConversation,
  getAgentResponse,
  deleteLastConversationInChat,
} from 'wasp/client/operations';

import { type Conversation, type Chat } from 'wasp/entities';
import { SelectedModelSchema } from '../interfaces/BuildPageInterfaces';

export const exceptionMessage = 'Oops! An unexpected problem occurred. Please click the button below to retry.';

type OutputMessage = {
  role: string;
  content: string;
};

export function prepareOpenAIRequest(input: Conversation[]): OutputMessage[] {
  const messages: OutputMessage[] = input.map((message) => {
    return {
      role: message.role,
      content: message.message,
    };
  });
  return messages;
}

export async function updateCurrentChatStatus(
  activeChatId: number,
  isUserRespondedWithNextAction: boolean,
  removeQueryParameters: Function
) {
  isUserRespondedWithNextAction && removeQueryParameters();
  await updateCurrentChat({
    id: activeChatId,
    data: {
      userRespondedWithNextAction: isUserRespondedWithNextAction,
    },
  });
}

export async function getFormattedChatMessages(activeChatId: number, userQuery: string, retrySameChat: boolean) {
  let allConversations;
  if (retrySameChat) {
    allConversations = await deleteLastConversationInChat(activeChatId);
  } else {
    allConversations = await createNewAndReturnAllConversations({
      chatId: activeChatId,
      userQuery,
      role: 'user',
    });
  }
  const messages: any = prepareOpenAIRequest(allConversations);
  await updateCurrentChat({
    id: activeChatId,
    data: {
      showLoader: true,
    },
  });
  return messages;
}

export async function getInProgressConversation(activeChatId: number, userQuery: string, retrySameChat: boolean) {
  const message = retrySameChat ? '' : userQuery;
  const inProgressConversation = await createNewAndReturnLastConversation({
    chatId: activeChatId,
    userQuery: message,
    role: 'assistant',
    isLoading: true,
  });
  return inProgressConversation;
}

export const continueChat = async (
  socket: any,
  currentChatDetails: any,
  inProgressConversation: any,
  userQuery: string,
  messages: any,
  activeChatId: number,
  selectedTeam: SelectedModelSchema
) => {
  socket.emit('sendMessageToTeam', currentChatDetails, selectedTeam.uuid, userQuery, inProgressConversation.id);
  await updateCurrentChat({
    id: activeChatId,
    data: {
      showLoader: false,
      team_status: 'inprogress',
    },
  });
};

export const initiateChat = async (
  activeChatId: number,
  currentChatDetails: any,
  inProgressConversation: any,
  socket: any,
  messages: any,
  refetchChatDetails: () => void,
  selectedTeam: SelectedModelSchema
) => {
  const response = await getAgentResponse({
    chatId: activeChatId,
    messages: messages,
    model_name: selectedTeam.model_name,
    uuid: selectedTeam.uuid,
  });
  await handleAgentResponse(
    response,
    currentChatDetails,
    inProgressConversation,
    socket,
    messages,
    activeChatId,
    refetchChatDetails,
    selectedTeam
  );
};

export const handleAgentResponse = async (
  response: any,
  currentChatDetails: any,
  inProgressConversation: any,
  socket: any,
  messages: any,
  activeChatId: number,
  refetchChatDetails: () => void,
  selectedTeam: SelectedModelSchema
) => {
  if (!!response.customer_brief) {
    socket.emit('sendMessageToTeam', currentChatDetails, selectedTeam.uuid, messages, inProgressConversation.id);
  }

  response['content'] &&
    (await updateCurrentConversation({
      id: inProgressConversation.id,
      data: {
        isLoading: false,
        message: response['content'],
      },
    }));

  const chatName = currentChatDetails.isChatNameUpdated
    ? null
    : response['conversation_name']
      ? response['conversation_name']
      : null;

  await updateCurrentChat({
    id: activeChatId,
    data: {
      showLoader: false,
      team_id: response['team_id'],
      team_name: response['team_name'],
      team_status: response['team_status'],
      isExceptionOccured: response['is_exception_occured'] || false,
      customerBrief: response['customer_brief'],
      ...(chatName && {
        name: chatName,
        isChatNameUpdated: true,
      }),
    },
  });

  chatName && refetchChatDetails();
};

export const handleChatError = async (err: any, activeChatId: number, inProgressConversation: any, history: any) => {
  await updateCurrentChat({
    id: activeChatId,
    data: { showLoader: false },
  });
  console.log('Error: ' + err.message);
  if (err.message === 'No Subscription Found') {
    history.push('/pricing');
  } else {
    await updateCurrentConversation({
      //@ts-ignore
      id: inProgressConversation.id,
      data: {
        isLoading: false,
        message: exceptionMessage,
      },
    });
    await updateCurrentChat({
      id: activeChatId,
      data: {
        showLoader: false,
        isExceptionOccured: true,
      },
    });
  }
};
