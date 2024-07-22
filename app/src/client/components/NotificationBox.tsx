import React, { useRef } from 'react';
import { useEscapeKeyHandler } from '../hooks/useEscapeKeyHandler';

interface NotificationBoxProps {
  type: 'success' | 'error';
  message: string;
  onClick: () => void;
}

const NotificationBox: React.FC<NotificationBoxProps> = ({ type, message, onClick }) => {
  const notificationCancelBtnRef = useRef<HTMLButtonElement>(null);
  useEscapeKeyHandler(notificationCancelBtnRef);

  const isSuccess = type === 'success';

  return (
    <div className='fixed inset-0 flex items-center justify-center z-50 p-16 backdrop-blur-sm bg-airt-font-base/30'>
      <div className='bg-airt-primary rounded-lg shadow-lg p-8 m-4 max-w-sm mx-auto'>
        <h2 className='text-xl font-bold mb-4 text-airt-font-base'>{isSuccess ? 'Success' : 'Error'}</h2>
        <p className='text-airt-font-base'>{message}</p>
        <div className='mt-4 text-right'>
          <button
            onClick={onClick}
            className={`py-2 px-4 rounded text-airt-font-base focus:outline-none hover:bg-opacity-85 ${
              isSuccess ? 'bg-airt-secondary' : 'bg-airt-error'
            }`}
            ref={notificationCancelBtnRef}
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default NotificationBox;
