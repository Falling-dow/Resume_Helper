import client from './client'

export async function login(email: string, password: string) {
  const { data } = await client.post('/auth/login', { email, password })
  return data as { access_token: string; token_type: string }
}

export async function register(email: string, password: string, username?: string) {
  const { data } = await client.post('/auth/register', { email, password, username })
  return data as { access_token: string; token_type: string }
}

export async function logout() {
  const { data } = await client.post('/auth/logout')
  return data as { detail: string }
}

