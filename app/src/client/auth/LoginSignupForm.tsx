import { useContext, useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

import { styled } from './configs/stitches.config';
import { AuthContext } from './Auth';
import config from './configs/config';
import TosAndMarketingEmails from '../components/TosAndMarketingEmails';
import { State } from './Auth';
import { Link } from 'wasp/client/router';

const SocialAuth = styled('div', {
  marginTop: '1.5rem',
  marginBottom: '1.5rem',
});

const SocialAuthButtons = styled('div', {
  marginTop: '0.5rem',
  display: 'flex',

  variants: {
    direction: {
      horizontal: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(48px, 1fr))',
      },
      vertical: {
        flexDirection: 'column',
        margin: '8px 0',
      },
    },
    gap: {
      small: {
        gap: '4px',
      },
      medium: {
        gap: '8px',
      },
      large: {
        gap: '16px',
      },
    },
  },
});

const googleSignInUrl = `${config.apiUrl}/auth/google/login`;

export const checkBoxErrMsg = {
  title: "To proceed, please ensure you've accepted our Terms & Conditions and Privacy Policy.",
  description: '',
};

export type LoginSignupFormFields = {
  [key: string]: string;
};

export const LoginSignupForm = ({
  state,
  socialButtonsDirection = 'horizontal',
  additionalSignupFields,
  errorMessage,
}: {
  state: 'login' | 'signup';
  socialButtonsDirection?: 'horizontal' | 'vertical';
  additionalSignupFields?: any;
  errorMessage?: any;
}) => {
  const { isLoading, setErrorMessage, setSuccessMessage, setIsLoading } = useContext(AuthContext);
  const [tocChecked, setTocChecked] = useState(false);
  const [marketingEmailsChecked, setMarketingEmailsChecked] = useState(false);
  const [loginFlow, setLoginFlow] = useState(state);
  const hookForm = useForm<LoginSignupFormFields>();
  const {
    register,
    formState: { errors },
    handleSubmit: hookFormHandleSubmit,
  } = hookForm;

  useEffect(() => {
    if (tocChecked) {
      setErrorMessage(null);
    }
  }, [tocChecked]);

  const handleTocChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTocChecked(event.target.checked);
  };

  const handleMarketingEmailsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMarketingEmailsChecked(event.target.checked);
  };

  const updateLocalStorage = () => {
    localStorage.removeItem('hasAcceptedTos');
    localStorage.removeItem('hasSubscribedToMarketingEmails');
    localStorage.setItem('hasAcceptedTos', JSON.stringify(tocChecked));
    localStorage.setItem('hasSubscribedToMarketingEmails', JSON.stringify(marketingEmailsChecked));
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>, googleSignInUrl: string) => {
    event.preventDefault();
    if (loginFlow === State.Login) {
      updateLocalStorage();
      window.location.href = googleSignInUrl;
    } else {
      if (tocChecked) {
        updateLocalStorage();
        window.location.href = googleSignInUrl;
      } else {
        setErrorMessage(checkBoxErrMsg);
      }
    }
  };

  const googleBtnText = loginFlow === State.Login ? 'Sign in with Google' : 'Sign up with Google';

  return (
    <>
      {loginFlow === State.Signup && (
        <TosAndMarketingEmails
          tocChecked={tocChecked}
          handleTocChange={handleTocChange}
          marketingEmailsChecked={marketingEmailsChecked}
          handleMarketingEmailsChange={handleMarketingEmailsChange}
          errorMessage={errorMessage}
        />
      )}
      <SocialAuth>
        <SocialAuthButtons gap='large' direction={socialButtonsDirection}>
          <button
            className='gsi-material-button'
            onClick={(event: React.MouseEvent<HTMLButtonElement>) => handleClick(event, googleSignInUrl)}
          >
            <div className='gsi-material-button-state'></div>
            <div className='gsi-material-button-content-wrapper'>
              <div className='gsi-material-button-icon'>
                <svg
                  version='1.1'
                  xmlns='http://www.w3.org/2000/svg'
                  viewBox='0 0 48 48'
                  xmlnsXlink='http://www.w3.org/1999/xlink'
                  style={{ display: 'block' }}
                >
                  <path
                    fill='#EA4335'
                    d='M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z'
                  ></path>
                  <path
                    fill='#4285F4'
                    d='M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z'
                  ></path>
                  <path
                    fill='#FBBC05'
                    d='M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z'
                  ></path>
                  <path
                    fill='#34A853'
                    d='M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z'
                  ></path>
                  <path fill='none' d='M0 0h48v48H0z'></path>
                </svg>
              </div>
              <span className='gsi-material-button-contents'>{googleBtnText}</span>
              <span style={{ display: 'none' }}>{googleBtnText}</span>
            </div>
          </button>
        </SocialAuthButtons>
      </SocialAuth>
      <div className='flex items-center justify-center'>
        <span className='text-sm block'>
          {loginFlow === State.Login ? "Don't have an account? " : 'Already have an account? '}
          <Link
            to={loginFlow === State.Login ? '/signup' : '/login'}
            className='no-underline hover:underline cursor-pointer text-airt-secondary'
          >
            {loginFlow === State.Login ? 'Sign up' : 'Sign in'}
          </Link>
        </span>
      </div>
    </>
  );
};
