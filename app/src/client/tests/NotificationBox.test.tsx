import { test, expect, describe } from 'vitest';
import { screen } from '@testing-library/react';
import { renderInContext } from 'wasp/client/test';

import NotificationBox from '../components/NotificationBox';

describe('NotificationBox', () => {
  test('renders NotificationBox component with success type', async () => {
    renderInContext(<NotificationBox type='success' message='Success message' onClick={() => {}} />);

    const heading = screen.getByText('Success');
    expect(heading).toBeInTheDocument();

    const message = screen.getByText('Success message');
    expect(message).toBeInTheDocument();

    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
  });

  test('renders NotificationBox component with error type', async () => {
    renderInContext(<NotificationBox type='error' message='Error message' onClick={() => {}} />);

    const heading = screen.getByText('Error');
    expect(heading).toBeInTheDocument();

    const message = screen.getByText('Error message');
    expect(message).toBeInTheDocument();

    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
  });
});
