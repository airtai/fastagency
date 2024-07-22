import React from 'react';
import { Link } from 'react-router-dom';

import { styled } from '../auth/configs/stitches.config';

export const Message = styled('div', {
  padding: '0.5rem 0.75rem',
  borderRadius: '0.375rem',
  marginTop: '1rem',
  background: '$gray400',
});

export const MessageError = styled(Message, {
  background: '#fff',
  color: '#003257',
});

interface TosAndMarketingEmailsProps {
  tocChecked: boolean;
  handleTocChange: any;
  marketingEmailsChecked: boolean;
  handleMarketingEmailsChange: any;
  errorMessage: { title: string; description?: string } | null;
}

const TosAndMarketingEmails: React.FC<TosAndMarketingEmailsProps> = ({
  tocChecked,
  handleTocChange,
  marketingEmailsChecked,
  handleMarketingEmailsChange,
  errorMessage,
}) => (
  <div className='toc-marketing-checkbox-wrapper text-airt-font-base'>
    <div className='mt-4'>
      <label className='checkbox-container text-sm mb-2' htmlFor='toc'>
        I agree to the{' '}
        <Link to='/toc' className='no-underline hover:underline text-airt-secondary' target='_blank'>
          Terms & Conditions
        </Link>{' '}
        and{' '}
        <Link to='/privacy' className='no-underline hover:underline text-airt-secondary' target='_blank'>
          Privacy Policy
        </Link>
        <input type='checkbox' id='toc' checked={tocChecked} onChange={handleTocChange} />
        <span className='checkmark'></span>
      </label>
    </div>
    <div>
      <label className='checkbox-container text-sm mb-2' htmlFor='marketingEmails'>
        I agree to receiving marketing emails
        <input
          type='checkbox'
          id='marketingEmails'
          checked={marketingEmailsChecked}
          onChange={handleMarketingEmailsChange}
        />
        <span className='checkmark'></span>
      </label>
    </div>
    {errorMessage && (
      <div className='text-sm'>
        <MessageError>
          {errorMessage.title}
          {errorMessage.description && ': '}
          {errorMessage.description}
        </MessageError>
      </div>
    )}
  </div>
);

export default TosAndMarketingEmails;
