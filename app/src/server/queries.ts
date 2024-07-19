import _ from 'lodash';
import { type DailyStats, type User, type PageViewSource, type Chat, type Conversation } from 'wasp/entities';
import { HttpError } from 'wasp/server';
import {
  type GetDailyStats,
  type GetPaginatedUsers,
  type GetModels,
  type PropertyDependencies,
  type GetChats,
  type GetConversations,
  type GetChat,
} from 'wasp/server/operations';
import { FASTAGENCY_SERVER_URL } from './common/constants';

type DailyStatsWithSources = DailyStats & {
  sources: PageViewSource[];
};

type DailyStatsValues = {
  dailyStats: DailyStatsWithSources;
  weeklyStats: DailyStatsWithSources[];
};

export const getDailyStats: GetDailyStats<void, DailyStatsValues> = async (_args, context) => {
  if (!context.user?.isAdmin) {
    throw new HttpError(401);
  }
  const dailyStats = await context.entities.DailyStats.findFirstOrThrow({
    orderBy: {
      date: 'desc',
    },
    include: {
      sources: true,
    },
  });

  const weeklyStats = await context.entities.DailyStats.findMany({
    orderBy: {
      date: 'desc',
    },
    take: 7,
    include: {
      sources: true,
    },
  });

  return { dailyStats, weeklyStats };
};

type GetPaginatedUsersInput = {
  skip: number;
  cursor?: number | undefined;
  hasPaidFilter: boolean | undefined;
  emailContains?: string;
  subscriptionStatus?: string[];
};
type GetPaginatedUsersOutput = {
  users: Pick<
    User,
    'id' | 'email' | 'username' | 'lastActiveTimestamp' | 'hasPaid' | 'subscriptionStatus' | 'stripeId'
  >[];
  totalPages: number;
};

export const getPaginatedUsers: GetPaginatedUsers<GetPaginatedUsersInput, GetPaginatedUsersOutput> = async (
  args,
  context
) => {
  let subscriptionStatus = args.subscriptionStatus?.filter((status) => status !== 'hasPaid');
  subscriptionStatus = subscriptionStatus?.length ? subscriptionStatus : undefined;

  const queryResults = await context.entities.User.findMany({
    skip: args.skip,
    take: 10,
    where: {
      email: {
        contains: args.emailContains || undefined,
        mode: 'insensitive',
      },
      hasPaid: args.hasPaidFilter,
      subscriptionStatus: {
        in: subscriptionStatus || undefined,
      },
    },
    select: {
      id: true,
      email: true,
      username: true,
      lastActiveTimestamp: true,
      hasPaid: true,
      subscriptionStatus: true,
      stripeId: true,
    },
    orderBy: {
      id: 'desc',
    },
  });

  const totalUserCount = await context.entities.User.count({
    where: {
      email: {
        contains: args.emailContains || undefined,
      },
      hasPaid: args.hasPaidFilter,
      subscriptionStatus: {
        in: subscriptionStatus || undefined,
      },
    },
  });
  const totalPages = Math.ceil(totalUserCount / 10);

  return {
    users: queryResults,
    totalPages,
  };
};

type GetModelsInput = {
  type_name?: string;
};
type PropertyValues = {
  uuid: string;
  user_uuid: string;
  type_name: string;
  model_name: string;
  model_uuid: string;
  json_str: {
    name: string;
    api_key: string;
  };
  created_at: string;
  updated_at: string;
};

export const getModels: GetModels<GetModelsInput, PropertyValues[]> = async (_args, context) => {
  try {
    let url = `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/models`;
    if (_.has(_args, 'type_name')) {
      url = `${url}?type_name=${_args.type_name}`;
    }
    const response = await fetch(url, {
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

type PropertyDependenciesInput = {
  properties: string[];
};

type PropertyDependenciesValues = {
  [key: string]: number;
};

export const propertyDependencies: PropertyDependencies<
  PropertyDependenciesInput,
  PropertyDependenciesValues[]
> = async (_args, context) => {
  try {
    let retVal: any = {};
    const promises = _args.properties.map(async function (property: string) {
      if (!property) return;
      const url = `${FASTAGENCY_SERVER_URL}/user/${context.user.uuid}/models?type_name=${property}`;
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const json: any = (await response.json()) as { detail?: string }; // Parse JSON once

      if (!response.ok) {
        const errorMsg = json.detail || `HTTP error with status code ${response.status}`;
        console.error('Server Error:', errorMsg);
        throw new Error(errorMsg);
      }
      retVal[property] = json.length;
    });

    await Promise.all(promises);
    return retVal;
  } catch (error: any) {
    throw new HttpError(500, error.message);
  }
};

export const getChats: GetChats<void, Chat[]> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }
  return context.entities.Chat.findMany({
    where: {
      user: {
        id: context.user.id,
      },
    },
    orderBy: { id: 'desc' },
  });
};

type GetConversationPayload = {
  chatId: number;
};

export const getConversations: GetConversations<GetConversationPayload, Conversation[]> = async (args, context) => {
  if (!context.user) {
    throw new HttpError(401);
  }
  let conversation = null;
  try {
    if (context.user.isAdmin) {
      conversation = context.entities.Conversation.findMany({
        where: { chatId: args.chatId },
        orderBy: { id: 'asc' },
      });
    } else {
      conversation = context.entities.Conversation.findMany({
        where: { chatId: args.chatId, userId: context.user.id },
        orderBy: { id: 'asc' },
      });
    }

    return conversation;
  } catch (error) {
    console.error('Error while fetching conversations:', error);
    return [];
  }
};

type getChatFromUUIDPayload = {
  chatUUID: string | null | undefined;
};

export const getChatFromUUID: GetChat<getChatFromUUIDPayload, Chat> = async (args: any, context: any) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  let chat = null;

  if (context.user.isAdmin) {
    chat = await context.entities.Chat.findFirst({
      where: {
        uuid: args.chatUUID,
      },
    });
  } else {
    chat = await context.entities.Chat.findFirst({
      where: {
        uuid: args.chatUUID,
        userId: context.user.id,
      },
    });
  }
  return chat;
};

type GetChatPayload = {
  chatId: number;
};

export const getChat: GetChat<GetChatPayload, Chat> = async (args: any, context: any) => {
  if (!context.user) {
    throw new HttpError(401);
  }

  let chat = null;

  if (context.user.isAdmin) {
    chat = await context.entities.Chat.findFirstOrThrow({
      where: {
        id: args.chatId,
      },
    });
  } else {
    chat = await context.entities.Chat.findFirstOrThrow({
      where: {
        id: args.chatId,
        userId: context.user.id,
      },
    });
  }
  return chat;
};
