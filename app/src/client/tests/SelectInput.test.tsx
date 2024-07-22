import { expect, describe, it } from 'vitest';
import { getSelectOptions } from '../components/form/SelectInput';

describe('getSelectOptions', () => {
  it('Generate options without refs', () => {
    const options = ['claude-3-5-sonnet-20240620', 'claude-3-opus-20240229'];
    const propertyTypes = null;
    const isRequired = false;
    const selectOptions = getSelectOptions(options, propertyTypes, isRequired);

    expect(selectOptions).toEqual([
      { value: 'claude-3-5-sonnet-20240620', label: 'claude-3-5-sonnet-20240620' },
      { value: 'claude-3-opus-20240229', label: 'claude-3-opus-20240229' },
    ]);
  });
  it('Generate options with refs and is not required', () => {
    const options = ['None'];
    const propertyTypes = ['secret'];
    const isRequired = false;
    const selectOptions = getSelectOptions(options, propertyTypes, isRequired);

    expect(selectOptions).toEqual([
      { value: 'None', label: 'None' },
      { value: 'secret', label: "Add new 'Secret'", isNewOption: true },
    ]);
  });

  it('Generate options with refs and is required', () => {
    const options = ['None'];
    const propertyTypes = ['secret'];
    const isRequired = true;
    const selectOptions = getSelectOptions(options, propertyTypes, isRequired);

    expect(selectOptions).toEqual([{ value: 'secret', label: "Add new 'Secret'", isNewOption: true }]);
  });
});
