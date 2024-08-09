import { cn } from '../../../shared/utils';

interface SubHeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

export const SubHeader: React.FC<SubHeaderProps> = ({ sidebarOpen, setSidebarOpen }) => {
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
