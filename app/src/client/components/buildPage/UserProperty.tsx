import React, { useEffect, useState, memo } from 'react';

import _ from 'lodash';
import { getModels, useQuery } from 'wasp/client/operations';

import CustomBreadcrumb from '../CustomBreadcrumb';
import Button from '../Button';
import ModelsList from '../ModelsList';
import { DynamicForm } from '../buildPage/DynamicForm';
import { ModelSelector } from '../buildPage/ModelSelector';
import { navLinkItems } from '../CustomSidebar';
import { PropertiesSchema } from '../../interfaces/BuildPageInterfacesNew';
import LoadingComponent from '../LoadingComponent';
import { usePropertySchemaParser } from './usePropertySchemaParser';

import { filerOutComponentData, capitalizeFirstLetter, filterPropertiesByType } from '../buildPage/buildPageUtilsNew';
import { UserFlow } from './PropertySchemaParser';

interface Props {
  activeProperty: string;
  propertiesSchema: PropertiesSchema;
  sideNavItemClickCount: number;
}

export const UserProperty = memo(({ activeProperty, propertiesSchema, sideNavItemClickCount }: Props) => {
  const propertyHeader = _.find(navLinkItems, ['componentName', activeProperty])?.label;
  const propertyName = activeProperty === 'llm' ? 'LLM' : capitalizeFirstLetter(activeProperty);
  const propertySchemasList = filerOutComponentData(propertiesSchema, activeProperty);

  const { parser, activeModel, createParser } = usePropertySchemaParser(propertySchemasList);

  const { data: userProperties, refetch: refetchUserProperties, isLoading: isLoading } = useQuery(getModels);
  const userPropertiesByType = (userProperties && filterPropertiesByType(userProperties, activeProperty)) || [];

  const setActiveModel = (model: string | null, userFlow: UserFlow = UserFlow.ADD_MODEL) => {
    createParser({ propertySchemasList, activeModel: model, userFlow: userFlow, userProperties });
  };

  const addProperty = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setActiveModel(propertySchemasList.schemas[0].name);
  };

  const getSelectedUserProperty = (index: number) => {
    const selectedProperty = userPropertiesByType[index];
    createParser({
      propertySchemasList,
      activeModel: selectedProperty.model_name,
      activeModelObj: selectedProperty,
      userFlow: UserFlow.UPDATE_MODEL,
      userProperties: userProperties,
    });
  };

  useEffect(() => {
    setActiveModel(null);
  }, [sideNavItemClickCount]);

  const title = parser?.getUserFlow() === UserFlow.ADD_MODEL ? `Add a new ${propertyName}` : `Update ${propertyName}`;

  return (
    <>
      <CustomBreadcrumb pageName={`${propertyHeader}`} />
      <div className='flex flex-col gap-10'>
        <div className='rounded-lg border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark min-h-[300px] sm:min-h-[600px]'>
          {isLoading ? (
            <LoadingComponent theme='dark' />
          ) : (
            <div className='flex-col flex items-start p-6 gap-3 w-full'>
              {!activeModel ? (
                <>
                  <div className={`${false ? 'hidden' : ''} flex justify-end w-full px-1 py-3`}>
                    <Button onClick={addProperty} label={`Add ${propertyName}`} />
                  </div>
                  {userPropertiesByType.length === 0 && (
                    <div className='flex flex-col gap-3'>
                      {/* <h2 className='text-lg font-semibold text-airt-primary'>Available Models</h2> */}
                      <p className='text-airt-primary mt-1 -mt-3 opacity-50'>{`No ${propertyHeader} found. Please add one.`}</p>
                    </div>
                  )}
                  {userPropertiesByType.length > 0 && (
                    <div className='flex-col flex w-full'>
                      <ModelsList
                        models={userPropertiesByType}
                        onSelectModel={getSelectedUserProperty}
                        type_name={propertyName}
                      />
                    </div>
                  )}
                </>
              ) : (
                <div className='flex flex-col w-full gap-9'>
                  <div className='flex flex-col gap-5.5 px-6.5'>
                    <h2 className='text-lg font-semibold text-airt-primary mt-6 '>{`${title}`}</h2>
                    <div className='relative z-20 bg-white dark:bg-form-input'>
                      <ModelSelector parser={parser} setActiveModel={setActiveModel} />
                      <DynamicForm
                        parser={parser}
                        setActiveModel={setActiveModel}
                        refetchUserProperties={refetchUserProperties}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
});
