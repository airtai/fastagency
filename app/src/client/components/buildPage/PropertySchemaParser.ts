import _ from 'lodash';

import { ListOfSchemas, Schema } from '../../interfaces/BuildPageInterfacesNew';

export enum UserFlow {
  UPDATE_MODEL = 'update_model',
  ADD_MODEL = 'add_model',
}

export type SetActiveModelType = (model: string | null) => void;

export interface SelectOption {
  value: string;
  label: string;
}

export interface UserProperties {
  uuid: string;
  user_uuid: string;
  type_name: string;
  model_name: string;
  model_uuid?: string;
  json_str: {
    name: string;
    [key: string]: any;
  };
  created_at: string;
  updated_at: string;
}

interface PropertySchemaParserInterface {
  getUserFlow(): UserFlow;
  setUserFlow(flow: UserFlow): void;
  getModelNames(): SelectOption[];
  getActiveModel(): string | null;
  setActiveModel(model: string | null): void;
  getPropertyName(): string;
  getValidationURL(): string;
  getDefaultValues(): { [key: string]: any };
  getSchemaForModel(): Schema | undefined;
  getSchema(): Schema;
  setActiveModelObj(obj: any): void;
  getActiveModelObj(): any | null;
  getSecretUpdateValidationURL(): string;
  setUserProperties(o: UserProperties[]): void;
  getUserProperties(): UserProperties[] | null;
  getRefFields(): { [key: string]: any };
  getNonRefButDropdownFields(): { [key: string]: any };
  findFirstReferringPropertyName(uuid: string): UserProperties | null;
  checkIfRefField(property: any): boolean;
  getRefTypes(property: any): string[];
}

export class PropertySchemaParser implements PropertySchemaParserInterface {
  private readonly propertySchemas: ListOfSchemas;
  private userFlow: UserFlow;
  private activeModel: string | null;
  private readonly propertyName: string;
  private activeModelObj: any;
  private schema: Schema | undefined;
  private userProperties: UserProperties[] | null;
  private refFields: { [key: string]: any } = {};
  private nonRefButDropdownFields: { [key: string]: any } = {};

  constructor(propertySchemas: ListOfSchemas) {
    this.propertySchemas = propertySchemas;
    this.propertyName = propertySchemas.name;
    this.userFlow = UserFlow.ADD_MODEL;
    this.activeModel = null;
    this.activeModelObj = null;
    this.userProperties = null;
  }

