// src/components/ModelForm.tsx
import React from 'react';
import { SchemaCategory, ApiSchema, JsonSchema, SelectedModelSchema } from '../interfaces/BuildPageInterfaces';

import ModelFormContainer from './ModelFormContainer';
import DynamicFormBuilder from './DynamicFormBuilder';
import { getSchemaByName } from '../utils/buildPageUtils';

interface ModelFormProps {
  allUserProperties: any;
  data: SchemaCategory;
  selectedModel: string;
  updateExistingModel: SelectedModelSchema | null;
  propertyHeader: string;
  onModelChange: (model: string) => void;
  onSuccessCallback: (data: any) => void;
  onCancelCallback: (event: React.FormEvent) => void;
  onDeleteCallback: (data: any) => void;
  addPropertyClick: (property_type: string) => void;
}

const ModelForm: React.FC<ModelFormProps> = ({
  allUserProperties,
  data,
  selectedModel,
  updateExistingModel,
  propertyHeader,
  onModelChange,
  onSuccessCallback,
  onCancelCallback,
  onDeleteCallback,
  addPropertyClick,
}) => {
  const modelSchemas: ApiSchema[] = data.schemas;
  const initialModelSchema: JsonSchema = getSchemaByName(data.schemas, selectedModel);
  const validationURL: string = `models/${data.name}/${selectedModel}/validate`;
  return (
    <div>
      {modelSchemas && (
        <>
          {/* {<h2 className='sm:mt-6 text-lg font-semibold text-airt-primary'>Update model</h2>} */}
          {
            <ModelFormContainer
              propertyHeader={propertyHeader}
              selectedModel={selectedModel}
              modelSchemas={modelSchemas}
              onModelChange={onModelChange}
              updateExistingModel={updateExistingModel ?? null}
            />
          }
          {initialModelSchema && (
            <DynamicFormBuilder
              allUserProperties={allUserProperties}
              type_name={data.name}
              jsonSchema={initialModelSchema}
              validationURL={validationURL}
              updateExistingModel={updateExistingModel ?? null}
              onSuccessCallback={onSuccessCallback}
              onCancelCallback={onCancelCallback}
              onDeleteCallback={onDeleteCallback}
              addPropertyClick={addPropertyClick}
            />
          )}
        </>
      )}
    </div>
  );
};

export default ModelForm;
