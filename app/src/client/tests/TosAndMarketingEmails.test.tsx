import { test, expect, describe, vi } from 'vitest';
import { screen, fireEvent } from '@testing-library/react';
import { renderInContext } from 'wasp/client/test';

import TosAndMarketingEmails from '../components/TosAndMarketingEmails';

describe('TosAndMarketingEmails', () => {
  test('renders TosAndMarketingEmails component correctly', async () => {
    const handleTocChange = vi.fn();
    const handleMarketingEmailsChange = vi.fn();

    renderInContext(
      <TosAndMarketingEmails
        tocChecked={false}
        handleTocChange={handleTocChange}
        marketingEmailsChecked={false}
        handleMarketingEmailsChange={handleMarketingEmailsChange}
        errorMessage={null}
      />
    );

    const tocCheckbox = screen.getByRole('checkbox', { name: /Terms & Conditions and Privacy Policy/i });
    expect(tocCheckbox).toBeInTheDocument();

    const marketingEmailsCheckbox = screen.getByRole('checkbox', { name: /I agree to receiving marketing emails/i });
    expect(marketingEmailsCheckbox).toBeInTheDocument();
  });

  test('handles checkbox changes correctly', async () => {
    const handleTocChange = vi.fn();
    const handleMarketingEmailsChange = vi.fn();

    renderInContext(
      <TosAndMarketingEmails
        tocChecked={false}
        handleTocChange={handleTocChange}
        marketingEmailsChecked={false}
        handleMarketingEmailsChange={handleMarketingEmailsChange}
        errorMessage={null}
      />
    );

    const tocCheckbox = screen.getByRole('checkbox', { name: /Terms & Conditions and Privacy Policy/i });
    fireEvent.click(tocCheckbox);
    expect(handleTocChange).toHaveBeenCalled();

    const marketingEmailsCheckbox = screen.getByRole('checkbox', { name: /I agree to receiving marketing emails/i });
    fireEvent.click(marketingEmailsCheckbox);
    expect(handleMarketingEmailsChange).toHaveBeenCalled();
  });

  test('displays error message when passed', async () => {
    const errorMessage = { title: 'Test Error', message: 'This is a test error.' };

    renderInContext(
      <TosAndMarketingEmails
        tocChecked={false}
        handleTocChange={() => {}}
        marketingEmailsChecked={false}
        handleMarketingEmailsChange={() => {}}
        errorMessage={errorMessage}
      />
    );

    const errorTitle = screen.getByText('Test Error');
    expect(errorTitle).toBeInTheDocument();
  });
});
