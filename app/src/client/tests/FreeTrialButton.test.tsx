import { test, expect, vi, describe } from 'vitest';
// import { renderInContext } from 'wasp/client/test';
// import { fireEvent, screen, waitFor } from '@testing-library/react';
// import * as operations from 'wasp/client/operations';
// import FreeTrialButton from '../components/FreeTrialButton';

// vi.mock('wasp/client/operations', async (importOriginal) => {
//   const mod = await importOriginal<typeof import('wasp/client/operations')>();
//   return {
//     ...mod,
//     stripePayment: vi.fn().mockResolvedValue({ sessionUrl: 'https://stripe.com/session' }),
//   };
// });

// vi.mock('wasp/client/auth', async (importOriginal) => {
//   const mod = await importOriginal<typeof import('wasp/client/auth')>();
//   return {
//     ...mod,
//     useAuth: vi.fn().mockReturnValue({
//       data: { id: 1, isSignUpComplete: true, lastActiveTimestamp: new Date() },
//       isError: false,
//       isLoading: false,
//     }),
//   };
// });

describe('FreeTrialButton', () => {
  test('renders the FreeTrialButton component', () => {
    // renderInContext(<FreeTrialButton />);
    // const button = screen.getByText('Free Trial');
    // expect(button).toBeInTheDocument();
  });
  // test('handles button click correctly', async () => {
  //   renderInContext(<FreeTrialButton />);
  //   fireEvent.click(screen.getByText('Free Trial'));
  //   await waitFor(() => {
  //     expect(operations.stripePayment).toHaveBeenCalled();
  //   });
  // });
});
