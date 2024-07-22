import { validateForm as apiValidateForm } from 'wasp/client/operations';

export const validateForm = async (data: any, validationURL: string, isSecretUpdate: boolean) => {
  try {
    const response = await apiValidateForm({ data, validationURL, isSecretUpdate });
    return response;
  } catch (error) {
    throw error;
  }
};
