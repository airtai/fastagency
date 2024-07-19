import React, { useEffect, useState } from 'react';
import _ from 'lodash';

import Button from '../Button';
import ModelForm from '../ModelForm';
import ModelsList from '../ModelsList';
import NotificationBox from '../NotificationBox';

import { SelectedModelSchema } from '../../interfaces/BuildPageInterfaces';
import { navLinkItems } from '../CustomSidebar';

import {
  getModels,
  useQuery,
  updateUserModels,
  addUserModels,
  deleteUserModels,
  propertyDependencies,
} from 'wasp/client/operations';
import { capitalizeFirstLetter, filterDataToValidate, dependsOnProperty } from '../../utils/buildPageUtils';
import Loader from '../../admin/common/Loader';
import CustomBreadcrumb from '../CustomBreadcrumb';
import { useHistory } from 'react-router-dom';

interface Props {
  data: any;
  togglePropertyList: boolean;
}

const UserPropertyHandler = ({ data, togglePropertyList }: Props) => {
  const history = useHistory();
  const [isLoading, setIsLoading] = useState(false);
  const [showAddModel, setShowAddModel] = useState(false);
  const [selectedModel, setSelectedModel] = useState(data.schemas[0].name);
  const [updateExistingModel, setUpdateExistingModel] = useState<SelectedModelSchema | null>(null);
  const propertyName = data.name;
  const { data: allUserProperties, refetch: refetchModels, isLoading: getModelsIsLoading } = useQuery(getModels);

  const [notificationErrorMessage, setNotificationErrorMessage] = useState<string | null>(null);
  useEffect(() => {
    setShowAddModel(false);
  }, [togglePropertyList]);

  useEffect(() => {
    if (data && data.schemas && data.schemas[0].name) {
      setSelectedModel(data.schemas[0].name);
    }
  }, [data]);

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
      if (updateExistingModel) {
        await updateUserModels({ data: filteredData, uuid: updateExistingModel.uuid });
        setUpdateExistingModel(null);
      } else {
        //@ts-ignore
        addUserModelResponse = await addUserModels(filteredData);
      }
      refetchModels();
      const isNewDeploymentAdded = propertyName === 'deployment' && !updateExistingModel;
      !isNewDeploymentAdded && setShowAddModel(false);
    } catch (error) {
      console.log('error: ', error, 'error.message: ');
      // setNotificationErrorMessage(`Error adding/updating ${propertyName}. Please try again later.`);
      throw error;
    } finally {
      setIsLoading(false);
    }

    return addUserModelResponse;
  };

  const onCancelCallback = (event: React.FormEvent) => {
    event.preventDefault();
    setShowAddModel(false);
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
      }
    }
  };

  const onClick = () => {
    setNotificationErrorMessage(null);
  };

  const addPropertyClick = (property_type: string) => {
    setShowAddModel(false);
    setUpdateExistingModel(null);
    handleClick();
    history.push(`/build/${property_type}`);
  };

  const propertyHeader = propertyName === 'llm' ? 'LLM' : capitalizeFirstLetter(propertyName);
  const propertyDisplayName = propertyName ? _.find(navLinkItems, ['componentName', propertyName]).label : '';

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
                    propertyHeader={propertyHeader}
                    onModelChange={handleModelChange}
                    onSuccessCallback={onSuccessCallback}
                    onCancelCallback={onCancelCallback}
                    onDeleteCallback={onDeleteCallback}
                    addPropertyClick={addPropertyClick}
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
