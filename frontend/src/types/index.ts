export type UserRole = 'admin' | 'sub_admin' | 'employee'

export interface User {
  id: string
  email: string
  username: string
  full_name?: string
  phone?: string
  role: UserRole
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}
