import React from 'react';
import _ from 'lodash';

import { navLinkItems } from './CustomSidebar';
import { formatApiKey } from '../utils/buildPageUtils';

interface JsonStr {
  name: string;
  api_key?: string;
}

export interface ItemProps {
  created_at: string;
  model_name: string;
  model_uuid: string;
  updated_at: string;
  type_name: string;
  user_uuid: string;
  uuid: string;
  json_str: JsonStr;
}

interface ModelItemProps {
  model: ItemProps;
  onClick: () => void;
}

const ModelItem: React.FC<ModelItemProps> = ({ model, onClick }) => {
  const propertyName = model.json_str.name ? model.json_str.name : model.model_name;
  const svgIcon = _.find(navLinkItems, ['componentName', model.type_name]).svgIcon;
  const svgClassName =
    model.type_name === ('llm' || 'secret')
      ? 'text-airt-primary mt-1 ml-1'
      : model.type_name === 'deployment'
        ? 'text-airt-primary mt-1 ml-2'
        : 'text-airt-primary ml-1';
  return (
    <div
      className='group relative cursor-pointer overflow-hidden bg-airt-primary text-airt-font-base px-6 pt-10 pb-8 transition-all duration-300 hover:-translate-y-1 sm:max-w-sm sm:rounded-lg sm:pl-8 sm:pr-24'
      onClick={onClick}
    >
      <div className='relative z-10 mx-auto max-w-md'>
        <div className='flex items-center mb-3'>
          <span className='absolute z-0 h-9 w-9 rounded-full bg-airt-secondary transition-all duration-300 group-hover:scale-[30]'></span>
          <div className='z-10 w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full dark:bg-indigo-500 bg-airt-secondary text-white flex-shrink-0'>
            <span className={svgClassName}>{svgIcon}</span>
          </div>
          <h2 className='z-10 text-airt-font-base group-hover:text-airt-primary dark:text-airt-font-base text-lg font-medium'>
            {propertyName}
          </h2>
        </div>
        {model.json_str.name && (
          <div className='flex flex-col gap-2 text-airt-font-base group-hover:text-airt-primary pt-4 sm:max-w-sm sm:rounded-lg'>
            <p className='z-10 '>{model.model_name}</p>
          </div>
        )}
        {model.json_str.api_key && (
          <div className='flex flex-col gap-2 text-airt-font-base group-hover:text-airt-primary pt-2 sm:max-w-sm sm:rounded-lg'>
            <p className='z-10'>{formatApiKey(model.json_str.api_key)}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ModelItem;
