import { useState } from 'react';
import { validateForm } from '../services/commonService';
import {
  getFormSubmitValues,
  getSecretUpdateFormSubmitValues,
  getSecretUpdateValidationURL,
} from '../utils/buildPageUtils';
import { DEPLOYMENT_INSTRUCTIONS } from '../utils/constants';
import { SelectedModelSchema } from '../interfaces/BuildPageInterfaces';
import { parseValidationErrors } from '../app/utils/formHelpers';

interface UseFormSubmissionProps {
  type_name: string;
  validationURL: string;
  updateExistingModel: SelectedModelSchema | null;
  onSuccessCallback: (data: any) => void;
  setFormErrors: (errors: any) => void;
}

export const useFormSubmission = ({
  type_name,
  validationURL,
  updateExistingModel,
  onSuccessCallback,
  setFormErrors,
}: UseFormSubmissionProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotification] = useState({
    message: 'Oops. Something went wrong. Please try again later.',
    show: false,
  });
  const [instructionForDeployment, setInstructionForDeployment] = useState<Record<string, string> | null>(null);
  const isDeployment = type_name === 'deployment';

  const handleSubmit = async (event: React.FormEvent, formData: any, refValues: Record<string, any>) => {
    event.preventDefault();
    if (instructionForDeployment && !updateExistingModel) {
      return;
    }
    setIsLoading(true);
    const isSecretUpdate = type_name === 'secret' && !!updateExistingModel;
    let formDataToSubmit: any = {};
    let updatedValidationURL = validationURL;

    if (isSecretUpdate) {
      formDataToSubmit = getSecretUpdateFormSubmitValues(formData, updateExistingModel);
      updatedValidationURL = getSecretUpdateValidationURL(validationURL, updateExistingModel);
    } else {
      formDataToSubmit = getFormSubmitValues(refValues, formData, false);
    }

    try {
      const response = await validateForm(formDataToSubmit, updatedValidationURL, isSecretUpdate);
      const onSuccessCallbackResponse: any = await onSuccessCallback(response);

      if (isDeployment && !updateExistingModel) {
        setInstructionForDeployment((prevState) => ({
          ...prevState,
          gh_repo_url: response.gh_repo_url,
          instruction: DEPLOYMENT_INSTRUCTIONS.replaceAll('<gh_repo_url>', onSuccessCallbackResponse.gh_repo_url),
        }));
      }
    } catch (error: any) {
      try {
        const errorMsgObj = JSON.parse(error.message);
        const errors = parseValidationErrors(errorMsgObj);
        setFormErrors(errors);
      } catch (e: any) {
        setNotification({ message: error.message || notification.message, show: true });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const notificationOnClick = () => {
    setNotification({ ...notification, show: false });
  };

  return {
    isLoading,
    notification,
    instructionForDeployment,
    handleSubmit,
    notificationOnClick,
    setInstructionForDeployment,
  };
};
