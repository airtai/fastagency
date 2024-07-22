-- CreateTable
CREATE TABLE "Chat" (
    "id" SERIAL NOT NULL,
    "uuid" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "team_id" INTEGER,
    "team_name" TEXT,
    "team_status" TEXT,
    "chatType" TEXT,
    "shouldShowChat" BOOLEAN NOT NULL DEFAULT false,
    "proposedUserAction" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "userRespondedWithNextAction" BOOLEAN NOT NULL DEFAULT false,
    "emailContent" TEXT,
    "agentChatHistory" TEXT,
    "isExceptionOccured" BOOLEAN NOT NULL DEFAULT false,
    "showLoader" BOOLEAN NOT NULL DEFAULT false,
    "smartSuggestions" JSONB NOT NULL DEFAULT '{ "suggestions": [""], "type": ""}',
    "streamAgentResponse" BOOLEAN NOT NULL DEFAULT false,
    "customerBrief" TEXT,
    "userId" INTEGER,
    "name" TEXT DEFAULT 'New chat',
    "isChatNameUpdated" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "Chat_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Conversation" (
    "id" SERIAL NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "message" TEXT NOT NULL,
    "role" TEXT NOT NULL,
    "agentConversationHistory" TEXT,
    "isLoading" BOOLEAN NOT NULL DEFAULT false,
    "chatId" INTEGER,
    "userId" INTEGER,

    CONSTRAINT "Conversation_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Chat" ADD CONSTRAINT "Chat_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Conversation" ADD CONSTRAINT "Conversation_chatId_fkey" FOREIGN KEY ("chatId") REFERENCES "Chat"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Conversation" ADD CONSTRAINT "Conversation_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
