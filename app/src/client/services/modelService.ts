// services/modelService.ts
import { getAvailableModels as apigetAvailableModels } from 'wasp/client/operations';

export const getAvailableModels = async () => {
  try {
    const response = await apigetAvailableModels();
    return response;
  } catch (error) {
    console.error('Failed to fetch models:', error);
    throw error;
  }
};
