import { type CustomizationOptions } from 'wasp/client/auth';
import { useState, createContext } from 'react';
import { createTheme } from '@stitches/react';
import { styled } from './configs/stitches.config';
import { LoginSignupForm } from './LoginSignupForm';

export enum State {
  Login = 'login',
  Signup = 'signup',
}

export type ErrorMessage = {
  title: string;
  description?: string;
};

export const Message = styled('div', {
  padding: '0.5rem 0.75rem',
  borderRadius: '0.375rem',
  marginTop: '1rem',
  background: '$gray400',
});

export const MessageSuccess = styled(Message, {
  background: '$successBackground',
  color: '$successText',
});

const logoStyle = {
  height: '3rem',
};

const Container = styled('div', {
  display: 'flex',
  flexDirection: 'column',
});

// const HeaderText = styled('h2', {
//   fontSize: '1.875rem',
//   fontWeight: '700',
//   marginTop: '1.5rem',
// });

export const AuthContext = createContext({
  isLoading: false,
  setIsLoading: (isLoading: boolean) => {},
  setErrorMessage: (errorMessage: ErrorMessage | null) => {},
  setSuccessMessage: (successMessage: string | null) => {},
});

const titles: Record<State, string> = {
  login: 'Sign in to your account',
  signup: 'Create an account',
};

function Auth({
  state,
  appearance,
  logo,
  socialLayout = 'horizontal',
  additionalSignupFields,
}: {
  state: State;
} & CustomizationOptions & {
    additionalSignupFields?: any;
  }) {
  const [errorMessage, setErrorMessage] = useState<ErrorMessage | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // TODO(matija): this is called on every render, is it a problem?
  // If we do it in useEffect(), then there is a glitch between the default color and the
  // user provided one.
  const customTheme = createTheme(appearance ?? {});

  // const title = titles[state];

  const socialButtonsDirection = socialLayout === 'vertical' ? 'vertical' : 'horizontal';

  return (
    <div className={customTheme}>
      <div>
        {logo && <img className='mt-10 mx-auto' style={logoStyle} src={logo} alt='Capt’n.ai' />}
        {/* <HeaderText>{title}</HeaderText> */}
        <p className='mt-6 text-2xl text-center'>{state === 'signup' ? titles.signup : titles.login}</p>
      </div>

      {/* {errorMessage && (
        <MessageError>
          {errorMessage.title}
          {errorMessage.description && ': '}
          {errorMessage.description}
        </MessageError>
      )} */}
      {successMessage && <MessageSuccess>{successMessage}</MessageSuccess>}
      <AuthContext.Provider value={{ isLoading, setIsLoading, setErrorMessage, setSuccessMessage }}>
        {(state === 'login' || state === 'signup') && (
          <LoginSignupForm
            state={state}
            socialButtonsDirection={socialButtonsDirection}
            additionalSignupFields={additionalSignupFields}
            errorMessage={errorMessage}
          />
        )}
      </AuthContext.Provider>
    </div>
  );
}

export default Auth;
