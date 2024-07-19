-- Update type_name and model_name for specific records
UPDATE "Model"
SET "type_name" = 'deployment',
    "model_name" = 'Deployment'
WHERE "type_name" = 'application';
