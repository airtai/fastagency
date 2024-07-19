import { useState, useEffect } from 'react';
import _ from 'lodash';
import { JsonSchema, SelectedModelSchema } from '../interfaces/BuildPageInterfaces';

interface UseFormProps {
  jsonSchema: JsonSchema;
  defaultValues?: SelectedModelSchema | null;
}

export interface FormData {
  [key: string]: any;
}

function getValueFromModel(model: SelectedModelSchema, key: keyof SelectedModelSchema): string | number | undefined {
  return typeof model[key] === 'string' || typeof model[key] === 'number'
    ? model[key]
    : model[key]
      ? // @ts-ignore
        model[key].model_name
      : '';
}

export const useForm = ({ jsonSchema, defaultValues }: UseFormProps) => {
  const [formData, setFormData] = useState<{ [key: string]: any }>({});
  const [formErrors, setFormErrors] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    const initialFormData: FormData = {};
    Object.keys(jsonSchema.properties).forEach((key) => {
      const property = jsonSchema.properties[key];
      if (defaultValues) {
        initialFormData[key] = defaultValues.hasOwnProperty(key)
          ? getValueFromModel(defaultValues, key as keyof SelectedModelSchema)
          : '';
      } else {
        if (property.enum && property.enum.length === 1) {
          initialFormData[key] = property.enum[0]; // Auto-set single enum value
        } else {
          if (
            _.has(property, 'anyOf') &&
            _.isEqual(
              _.map(property.anyOf, (o: any) => o.type),
              ['integer', 'null']
            )
          ) {
            initialFormData[key] = null;
          } else {
            initialFormData[key] = property.default ?? ''; // Use default or empty string if no default
          }
        }
      }
    });
    setFormData(initialFormData);
    setFormErrors({}); // Reset errors on schema change
  }, [jsonSchema, defaultValues]);

  const handleChange = (key: string, value: any) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
    setFormErrors((prev) => ({ ...prev, [key]: '' })); // Clear error on change
  };

  return {
    formData,
    handleChange,
    formErrors,
    setFormErrors, // Expose this to allow setting errors from the component
  };
};
