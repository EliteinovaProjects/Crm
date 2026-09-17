import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { api } from '../services/api'
import type { User, LoginResponse } from '../types'

interface AuthContextValue {
  user: User | null
  loading: boolean
  login: (username: string, password: string, portal: 'admin' | 'employee') => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setLoading(false)
      return
    }
    api
      .get<User>('/auth/me')
      .then((res) => setUser(res.data))
      .catch(() => localStorage.removeItem('access_token'))
      .finally(() => setLoading(false))
  }, [])

  async function login(username: string, password: string, portal: 'admin' | 'employee') {
    const res = await api.post<LoginResponse>('/auth/login', { username, password, portal })
    localStorage.setItem('access_token', res.data.access_token)
    setUser(res.data.user)
  }

  function logout() {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
