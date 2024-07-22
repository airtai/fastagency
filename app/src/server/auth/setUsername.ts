import { defineUserSignupFields } from 'wasp/auth/providers/types';
import { generateAvailableUsername } from './authHelper';

const adminEmails = process.env.ADMIN_EMAILS?.split(',') || [];

export const getGoogleUserFields = defineUserSignupFields({
  username: async (data: any) => {
    return await generateAvailableUsername(data.profile.name, {
      separator: '.',
    });
  },
  email: (data: any) => data.profile.email,
  isAdmin: (data: any) => adminEmails.includes(data.profile.email),
  hasPaid: () => true,
  isSetUpComplete: () => false,
});

export function getGoogleAuthConfig() {
  return {
    scopes: ['profile', 'email'], // must include at least 'profile' for Google
  };
}
