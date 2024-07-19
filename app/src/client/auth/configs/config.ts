export function stripTrailingSlash(url?: string): string | undefined {
    return url?.replace(/\/$/, "");
}

const apiUrl = stripTrailingSlash(import.meta.env.REACT_APP_API_URL) || 'http://localhost:3001';

const config = {
  apiUrl,
}

export default config
