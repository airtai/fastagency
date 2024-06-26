import { useEffect, useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';

export default function CheckoutPage() {
  const [paymentStatus, setPaymentStatus] = useState('loading');

  const history = useHistory();
  const location = useLocation();

  useEffect(() => {
    function delayedRedirect() {
      return setTimeout(() => {
        history.push('/build');
      }, 2000);
    }

    const queryParams = new URLSearchParams(location.search);
    const isSuccess = queryParams.get('success');
    const isCanceled = queryParams.get('canceled');

    if (isCanceled) {
      setPaymentStatus('canceled');
    } else if (isSuccess) {
      setPaymentStatus('paid');
    } else {
      history.push('/build');
    }
    delayedRedirect();
    return () => {
      clearTimeout(delayedRedirect());
    };
  }, [location]);

  return (
    <div className='flex min-h-full flex-col justify-center mt-10 sm:px-6 lg:px-8'>
      <div className='sm:mx-auto sm:w-full sm:max-w-md p-4'>
        <div className='py-8 px-4 shadow-xl ring-1 ring-airt-font-base dark:ring-gray-100/10 rounded-lg sm:px-10'>
          <h1>
            {paymentStatus === 'paid'
              ? '🥳 Payment Successful!'
              : paymentStatus === 'canceled'
                ? '😢 Payment Canceled'
                : paymentStatus === 'error' && '🙄 Payment Error'}
          </h1>
          {paymentStatus !== 'loading' && (
            <span className='text-center'>
              You are being redirected to your build page... <br />
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
