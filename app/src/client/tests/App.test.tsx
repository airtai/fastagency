import { renderInContext } from 'wasp/client/test';
import { screen } from '@testing-library/react';
import { describe, it, vi, expect, beforeEach, afterEach } from 'vitest';
import { MemoryRouter } from 'react-router-dom';

interface LocalStorageMock extends Storage {
  store: Record<string, string>;
}

const localStorageMock: LocalStorageMock = (function () {
  let store: Record<string, string> = {};

  return {
    get length(): number {
      return Object.keys(store).length;
    },
    getItem(key: string): string | null {
      return store[key] || null;
    },
    setItem(key: string, value: string): void {
      store[key] = value;
    },
    removeItem(key: string): void {
      delete store[key];
    },
    clear(): void {
      store = {};
    },
    key(index: number): string | null {
      const keys = Object.keys(store);
      return keys[index] || null;
    },
    store,
  };
})();

global.localStorage = localStorageMock;

// Shared mock setup function
function setupMocks(mockUser: any, pathName = '/') {
  // Always mock useAuth with provided user data
  vi.doMock('wasp/client/auth', () => ({ useAuth: () => mockUser }));

  // Correctly mock useLocation to consistently return a pathname
  vi.doMock('react-router-dom', () => ({
    ...vi.importActual('react-router-dom'), // Maintain other hooks and routing components
    useLocation: () => ({
      pathname: pathName, // Ensure this is correctly set according to the test scenario
    }),
    useHistory: () => ({
      // Mock useHistory with minimal implementation if not used
      push: vi.fn(),
      replace: vi.fn(),
      goBack: vi.fn(),
    }),
    Link: ({ children, to }) => <a href={to}>{children}</a>,
  }));

  // Optionally mock updateCurrentUser if the user's sign-up is not complete
  if (!mockUser.data.isSignUpComplete) {
    const mockUpdateCurrentUser = vi.fn();
    vi.doMock('wasp/client/operations', () => ({
      updateCurrentUser: mockUpdateCurrentUser,
    }));
    return mockUpdateCurrentUser; // Return the mock function for assertions in tests
  }
}

beforeEach(() => {
  vi.resetModules();
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('App Component', () => {
  it('dynamically imports and test isSignUpComplete', async () => {
    const mockUser = {
      data: {
        id: 1,
        lastActiveTimestamp: new Date(),
        isSignUpComplete: true,
      },
      isError: false,
      isLoading: false,
    };
    setupMocks(mockUser);
    const { default: App } = await import('../App');
    renderInContext(
      <MemoryRouter>
        <App children={<div>Test</div>} />
      </MemoryRouter>
    );

    await screen.findByText('Test');
  });

  it('dynamically imports and test isSignUpComplete', async () => {
    const mockUser = {
      data: {
        id: 1,
        lastActiveTimestamp: new Date(),
        isSignUpComplete: false,
        hasAcceptedTos: true,
      },
      isError: false,
      isLoading: false,
    };
    const mockUpdateCurrentUser = setupMocks(mockUser);
    const { default: App } = await import('../App');
    renderInContext(
      <MemoryRouter>
        <App children={<div>Test</div>} />
      </MemoryRouter>
    );

    await screen.findByText('Test');
    expect(mockUpdateCurrentUser).toHaveBeenCalledWith({ isSignUpComplete: true });
  });

  it('dynamically imports and test isSignUpComplete', async () => {
    const mockUser = {
      data: {
        id: 1,
        lastActiveTimestamp: new Date(),
        isSignUpComplete: false,
        hasAcceptedTos: false,
      },
      isError: false,
      isLoading: false,
    };
    setupMocks(mockUser, '/playground');
    const { default: App } = await import('../App');
    renderInContext(
      <MemoryRouter>
        <App children={<div>Test on Playground</div>} />
      </MemoryRouter>
    );
    await screen.findByText('Almost there...');
  });

  it('dynamically imports and test isSignUpComplete', async () => {
    // Set a specific item for this test
    localStorage.setItem('hasAcceptedTos', 'true');

    const mockUser = {
      data: {
        id: 1,
        lastActiveTimestamp: new Date(),
        isSignUpComplete: false,
        hasAcceptedTos: false,
      },
      isError: false,
      isLoading: false,
    };
    const mockUpdateCurrentUser = setupMocks(mockUser);
    const { default: App } = await import('../App');
    renderInContext(
      <MemoryRouter>
        <App children={<div>Test</div>} />
      </MemoryRouter>
    );

    await screen.findByText('Test');
    expect(mockUpdateCurrentUser).toHaveBeenCalledWith({
      isSignUpComplete: true,
      hasAcceptedTos: true,
      hasSubscribedToMarketingEmails: false,
    });

    // Cleanup localStorage mock to avoid affecting other tests
    delete global.localStorage;
  });

  it('dynamically imports and test isSignUpComplete - server error', async () => {
    const mockUser = {
      data: {
        id: 1,
        lastActiveTimestamp: new Date(),
        isSignUpComplete: true,
      },
      isError: true,
      isLoading: false,
    };
    setupMocks(mockUser, '/playground');
    const { default: App } = await import('../App');
    renderInContext(
      <MemoryRouter>
        <App children={<div>Test</div>} />
      </MemoryRouter>
    );
    await screen.debug();
    await screen.findByTestId('server-error-component');
  });
});
