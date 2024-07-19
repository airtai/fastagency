import { useMemo, useEffect, ReactNode, useState } from 'react';
import { useLocation } from 'react-router-dom';

import './Main.css';

import { useAuth } from 'wasp/client/auth';
import { updateCurrentUser, userModelSetup } from 'wasp/client/operations';

import AppNavBar from './components/AppNavBar';
import Footer from './components/Footer';
import ServerNotRechableComponent from './components/ServerNotRechableComponent';
import LoadingComponent from './components/LoadingComponent';
import TosAndMarketingEmailsModal from './components/TosAndMarketingEmailsModal';

const addServerErrorClass = () => {
  if (!document.body.classList.contains('server-error')) {
    document.body.classList.add('server-error');
  }
};

const removeServerErrorClass = () => {
  if (document.body.classList.contains('server-error')) {
    document.body.classList.remove('server-error');
  }
};

/**
 * use this component to wrap all child components
 * this is useful for templates, themes, and context
 */
export default function App({ children }: { children: ReactNode }) {
  const location = useLocation();
  const [showTosAndMarketingEmailsModal, setShowTosAndMarketingEmailsModal] = useState(false);
  const [isUserModelSetupCalled, setIsUserModelSetupCalled] = useState(false);
  const { data: user, isError, isLoading } = useAuth();

  const shouldDisplayAppNavBar = useMemo(() => {
    return location.pathname !== '/'; //&& location.pathname !== '/login' && location.pathname !== '/signup';
  }, [location]);

  const isAdminDashboard = useMemo(() => {
    return location.pathname.startsWith('/admin');
  }, [location]);

  const isCheckoutPage = useMemo(() => {
    return location.pathname.startsWith('/checkout');
  }, [location]);

  const isAccountPage = useMemo(() => {
    return location.pathname.startsWith('/account');
  }, [location]);

  const isPlayGroundPage = useMemo(() => {
    return location.pathname.startsWith('/playground');
  }, [location]);

  const isBuildPage = useMemo(() => {
    return location.pathname.startsWith('/build');
  }, [location]);

  useEffect(() => {
    const handleUserSetup = async () => {
      if (user) {
        if (!user.isSignUpComplete) {
          if (user.hasAcceptedTos) {
            updateCurrentUser({
              isSignUpComplete: true,
            });
            setShowTosAndMarketingEmailsModal(false);
          } else {
            const hasAcceptedTos = localStorage.getItem('hasAcceptedTos') === 'true';
            const hasSubscribedToMarketingEmails = localStorage.getItem('hasSubscribedToMarketingEmails') === 'true';
            if (!hasAcceptedTos) {
              setShowTosAndMarketingEmailsModal(true);
            } else {
              updateCurrentUser({
                isSignUpComplete: true,
                hasAcceptedTos: hasAcceptedTos,
                hasSubscribedToMarketingEmails: hasSubscribedToMarketingEmails,
              });
              setShowTosAndMarketingEmailsModal(false);
            }
          }
        } else {
          if (!user.isSetUpComplete && !isUserModelSetupCalled) {
            setIsUserModelSetupCalled(true);
            try {
              await userModelSetup();
              console.log('userModelSetup done!');
            } catch (error) {
              console.log('Error in userModelSetup!');
            }
          }
          setShowTosAndMarketingEmailsModal(false);
          const lastSeenAt = new Date(user.lastActiveTimestamp);
          const today = new Date();
          if (today.getTime() - lastSeenAt.getTime() > 5 * 60 * 1000) {
            updateCurrentUser({ lastActiveTimestamp: today });
          }
        }
      }
    };
    handleUserSetup();
  }, [user, isUserModelSetupCalled]);

  useEffect(() => {
    if (location.hash) {
      const id = location.hash.replace('#', '');
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView();
      }
    }
  }, [location]);

  return (
    <>
      <div className='bg-gradient-to-b from-airt-hero-gradient-start via-airt-hero-gradient-middle to-airt-secondary min-h-screen dark:text-white dark:bg-boxdark-2'>
        {isError && (addServerErrorClass(), (<ServerNotRechableComponent />))}
        {isAdminDashboard || isPlayGroundPage || isBuildPage ? (
          <>
            {showTosAndMarketingEmailsModal ? (
              <>
                <TosAndMarketingEmailsModal />
              </>
            ) : (
              <>
                {shouldDisplayAppNavBar && <AppNavBar />}
                {children}
              </>
            )}
          </>
        ) : (
          <div className='relative flex flex-col min-h-screen justify-between'>
            {shouldDisplayAppNavBar && <AppNavBar />}
            <div className='mx-auto max-w-7xl sm:px-6 lg:px-8 w-full'>
              {isError ? (
                children
              ) : isLoading ? (
                <LoadingComponent />
              ) : (
                (removeServerErrorClass(),
                showTosAndMarketingEmailsModal && (isCheckoutPage || isAccountPage) ? (
                  <>
                    <TosAndMarketingEmailsModal />
                  </>
                ) : (
                  children
                ))
              )}
            </div>
            <FooterWrapper />
          </div>
        )}
      </div>
    </>
  );
}

const FooterWrapper: React.FC = () => {
  return (
    <div>
      <Footer />
      <div className='flex items-center h-20 bg-airt-footer-copyrights'>
        <p className='text-center w-full text-sm text-airt-font-base opacity-50'>
          © 2024{' '}
          <a
            href='https://airt.ai'
            className='text-sm leading-6 text-airt-font-base underline dark:text-white hover:opacity-80'
            target='_blank'
          >
            airt
          </a>
          . All rights reserved.
        </p>
      </div>
    </div>
  );
};
