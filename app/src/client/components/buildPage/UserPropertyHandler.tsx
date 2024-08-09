/* This file should be deleted */

import React, { useEffect, useRef, useState } from 'react';
import { useHistory } from 'react-router-dom';
import _ from 'lodash';

import Button from '../Button';
import ModelForm from '../ModelForm';
import ModelsList from '../ModelsList';
import NotificationBox from '../NotificationBox';

import { navLinkItems } from '../CustomSidebar';

import { getModels, useQuery, updateUserModels, addUserModels, deleteUserModels } from 'wasp/client/operations';
import { capitalizeFirstLetter, filterDataToValidate, dependsOnProperty } from '../../utils/buildPageUtils';
import Loader from '../../admin/common/Loader';
import CustomBreadcrumb from '../CustomBreadcrumb';

import { FormData } from '../../hooks/useForm';
import { useFormDataStack } from './useFormDataStack';
import { FormDataStackItem, Props } from './types';
import { FORM_DATA_STORAGE_KEY } from './utils';
import { getTargetModel, storeFormData } from './utils';
import useDetectRefresh from './useDetectRefresh';
import { SelectedModelSchema } from '../../interfaces/BuildPageInterfaces';

const UserPropertyHandler = ({ data, togglePropertyList }: Props) => {
  const history = useHistory();
  const [isLoading, setIsLoading] = useState(false);
  const [showAddModel, setShowAddModel] = useState(false);
  const [selectedModel, setSelectedModel] = useState(data.schemas[0].name);
  const [notificationErrorMessage, setNotificationErrorMessage] = useState<string | null>(null);
  const { data: allUserProperties, refetch: refetchModels, isLoading: getModelsIsLoading } = useQuery(getModels);
  const [updateExistingModel, setUpdateExistingModel] = useState<SelectedModelSchema | null>(null);
  const { resumeFormData, setResumeFormData, targetModelToAdd, handleFormResume } = useFormDataStack(setShowAddModel);

  const propertyName = data.name;

  useEffect(() => {
    setShowAddModel(false);
  }, [togglePropertyList]);

  useEffect(() => {
    if (data && data.schemas && data.schemas[0].name) {
      const targetModel = targetModelToAdd.current || data.schemas[0].name;
      setSelectedModel(targetModel);
    }
  }, [data]);

  useDetectRefresh(() => {
    sessionStorage.removeItem(FORM_DATA_STORAGE_KEY);
    setShowAddModel(false);
    setUpdateExistingModel(null);
    if (targetModelToAdd.current) {
      targetModelToAdd.current = null;
    }
  });

  const updateModel = (model_type: string) => {
    setSelectedModel(model_type);
    setShowAddModel(true);
  };

  const handleClick = () => {
    setUpdateExistingModel(null);
    updateModel(data.schemas[0].name);
  };
  const handleModelChange = (newModel: string) => {
    setSelectedModel(newModel);
  };

  const onSuccessCallback = async (payload: any): Promise<{ addUserModelResponse: any }> => {
    let addUserModelResponse;
    try {
      setIsLoading(true);
      const mergedData = { ...payload, type_name: propertyName, model_name: selectedModel, uuid: payload.uuid };
      const filteredData = filterDataToValidate(mergedData);
      if (updateExistingModel && !targetModelToAdd.current) {
        await updateUserModels({ data: filteredData, uuid: updateExistingModel.uuid });
        setUpdateExistingModel(null);
      } else {
        //@ts-ignore
        addUserModelResponse = await addUserModels(filteredData);
      }
      refetchModels();
      const isNewDeploymentAdded = propertyName === 'deployment' && !updateExistingModel;
      !isNewDeploymentAdded && setShowAddModel(false);

      handleFormResume(filteredData);
    } catch (error) {
      console.log('error: ', error, 'error.message: ');
      throw error;
    } finally {
      setIsLoading(false);
    }
    return addUserModelResponse;
  };

  const onCancelCallback = (event: React.FormEvent) => {
    event.preventDefault();
    let formDataStack: FormDataStackItem[] = JSON.parse(sessionStorage.getItem(FORM_DATA_STORAGE_KEY) || '[]');
    if (formDataStack.length > 0) {
      const currentItem = formDataStack[formDataStack.length - 1];
      const nextRoute = `/build/${currentItem.source.propertyName}`;
      // @ts-ignore
      setResumeFormData(currentItem.formData);
      targetModelToAdd.current = currentItem.formData.uuid ? null : currentItem.source.selectedModel;

      formDataStack.pop();
      sessionStorage.setItem(FORM_DATA_STORAGE_KEY, JSON.stringify(formDataStack));

      if (nextRoute) {
        history.push(nextRoute);
      }
    } else {
      setShowAddModel(false);
      setResumeFormData(null);
      targetModelToAdd.current = null;
    }
  };

  const onDeleteCallback = async () => {
    try {
      setIsLoading(true);
      if (updateExistingModel) {
        if (allUserProperties) {
          const propertyName = dependsOnProperty(allUserProperties, updateExistingModel.uuid);
          if (propertyName !== '') {
            const currentPropertyName = _.has(updateExistingModel, 'name') ? updateExistingModel.name : '';
            setNotificationErrorMessage(
              `Oops! You can't delete '${currentPropertyName}' because it's being used by '${propertyName}'.`
            );
          } else {
            await deleteUserModels({ uuid: updateExistingModel.uuid, type_name: updateExistingModel.type_name });
            await refetchModels();
            setUpdateExistingModel(null);
            setShowAddModel(false);
          }
        }
      }
    } catch (error) {
      setNotificationErrorMessage(`Error deleting ${propertyName}. Please try again later.`);
    } finally {
      setIsLoading(false);
    }
  };

  const getFilteredProperties = () => {
    if (allUserProperties) {
      const properties = _.filter(allUserProperties, ['type_name', propertyName]);
      return _.sortBy(properties, ['created_at']);
    }
  };

  const updateSelectedModel = (index: number) => {
    if (allUserProperties) {
      const filteredProperties = getFilteredProperties();
      if (filteredProperties) {
        const selectedModel = filteredProperties[index];
        setSelectedModel(selectedModel.model_name);
        // @ts-ignore
        setUpdateExistingModel({ ...selectedModel.json_str, ...{ uuid: selectedModel.uuid } });
        setShowAddModel(true);
        targetModelToAdd.current = null;
      }
    }
  };

  const onClick = () => {
    setNotificationErrorMessage(null);
  };

  const handleAddProperty = (targetPropertyName: string, formData: FormData, key: string) => {
    const targetModel = getTargetModel(data.schemas, selectedModel, key);
    storeFormData(propertyName, selectedModel, targetPropertyName, targetModel, formData, key, updateExistingModel);

    // setShowAddModel(false);
    setShowAddModel(true);
    setUpdateExistingModel(null);
    targetModelToAdd.current = targetModel;

    history.push(`/build/${targetPropertyName}`);
  };

  const propertyHeader = propertyName === 'llm' ? 'LLM' : capitalizeFirstLetter(propertyName);
  const propertyDisplayName = propertyName ? _.find(navLinkItems, ['componentName', propertyName])?.label : '';

  return (
    <>
      <CustomBreadcrumb pageName={`${propertyDisplayName}`} />
      <div className='flex flex-col gap-10'>
        <div className='flex flex-col gap-4'>
          <div className='rounded-lg border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark min-h-[300px] sm:min-h-[600px]'>
            <div className='flex-col flex items-start p-6 gap-3 w-full'>
              <div className={`${showAddModel ? 'hidden' : ''} flex justify-end w-full px-1 py-3`}>
                <Button onClick={handleClick} label={`Add ${propertyHeader}`} />
              </div>
              <div className='flex-col flex w-full'>
                {!showAddModel ? (
                  <ModelsList
                    models={(allUserProperties && getFilteredProperties()) || []}
                    onSelectModel={updateSelectedModel}
                    type_name={propertyName}
                  />
                ) : (
                  <ModelForm
                    allUserProperties={allUserProperties}
                    data={data}
                    selectedModel={selectedModel}
                    updateExistingModel={updateExistingModel}
                    resumeFormData={resumeFormData}
                    propertyHeader={propertyHeader}
                    onModelChange={handleModelChange}
                    onSuccessCallback={onSuccessCallback}
                    onCancelCallback={onCancelCallback}
                    onDeleteCallback={onDeleteCallback}
                    handleAddProperty={handleAddProperty}
                  />
                )}
              </div>
              {notificationErrorMessage && (
                <NotificationBox type='error' onClick={onClick} message={notificationErrorMessage} />
              )}
              {isLoading && (
                <div className='z-[999999] absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 h-screen'>
                  <Loader />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default UserPropertyHandler;
