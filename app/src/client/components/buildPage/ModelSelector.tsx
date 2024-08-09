import Select, { StylesConfig, SingleValue } from 'react-select';
import { PropertySchemaParser, SetActiveModelType } from './PropertySchemaParser';
import { SelectOption } from './PropertySchemaParser';
import { capitalizeFirstLetter } from './buildPageUtilsNew';

export const ModelSelector = ({
  parser,
  setActiveModel,
}: {
  parser: PropertySchemaParser | null;
  setActiveModel: SetActiveModelType;
}) => {
  const selectOptions = parser?.getModelNames();
  const propertyName = parser?.getPropertyName();
  const propertyHeader = propertyName ? capitalizeFirstLetter(propertyName) : propertyName;
  const customStyles: StylesConfig<SelectOption, false> = {
    control: (baseStyles) => ({
      ...baseStyles,
      borderColor: '#003257',
    }),
  };

  const handleChange = (selectedOption: SingleValue<SelectOption>) => {
    if (selectedOption) {
      setActiveModel(selectedOption.value);
    }
  };

  const activeModel = parser?.getActiveModel();
  const header = propertyHeader === 'Llm' ? 'Select LLM' : `Select ${propertyHeader}`;

  return (
    <>
      {selectOptions && (
        <>
          <label className='mb-3 block text-black dark:text-white'>{header}</label>
          <div className='relative z-20 bg-white dark:bg-form-input'>
            <Select
              data-testid='select-model-type'
              classNamePrefix='react-select-model-type'
              options={selectOptions}
              onChange={handleChange}
              className='pt-1 pb-1'
              defaultValue={activeModel ? { value: activeModel, label: activeModel } : selectOptions[0]}
              isSearchable={true}
              isClearable={false}
              styles={customStyles}
            />
          </div>
        </>
      )}
    </>
  );
};
