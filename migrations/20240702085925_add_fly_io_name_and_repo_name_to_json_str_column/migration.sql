-- Add default values for fly io name and repo name in the json str column for deployments
UPDATE "Model"
SET "json_str" = jsonb_set(
    jsonb_set(
        "json_str"::jsonb,
        '{fly_app_name}',
        '"N/A"',
        true
    ),
    '{repo_name}',
    '"N/A"',
    true
)
WHERE "type_name" = 'deployment';
