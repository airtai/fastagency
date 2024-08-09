/* This file should be deleted */

import { useEffect } from 'react';

const useDetectRefresh = (onRefresh: () => void) => {
  useEffect(() => {
    if (sessionStorage.getItem('isLoaded')) {
      // This is a refresh
      onRefresh();
    } else {
      // This is the initial load
      sessionStorage.setItem('isLoaded', 'true');
    }
  }, []);
};

export default useDetectRefresh;
