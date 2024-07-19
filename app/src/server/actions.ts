import { v4 as uuidv4 } from 'uuid';
import { type User, type Chat, type Conversation } from 'wasp/entities';
import { HttpError } from 'wasp/server';
import {
  // type StripePayment,
  type UpdateCurrentUser,
  type UpdateUserById,
  type GetAvailableModels,
  type ValidateForm,
  type UpdateUserModels,
  type AddUserModels,
  type DeleteUserModels,
  type CreateNewChat,
  type CreateNewAndReturnAllConversations,
  type CreateNewAndReturnLastConversation,
  type UpdateCurrentChat,
  type UpdateCurrentConversation,
  type GetAgentResponse,
  type UserModelSetup,
  type DeleteLastConversationInChat,
  type RetryTeamChat,
} from 'wasp/server/operations';
// import Stripe from 'stripe';
// import type { StripePaymentResult } from '../shared/types';
// import { fetchStripeCustomer, createStripeCheckoutSession } from './payments/stripeUtils.js';
// import { TierIds } from '../shared/constants.js';

import { FASTAGENCY_SERVER_URL } from './common/constants';

// export const stripePayment: StripePayment<string, StripePaymentResult> = async (tier, context) => {
//   if (!context.user || !context.user.email) {
//     throw new HttpError(401);
//   }

//   let priceId;
//   if (tier === TierIds.HOBBY) {
//     priceId = process.env.HOBBY_SUBSCRIPTION_PRICE_ID!;
//   } else if (tier === TierIds.PRO) {
//     priceId = process.env.PRO_SUBSCRIPTION_PRICE_ID!;
//   } else {
//     throw new HttpError(400, 'Invalid tier');
//   }

//   let customer: Stripe.Customer;
//   let session: Stripe.Checkout.Session;
//   try {
//     customer = await fetchStripeCustomer(context.user.email);
//     session = await createStripeCheckoutSession({
//       priceId,
//       customerId: customer.id,
//     });
//   } catch (error: any) {
//     throw new HttpError(500, error.message);
//   }

//   await context.entities.User.update({
//     where: {
//       id: context.user.id,
//     },
//     data: {
//       checkoutSessionId: session.id,
//       stripeId: customer.id,
//     },
//   });

//   return {
//     sessionUrl: session.url,
//     sessionId: session.id,
//   };
// };

export const updateUserById: UpdateUserById<{ id: number; data: Partial<User> }, User> = async (
  { id, data },
  context
) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  if (!context.user.isAdmin) {
    throw new HttpError(403);
  }

  const updatedUser = await context.entities.User.update({
    where: {
      id,
    },
    data,
  });

  return updatedUser;
};

export const updateCurrentUser: UpdateCurrentUser<Partial<User>, User> = async (user, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  return context.entities.User.update({
    where: {
      id: context.user.id,
    },
    data: user,
  });
};

