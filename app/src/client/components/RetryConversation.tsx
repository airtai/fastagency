import { type Chat } from 'wasp/entities';
import React, { useState } from 'react';

import Markdown from 'markdown-to-jsx';

export default function RetryConversation({
  currentChatDetails,
  retryOnClick,
}: {
  currentChatDetails: Chat;
  retryOnClick: any;
}) {
  const [isShowSuggestions, setIsShowSuggestions] = useState(true);

  const suggestions = ["Let's try again"];

  async function handleSuggestionClick(suggestion: string, retryOnClick: any) {
    setIsShowSuggestions(false);
    retryOnClick(null, false, true);
  }

  return (
    <div>
      <div className={`mt-2 pb-4 flex items-center group bg-captn-dark-blue`}>
        <div
          style={{ maxWidth: '800px', margin: 'auto' }}
          className={`fade-in  relative block w-full rounded-lg bg-captn-light-green`}
        >
          <div className='chat-conversations text-base flex flex-wrap'>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className='rounded-md px-3.5 pt-2 pb-2.5 text-sm hover:bg-opacity-85 shadow-sm bg-airt-secondary text-airt-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                onClick={() => handleSuggestionClick(suggestion, retryOnClick)}
              >
                <Markdown>{suggestion}</Markdown>
              </button>
            ))}
          </div>
          {!currentChatDetails.isExceptionOccured && (
            <p className='my-2 ml-6 pt-2 text-captn-light-cream'>
              You can choose from the listed options above or type your own answers in the input field below.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
