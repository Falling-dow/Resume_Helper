import axios from 'axios'

const baseURL = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000/api/v1'

const client = axios.create({ baseURL })

client.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    cfg.headers = cfg.headers || {}
    cfg.headers['Authorization'] = `Bearer ${token}`
  }
  return cfg
})

client.interceptors.response.use(
  (resp) => resp,
  (err) => Promise.reject(err)
)

export default client
