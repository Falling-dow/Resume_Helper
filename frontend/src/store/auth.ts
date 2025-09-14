import { create } from 'zustand'

export type AuthState = {
  token: string | null
  setToken: (t: string | null) => void
  logout: () => void
}

const initial = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null

export const useAuth = create<AuthState>((set) => ({
  token: initial,
  setToken: (t) => {
    if (t) localStorage.setItem('auth_token', t)
    else localStorage.removeItem('auth_token')
    set({ token: t })
  },
  logout: () => {
    localStorage.removeItem('auth_token')
    set({ token: null })
  },
}))
