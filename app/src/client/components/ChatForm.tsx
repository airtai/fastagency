import React, { useRef, useState, useEffect, useCallback } from 'react';

import TextareaAutosize from 'react-textarea-autosize';
import { useSocketListener } from 'wasp/client/webSocket';
import { type Chat } from 'wasp/entities';

interface ChatFormProps {
  handleFormSubmit: (userQuery: string, isUserRespondedWithNextAction?: boolean, retrySameChat?: boolean) => void;
  currentChatDetails: Chat;
  triggerChatFormSubmitMsg?: string | null;
}

export default function ChatForm({ handleFormSubmit, currentChatDetails, triggerChatFormSubmitMsg }: ChatFormProps) {
  const [formInputValue, setFormInputValue] = useState('');
  const [disableFormSubmit, setDisableFormSubmit] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toggleTextAreaFocus, setToggleTextAreaFocus] = useState(false);
  const isProcessing = useRef(false);
  const textAreaRef = React.useRef<HTMLTextAreaElement>();
  const isEmptyMessage = formInputValue.trim().length === 0;

  const formRef = useCallback(
    async (node: any) => {
      if (node !== null && triggerChatFormSubmitMsg) {
        await handleFormSubmit(triggerChatFormSubmitMsg, true);
      }
    },
    [triggerChatFormSubmitMsg]
  );

  useEffect(() => {
    if (toggleTextAreaFocus && (!disableFormSubmit || !isSubmitting || !isProcessing.current)) {
      if (textAreaRef.current) {
        textAreaRef.current.focus();
      }
    }
  }, [disableFormSubmit, isSubmitting, isProcessing.current, toggleTextAreaFocus]);

  const setFocusOnTextArea = () => {
    setToggleTextAreaFocus(true);
  };
  useSocketListener('streamFromTeamFinished', setFocusOnTextArea);

  useEffect(() => {
    if (currentChatDetails) {
      setDisableFormSubmit(currentChatDetails.team_status === 'inprogress');
    } else {
      setDisableFormSubmit(false);
    }
  }, [currentChatDetails]);

  const submitForm = async (inputValue: string) => {
    if (isSubmitting || disableFormSubmit || isProcessing.current || isEmptyMessage) return;

    setIsSubmitting(true);
    setToggleTextAreaFocus(false);
    isProcessing.current = true;

    try {
      await handleFormSubmit(inputValue);
      setFormInputValue('');
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
      isProcessing.current = false;
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await submitForm(formInputValue);
  };

  const handleButtonClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    await submitForm(formInputValue);
  };

  const handleKeyDown = async (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      await submitForm(formInputValue);
    }
  };

  return (
    <div className='mt-2 mb-2'>
      <form data-testid='chat-form' onSubmit={handleSubmit} className='' ref={formRef}>
        <label
          htmlFor='search'
          className='mb-2 text-sm font-medium text-captn-dark-blue sr-only dark:text-airt-font-base'
        >
          Search
        </label>
        <div className='relative bottom-0 left-0 right-0 flex items-center justify-between m-1'>
          <TextareaAutosize
            minRows={1}
            maxRows={4}
            style={{
              lineHeight: 2,
              resize: 'none',
            }}
            id='userQuery'
            name='search'
            className='block rounded-lg w-full h-12 text-sm text-airt-font-base bg-airt-primary focus:outline-none focus:ring-0 focus:border-captn-light-blue'
            placeholder='Enter your message...'
            required
            disabled={disableFormSubmit || isSubmitting}
            ref={textAreaRef}
            value={formInputValue}
            onChange={(e) => setFormInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            type='button'
            disabled={disableFormSubmit || isSubmitting || isEmptyMessage}
            onClick={handleButtonClick}
            className={`text-airt-primary bg-airt-secondary hover:opacity-90 absolute right-2 font-medium rounded-lg text-sm px-1.5 py-1.5 transition-all duration-300 ${
              disableFormSubmit || isSubmitting || isEmptyMessage
                ? 'cursor-not-allowed bg-white opacity-70 hover:opacity-70'
                : 'cursor-pointer'
            }`}
          >
            <span className=''>
              <svg width='24' height='24' viewBox='0 0 24 24' fill='none' className='text-airt-primary'>
                <path
                  d='M7 11L12 6L17 11M12 18V7'
                  stroke='currentColor'
                  strokeWidth='2'
                  strokeLinecap='round'
                  strokeLinejoin='round'
                ></path>
              </svg>
            </span>
          </button>
        </div>
      </form>
    </div>
  );
}
