import { useState, useEffect } from 'react';

import { getAvailableModels } from '../services/modelService';

import { ApiResponse } from '../interfaces/BuildPageInterfaces';

export const useBuildPage = () => {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response: ApiResponse = await getAvailableModels();
      setData(response);
    } catch (error: any) {
      setError(error.message);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { data, loading, error };
};
