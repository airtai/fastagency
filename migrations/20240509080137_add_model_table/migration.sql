-- CreateTable
CREATE TABLE "Model" (
    "uuid" TEXT NOT NULL,
    "user_uuid" UUID NOT NULL,
    "type_name" TEXT NOT NULL,
    "model_name" TEXT NOT NULL,
    "json_str" JSONB NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Model_pkey" PRIMARY KEY ("uuid")
);
