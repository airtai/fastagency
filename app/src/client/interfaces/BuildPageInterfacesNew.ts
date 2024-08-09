export interface JsonSchema {
  $defs?: { [key: string]: SchemaDefs };
  properties: { [key: string]: Property };
  required?: string[];
  title: string;
  type: string;
}

export interface SchemaDefs {
  properties: { [key: string]: Property };
  required?: string[];
  title: string;
  type: string;
}

export interface Property {
  description?: string;
  title?: string;
  type?: string;
  format?: string;
  const?: string;
  default?: any;
  enum?: string[];
  allOf?: Array<{ $ref: string }>;
  maxLength?: number;
  minLength?: number;
  anyOf?: SchemaReference[];
  $ref?: string;
}

interface SchemaReference {
  $ref?: string;
  type?: string;
}

export interface Schema {
  name: string;
  json_schema: JsonSchema;
}

export interface ListOfSchemas {
  name: string;
  schemas: Schema[];
}

export interface PropertiesSchema {
  list_of_schemas: ListOfSchemas[];
}

export interface SelectedModelSchema {
  uuid: string;
  user_uuid: string;
  type_name: string;
  model_name: string;
  json_str: {
    name: string;
    api_key: string;
  };
  created_at: string;
  updated_at: string;
  name?: string;
  api_key?: string;
  app_deploy_status?: string;
  gh_repo_url?: string;
  flyio_app_url?: string;
}
