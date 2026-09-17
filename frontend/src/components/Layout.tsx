import { useState, useEffect, useRef } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { adminLMSNav, adminCMSNav, employeeLMSNav, employeeCMSNav } from '../config/sidebar'
import { BellIcon, PhoneIcon, UserIcon, LogOutIcon, SettingsIcon } from './icons'
import { DialPad } from './DialPad'
import { api } from '../services/api'

export function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [showProfileMenu, setShowProfileMenu] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const [updatingAttendance, setUpdatingAttendance] = useState(false)
  const [attendanceError, setAttendanceError] = useState('')
  const [workspace, setWorkspace] = useState<'lms' | 'cms'>(() => {
    const saved = sessionStorage.getItem('crm_workspace')
    return saved === 'cms' ? 'cms' : 'lms'
  })
  const profileMenuRef = useRef<HTMLDivElement>(null)
  const notificationRef = useRef<HTMLDivElement>(null)
  const isEmployee = user?.role === 'employee'
  const lmsNav = isEmployee ? employeeLMSNav : adminLMSNav
  const cmsNav = isEmployee ? employeeCMSNav : adminCMSNav
  const liveCallsPath = user?.role === 'employee' ? '/employee/live-calls' : '/admin/live-calls'

  // Close dropdowns when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setShowProfileMenu(false)
      }
      if (notificationRef.current && !notificationRef.current.contains(event.target as Node)) {
        setShowNotifications(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  async function handleCheckIn() {
    if (updatingAttendance) return
    setUpdatingAttendance(true)
    try {
      await api.post('/attendance/quick-check-in')
      // Reload the authenticated user so the header reflects the new status.
      window.location.reload()
    } catch (error: any) {
      setAttendanceError(error?.response?.data?.detail || 'Check-in failed. Please try again.')
      console.error('Check-in failed:', error)
    } finally {
      setUpdatingAttendance(false)
    }
  }

  async function handleCheckOut() {
    if (updatingAttendance) return
    setUpdatingAttendance(true)
    try {
      await api.post('/attendance/quick-check-out')
      window.location.reload()
    } catch (error: any) {
      setAttendanceError(error?.response?.data?.detail || 'Check-out failed. Please try again.')
      console.error('Check-out failed:', error)
    } finally {
      setUpdatingAttendance(false)
    }
  }

  async function handleBreakToggle() {
    if (updatingAttendance) return
    setUpdatingAttendance(true)
    try {
      if (user?.is_on_break) {
        await api.post('/attendance/quick-break-end')
      } else {
        await api.post('/attendance/quick-break-start')
      }
      window.location.reload()
    } catch (error: any) {
      setAttendanceError(error?.response?.data?.detail || 'Break update failed. Please try again.')
      console.error('Break toggle failed:', error)
    } finally {
      setUpdatingAttendance(false)
    }
  }

  return (
    <div className="app-shell" style={{ display: 'flex', minHeight: '100vh' }}>
      <aside className="app-sidebar"
        style={{
          width: 96,
          background: '#fff',
          borderRight: '1px solid var(--border-soft)',
          padding: '20px 0',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            width: 40,
            height: 40,
            borderRadius: 12,
            background: 'var(--brand-gradient)',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 800,
            marginBottom: 28,
          }}
        >
          E
        </div>
        <div style={{ display: 'flex', gap: 4, padding: '0 8px 12px', width: '100%', boxSizing: 'border-box' }}>
          {(['lms', 'cms'] as const).map((section) => (
            <button key={section} onClick={() => { setWorkspace(section); sessionStorage.setItem('crm_workspace', section) }} style={{ flex: 1, border: 0, borderRadius: 6, padding: '6px 2px', cursor: 'pointer', fontSize: 9, fontWeight: 800, letterSpacing: 0.6, textTransform: 'uppercase', color: workspace === section ? '#fff' : '#8b8ba7', background: workspace === section ? 'var(--brand-gradient)' : 'transparent' }}>{section}</button>
          ))}
        </div>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: 8, width: '100%' }}>
          <div style={{ padding: '0 14px 4px', color: '#a09ab0', fontSize: 9, fontWeight: 800, letterSpacing: 1, textTransform: 'uppercase' }}>
            {workspace.toUpperCase()}
          </div>
          {(workspace === 'lms' ? lmsNav : cmsNav).map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.path}
                to={item.path}
                style={({ isActive }) => ({
                  display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
                  padding: '10px 4px', margin: '0 10px', borderRadius: 12,
                  textDecoration: 'none', color: isActive ? '#fff' : '#8b8ba7',
                  background: isActive ? 'var(--brand-gradient)' : 'transparent',
                  fontSize: 10.5, fontWeight: 600, textAlign: 'center',
                })}
              >
                <Icon width={19} height={19} />
                <span>{item.label}</span>
              </NavLink>
            )
          })}

        </nav>
      </aside>

      <div className="app-main" style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <header className="app-header"
          style={{
            height: 64,
            borderBottom: '1px solid var(--border-soft)',
            background: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0 28px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div
              style={{
                width: 30,
                height: 30,
                borderRadius: 9,
                background: 'var(--brand-gradient)',
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: 13,
              }}
            >
              E
            </div>
            <div>
              <div style={{ fontWeight: 800, fontSize: 15 }}>
                ELITEINOVA <span style={{ color: '#ec4899' }}>CRM</span>
              </div>
              <div style={{ fontSize: 9, color: 'var(--text-muted)', letterSpacing: 0.5 }}>
                CRM PORTAL 
              </div>
            </div>
          </div>

          <div style={{ textAlign: 'right', fontSize: 11.5, color: 'var(--text-muted)', lineHeight: 1.6 }}>
            <div>
              Active IVR Number: <strong style={{ color: 'var(--text-main)' }}>9940200578</strong>
            </div>
            <div>Account Expires On: 30 Nov 2026 05:46:19</div>
            
            {/* Employee Check-in/Check-out and Break Section */}
            {user?.role === 'employee' && (
              <div style={{ marginTop: 8, display: 'flex', gap: 12, alignItems: 'center' }}>
                <div>
                  Check-in: <strong style={{ color: 'var(--text-main)' }}>{user.last_check_in ? new Date(user.last_check_in).toLocaleTimeString() : '--:--'}</strong>
                </div>
                <div>
                  Check-out: <strong style={{ color: 'var(--text-main)' }}>{user.last_check_out ? new Date(user.last_check_out).toLocaleTimeString() : '--:--'}</strong>
                </div>
                {attendanceError && <span style={{ color: '#e05252', fontSize: 10 }}>{attendanceError}</span>}
                <button
                  onClick={() => { setAttendanceError(''); (user.current_status === 'online' ? handleCheckOut : handleCheckIn)() }}
                  disabled={updatingAttendance}
                  style={{
                    background: user.current_status === 'online' ? '#ef4444' : '#22c55e',
                    color: '#fff',
                    border: 'none',
                    borderRadius: 6,
                    padding: '4px 12px',
                    fontSize: 11,
                    fontWeight: 600,
                    cursor: updatingAttendance ? 'default' : 'pointer',
                    opacity: updatingAttendance ? 0.7 : 1,
                  }}
                >
                  {updatingAttendance ? 'Processing...' : (user.current_status === 'online' ? 'Check Out' : 'Check In')}
                </button>
                <button
                  onClick={handleBreakToggle}
                  disabled={updatingAttendance}
                  style={{
                    background: user.is_on_break ? '#f59e0b' : '#6b7280',
                    color: '#fff',
                    border: 'none',
                    borderRadius: 6,
                    padding: '4px 12px',
                    fontSize: 11,
                    fontWeight: 600,
                    cursor: updatingAttendance ? 'default' : 'pointer',
                    opacity: updatingAttendance ? 0.7 : 1,
                  }}
                >
                  {updatingAttendance ? 'Processing...' : (user.is_on_break ? 'End Break' : 'Take Break')}
                </button>
              </div>
            )}
          </div>

          <div className="header-actions" style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
            <button
              onClick={() => navigate(liveCallsPath)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                background: 'var(--brand-gradient)',
                color: '#fff',
                padding: '8px 16px',
                borderRadius: 999,
                fontSize: 13,
                fontWeight: 600,
                border: 'none',
                cursor: 'pointer',
              }}
            >
              <PhoneIcon width={15} height={15} />
              Live Calls
              <span style={{ background: 'rgba(255,255,255,0.25)', padding: '1px 8px', borderRadius: 999 }}>0</span>
              <span style={{ background: 'rgba(255,255,255,0.25)', padding: '1px 8px', borderRadius: 999 }}>0</span>
            </button>
            
            {/* Notification Button */}
            <div ref={notificationRef} style={{ position: 'relative' }}>
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: 'var(--text-muted)',
                  padding: 4,
                  borderRadius: 8,
                }}
              >
                <BellIcon />
                <span
                  style={{
                    position: 'absolute',
                    top: -2,
                    right: -2,
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    background: '#ec4899',
                  }}
                />
              </button>
              
              {showNotifications && (
                <div
                  style={{
                    position: 'absolute',
                    right: 0,
                    top: '100%',
                    marginTop: 8,
                    width: 280,
                    background: '#fff',
                    borderRadius: 12,
                    boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                    border: '1px solid var(--border-soft)',
                    zIndex: 1000,
                    padding: 16,
                  }}
                >
                  <div style={{ fontWeight: 600, marginBottom: 12, fontSize: 14 }}>Notifications</div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', textAlign: 'center', padding: 20 }}>
                    No new notifications
                  </div>
                </div>
              )}
            </div>
            
            {/* Profile Menu */}
            <div ref={profileMenuRef} style={{ position: 'relative' }}>
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: 4,
                  borderRadius: 8,
                }}
              >
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    background: 'var(--brand-gradient)',
                    color: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 13,
                    fontWeight: 700,
                  }}
                >
                  {(user?.full_name || user?.username || '?').slice(0, 1).toUpperCase()}
                </div>
                <span style={{ fontSize: 13, fontWeight: 600 }}>{user?.full_name || user?.username}</span>
              </button>
              
              {showProfileMenu && (
                <div
                  style={{
                    position: 'absolute',
                    right: 0,
                    top: '100%',
                    marginTop: 8,
                    width: 200,
                    background: '#fff',
                    borderRadius: 12,
                    boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                    border: '1px solid var(--border-soft)',
                    zIndex: 1000,
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      padding: '12px 16px',
                      borderBottom: '1px solid var(--border-soft)',
                      fontSize: 13,
                      fontWeight: 600,
                    }}
                  >
                    {user?.full_name || user?.username}
                  </div>
                  <div
                    style={{
                      padding: '12px 16px',
                      fontSize: 12,
                      color: 'var(--text-muted)',
                      borderBottom: '1px solid var(--border-soft)',
                    }}
                  >
                    {user?.email}
                  </div>
                  <button
                    onClick={() => {
                      setShowProfileMenu(false)
                      navigate(user?.role === 'employee' ? '/employee/settings' : '/admin/settings')
                    }}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      background: 'none',
                      border: 'none',
                      textAlign: 'left',
                      cursor: 'pointer',
                      fontSize: 13,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 8,
                      color: 'var(--text-main)',
                    }}
                  >
                    <SettingsIcon width={16} height={16} />
                    Settings
                  </button>
                  <button
                    onClick={handleLogout}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      background: 'none',
                      border: 'none',
                      textAlign: 'left',
                      cursor: 'pointer',
                      fontSize: 13,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 8,
                      color: '#e11d48',
                    }}
                  >
                    <LogOutIcon width={16} height={16} />
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        <main className="app-content" style={{ flex: 1, padding: 24, background: 'var(--bg-app)', minWidth: 0 }}>
          <Outlet />
        </main>
      </div>

      <DialPad />
    </div>
  )
}