-- AlterTable
ALTER TABLE "User" ADD COLUMN     "hasAcceptedTos" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "hasSubscribedToMarketingEmails" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "isSignUpComplete" BOOLEAN NOT NULL DEFAULT false;
