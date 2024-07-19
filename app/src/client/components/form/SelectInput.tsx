import React, { useEffect, useState } from 'react';

import _ from 'lodash';
import Select from 'react-select';

import { capitalizeFirstLetter } from '../../utils/buildPageUtils';

interface SelectInputProps {
  id: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
  propertyTypes: string[];
  addPropertyClick: (property_type: string) => void;
  isRequired: boolean;
}

export function getSelectOptions(options: string[], propertyTypes: string[] | null, isRequired: boolean) {
  if (options.length === 1 && options[0] === 'None' && isRequired) {
    options = [];
  }
  let selectOptions = options.map((option) => ({ value: option, label: option }));

  if (propertyTypes && propertyTypes.length > 0) {
    selectOptions = selectOptions.concat(
      propertyTypes.map((option) => ({
        value: option,
        label: `Add new '${option === 'llm' ? 'LLM' : capitalizeFirstLetter(option)}'`,
        isNewOption: true, // Flag to identify new property options
      })) as any
    );
  }

  return selectOptions;
}

export const SelectInput: React.FC<SelectInputProps> = ({
  id,
  value,
  options,
  onChange,
  propertyTypes,
  addPropertyClick,
  isRequired,
}) => {
  const [selectedOption, setSelectedOption] = useState(value);
  let selectOptions = getSelectOptions(options, propertyTypes, isRequired);
  useEffect(() => {
    if (options.length === 1 && options[0] === 'None' && isRequired) {
      return;
    }
    const defaultValue = value === '' && selectOptions.length > 0 ? selectOptions[0].value : value;
    setSelectedOption(defaultValue);
  }, [value, options]);

  const handleTypeSelect = (e: any) => {
    const selectedOption = e.value;
    setSelectedOption(selectedOption);
    if (_.includes(propertyTypes, selectedOption)) {
      addPropertyClick(selectedOption);
    }
    onChange(selectedOption);
  };

  const customStyles = {
    control: (baseStyles: any, state: any) => ({
      ...baseStyles,
      borderColor: '#003257',
    }),
    option: (styles: any, { data }: any) => {
      return {
        ...styles,
        fontWeight: data.isNewOption ? 'bold' : 'normal',
        '::before': data.isNewOption
          ? {
              content: '"➕"',
              marginRight: '5px',
            }
          : {},
      };
    },
  };

  return (
    <div className=''>
      <Select
        inputId={id}
        options={selectOptions}
        onChange={handleTypeSelect}
        className='pt-1 pb-1'
        value={selectOptions.filter(function (option) {
          return option.value === selectedOption;
        })}
        isSearchable={false}
        isClearable={true}
        styles={customStyles}
      />
    </div>
  );
};
