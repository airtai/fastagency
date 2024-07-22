import { Link } from 'wasp/client/router';
import { useAuth } from 'wasp/client/auth';
import { useState } from 'react';
import { Dialog } from '@headlessui/react';
import { AiFillCloseCircle } from 'react-icons/ai';
import { HiBars3 } from 'react-icons/hi2';
import { BiLogIn } from 'react-icons/bi';
import logo from '../static/logo.svg';
import openSaasBanner from '../static/open-saas-banner.png';
import { features, navigation, faqs, footerNavigation, testimonials } from './contentSections';
import DropdownUser from '../components/DropdownUser';
import { DOCS_URL } from '../../shared/constants';
import { UserMenuItems } from '../components/UserMenuItems';
import UserActionButton from '../components/UserActionButton';
import DarkModeSwitcher from '../admin/components/DarkModeSwitcher';
import SocialMediaIcons from '../components/SocialMediaIcons';

export default function LandingPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const { data: user, isLoading: isUserLoading } = useAuth();

  const NavLogo = () => <img className='h-8' src={logo} style={{ width: '1.8rem' }} alt='FastAgency' />;

  return (
    <div className='dark:text-white dark:bg-boxdark-2'>
      {/* Header */}
      <header className='bg-airt-primary absolute inset-x-0 top-0 z-50 dark:bg-boxdark-2'>
        <nav className='flex items-center justify-between p-6 lg:px-8' aria-label='Global'>
          <div className='flex items-center lg:flex-1'>
            <a
              href='/'
              className='flex items-center -m-1.5 p-1.5 text-airt-font-base duration-300 ease-in-out hover:text-airt-secondary'
            >
              <NavLogo />
              <span className='ml-2 text-4xl font-rubik text-airt-font-base leading-6 dark:text-white'>FastAgency</span>
              <span className='ml-2 text-sm font-semibold leading-6 '>
                <sup className='text-base text-airt-font-base'>αlpha</sup>
              </span>
            </a>
          </div>
          <div className='flex lg:hidden'>
            <button
              type='button'
              className='-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-airt-font-base dark:text-white'
              onClick={() => setMobileMenuOpen(true)}
            >
              <span className='sr-only'>Open main menu</span>
              <HiBars3 className='h-6 w-6' aria-hidden='true' />
            </button>
          </div>
          <div className='hidden lg:flex lg:gap-x-12'>
            {navigation.map((item, index) => {
              const isFirstItem = index === 0;
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className={`text-sm font-semibold leading-6 duration-300 ease-in-out hover:text-airt-secondary dark:text-white ${
                    isFirstItem ? 'text-airt-secondary' : 'text-airt-font-base'
                  }`}
                >
                  {item.name}
                </a>
              );
            })}
          </div>
          <div className='hidden lg:flex lg:flex-1 lg:justify-end lg:align-end'>
            {/* <!-- Dark Mode Toggler --> */}
            <div className='flex items-center gap-3 2xsm:gap-7'>
              <ul className='flex justify-center items-center gap-2 2xsm:gap-4'>
                <SocialMediaIcons />
              </ul>
              <UserActionButton user={user} renderGoToChat={false} theme='light' />
              {isUserLoading ? null : !user ? (
                <Link to='/login'>
                  <div className='text-sm flex justify-end items-center duration-300 ease-in-out text-airt-font-base hover:text-airt-secondary dark:text-white'>
                    Log in <BiLogIn size='1.1rem' className='ml-1' />
                  </div>
                </Link>
              ) : (
                <DropdownUser user={user} />
              )}
            </div>
          </div>
        </nav>
        <Dialog as='div' className='lg:hidden' open={mobileMenuOpen} onClose={setMobileMenuOpen}>
          <div className='fixed inset-0 z-50' />
          <Dialog.Panel className='fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-airt-font-base dark:bg-boxdark dark:text-white'>
            <div className='flex items-center justify-between'>
              <a href='/' className='-m-1.5 p-1.5'>
                <span className='sr-only'>Your SaaS</span>
                <NavLogo />
              </a>
              <button
                type='button'
                className='-m-2.5 rounded-md p-2.5 text-airt-font-base dark:text-gray-50'
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className='sr-only'>Close menu</span>
                <AiFillCloseCircle className='h-6 w-6' aria-hidden='true' />
              </button>
            </div>
            <div className='mt-6 flow-root'>
              <div className='-my-6 divide-y divide-airt-font-base'>
                <div className='space-y-2 py-6'>
                  {navigation.map((item, index) => (
                    <a
                      key={item.name}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`${
                        index === 0 ? 'text-airt-secondary' : ''
                      } -mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-airt-primary hover:bg-gray-50 dark:text-white dark:hover:bg-boxdark-2`}
                    >
                      {item.name}
                    </a>
                  ))}
                </div>
                <div className='py-6'>
                  {isUserLoading ? null : !user ? (
                    <Link to='/login'>
                      <div className='text-sm flex justify-start items-center duration-300 ease-in-out text-airt-font-base hover:text-airt-secondary dark:text-white'>
                        Log in <BiLogIn size='1.1rem' className='ml-1' />
                      </div>
                    </Link>
                  ) : (
                    <UserMenuItems user={user} />
                  )}
                </div>
                <div className='py-6'>
                  <SocialMediaIcons />
                </div>
              </div>
            </div>
          </Dialog.Panel>
        </Dialog>
      </header>

      <main className='isolate dark:bg-boxdark-2'>
        {/* Hero section */}
        <div className='relative pt-14 w-full '>
          <div className='py-24 sm:py-32'>
            <div className='mx-auto max-w-8xl px-6 lg:px-8'>
              <div className='lg:mb-18 mx-auto max-w-5xl text-center'>
                <h1 className='text-4xl font-rubik text-airt-font-base sm:text-6xl dark:text-white'>
                  FastAgency: A framework for building <span className='italic'>multi-agent </span> AI services.
                </h1>
                <p className='mt-6 mx-auto max-w-2xl text-lg leading-8 text-airt-font-base dark:text-white'>
                  Quickly build scalable SaaS solutions using our powerful, multi-agent AI framework that streamlines
                  complex processes.
                </p>
                <div className='mt-10 flex items-center justify-center gap-x-6'>
                  {/* <a
                    href={DOCS_URL}
                    className='rounded-md px-3.5 py-2.5 text-sm font-semibold text-airt-font-base ring-1 ring-inset ring-gray-200 hover:ring-2 hover:ring-airt-primary shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:text-white'
                  >
                    Get Started <span aria-hidden='true'>→</span>
                  </a> */}
                  <UserActionButton user={user} renderGoToChat={true} />
                </div>
              </div>
              <div className='mt-14 flow-root sm:mt-14 '>
                <div className='-m-2 rounded-xl  lg:-m-4 lg:rounded-2xl lg:p-4'>
                  <div className='video-responsive'>
                    <iframe
                      className='aspect-video w-full rounded-lg shadow-lg shadow-yellow-800/70'
                      src='https://www.youtube.com/embed/9y4cDOkWIBw'
                      allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                      allowFullScreen
                    ></iframe>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Feature section */}
        <div id='features' className='mx-auto mt-5 max-w-7xl px-6 lg:px-8'>
          <div className='mx-auto max-w-2xl text-center'>
            <p className='mt-2 text-4xl font-bold tracking-tight text-airt-font-base sm:text-5xl dark:text-airt-font-base'>
              <span className='text-airt-font-base'>Features</span>
            </p>
            {/* <p className='mt-6 text-lg leading-8 text-airt-font-base dark:text-airt-font-base'>
              Don't work harder.
              <br /> Work smarter.
            </p> */}
          </div>
          <div className='mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl'>
            <dl className='grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16'>
              {features.map((feature) => (
                <div key={feature.name} className={`relative pl-16`}>
                  <dt className='text-base font-semibold leading-7 text-airt-font-base dark:text-airt-font-base'>
                    <div className='absolute left-0 top-0 flex h-10 w-10 items-center justify-center border border-airt-font-base bg-airt-font-base-100/50 dark:bg-boxdark rounded-lg'>
                      <div className='text-2xl'>{feature.icon}</div>
                    </div>
                    {feature.name}
                  </dt>
                  <dd className='mt-2 text-base leading-7 text-airt-font-base dark:text-airt-font-base'>
                    {feature.description}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>

        {/* Testimonial section */}
        {/* <div className='mx-auto mt-32 max-w-7xl sm:mt-56 sm:px-6 lg:px-8'>
          <div className='relative sm:left-5 -m-2 rounded-xl bg-airt-primary lg:ring-1 lg:ring-airt-primary lg:-m-4 '>
            <div className='relative sm:top-5 sm:right-5 bg-airt-font-base dark:bg-boxdark px-8 py-20 shadow-xl sm:rounded-xl sm:px-10 sm:py-16 md:px-12 lg:px-20'>
              <h2 className='text-left text-xl font-semibold tracking-wide leading-7 text-airt-primary dark:text-white'>
                What Our Users Say
              </h2>
              <div className='relative flex flex-wrap gap-6 w-full mt-6 z-10 justify-between lg:mx-0'>
                {testimonials.map((testimonial) => (
                  <figure className='w-full lg:w-1/4 box-content flex flex-col justify-between p-8 rounded-xl bg-airt-primary '>
                    <blockquote className='text-lg text-white sm:text-md sm:leading-8'>
                      <p>{testimonial.quote}</p>
                    </blockquote>
                    <figcaption className='mt-6 text-base text-white'>
                      <a href={testimonial.socialUrl} className='flex items-center gap-x-2'>
                        <img src={testimonial.avatarSrc} className='h-12 w-12 rounded-full' />
                        <div>
                          <div className='font-semibold hover:underline'>{testimonial.name}</div>
                          <div className='mt-1'>{testimonial.role}</div>
                        </div>
                      </a>
                    </figcaption>
                  </figure>
                ))}
              </div>
            </div>
          </div>
        </div> */}
      </main>
    </div>
  );
}
