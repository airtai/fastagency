import { test, expect, describe, vi } from 'vitest';
import { fireEvent, screen } from '@testing-library/react';
import { renderInContext } from 'wasp/client/test';
import TosAndMarketingEmailsModal from '../components/TosAndMarketingEmailsModal';

vi.mock('wasp/client/operations', async (importOriginal) => {
  const mod = await importOriginal<typeof import('wasp/client/operations')>();
  return {
    ...mod,
    updateCurrentUser: vi.fn().mockReturnValue('Ok'),
  };
});

const mockHistoryPush = vi.fn();
vi.mock('react-router-dom', async (importOriginal) => {
  const mod = await importOriginal<typeof import('react-router-dom')>();
  return {
    ...mod,
    useHistory: () => ({
      push: mockHistoryPush,
    }),
  };
});

describe('TosAndMarketingEmailsModal', () => {
  const mockSetSuccessMessage = vi.fn();
  const mockSetIsLoading = vi.fn();

  //   beforeEach(() => {
  //     render(
  //       <AuthContext.Provider value={{ isLoading: false, setSuccessMessage: mockSetSuccessMessage, setIsLoading: mockSetIsLoading }}>
  //         <Router>
  //           <TosAndMarketingEmailsModal />
  //         </Router>
  //       </AuthContext.Provider>
  //     );
  //   });

  test('renders TosAndMarketingEmailsModal component correctly', () => {
    renderInContext(<TosAndMarketingEmailsModal />);
    const heading = screen.getByText('Almost there...');
    expect(heading).toBeInTheDocument();

    const notificationMessage = screen.getByText(
      /Before accessing the application, please confirm your agreement to the Terms & Conditions and Privacy Policy./
    );
    expect(notificationMessage).toBeInTheDocument();

    const saveButton = screen.getByRole('button', { name: /Save/i });
    expect(saveButton).toBeInTheDocument();
  });

  test('handles Save button click correctly when Terms & Conditions is not checked', () => {
    renderInContext(<TosAndMarketingEmailsModal />);
    const saveButton = screen.getByRole('button', { name: /Save/i });
    fireEvent.click(saveButton);

    const errorMessage = screen.getByText(
      "To proceed, please ensure you've accepted our Terms & Conditions and Privacy Policy."
    );
    expect(errorMessage).toBeInTheDocument();
  });

  test('handles Save button click correctly when Terms & Conditions is checked', () => {
    renderInContext(<TosAndMarketingEmailsModal />);
    const tocCheckbox = screen.getByRole('checkbox', { name: /Terms & Conditions and Privacy Policy/i });
    fireEvent.click(tocCheckbox);

    const saveButton = screen.getByRole('button', { name: /Save/i });
    fireEvent.click(saveButton);

    expect(mockHistoryPush).toHaveBeenCalledWith('/build');
  });
});
