import { test, expect, describe } from 'vitest';
import { screen } from '@testing-library/react';
import { renderInContext } from 'wasp/client/test';

import AnimatedCharacterLoader from '../components/AnimatedCharacterLoader';

describe('AnimatedCharacterLoader', () => {
  test('renders AnimatedCharacterLoader component with default props', async () => {
    renderInContext(<AnimatedCharacterLoader />);

    const logo = screen.getByAltText('FastAgency logo');
    expect(logo).toBeInTheDocument();
  });
});