export const getAvailableModels: GetAvailableModels<void, any> = async (user, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  try {
    const response = await fetch(`${FASTAGENCY_SERVER_URL}/models/schemas`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

    if (!response.ok) {
      const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
      console.error('Server Error:', errorMsg);
      throw new Error(errorMsg);
    }

    return json;
  } catch (error: any) {
    throw new HttpError(500, error.message);
  }
};

type AddModelsValues = {
  uuid: string;
  userId?: number;
  model?: string;
  base_url?: string;
  api_type?: string;
  api_version?: string;
  api_key?: string;
  type_name?: string;
  model_name?: string;
  llm?: any;
  summarizer_llm?: any;
  bing_api_key?: any;
  system_message?: string;
  viewport_size?: number;
};

type AddUserModelsPayload = {
  data: AddModelsValues;
  type_name: string;
  model_name: string;
  uuid: string;
};

export const addUserModels: AddUserModels<AddUserModelsPayload, any> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }
  try {
    const url = `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/models/${args.type_name}/${args.model_name}/${args.uuid}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...args }),
    });
    const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

    if (!response.ok) {
      const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
      console.error('Server Error:', errorMsg);
      throw new Error(errorMsg);
    }

    return json;
  } catch (error: any) {
    throw new HttpError(500, error.message);
  }
};

type UpdateUserModelsValues = {
  uuid: string;
  userId?: number;
  model?: string;
  base_url?: string;
  api_type?: string;
  api_version?: string;
  api_key?: string;
  type_name?: string;
  model_name?: string;
};

type UpdateUserModelsPayload = {
  data: UpdateUserModelsValues;
  uuid: string;
};

export const updateUserModels: UpdateUserModels<UpdateUserModelsPayload, void> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }
  try {
    const url = `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/models/${args.data.type_name}/${args.data.model_name}/${args.uuid}`;
    console.log(JSON.stringify({ ...args.data }));
    const response = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...args.data }),
    });
    const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

    if (!response.ok) {
      const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
      console.error('Server Error:', errorMsg);
      throw new Error(errorMsg);
    }
  } catch (error: any) {
    throw new HttpError(500, error.message);
  }
};

type DeleteUserModelsPayload = {
  uuid: string;
  type_name: string;
};

export const deleteUserModels: DeleteUserModels<DeleteUserModelsPayload, void> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  try {
    const url = `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/models/${args.type_name}/${args.uuid}`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    });
    const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

    if (!response.ok) {
      const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
      console.error('Server Error:', errorMsg);
      throw new Error(errorMsg);
    }
  } catch (error: any) {
    throw new HttpError(500, error.message);
  }
};

export const validateForm: ValidateForm<{ data: any; validationURL: string; isSecretUpdate: boolean }, any> = async (
  { data, validationURL, isSecretUpdate }: { data: any; validationURL: string; isSecretUpdate: boolean },
  context: any
) => {
  if (!context.user) {
    throw new HttpError(401);
  }
  try {
    if (!data.uuid) data.uuid = uuidv4();
    const url = isSecretUpdate
      ? `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/${validationURL}`
      : `${FASTAGENCY_SERVER_URL}/${validationURL}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const json = await response.json();
    if (!response.ok) {
      throw new HttpError(
        response.status,
        JSON.stringify(json.detail) || `HTTP error with status code ${response.status}`
      );
    }
    if (!json.uuid) {
      json.uuid = data.uuid;
    }
    if (isSecretUpdate) {
      if (data.api_key) {
        json.api_key = data.api_key;
      }
    }
    const retVal = isSecretUpdate ? json : data;
    return retVal;
  } catch (error: any) {
    throw new HttpError(error.statusCode || 500, error.message || 'Server or network error occurred');
  }
};

export const createNewChat: CreateNewChat<any, Chat> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  if (!context.user.hasPaid) {
    throw new HttpError(500, 'No Subscription Found');
  }

  const chat = await context.entities.Chat.create({
    data: {
      user: { connect: { id: context.user.id } },
      selectedTeam: args.teamName ? args.teamName : null,
    },
  });

  // if (args.teamName) {
  //   await context.entities.Conversation.create({
  //     data: {
  //       chat: { connect: { id: chat.id } },
  //       user: { connect: { id: context.user.id } },
  //       message: `${args.task}`,
  //       role: 'user',
  //     },
  //   });
  // }

  return chat;
};

export const updateCurrentChat: UpdateCurrentChat<{ id: number; data: Partial<Chat> }, Chat> = async (
  { id, data },
  context
) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  const chat = await context.entities.Chat.update({
    where: {
      id: id,
    },
    data,
  });

  return chat;
};

export const updateCurrentConversation: UpdateCurrentConversation<
  { id: number; data: Partial<Conversation> },
  Conversation
> = async ({ id, data }, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  const conversation = await context.entities.Conversation.update({
    where: {
      id: id,
    },
    data,
  });

  return conversation;
};

export const deleteLastConversationInChat: DeleteLastConversationInChat<number, Conversation[]> = async (
  chatId: number,
  context: any
) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  const conversations = await context.entities.Conversation.findMany({
    where: { chatId: chatId },
    orderBy: { id: 'desc' },
  });

  const lastConvId = conversations[0].id;
  await context.entities.Conversation.delete({
    where: { id: lastConvId },
  });

  const allConversations = await context.entities.Conversation.findMany({
    where: { chatId: chatId, userId: context.user.id },
    orderBy: { id: 'asc' },
  });
  return allConversations;
};

