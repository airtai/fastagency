import { Link } from 'wasp/client/router';
import { type User } from 'wasp/entities';
import { logout } from 'wasp/client/auth';
// import { STRIPE_CUSTOMER_PORTAL_LINK } from '../../shared/constants';
import CustomAuthRequiredLayout from '../app/layout/CustomAuthRequiredLayout';
import Button from '../components/Button';
// import FreeTrialButton from '../components/FreeTrialButton';
import { MarketingEmailPreferenceSwitcher } from '../components/MarketingEmailPreferenceSwitcher';

const AccountPage = ({ user }: { user: User }) => {
  return (
    <div className='mt-10 px-6'>
      <div className='overflow-hidden border border-airt-primary shadow-lg sm:rounded-lg lg:m-8 dark:border-gray-100/10'>
        <div className='px-4 py-5 sm:px-6 lg:px-8'>
          <h3 className='text-base font-semibold leading-6 text-airt-font-base dark:text-white'>Account Information</h3>
        </div>
        <div className='border-t border-airt-primary dark:border-gray-100/10 px-4 py-5 sm:p-0'>
          <dl className=' sm:dark:divide-gray-100/10'>
            {!!user.email && (
              <div className='py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:py-5 sm:px-6'>
                <dt className='text-sm font-medium text-airt-font-base dark:text-white'>Email address</dt>
                <dd className='mt-1 text-sm text-airt-font-base dark:text-airt-font-base sm:col-span-2 sm:mt-0'>
                  {user.email}
                </dd>
              </div>
            )}
            {!!user.username && (
              <div className='py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:py-5 sm:px-6'>
                <dt className='text-sm font-medium text-airt-font-base dark:text-white'>Username</dt>
                <dd className='mt-1 text-sm text-airt-font-base dark:text-airt-font-base sm:col-span-2 sm:mt-0'>
                  {user.username}
                </dd>
              </div>
            )}
            {/* <div className='py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:py-5 sm:px-6'>
              <dt className='text-sm font-medium text-airt-font-base dark:text-white '>Subscription status</dt>
              {user.hasPaid ? (
                <>
                  {user.subscriptionStatus !== 'past_due' ? (
                    <dd className='mt-1 text-sm font-medium text-airt-font-base dark:text-white sm:col-span-1 sm:mt-0'>

                      Active
                    </dd>
                  ) : (
                    <dd className='mt-1 text-sm text-airt-font-base dark:text-airt-font-base sm:col-span-1 sm:mt-0'>
                      Your Account is Past Due! Please Update your Payment Information
                    </dd>
                  )}
                  <CustomerPortalButton />
                </>
              ) : (
                <>
                  <dd className='mt-1 text-sm font-medium text-airt-font-base dark:text-white sm:col-span-1 sm:mt-0'>
                    N/A
                  </dd>
                  <div className='flex items-center justify-left -mt-2'>
                    <FreeTrialButton />
                  </div>
                </>
              )}
            </div> */}
            <div className='py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:py-5 sm:px-6'>
              <dt className='text-sm font-medium text-airt-font-base'>I agree to receiving marketing emails</dt>
              <>
                <MarketingEmailPreferenceSwitcher
                  hasSubscribedToMarketingEmails={user.hasSubscribedToMarketingEmails}
                />
              </>
            </div>
          </dl>
        </div>
      </div>
      <div className='inline-flex w-full justify-end'>
        <Button onClick={logout} label='logout' />
      </div>
    </div>
  );
};

function BuyMoreButton() {
  return (
    <div className='ml-4 flex-shrink-0 sm:col-span-1 sm:mt-0'>
      <Link to='/pricing' className='font-medium text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-500'>
        Buy More/Upgrade
      </Link>
    </div>
  );
}

// function CustomerPortalButton() {
//   const handleClick = () => {
//     window.open(STRIPE_CUSTOMER_PORTAL_LINK, '_blank');
//   };

//   return (
//     <div className='ml-4 flex-shrink-0 sm:col-span-1 sm:mt-0'>
//       <button
//         onClick={handleClick}
//         className='font-medium text-sm text-airt-font-base dark:text-white hover:underline dark:text-indigo-400 dark:hover:text-indigo-300'
//       >
//         Manage Subscription
//       </button>
//     </div>
//   );
// }

const AccountPageWithCustomAuth = CustomAuthRequiredLayout(AccountPage);
export default AccountPageWithCustomAuth;
