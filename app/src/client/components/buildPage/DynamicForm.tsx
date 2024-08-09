import React, { useMemo, useRef } from 'react';
import _ from 'lodash';
import { PropertySchemaParser, SetActiveModelType } from './PropertySchemaParser';
import { useEscapeKeyHandler } from '../../hooks/useEscapeKeyHandler';
import { usePropertyManager } from './usePropertyManager';
import { FormField } from './FormField';
import Loader from '../../admin/common/Loader';
import NotificationBox from '../NotificationBox';

interface DynamicFormProps {
  parser: PropertySchemaParser | null;
  setActiveModel: SetActiveModelType;
  refetchUserProperties: () => void;
}

const LoaderContainer = () => (
  <div className='fixed inset-0 z-[999999] flex items-center justify-center bg-white bg-opacity-50'>
    <Loader />
  </div>
);

export const DynamicForm: React.FC<DynamicFormProps> = ({ parser, setActiveModel, refetchUserProperties }) => {
  const { form, schema, handleCtaAction, isLoading, setNotification, notification } = usePropertyManager(
    parser,
    setActiveModel,
    refetchUserProperties
  );

  const formFields = useMemo(() => {
    if (schema && 'json_schema' in schema) {
      return Object.entries(schema.json_schema.properties).map(([key, property]: [string, any]) => {
        if (key === 'uuid') {
          return null;
        }
        const isReferenceField = parser?.checkIfRefField(property);
        let propertyCopy = Object.assign({}, property);
        let isOptionalRefField = false;
        if (isReferenceField) {
          const refFields = parser?.getRefFields();
          const refTypes = parser?.getRefTypes(property);
          if (refTypes && refTypes.length > 0 && refFields && refFields[key]) {
            propertyCopy = refFields[key].htmlForSelectBox;
            isOptionalRefField = refFields[key].isOptional;
          }
        } else {
          const isNonRefButDropDownFields = parser?.getNonRefButDropdownFields();
          if (isNonRefButDropDownFields && isNonRefButDropDownFields[key]) {
            propertyCopy = isNonRefButDropDownFields[key].htmlForSelectBox;
          }
        }
        return (
          <form.Field
            key={key}
            name={key}
            children={(field) => (
              <FormField field={field} property={propertyCopy} fieldKey={key} isOptionalRefField={isOptionalRefField} />
            )}
            validators={{
              onChange: ({ value }) => undefined,
            }}
          />
        );
      });
    } else {
      return null;
    }
  }, [schema, form]);

  const cancelButtonRef = useRef<HTMLButtonElement>(null);
  useEscapeKeyHandler(cancelButtonRef);

  const notificationOnClick = () => {
    setNotification(null);
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
    >
      {isLoading && <LoaderContainer />}
      {notification && <NotificationBox type='error' onClick={notificationOnClick} message={notification} />}
      {formFields}
      <form.Subscribe
        selector={(state) => [state.canSubmit, state.isSubmitting]}
        children={([canSubmit, isSubmitting]) => (
          <>
            {isSubmitting && <LoaderContainer />}
            <div className='col-span-full mt-7'>
              <div className='float-right'>
                <button
                  className='rounded-md px-3.5 py-2.5 text-sm border border-airt-error text-airt-primary hover:bg-opacity-10 hover:bg-airt-error shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                  type='reset'
                  onClick={() => handleCtaAction('cancel')}
                  ref={cancelButtonRef}
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
                <button
                  data-testid='form-submit-button'
                  type='submit'
                  className={`ml-3 rounded-md px-3.5 py-2.5 text-sm bg-airt-primary text-airt-font-base hover:bg-opacity-85 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 ${
                    !canSubmit ? 'cursor-not-allowed disabled' : ''
                  }`}
                  disabled={!canSubmit}
                >
                  {isSubmitting ? 'Saving...' : 'Save'}
                </button>
              </div>
              {parser?.getUserFlow() === 'update_model' && (
                <button
                  type='button'
                  className='float-left rounded-md px-3.5 py-2.5 text-sm border bg-airt-error text-airt-font-base hover:bg-opacity-80 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                  disabled={isSubmitting}
                  data-testid='form-cancel-button'
                  onClick={() => handleCtaAction('delete')}
                >
                  Delete
                </button>
              )}
            </div>
          </>
        )}
      />
    </form>
  );
};
