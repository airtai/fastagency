import React, { useEffect, useRef, useState } from 'react';

interface TerminalDisplayProps {
  messages: string;
  maxHeight: number;
  isOpenOnLoad?: boolean;
  theme?: string | null;
  containerTitle?: string;
}

const TerminalDisplay: React.FC<TerminalDisplayProps> = ({
  messages,
  maxHeight,
  isOpenOnLoad,
  theme,
  containerTitle,
}) => {
  const [isMinimized, setIsMinimized] = useState(isOpenOnLoad ? false : true); // Track if terminal is minimized
  const containerRef = useRef<HTMLDivElement | null>(null); // Reference to the scroll container
  const [isAutoScroll, setIsAutoScroll] = useState(true); // Track if auto-scroll is enabled
  const isModelDeploymentTheme = theme === 'modelDeployment'; // Check if the theme is modelDeployment
  const title = containerTitle ? containerTitle : 'Agent conversations'; // Title of the terminal

  // Convert ANSI codes to HTML with inline styles
  const convertAnsiToHtml = (text: string): string => {
    text = text
      .replace(/\[0m/g, '</span>') // Reset / Normal
      .replace(/\[1m/g, '<span style="font-weight: bold;">') // Bold or increased intensity
      .replace(/\[4m/g, '<span style="text-decoration: underline;">') // Underline
      .replace(/\[30m/g, '<span style="color: #003851;">') // Black
      .replace(/\[31m/g, '<span style="color: #c22828;">') // Red
      .replace(/\[32m/g, '<span style="color: #71ad3d;">') // Green
      .replace(/\[33m/g, '<span style="color: #6800a8;">') // Yellow
      .replace(/\[34m/g, '<span style="color: #6e7cbb;">') // Blue
      .replace(/\[35m/g, '<span style="color: #6800a8;">') // Magenta
      .replace(/\[36m/g, '<span style="color: #6faabc;">') // Cyan
      .replace(/\[37m/g, '<span style="color: #eae4d9;">') // White
      .replace(/\n/g, '<br/>'); // Convert newlines to <br/>
    return text;
  };

  const handleUserScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const el = e.currentTarget;
    // If the user scrolls up, disable auto-scroll
    const isAtBottom = el.scrollHeight - el.scrollTop === el.clientHeight;
    setIsAutoScroll(isAtBottom);
  };

  useEffect(() => {
    if (isAutoScroll && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages, isAutoScroll]);

  return (
    <div className={`accordion-wrapper terminal ${isMinimized ? 'minimized' : ''}`}>
      <div
        className={`relative terminal-header ${
          isMinimized ? 'rounded-lg' : 'rounded-t-lg'
        } text-airt-font-base p-1 text-right bg-airt-secondary hover:cursor-pointer`}
        onClick={() => setIsMinimized(!isMinimized)}
      >
        <p className='accordion-title text-sm text-left text-airt-primary'>{title}</p>
        <button className={`absolute right-4 top-4 ${isMinimized ? '' : 'open'} text-sm text-airt-primary `}>
          {isMinimized ? (
            <svg
              xmlns='http://www.w3.org/2000/svg'
              fill='currentColor'
              className='bi bi-chevron-up'
              viewBox='0 0 16 16'
              height='16'
            >
              <path
                fillRule='evenodd'
                d='M1.646 11.854a.5.5 0 0 0 .708 0L8 6.207l5.646 5.647a.5.5 0 0 0 .708-.708l-6-6a.5.5 0 0 0-.708 0l-6 6a.5.5 0 0 0 0 .708z'
              />
            </svg>
          ) : (
            <svg
              xmlns='http://www.w3.org/2000/svg'
              fill='currentColor'
              className='bi bi-chevron-down'
              viewBox='0 0 16 16'
              height='16'
            >
              <path
                fillRule='evenodd'
                d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.793l5.646-5.647a.5.5 0 0 1 .708 .708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'
              />
            </svg>
          )}
        </button>
      </div>
      <div className={`accordion-item rounded-b-lg ${isMinimized ? '' : 'collapsed'}`}>
        <div
          ref={containerRef}
          onScroll={handleUserScroll}
          className={`${
            isModelDeploymentTheme ? 'text-airt-font-base bg-airt-primary' : 'bg-airt-font-base text-airt-primary'
          } accordion-content scroll-container p-4 font-mono text-xs overflow-y-auto overflow-x-hidden ${
            isMinimized ? 'hidden' : ''
          }`}
          style={{
            ...(isModelDeploymentTheme
              ? { wordWrap: 'break-word', maxHeight: `${maxHeight}px` }
              : { maxHeight: `${maxHeight}px`, wordWrap: 'break-word' }),
          }}
          dangerouslySetInnerHTML={{ __html: convertAnsiToHtml(messages) }} // nosemgrep
        />
      </div>
    </div>
  );
};

export default TerminalDisplay;
