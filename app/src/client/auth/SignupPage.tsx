import { AuthWrapper } from './authWrapper';
import imgUrl from '../static/logo.svg';
import { State, LoginForm } from './LoginPage';

export function Signup() {
  return (
    <AuthWrapper>
      <LoginForm logo={imgUrl} state={State.Signup} />
    </AuthWrapper>
  );
}
