import React, { useRef, useEffect } from 'react';

interface AutoScrollContainerProps {
  children: React.ReactNode;
  shouldAutoScroll: boolean;
}

const AutoScrollContainer: React.FC<AutoScrollContainerProps> = ({ children, shouldAutoScroll }) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const userHasScrolled = useRef(false);

  useEffect(() => {
    const scrollElement = scrollRef.current;

    // MutationObserver to observe changes in the container
    const observer = new MutationObserver(() => {
      if (scrollElement) {
        scrollElement.scrollTo({
          top: scrollElement.scrollHeight,
          behavior: 'smooth',
        });
      }
    });

    if (scrollElement) {
      observer.observe(scrollElement, { childList: true, subtree: true });
    }

    // Disconnect observer on cleanup
    return () => {
      observer.disconnect();
    };
  }, []); // Observer itself does not depend on `shouldAutoScroll`

  useEffect(() => {
    // Reset user scrolling flag if auto-scroll is re-enabled
    if (shouldAutoScroll) {
      userHasScrolled.current = false;
    }
  }, [shouldAutoScroll]);

  // Handle user scroll to disable auto-scrolling
  const handleUserScroll = (event: React.UIEvent<HTMLDivElement>) => {
    // Check if the user has scrolled up from the bottom
    if (event.currentTarget.scrollTop < event.currentTarget.scrollHeight - event.currentTarget.clientHeight) {
      userHasScrolled.current = true;
    }
  };

  return (
    <div className='flex-auto overflow-y-auto' ref={scrollRef} onScroll={handleUserScroll}>
      {children}
    </div>
  );
};

export default AutoScrollContainer;
