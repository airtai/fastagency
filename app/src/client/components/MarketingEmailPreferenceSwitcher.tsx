import React, { useState } from 'react';

import { updateCurrentUser } from 'wasp/client/operations';
import NotificationBox from './NotificationBox';

export function MarketingEmailPreferenceSwitcher({
  hasSubscribedToMarketingEmails,
}: {
  hasSubscribedToMarketingEmails: boolean;
}) {
  const [status, setStatus] = useState(hasSubscribedToMarketingEmails);
  const [hasChanged, setHasChanged] = useState(false);
  const [notificationType, setNotificationType] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setStatus(e.target.value === 'Yes');
    setHasChanged(true);
  };

  const onClick = () => {
    setNotificationType(null);
  };

  const handleClick = async (status: boolean) => {
    try {
      await updateCurrentUser({ hasSubscribedToMarketingEmails: status });
      setNotificationType('success');
    } catch (e) {
      setNotificationType('error');
    }
    setHasChanged(false);
  };

  const notificationMsg =
    notificationType === 'success'
      ? 'Your changes are saved successfully.'
      : 'Something went wrong. Please try again later.';

  return (
    <>
      {notificationType && (
        <NotificationBox type={notificationType as 'success' | 'error'} onClick={onClick} message={notificationMsg} />
      )}
      <div className='mt-1 text-sm text-captn-dark-blue sm:col-span-1 sm:mt-0'>
        <label className='mr-4'>
          <input
            type='radio'
            value='Yes'
            checked={status}
            onChange={handleChange}
            className='form-radio text-captn-light-blue mr-2 focus:ring-1 outline-none'
          />
          Yes
        </label>
        <label>
          <input
            type='radio'
            value='No'
            checked={!status}
            onChange={handleChange}
            className='form-radio text-captn-light-blue mr-2 focus:ring-1 outline-none'
          />
          No
        </label>
      </div>

      <div className='ml-0 md:ml-4 flex-shrink-0 sm:col-span-1 sm:mt-0' style={{ height: '24px' }}>
        <button
          onClick={() => handleClick(status)}
          disabled={!hasChanged}
          className={`mt-4 md:-mt-10 no-underline rounded-md px-3.5 py-2.5 text-sm text-airt-font-base ring-1 ring-inset ring-gray-200  shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:text-airt-font-base bg-airt-primary hover:bg-opacity-85 ${
            !hasChanged ? 'opacity-40 cursor-not-allowed' : ''
          }`}
        >
          Save
        </button>
      </div>
    </>
  );
}
