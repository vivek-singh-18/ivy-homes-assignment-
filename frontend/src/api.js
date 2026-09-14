import axios from 'axios';

// IMPORTANT: Replace this with your actual deployed Vercel URL
export const PROXY_BASE = 'https://ivy-homes-assignment-snowy.vercel.app';

const api = axios.create({
  baseURL: `${PROXY_BASE}/api/proxy`,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  // Store the target URL in a custom header so the proxy knows where to route
  // Combine baseURL and url only if the url isn't already absolute
  let targetPath = config.url;
  config.headers['X-Target-Path'] = targetPath;
  
  // We want to send it to the proxy base URL ALWAYS
  config.url = '';
  return config;
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function(resolve, reject) {
          failedQueue.push({resolve, reject})
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        localStorage.removeItem('access_token');
        window.location.href = '#/login';
        return Promise.reject(error);
      }

      try {
        const { data } = await axios.post(`${PROXY_BASE}/api/proxy`, {
          refresh_token: refreshToken
        }, {
          headers: {
            'X-Target-Path': '/auth/refresh'
          }
        });
        
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
        }
        
        api.defaults.headers.common['Authorization'] = 'Bearer ' + data.access_token;
        originalRequest.headers['Authorization'] = 'Bearer ' + data.access_token;
        processQueue(null, data.access_token);
        return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '#/login';
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
