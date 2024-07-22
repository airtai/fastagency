import React, { useRef } from 'react';
import { useForm } from '../hooks/useForm';
import { useFormSubmission } from '../hooks/useFormSubmission';
import { usePropertyReferenceValues } from '../hooks/usePropertyReferenceValues';
import { useDeploymentInstructions } from '../hooks/useDeploymentInstructions';
import { useEscapeKeyHandler } from '../hooks/useEscapeKeyHandler';
import Loader from '../admin/common/Loader';
import NotificationBox from './NotificationBox';
import { DynamicFormBuilderProps } from '../interfaces/DynamicFormBuilderInterface';
import AgentConversationHistory from './AgentConversationHistory';
import { DEPLOYMENT_PREREQUISITES } from '../utils/constants';
import DynamicForm from './form/DynamicForm';

const DynamicFormBuilder: React.FC<DynamicFormBuilderProps> = ({
  allUserProperties,
  type_name,
  jsonSchema,
  validationURL,
  updateExistingModel,
  onSuccessCallback,
  onCancelCallback,
  onDeleteCallback,
  addPropertyClick,
}) => {
  const { formData, handleChange, formErrors, setFormErrors } = useForm({
    jsonSchema,
    defaultValues: updateExistingModel,
  });

  const {
    isLoading,
    notification,
    instructionForDeployment,
    handleSubmit,
    notificationOnClick,
    setInstructionForDeployment,
  } = useFormSubmission({
    type_name,
    validationURL,
    updateExistingModel,
    onSuccessCallback,
    setFormErrors,
  });

  const refValues = usePropertyReferenceValues({
    jsonSchema,
    allUserProperties,
    updateExistingModel,
  });

  const cancelButtonRef = useRef<HTMLButtonElement>(null);
  const isDeployment = type_name === 'deployment';

  useDeploymentInstructions(updateExistingModel, type_name, setInstructionForDeployment);
  useEscapeKeyHandler(cancelButtonRef);

  const onSubmit = (event: React.FormEvent) => {
    handleSubmit(event, formData, refValues);
  };

  return (
    <>
      {!instructionForDeployment && isDeployment && (
        <div className='w-full mt-8 px-6.5 py-2'>
          <AgentConversationHistory
            agentConversationHistory={DEPLOYMENT_PREREQUISITES}
            isDeploymentInstructions={true}
            containerTitle='Prerequisites for Deployment Generation and Deployment'
          />
        </div>
      )}
      <DynamicForm
        jsonSchema={jsonSchema}
        formData={formData}
        handleChange={handleChange}
        formErrors={formErrors}
        refValues={refValues}
        isLoading={isLoading}
        addPropertyClick={addPropertyClick}
        updateExistingModel={updateExistingModel}
        handleSubmit={onSubmit}
        instructionForDeployment={instructionForDeployment}
        onCancelCallback={onCancelCallback}
        cancelButtonRef={cancelButtonRef}
        onDeleteCallback={onDeleteCallback}
      />
      {isLoading && (
        <div className='z-[999999] absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 h-screen'>
          <Loader />
        </div>
      )}
      {notification.show && (
        <NotificationBox type='error' onClick={notificationOnClick} message={notification.message} />
      )}
    </>
  );
};

export default DynamicFormBuilder;
