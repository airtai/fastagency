/*
  Warnings:

  - You are about to drop the column `chatType` on the `Chat` table. All the data in the column will be lost.
  - You are about to drop the column `emailContent` on the `Chat` table. All the data in the column will be lost.
  - You are about to drop the column `proposedUserAction` on the `Chat` table. All the data in the column will be lost.
  - You are about to drop the column `shouldShowChat` on the `Chat` table. All the data in the column will be lost.
  - You are about to drop the column `smartSuggestions` on the `Chat` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "Chat" DROP COLUMN "chatType",
DROP COLUMN "emailContent",
DROP COLUMN "proposedUserAction",
DROP COLUMN "shouldShowChat",
DROP COLUMN "smartSuggestions";
