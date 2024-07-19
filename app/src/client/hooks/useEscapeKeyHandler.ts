import { useEffect, RefObject } from 'react';

export const useEscapeKeyHandler = (cancelButtonRef: RefObject<HTMLButtonElement>) => {
  useEffect(() => {
    const keyHandler = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      cancelButtonRef.current?.click();
    };
    document.addEventListener('keydown', keyHandler);
    return () => document.removeEventListener('keydown', keyHandler);
  }, [cancelButtonRef]);
};
