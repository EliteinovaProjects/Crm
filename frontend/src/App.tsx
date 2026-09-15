import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { Layout } from './components/Layout'
import { PagePlaceholder } from './components/PagePlaceholder'
import { Login } from './pages/Login'
import { Settings } from './pages/Settings'
import { AdminDashboard } from './pages/admin/AdminDashboard'
import { EmployeeDashboard } from './pages/employee/EmployeeDashboard'
import { LeadsList } from './pages/leads/LeadsList'
import { LiveCalls } from './pages/calls/LiveCalls'

function RootRedirect() {
  const { user, loading } = useAuth()
  if (loading) return <div style={{ padding: 24 }}>Loading...</div>
  if (!user) return <Navigate to="/login" replace />
  return <Navigate to={user.role === 'employee' ? '/employee/dashboard' : '/admin/dashboard'} replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<RootRedirect />} />

          <Route
            element={
              <ProtectedRoute roles={['admin', 'sub_admin']}>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/live-calls" element={<LiveCalls />} />
            <Route path="/admin/agents" element={<PagePlaceholder title="Agents" />} />
            <Route path="/admin/leads" element={<LeadsList />} />
            <Route path="/admin/reports" element={<PagePlaceholder title="Reports" />} />
            <Route path="/admin/settings/*" element={<Settings />} />
          </Route>

          <Route
            element={
              <ProtectedRoute roles={['employee']}>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/employee/dashboard" element={<EmployeeDashboard />} />
            <Route path="/employee/live-calls" element={<LiveCalls />} />
            <Route path="/employee/agents" element={<PagePlaceholder title="Agents" />} />
            <Route path="/employee/leads" element={<LeadsList />} />
            <Route path="/employee/reports" element={<PagePlaceholder title="Reports" />} />
            <Route path="/employee/settings/*" element={<Settings />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}