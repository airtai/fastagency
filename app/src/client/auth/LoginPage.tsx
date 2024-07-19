import { createTheme } from '@stitches/react';
import { useAuth } from 'wasp/client/auth';
import { useHistory } from 'react-router-dom';
import { useEffect } from 'react';
import { AuthWrapper } from './authWrapper';
import Auth from './Auth';
import imgUrl from '../static/logo.svg';

export enum State {
  Login = 'login',
  Signup = 'signup',
}

export default function Login() {
  const history = useHistory();

  const { data: user } = useAuth();

  useEffect(() => {
    if (user) {
      history.push('/');
    }
  }, [user, history]);

  return (
    <AuthWrapper>
      <LoginForm logo={imgUrl} state={State.Login} />
    </AuthWrapper>
  );
}

export type CustomizationOptions = {
  logo?: string;
  socialLayout?: 'horizontal' | 'vertical';
  appearance?: Parameters<typeof createTheme>[0];
  state: State;
};

export function LoginForm({ appearance, logo, socialLayout, state }: CustomizationOptions) {
  return <Auth appearance={appearance} logo={logo} socialLayout={socialLayout} state={state} />;
}
