/* This file should be deleted */

import { useState, useEffect, useRef } from 'react';
import { useHistory } from 'react-router-dom';
import { processFormDataStack, FORM_DATA_STORAGE_KEY } from './utils';
import { SelectedModelSchema } from '../../interfaces/BuildPageInterfaces';

export const useFormDataStack = (setShowAddModel: React.Dispatch<React.SetStateAction<boolean>>) => {
  const history = useHistory();
  const [resumeFormData, setResumeFormData] = useState<SelectedModelSchema | null>(null);
  const targetModelToAdd = useRef<string | null>(null);

  const handleFormResume = (filteredData: any) => {
    const { currentItem, nextRoute, updatedStack } = processFormDataStack(filteredData);

    if (currentItem) {
      setShowAddModel(true);
      // @ts-ignore
      setResumeFormData(currentItem.formData);
      targetModelToAdd.current = currentItem.formData.uuid ? null : currentItem.source.selectedModel;

      sessionStorage.setItem(FORM_DATA_STORAGE_KEY, JSON.stringify(updatedStack));

      if (nextRoute) {
        history.push(nextRoute);
      }
    } else {
      setShowAddModel(false);
      setResumeFormData(null);
      targetModelToAdd.current = null;
    }
  };

  return {
    resumeFormData,
    setResumeFormData,
    targetModelToAdd,
    handleFormResume,
  };
};
