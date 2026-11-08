import axios from 'axios';
import { getEnvVar } from './envVars';

const axiosClient = axios.create({
  baseURL: getEnvVar('API_BASE_URL', process.env.NEXT_PUBLIC_API_BASE_URL),
});

// Logged axios errors include the request config; never let the bearer token
// travel with them into console output or log collectors.
axiosClient.interceptors.response.use(undefined, (error) => {
  if (error?.config?.headers) {
    error.config.headers.Authorization = undefined;
  }
  return Promise.reject(error);
});

export default axiosClient;
