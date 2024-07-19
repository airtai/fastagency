import { test, expect, describe } from 'vitest';
import { screen } from '@testing-library/react';
import { renderInContext } from 'wasp/client/test';

import Button from '../components/Button';

describe('Button', () => {
  test('renders Button component with default props', async () => {
    renderInContext(<Button onClick={() => {}} />);

    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
  });

  test('renders Button component with label', async () => {
    renderInContext(<Button onClick={() => {}} label='Test Button' />);

    const button = screen.getByText('Test Button');
    expect(button).toBeInTheDocument();
  });
});
