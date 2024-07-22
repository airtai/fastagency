import { test, expect, vi, describe } from 'vitest';
import { renderInContext } from 'wasp/client/test';
import { fireEvent } from '@testing-library/react';

import * as operations from 'wasp/client/operations';

import { MarketingEmailPreferenceSwitcher } from '../components/MarketingEmailPreferenceSwitcher';

describe('MarketingEmailPreferenceSwitcher', () => {
  test('renders correctly with initial value (true)', async () => {
    const { getByLabelText } = renderInContext(
      <MarketingEmailPreferenceSwitcher hasSubscribedToMarketingEmails={true} />
    );

    expect(getByLabelText('Yes')).toBeChecked();
    expect(getByLabelText('No')).not.toBeChecked();
  });

  test('renders correctly with initial value (false)', async () => {
    const { getByLabelText } = renderInContext(
      <MarketingEmailPreferenceSwitcher
        hasSubscribedToMarketingEmails={false}
      />
    );

    expect(getByLabelText('Yes')).not.toBeChecked();
    expect(getByLabelText('No')).toBeChecked();
  });

  test('changes value when radio button is clicked', () => {
    const { getByLabelText } = renderInContext(
      <MarketingEmailPreferenceSwitcher hasSubscribedToMarketingEmails={true} />
    );

    fireEvent.click(getByLabelText('No'));

    expect(getByLabelText('Yes')).not.toBeChecked();
    expect(getByLabelText('No')).toBeChecked();
  });

  test('shows save button when value is changed', () => {
    const { getByLabelText, getByText } = renderInContext(
      <MarketingEmailPreferenceSwitcher hasSubscribedToMarketingEmails={true} />
    );

    fireEvent.click(getByLabelText('No'));

    expect(getByText('Save')).toBeInTheDocument();
  });

  test('calls updateCurrentUser with correct value when save button is clicked', async () => {
    const updateCurrentUserSpy = vi.spyOn(operations, 'updateCurrentUser');

    const { getByLabelText, getByText } = renderInContext(
      <MarketingEmailPreferenceSwitcher hasSubscribedToMarketingEmails={true} />
    );

    fireEvent.click(getByLabelText('No'));
    fireEvent.click(getByText('Save'));

    expect(updateCurrentUserSpy).toHaveBeenCalledWith({
      hasSubscribedToMarketingEmails: false,
    });
  });
});
