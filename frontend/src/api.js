import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

let isRefreshing = false
let refreshSubscribers = []

function onRefreshed(newToken) {
  refreshSubscribers.forEach((cb) => cb(newToken))
  refreshSubscribers = []
}

function addRefreshSubscriber(cb) {
  refreshSubscribers.push(cb)
}

api.interceptors.request.use(
  (config) => {
    // Use Pinia store for token
    const authStore = useAuthStore()
    if (authStore.token && !config.headers.Authorization) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/oauth/token') &&
      !originalRequest.url.includes('/oauth/refresh')
    ) {
      originalRequest._retry = true
      if (!isRefreshing) {
        isRefreshing = true
        try {
          const refreshResponse = await api.post('/oauth/refresh', null, {
            withCredentials: true,
          })
          const newAccessToken = refreshResponse.data.access_token
          authStore.setToken(newAccessToken)
          onRefreshed(newAccessToken)
          isRefreshing = false
        } catch (refreshError) {
          isRefreshing = false
          authStore.logout()
          if (refreshError.response && refreshError.response.status === 401) {
            window.location.replace('/')
          }
          return Promise.reject(refreshError)
        }
      }
      return new Promise((resolve, reject) => {
        addRefreshSubscriber((token) => {
          if (token) {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(api(originalRequest))
          } else {
            reject(error)
          }
        })
      })
    }
    return Promise.reject(error)
  }
)

export default api
