import { sendMsgToNatsServer } from './nats';

async function getChat(chatId, context) {
  return await context.entities.Chat.findFirst({
    where: {
      id: chatId,
    },
    select: {
      id: true,
    },
  });
}

export async function updateDB(context, chatId, message, conversationId, socketConversationHistory, isChatTerminated) {
  let obj = {};
  try {
    const jsonString = message.replace(/True/g, true).replace(/False/g, false);
    obj = JSON.parse(jsonString);
  } catch (error) {
    obj = { message: message, smart_suggestions: [] };
  }
  await context.entities.Conversation.update({
    where: {
      id: conversationId,
    },
    data: {
      isLoading: false,
      message: obj.message,
      agentConversationHistory: socketConversationHistory,
    },
  });

  // const smart_suggestions = isExceptionOccured
  //   ? {
  //       suggestions: ["Let's try again"],
  //       type: 'oneOf',
  //     }
  //   : obj.smart_suggestions;

  await context.entities.Chat.update({
    where: {
      id: chatId,
    },
    data: {
      team_status: 'completed',
      isChatTerminated: isChatTerminated,
    },
  });
}

export const socketFn = (io, context) => {
  // When a new user is connected
  io.on('connection', async (socket) => {
    if (socket.data.user) {
      const userEmail = socket.data.user.email;
      const userUUID = socket.data.user.uuid;
      console.log('========');
      console.log('a user connected: ', userEmail);

      socket.on(
        'sendMessageToTeam',
        async (currentChatDetails, selectedTeamUUID, allMessagesOrUserQuery, conversationId) => {
          let message = '';
          let shouldCallInitiateChat = true;
          if (typeof allMessagesOrUserQuery === 'string') {
            message = allMessagesOrUserQuery;
            shouldCallInitiateChat = false;
          } else {
            message = allMessagesOrUserQuery[0].content;
          }
          sendMsgToNatsServer(
            socket,
            context,
            currentChatDetails,
            selectedTeamUUID,
            userUUID,
            message,
            conversationId,
            shouldCallInitiateChat
          );
        }
      );
    }
  });
};
