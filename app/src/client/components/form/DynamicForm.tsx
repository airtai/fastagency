import React from 'react';
import _ from 'lodash';
import { TextInput } from './TextInput';
import { SelectInput } from './SelectInput';
import { TextArea } from './TextArea';
import { SECRETS_TO_MASK } from '../../utils/constants';
import { JsonSchema } from '../../interfaces/BuildPageInterfaces';
import { FormData } from '../../hooks/useForm';
import AgentConversationHistory from '../AgentConversationHistory';

interface DynamicFormProps {
  jsonSchema: JsonSchema;
  formData: FormData;
  handleChange: (key: string, value: any) => void;
  formErrors: Record<string, string>;
  refValues: Record<string, any>;
  isLoading: boolean;
  addPropertyClick: (property_type: string) => void;
  updateExistingModel: any;
  handleSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
  instructionForDeployment: Record<string, string> | null;
  onCancelCallback: (event: React.FormEvent) => void;
  cancelButtonRef: React.RefObject<HTMLButtonElement>;
  onDeleteCallback: (data: any) => void;
}

const DynamicForm: React.FC<DynamicFormProps> = ({
  jsonSchema,
  formData,
  handleChange,
  formErrors,
  refValues,
  isLoading,
  addPropertyClick,
  updateExistingModel,
  handleSubmit,
  instructionForDeployment,
  onCancelCallback,
  cancelButtonRef,
  onDeleteCallback,
}) => {
  return (
    <form onSubmit={handleSubmit} className='px-6.5 py-2'>
      {Object.entries(jsonSchema.properties).map(([key, property]) => {
        if (key === 'uuid') {
          return null;
        }
        const inputValue = formData[key] || '';
        let propertyTypes = null;
        let isRequired = false;
        let formElementsObject = property;
        if (_.has(property, '$ref') || _.has(property, 'anyOf') || _.has(property, 'allOf')) {
          if (refValues[key]) {
            formElementsObject = refValues[key].htmlSchema;
            propertyTypes = refValues[key].propertyTypes;
            isRequired = refValues[key].isRequired;
          }
        }
        return (
          <div key={key} className='w-full mt-2'>
            <label htmlFor={key}>{formElementsObject.title}</label>
            {formElementsObject.enum ? (
              <SelectInput
                id={key}
                value={inputValue}
                options={formElementsObject.enum}
                onChange={(value) => handleChange(key, value)}
                propertyTypes={propertyTypes}
                addPropertyClick={addPropertyClick}
                isRequired={isRequired}
              />
            ) : key === 'system_message' ? (
              <TextArea
                id={key}
                value={inputValue}
                placeholder={formElementsObject.description || ''}
                onChange={(value) => handleChange(key, value)}
              />
            ) : (
              <TextInput
                id={key}
                type={_.includes(SECRETS_TO_MASK, key) && typeof inputValue === 'string' ? 'password' : 'text'}
                value={inputValue}
                placeholder={formElementsObject.description || ''}
                onChange={(value) => handleChange(key, value)}
              />
            )}
            {formErrors[key] && <div style={{ color: 'red' }}>{formErrors[key]}</div>}
          </div>
        );
      })}
      {instructionForDeployment && instructionForDeployment.instruction && (
        <div className='w-full mt-8'>
          <AgentConversationHistory
            agentConversationHistory={instructionForDeployment.instruction}
            isDeploymentInstructions={true}
            containerTitle='Deployment Details and Next Steps'
          />
        </div>
      )}
      <div className='col-span-full mt-7'>
        <div className='float-right'>
          <button
            className='rounded-md px-3.5 py-2.5 text-sm border border-airt-error text-airt-primary hover:bg-opacity-10 hover:bg-airt-error shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
            disabled={isLoading}
            data-testid='form-cancel-button'
            onClick={onCancelCallback}
            ref={cancelButtonRef}
          >
            Cancel
          </button>
          <button
            type='submit'
            className='ml-3 rounded-md px-3.5 py-2.5 text-sm bg-airt-primary text-airt-font-base hover:bg-opacity-85 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
            disabled={isLoading}
            data-testid='form-submit-button'
          >
            Save
          </button>
        </div>

        {updateExistingModel && (
          <button
            type='button'
            className='float-left rounded-md px-3.5 py-2.5 text-sm border bg-airt-error text-airt-font-base hover:bg-opacity-80 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
            disabled={isLoading}
            data-testid='form-cancel-button'
            onClick={onDeleteCallback}
          >
            Delete
          </button>
        )}
      </div>
    </form>
  );
};

export default DynamicForm;
