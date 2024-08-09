import { useState, useEffect } from 'react';
import { PropertiesSchema } from '../interfaces/BuildPageInterfacesNew';
import { getSchema } from 'wasp/client/operations';

export const useBuildPageNew = () => {
  const [data, setData] = useState<PropertiesSchema | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response: PropertiesSchema = await getSchema();
      setData(response);
    } catch (error: any) {
      console.error('Failed to fetch schemas:', error);
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
