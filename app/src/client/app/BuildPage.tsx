import React, { useEffect, useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';

import { type User } from 'wasp/entities';

import CustomAuthRequiredLayout from './layout/CustomAuthRequiredLayout';
import CustomSidebar from '../components/CustomSidebar';
import { cn } from '../../shared/utils';

import LoadingComponent from '../components/LoadingComponent';
import { useBuildPage } from '../hooks/useBuildPage';
import { filerOutComponentData } from '../utils/buildPageUtils';
import UserPropertyHandler from '../components/buildPage/UserPropertyHandler';

interface BuildPageProps {
  user: User;
}

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

export const Header: React.FC<HeaderProps> = ({ sidebarOpen, setSidebarOpen }) => {
  return (
    <header className='sticky top-0 z-9 flex w-full bg-airt-hero-gradient-start dark:bg-boxdark dark:drop-shadow-none lg:hidden'>
      <div className='flex flex-grow items-center justify-between sm:justify-end sm:gap-5 px-8 py-5 shadow '>
        <div className='flex items-center gap-2 sm:gap-4 lg:hidden'>
          {/* <!-- Hamburger Toggle BTN --> */}

          <button
            aria-controls='sidebar'
            onClick={(e) => {
              e.stopPropagation();
              setSidebarOpen(!sidebarOpen);
            }}
            className='z-99999 block rounded-sm border border-airt-primary border-airt-hero-gradient-start bg-airt-hero-gradient-start p-1.5 shadow-sm dark:border-strokedark dark:bg-boxdark lg:hidden'
          >
            <span className='relative block h-5.5 w-5.5 cursor-pointer'>
              <span className='du-block absolute right-0 h-full w-full'>
                <span
                  className={cn(
                    'relative top-0 left-0 my-1 block h-0.5 w-0 rounded-sm bg-airt-primary delay-[0] duration-200 ease-in-out dark:bg-white',
                    {
                      '!w-full delay-300': !sidebarOpen,
                    }
                  )}
                ></span>
                <span
                  className={cn(
                    'relative top-0 left-0 my-1 block h-0.5 w-0 rounded-sm bg-airt-primary delay-150 duration-200 ease-in-out dark:bg-white',
                    {
                      'delay-400 !w-full': !sidebarOpen,
                    }
                  )}
                ></span>
                <span
                  className={cn(
                    'relative top-0 left-0 my-1 block h-0.5 w-0 rounded-sm bg-airt-primary delay-200 duration-200 ease-in-out dark:bg-white',
                    {
                      '!w-full delay-500': !sidebarOpen,
                    }
                  )}
                ></span>
              </span>
              <span className='absolute right-0 h-full w-full rotate-45'>
                <span
                  className={cn(
                    'absolute left-2.5 top-0 block h-full w-0.5 rounded-sm bg-airt-primary delay-300 duration-200 ease-in-out dark:bg-white',
                    {
                      '!h-0 !delay-[0]': !sidebarOpen,
                    }
                  )}
                ></span>
                <span
                  className={cn(
                    'delay-400 absolute left-0 top-2.5 block h-0.5 w-full rounded-sm bg-airt-primary duration-200 ease-in-out dark:bg-white',
                    {
                      '!h-0 !delay-200': !sidebarOpen,
                    }
                  )}
                ></span>
              </span>
            </span>
          </button>

          {/* <!-- Hamburger Toggle BTN --> */}
        </div>
      </div>
    </header>
  );
};

const BuildPage = ({ user }: BuildPageProps) => {
  const { data, loading, error } = useBuildPage();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sideNavSelectedItem, setSideNavSelectedItem] = useState('secret');
  const [togglePropertyList, setTogglePropertyList] = useState(false);
  const { pathname } = location;
  const activeBuildPageTab = pathname.split('/').pop();

  const wrapperClass = document.body.classList.contains('server-error')
    ? 'h-[calc(100vh-173px)]'
    : 'h-[calc(100vh-80px)]';

  const history = useHistory();
  useEffect(() => {
    if (!user) {
      history.push('/login');
    } else {
      if (!user.hasPaid && user.isSignUpComplete) {
        history.push('/pricing');
      }
    }
  }, [user, history]);

  useEffect(() => {
    if (!activeBuildPageTab) return;
    if (activeBuildPageTab === 'build') {
      history.push(`/build/secret`);
    } else {
      setSideNavSelectedItem(activeBuildPageTab);
    }
  }, [activeBuildPageTab]);

  if (loading) {
    return <LoadingComponent />;
  }

  const handleSideNavItemClick = (selectedComponentName: string) => {
    setSideNavSelectedItem(selectedComponentName);
    setTogglePropertyList(!togglePropertyList);
    history.push(`/build/${selectedComponentName}`);
  };

  return (
    <div className='dark:bg-boxdark-2 dark:text-bodydark bg-captn-light-blue'>
      {/* <!-- ===== Page Wrapper Start ===== --> */}
      <div className={`flex ${wrapperClass} overflow-hidden`}>
        {/* <!-- ===== Sidebar Start ===== --> */}
        <CustomSidebar
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          onSideNavItemClick={handleSideNavItemClick}
          sideNavSelectedItem={sideNavSelectedItem}
        />
        {/* <!-- ===== Sidebar End ===== --> */}

        {/* <!-- ===== Content Area Start ===== --> */}
        <div className='relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden'>
          {/* <!-- ===== Header Start ===== --> */}
          <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
          {/* <!-- ===== Header End ===== --> */}

          {/* <!-- ===== Main Content Start ===== --> */}
          <main className='lg:mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10'>
            <div className='w-full lg:min-w-[700px] 2xl:min-w-[1200px]'>
              {error ? (
                <p
                  className='absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 text-xl md:text-xl text-airt-font-base'
                  style={{ lineHeight: 'normal' }}
                >
                  Oops! Something went wrong. Our server is currently unavailable. Please try again later.
                </p>
              ) : data ? (
                <UserPropertyHandler
                  data={filerOutComponentData(data, sideNavSelectedItem)}
                  togglePropertyList={togglePropertyList}
                />
              ) : (
                <p
                  className='absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 text-xl md:text-6xl text-airt-font-base'
                  style={{ lineHeight: 'normal' }}
                >
                  Build Page - No valid component found for this section.
                </p>
              )}
            </div>
          </main>
          {/* <!-- ===== Main Content End ===== --> */}
          <></>
        </div>

        {/* <!-- ===== Content Area End ===== --> */}
      </div>
      {/* <!-- ===== Page Wrapper End ===== --> */}
    </div>
  );
};

const BuildPageWithCustomAuth = CustomAuthRequiredLayout(BuildPage);
export default BuildPageWithCustomAuth;
