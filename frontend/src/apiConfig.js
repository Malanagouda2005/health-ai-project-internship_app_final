export const API_OVERRIDE_STORAGE_KEY = 'HEALTH_AI_BACKEND_URL';

export const isAndroidPlatform = () => {
  if (typeof window === 'undefined') return false;
  const userAgent = navigator?.userAgent?.toLowerCase() || '';
  return /android/i.test(userAgent);
};

export const isCapacitorWebView = () => {
  if (typeof window === 'undefined') return false;
  const protocol = window.location.protocol || '';
  const isCapacitor = protocol.startsWith('capacitor') || protocol.startsWith('ionic') || protocol === 'file:';
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  return isCapacitor || isLocalhost;
};

const normalizeApiUrl = (value) => {
  if (!value) return '';
  let url = value.trim();
  if (!/^https?:\/\//i.test(url)) url = `http://${url}`;
  try {
    return new URL(url).origin;
  } catch {
    return '';
  }
};

const getApiBaseUrl = () => {
  console.log('[apiConfig] Environment check:');
  console.log('  - window.location.protocol:', typeof window !== 'undefined' ? window.location.protocol : 'undefined');
  console.log('  - window.location.href:', typeof window !== 'undefined' ? window.location.href : 'undefined');
  console.log('  - process.env.REACT_APP_API_URL:', process.env.REACT_APP_API_URL);

  // 1. Check localStorage override FIRST (user-set via UI)
  const storedOverride = typeof window !== 'undefined' ? localStorage.getItem(API_OVERRIDE_STORAGE_KEY) : null;
  console.log('  - storedOverride:', storedOverride);
  if (storedOverride) {
    const normalized = normalizeApiUrl(storedOverride);
    console.log('[apiConfig] Using stored override:', normalized);
    return normalized || 'https://backend-intership-health-risk-predi-nine.vercel.app/';
  }

  // 2. Check environment variable (REACT_APP_API_URL from .env)
  if (process.env.REACT_APP_API_URL) {
    const normalized = normalizeApiUrl(process.env.REACT_APP_API_URL);
    console.log('[apiConfig] Using REACT_APP_API_URL from .env:', normalized);
    return normalized || 'https://backend-intership-health-risk-predi-nine.vercel.app/';
  }

  // 3. SSR or no window
  if (typeof window === 'undefined') {
    console.log('[apiConfig] SSR environment, using default');
    return 'https://backend-intership-health-risk-predi-nine.vercel.app/';
  }

  // 4. Default: use the configured IP for Android emulator
  console.log('[apiConfig] Using default IP for Android emulator');
  return 'https://backend-intership-health-risk-predi-nine.vercel.app/';
};


export default getApiBaseUrl;
