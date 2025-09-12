import axios from 'axios'

const baseURL = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000/api/v1'

const client = axios.create({ baseURL })

client.interceptors.response.use(
  (resp) => resp,
  (err) => Promise.reject(err)
)

export default client