  private capitalizeWords(str: string): string {
    return str
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  public getSchemaForModel(): Schema | undefined {
    if (!this.activeModel) {
      return undefined;
    }

    this.schema = this.propertySchemas.schemas.find((s) => s.name === this.activeModel);
    return this.schema;
  }

  public getSchema(): Schema {
    if (this.schema) {
      return this.schema;
    }

    return this.propertySchemas.schemas[0];
  }

  public checkIfRefField(property: any): boolean {
    return _.has(property, '$ref') || _.has(property, 'anyOf') || _.has(property, 'allOf');
  }

  public getDefaultValues(): { [key: string]: any } {
    const schema = this.getSchema();
    const defaultValues: { [key: string]: any } = {};
    this.refFields = {};
    this.nonRefButDropdownFields = {};

    if ('json_schema' in schema) {
      Object.entries(schema.json_schema.properties).forEach(([key, property]: [string, any]) => {
        const isReferenceField = this.checkIfRefField(property);
        if (isReferenceField) {
          this.handleReferenceField(key, property, defaultValues);
        } else {
          this.handleNonReferenceField(key, property, defaultValues);
        }
      });
    }
    return defaultValues;
  }

  private handleReferenceField(key: string, property: any, defaultValues: { [key: string]: any }): void {
    const refTypes = this.getRefTypes(property);
    const matchingProperties = this.getMatchingProperties(refTypes);
    const enumValues = this.createEnumValues(matchingProperties);
    const isOptional = this.isOptionalField(property);
    const defaultValue = this.getDefaultValueForRefField(key, enumValues, isOptional);

    this.refFields[key] = {
      property: matchingProperties,
      htmlForSelectBox: {
        description: '',
        enum: enumValues,
        default: defaultValue,
        title: this.capitalizeWords(key),
      },
      initialFormValue: defaultValue?.value ?? null,
      isOptional: isOptional,
    };
    defaultValues[key] = this.refFields[key].initialFormValue;
  }

  public getRefTypes(property: any): string[] {
    if (_.has(property, '$ref')) {
      return [property.$ref.split('/').pop()?.replace(/Ref$/, '') ?? ''];
    } else if (_.has(property, 'anyOf') || _.has(property, 'allOf')) {
      const items: any[] = (property as any).anyOf || (property as any).allOf || [];
      return items
        .filter((item: any) => _.has(item, '$ref'))
        .map((item: any) => item.$ref.split('/').pop()?.replace(/Ref$/, '') ?? '');
    }
    return [];
  }

  private getMatchingProperties(refTypes: string[]): UserProperties[] {
    if (!this.userProperties) return [];
    return this.userProperties.filter((prop) => refTypes.includes(prop.model_name));
  }

  private isOptionalField(property: any): boolean {
    if (_.has(property, 'anyOf')) {
      return property.anyOf.some((p: any) => p.type === 'null');
    }
    return false;
  }

  private handleNonReferenceField(key: string, property: any, defaultValues: { [key: string]: any }): void {
    const isDropDownField = Array.isArray(property.enum);
    if (isDropDownField) {
      this.handleDropdownField(key, property, defaultValues);
    } else {
      defaultValues[key] = this.getNonDropdownDefaultValue(key, property);
    }
  }

  private handleDropdownField(key: string, property: any, defaultValues: { [key: string]: any }): void {
    const defaultValue = this.getDefaultValueForDropdownField(key, property);
    const enumValues = property.enum.map((i: string) => ({ label: i, value: i }));

    this.nonRefButDropdownFields[key] = {
      htmlForSelectBox: {
        description: '',
        enum: enumValues,
        default: defaultValue,
        title: this.capitalizeWords(key),
      },
      initialFormValue: defaultValue?.value ?? null,
    };
    defaultValues[key] = this.nonRefButDropdownFields[key].initialFormValue;
  }

  private createEnumValues(properties: UserProperties[]): SelectOption[] {
    return properties.map((prop) => ({
      value: prop.uuid,
      label: prop.json_str.name,
    }));
  }

  private getDefaultValueForRefField(
    key: string,
    enumValues: SelectOption[],
    isOptional: boolean
  ): SelectOption | null {
    if (this.activeModelObj?.json_str?.[key]) {
      const matchingUserProperty = this.getMatchingUserProperty(this.activeModelObj.json_str[key].uuid);
      if (matchingUserProperty) {
        return { label: matchingUserProperty.json_str.name, value: matchingUserProperty.uuid };
      }
    }
    return isOptional ? null : enumValues[0] || null;
  }

  private getDefaultValueForDropdownField(key: string, property: any): SelectOption | null {
    if (this.activeModelObj?.json_str?.[key]) {
      const existingValue = this.activeModelObj.json_str[key];
      return { label: existingValue, value: existingValue };
    }
    const defaultValueFromSchema = property.default;
    return defaultValueFromSchema ? { label: defaultValueFromSchema, value: defaultValueFromSchema } : null;
  }

  private getNonDropdownDefaultValue(key: string, property: any): any {
    return this.activeModelObj?.json_str?.[key] ?? property.default ?? '';
  }

  public getUserFlow(): UserFlow {
    return this.userFlow;
  }

  public setUserFlow(flow: UserFlow): void {
    this.userFlow = flow;
  }

  public getModelNames(): SelectOption[] {
    return this.propertySchemas.schemas.map((s) => ({ value: s.name, label: s.name }));
  }

  public getActiveModel(): string | null {
    return this.activeModel;
  }

  public setActiveModel(model: string | null): void {
    this.activeModel = model;
  }

  public getPropertyName(): string {
    return this.propertyName;
  }

  public getValidationURL(): string {
    return `models/${this.propertyName}/${this.activeModel}/validate`;
  }

  public setActiveModelObj(obj: any): void {
    this.activeModelObj = obj;
  }

  public getActiveModelObj(): any {
    return this.activeModelObj;
  }

  public getSecretUpdateValidationURL(): string {
    return `models/${this.propertyName}/${this.activeModel}/${this.activeModelObj.uuid}/validate`;
  }

  public setUserProperties(o: UserProperties[]): void {
    this.userProperties = o;
  }

  public getUserProperties(): UserProperties[] | null {
    return this.userProperties;
  }

  public getRefFields(): { [key: string]: any } {
    return this.refFields;
  }

  public getNonRefButDropdownFields(): { [key: string]: any } {
    return this.nonRefButDropdownFields;
  }

  public getMatchingUserProperty(uuid: string): UserProperties | null {
    return this.userProperties?.find((prop) => prop.uuid === uuid) || null;
  }

  public findFirstReferringPropertyName(uuid: string): UserProperties | null {
    if (!this.userProperties) {
      return null;
    }

    for (const userProperty of this.userProperties) {
      const jsonStr = userProperty.json_str;

      for (const [key, value] of Object.entries(jsonStr)) {
        if (typeof value !== 'object' || value === null) {
          continue;
        }

        if ('uuid' in value && value.uuid === uuid) {
          return userProperty;
        }
      }
    }

    return null;
  }
}
