-- Populate uuid field with unique UUIDs for existing entries
UPDATE "User" SET "uuid" = gen_random_uuid() WHERE "uuid" IS NULL;
