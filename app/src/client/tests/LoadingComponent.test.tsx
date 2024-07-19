import { test, expect, describe } from 'vitest';
import { render, screen } from '@testing-library/react';
import LoadingComponent from '../components/LoadingComponent';

describe('LoadingComponent', () => {
  test('renders the LoadingComponent correctly', () => {
    render(<LoadingComponent />);

    const loadingButton = screen.getByText('Loading...');
    expect(loadingButton).toBeInTheDocument();
  });
});
