import React, { useEffect, useState } from 'react';
import _ from 'lodash';
import { FieldApi } from '@tanstack/react-form';
import Select, { StylesConfig } from 'react-select';

import { TextInput } from '../form/TextInput';
import { SECRETS_TO_MASK } from '../../utils/constants';
import { TextArea } from '../form/TextArea';

interface FormFieldProps {
  field: FieldApi<any, any, any, any>;
  property: any;
  fieldKey: string;
  isOptionalRefField: boolean;
}

function FieldInfo({ field }: { field: FieldApi<any, any, any, any> }) {
  return (
    <>
      {field.state.meta.isTouched && field.state.meta.errors.length ? (
        <p role='alert' className='text-red-600'>
          {field.state.meta.errors.join(',')}
        </p>
      ) : null}
      {field.state.meta.isValidating ? 'Validating...' : null}
    </>
  );
}

const getSelectObject = (val: string): {} => {
  return { value: val, label: val };
};

export const FormField: React.FC<FormFieldProps> = ({ field, property, fieldKey, isOptionalRefField }) => {
  const [selectOptions, setSelectOptions] = useState([]);
  const [defaultValue, setDefaultValue] = useState(null);
  const [key, setKey] = useState(0);
  const getInputType = () => {
    if (_.includes(SECRETS_TO_MASK, fieldKey) && typeof property.type === 'string') {
      return 'password';
    }
    return 'text';
  };

  useEffect(() => {
    if (property.enum) {
      const opts = property.enum;

      let optsDefault = opts.length > 0 ? property.default : null;
      if (typeof optsDefault === 'string') {
        optsDefault = getSelectObject(optsDefault);
      }

      setSelectOptions(opts);
      setDefaultValue(optsDefault);
      setKey((prevKey) => prevKey + 1);
    } else {
      setSelectOptions([]);
      setDefaultValue(null);
    }
  }, [property.enum]);

  return (
    <div className='w-full mt-2'>
      <label htmlFor={fieldKey}>{`${property.title} ${isOptionalRefField ? ' (Optional)' : ''}`}</label>
      {property.enum ? (
        <Select
          key={key}
          data-testid='select-container'
          classNamePrefix='react-select'
          inputId={fieldKey}
          options={selectOptions}
          onChange={(e: any) => field.handleChange(e?.value || null)} // field.handleChange(e.value)
          className='pt-1 pb-1'
          defaultValue={defaultValue}
          isSearchable={true}
          isClearable={isOptionalRefField}
          // styles={customStyles}
        />
      ) : fieldKey === 'system_message' ? (
        <TextArea
          id={fieldKey}
          value={field.state.value}
          placeholder={property.description || ''}
          onChange={(e) => field.handleChange(e)}
        />
      ) : (
        <TextInput
          id={fieldKey}
          value={field.state.value}
          onChange={(e) => field.handleChange(e)}
          type={getInputType()}
          placeholder={property.description || ''}
        />
      )}
      <FieldInfo field={field} />
    </div>
  );
};
