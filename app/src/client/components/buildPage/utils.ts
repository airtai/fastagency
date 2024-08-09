/* This file should be deleted */

import _ from 'lodash';
import { FormData } from '../../hooks/useForm';
import { FormDataStackItem } from './types';

export const FORM_DATA_STORAGE_KEY = 'formDataStack';

export const getTargetModel = (schemas: any, selectedModel: string, key: string) => {
  const matchedModel = _.find(schemas, ['name', selectedModel]);
  let retVal = null;
  if (!matchedModel) {
    return retVal;
  }
  const matchedModeRef = matchedModel.json_schema.properties[key];
  if (_.has(matchedModeRef, '$ref')) {
    // remove "Ref" word from the end of the string
    const refValue = matchedModeRef['$ref'].split('/').pop();
    retVal = refValue.replace(/Ref$/, '');
  }
  return retVal;
};

export const storeFormData = (
  propertyName: string,
  selectedModel: string,
  targetPropertyName: string,
  targetModel: string,
  formData: FormData,
  key: string,
  updateExistingModel: any
) => {
  const newStackItem: FormDataStackItem = {
    source: {
      propertyName: propertyName,
      selectedModel: selectedModel,
    },
    target: {
      propertyName: targetPropertyName,
      selectedModel: targetModel,
    },
    formData: updateExistingModel ? updateExistingModel : formData,
    key: key,
  };

  let formDataStack: FormDataStackItem[] = JSON.parse(sessionStorage.getItem(FORM_DATA_STORAGE_KEY) || '[]');
  formDataStack.push(newStackItem);
  sessionStorage.setItem(FORM_DATA_STORAGE_KEY, JSON.stringify(formDataStack));
};

export const processFormDataStack = (
  filteredData: any
): {
  currentItem: FormDataStackItem | null;
  nextRoute: string | null;
  updatedStack: FormDataStackItem[];
} => {
  let formDataStack: FormDataStackItem[] = JSON.parse(sessionStorage.getItem(FORM_DATA_STORAGE_KEY) || '[]');
  let currentItem = null;
  let nextRoute = null;

  if (formDataStack.length > 0) {
    currentItem = formDataStack[formDataStack.length - 1];
    const key: string = currentItem.key;
    currentItem.formData[key] = {
      name: currentItem.target.selectedModel,
      type: currentItem.target.propertyName,
      uuid: filteredData.uuid,
    };

    // Remove the completed item from the stack
    formDataStack.pop();

    // Check if there are more levels to process
    if (formDataStack.length > 0) {
      const nextItem = formDataStack[formDataStack.length - 1];
      nextRoute = `/build/${nextItem.target.propertyName}`;
    } else {
      // If the stack is empty, we've completed all levels
      nextRoute = `/build/${currentItem.source.propertyName}`;
    }
  }

  return { currentItem, nextRoute, updatedStack: formDataStack };
};
