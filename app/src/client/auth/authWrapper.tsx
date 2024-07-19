import { ReactNode } from 'react';

export function AuthWrapper({ children }: { children: ReactNode }) {
  return (
    <div className='flex min-h-full flex-col justify-center pt-10 sm:px-6 lg:px-8'>
      <div className='sm:mx-auto sm:w-full sm:max-w-md p-4'>
        <div className='bg-airt-primary p-8 shadow-xl rounded-lg sm:px-7 sm:py-7 dark:bg-white text-airt-font-base'>
          <div className='-mt-8'>{children}</div>
        </div>
      </div>
    </div>
  );
}