export const retryTeamChat: RetryTeamChat<number, [Chat, string]> = async (chatId: number, context: any) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  const newChat = await context.entities.Chat.create({
    data: {
      user: { connect: { id: context.user.id } },
    },
  });

  const allChatConversations = await context.entities.Conversation.findMany({
    where: { chatId: chatId, userId: context.user.id },
    orderBy: { id: 'asc' },
  });

  const lastInitialConversationindex = allChatConversations.findIndex(
    (conversation: Conversation) => conversation.agentConversationHistory !== null
  );

  let initialConversations = allChatConversations.slice(
    0,
    lastInitialConversationindex >= 0 ? lastInitialConversationindex : allChatConversations.length
  );
  let lastConversation = initialConversations.pop();

  initialConversations = initialConversations.map((conversation: Conversation) => {
    return {
      message: conversation.message,
      role: conversation.role,
      isLoading: conversation.isLoading,
      chatId: newChat.id,
      userId: context.user.id,
    };
  });

  await context.entities.Conversation.createMany({
    data: initialConversations,
  });

  return [newChat, lastConversation.message];
};

export const createNewAndReturnAllConversations: CreateNewAndReturnAllConversations<
  { chatId: number; userQuery: string; role: 'user' | 'assistant' },
  Conversation[]
> = async ({ chatId, userQuery, role }, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  if (!context.user.hasPaid) {
    throw new HttpError(500, 'No Subscription Found');
  }

  await context.entities.Conversation.create({
    data: {
      chat: { connect: { id: chatId } },
      user: { connect: { id: context.user.id } },
      message: userQuery,
      role,
    },
  });

  return context.entities.Conversation.findMany({
    where: { chatId: chatId, userId: context.user.id },
    orderBy: { id: 'asc' },
  });
};

export const createNewAndReturnLastConversation: CreateNewAndReturnLastConversation<
  {
    chatId: number;
    userQuery: string;
    role: 'user' | 'assistant';
    isLoading: boolean;
  },
  Conversation
> = async ({ chatId, userQuery, role, isLoading }, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  if (!context.user.hasPaid) {
    throw new HttpError(500, 'No Subscription Found');
  }

  return await context.entities.Conversation.create({
    data: {
      chat: { connect: { id: chatId } },
      user: { connect: { id: context.user.id } },
      message: userQuery,
      role,
      isLoading,
    },
  });
};

type AgentPayload = {
  chatId: number;
  messages: any;
  model_name: string;
  uuid: string;
};

export const getAgentResponse: GetAgentResponse<AgentPayload, Record<string, any>> = async (
  {
    chatId,
    messages,
    model_name,
    uuid,
  }: {
    chatId: number;
    messages: any;
    model_name: string;
    uuid: string;
  },
  context: any
) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  const payload = {
    chat_id: chatId,
    message: messages,
    user_id: context.user.id,
  };
  console.log('===========');
  console.log('Payload to Python server');
  console.log(payload);
  console.log('===========');
  try {
    const url = `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/chat/${model_name}/${uuid}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

    if (!response.ok) {
      const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
      console.error('Server Error:', errorMsg);
      throw new Error(errorMsg);
    }

    return {
      content: json['content'],
      smart_suggestions: json['smart_suggestions'],
      team_status: json['team_status'],
      team_name: json['team_name'],
      team_id: json['team_id'],
      ...(json['customer_brief'] !== undefined && {
        customer_brief: json['customer_brief'],
      }),
      ...(json['conversation_name'] !== undefined && {
        conversation_name: json['conversation_name'],
      }),
      ...(json['is_exception_occured'] !== undefined && {
        is_exception_occured: Boolean(json['is_exception_occured']),
      }),
    };
  } catch (error: any) {
    throw new HttpError(500, 'Something went wrong. Please try again later');
  }
};

export const userModelSetup: UserModelSetup<void, any> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }
  const userUUID = context.user.uuid;
  try {
    const url = `${FASTAGENCY_SERVER_URL}/user/${userUUID}/setup`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

    if (!response.ok) {
      const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
      console.error(`Server Error: ${errorMsg} for user ${userUUID}`);
      if (!errorMsg.includes('toolbox already exists')) {
        throw new Error(errorMsg);
      }
    }

    await context.entities.User.update({
      where: {
        id: context.user.id,
      },
      data: {
        isSetUpComplete: true,
      },
    });
    return json;
  } catch (error: any) {
    console.log('-----');
    console.log(`error.message: ${error.message}`);
    throw new HttpError(500, error.message);
  }
};
