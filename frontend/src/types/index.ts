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
  // Attendance tracking fields
  last_check_in?: string
  last_check_out?: string
  is_on_break?: boolean
  break_start_time?: string
  current_status?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}
