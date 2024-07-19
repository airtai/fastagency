import { test, expect, describe } from 'vitest';
import { screen } from '@testing-library/react';
import { renderInContext } from 'wasp/client/test';

import ServerNotRechableComponent from '../components/ServerNotRechableComponent';

describe('ServerNotRechableComponent', () => {
  test('renders ServerNotRechableComponent correctly', async () => {
    renderInContext(<ServerNotRechableComponent />);

    const loadingMessage = screen.queryByText(/Oops! Something went wrong./);
    expect(loadingMessage).toBeInTheDocument();
  });
});
