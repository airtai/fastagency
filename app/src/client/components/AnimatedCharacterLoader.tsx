import React, { useState, useEffect } from 'react';

import logo from '../static/logo.svg';

interface AnimatedCharacterLoaderProps {
  loadingMessage?: string; // Optional prop for customizing the loading message
  bgColor?: string;
  showLogo?: boolean;
}

const AnimatedCharacterLoader: React.FC<AnimatedCharacterLoaderProps> = ({
  loadingMessage = 'Loading...', // Default loading message
  bgColor = 'airt-primary',
  showLogo = true,
}) => {
  const [frameIndex, setFrameIndex] = useState(0); // State to track the current frame of the animation
  const loadingAnimation = ['—', '\\', '|', '/']; // Characters used for the loading animation
  const textColor = bgColor === 'airt-primary' ? 'airt-font-base' : 'airt-primary'; // Text color based on background color

  useEffect(() => {
    // Set up an interval to cycle through the animation characters
    const interval = setInterval(() => {
      setFrameIndex((prevIndex) => (prevIndex + 1) % loadingAnimation.length); // Cycle through indices in a loop
    }, 250); // Animation frame update interval in milliseconds

    // Cleanup function to clear the interval on component unmount
    return () => clearInterval(interval);
  }, [loadingAnimation.length]); // Dependence on the length is constant, but included for completeness

  return (
    <div
      style={{ minHeight: '85px' }}
      className={`flex items-center px-5 group bg-${bgColor} flex-col agent-conversation-container`}
    >
      <div
        style={{ maxWidth: '800px', margin: 'auto' }}
        className={`relative ml-3 block w-full p-4 pl-10 text-sm text-airt-font-base  border-airt-primary rounded-lg bg-${bgColor} `}
      >
        {showLogo && (
          <span
            className='absolute inline-block'
            style={{
              left: '-15px',
              top: '8px',
              height: ' 45px',
              width: '45px',
            }}
          >
            <span
              className='bg-airt-font-base inline-block'
              style={{ borderRadius: '50%', width: '93%', height: '93%', paddingTop: '3px' }}
            >
              <img
                alt='FastAgency logo'
                src={logo}
                className='w-full h-full'
                style={{ width: '78%', height: '78%', marginLeft: '4px' }}
              />
            </span>
          </span>
        )}
        <div className={`chat-conversations text-base text-${textColor} flex flex-col gap-2 pl-4`}>
          {/* <Markdown> */}
          {loadingMessage} {loadingAnimation[frameIndex]}
          {/* </Markdown> */}
        </div>
      </div>
    </div>
  );
};

export default AnimatedCharacterLoader;
