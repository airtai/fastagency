import { useEffect } from 'react';
import { DEPLOYMENT_INSTRUCTIONS } from '../utils/constants';

export const useDeploymentInstructions = (
  updateExistingModel: any,
  type_name: string,
  setInstructionForDeployment: (value: any) => void
) => {
  useEffect(() => {
    if (updateExistingModel && type_name === 'deployment') {
      const msg = DEPLOYMENT_INSTRUCTIONS;

      setInstructionForDeployment((prevState: any) => ({
        ...prevState,
        gh_repo_url: updateExistingModel.gh_repo_url,
        flyio_app_url: updateExistingModel.flyio_app_url,
        instruction: msg
          .replaceAll('<gh_repo_url>', updateExistingModel.gh_repo_url)
          .replaceAll('<flyio_app_url>', updateExistingModel.flyio_app_url),
      }));
    }
  }, [updateExistingModel, type_name, setInstructionForDeployment]);
};
