-- Update records with duplicate names for the same user
UPDATE "Model"
SET json_str = jsonb_set(
    json_str::jsonb,
    '{name}',
    -- Append a random 5-digit suffix to the name
    to_jsonb(json_str->>'name' || '_' || LPAD(FLOOR(RANDOM() * 100000)::text, 5, '0'))
)
-- Select records with duplicate names
WHERE (user_uuid, json_str->>'name') IN (
    SELECT user_uuid, json_str->>'name'
    FROM "Model"
    GROUP BY user_uuid, json_str->>'name'
    HAVING COUNT(*) > 1
)
-- Exclude the first occurrence of each duplicate set
AND uuid NOT IN (
    SELECT DISTINCT ON (user_uuid, json_str->>'name') uuid
    FROM "Model"
    ORDER BY user_uuid, json_str->>'name', created_at
);
