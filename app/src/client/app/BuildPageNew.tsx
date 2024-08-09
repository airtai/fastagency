import React, { useEffect, useState, memo } from 'react';
import { useHistory } from 'react-router-dom';
import { type User } from 'wasp/entities';

import _ from 'lodash';

import { useBuildPageNew } from '../hooks/useBuildPageNew';

import CustomAuthRequiredLayout from './layout/CustomAuthRequiredLayout';
import CustomSidebar from '../components/CustomSidebar';
import LoadingComponent from '../components/LoadingComponent';

import { SubHeader } from '../components/buildPage/SubHeader';
import { UserProperty } from '../components/buildPage/UserProperty';

interface BuildPageProps {
  user: User;
}

const BuildPage = ({ user }: BuildPageProps) => {
  const history = useHistory();
  const { data: propertiesSchema, loading, error } = useBuildPageNew();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeProperty, setActiveProperty] = useState<string | null>(null);
  const [sideNavItemClickCount, setSideNavItemClickCount] = useState(0);
  const wrapperClass = document.body.classList.contains('server-error')
    ? 'h-[calc(100vh-173px)]'
    : 'h-[calc(100vh-75px)]';

  const handleSideNavItemClick = (selectedComponentName: string) => {
    setActiveProperty(selectedComponentName);
    setSideNavItemClickCount(sideNavItemClickCount + 1);
  };

  const setActivePropertyInSessionStorage = (propertyName: string) => {
    sessionStorage.setItem('activeProperty', propertyName);
  };

  useEffect(() => {
    if (propertiesSchema) {
      const propertyName = sessionStorage.getItem('activeProperty') || propertiesSchema.list_of_schemas[0].name;
      setActiveProperty(propertyName);
    }
  }, [propertiesSchema]);

  useEffect(() => {
    if (activeProperty) {
      history.push(`/build-new/${activeProperty}`);
      setActivePropertyInSessionStorage(activeProperty);
    }
  }, [activeProperty]);

  const canRenderProperty = propertiesSchema && activeProperty;

  return (
    <div className='dark:bg-boxdark-2 dark:text-bodydark bg-captn-light-blue'>
      {loading && <LoadingComponent />}
      {error && (
        <p
          className='absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 text-xl md:text-xl text-airt-font-base'
          style={{ lineHeight: 'normal' }}
        >
          Oops! Something went wrong. Our server is currently unavailable. Please try again later.
        </p>
      )}
      {/* <!-- ===== Page Wrapper Start ===== --> */}
      {canRenderProperty && (
        <div className={`flex ${wrapperClass} overflow-hidden`}>
          {/* <!-- ===== Sidebar Start ===== --> */}
          <CustomSidebar
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
            onSideNavItemClick={handleSideNavItemClick}
            activeProperty={activeProperty}
          />
          {/* <!-- ===== Sidebar End ===== --> */}
          {/* <!-- ===== Content Area Start ===== --> */}
          <div className='relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden'>
            {/* <!-- ===== Mobile Header For Sidenav Start ===== --> */}
            <SubHeader sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
            {/* <!-- ===== Mobile Header For Sidenav End ===== --> */}

            {/* <!-- ===== Main Content Start ===== --> */}
            <main className='lg:mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10'>
              <div className='w-full lg:min-w-[700px] 2xl:min-w-[1200px]'>
                <UserProperty
                  activeProperty={activeProperty}
                  propertiesSchema={propertiesSchema}
                  sideNavItemClickCount={sideNavItemClickCount}
                />
              </div>
            </main>
          </div>
        </div>
      )}
    </div>
  );
};

const BuildPageNewWithCustomAuth = CustomAuthRequiredLayout(BuildPage);
export default BuildPageNewWithCustomAuth;
