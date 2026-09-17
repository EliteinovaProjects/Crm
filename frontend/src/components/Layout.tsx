import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { adminNav, employeeNav } from '../config/sidebar'
import { BellIcon, PhoneIcon } from './icons'
import { DialPad } from './DialPad'

export function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const nav = user?.role === 'employee' ? employeeNav : adminNav
  const liveCallsPath = user?.role === 'employee' ? '/employee/live-calls' : '/admin/live-calls'

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside
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
        <nav style={{ display: 'flex', flexDirection: 'column', gap: 8, width: '100%' }}>
          {nav.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.path}
                to={item.path}
                style={({ isActive }) => ({
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: 6,
                  padding: '10px 4px',
                  margin: '0 10px',
                  borderRadius: 12,
                  textDecoration: 'none',
                  color: isActive ? '#fff' : '#8b8ba7',
                  background: isActive ? 'var(--brand-gradient)' : 'transparent',
                  fontSize: 10.5,
                  fontWeight: 600,
                  textAlign: 'center',
                })}
              >
                <Icon width={19} height={19} />
                <span>{item.label}</span>
              </NavLink>
            )
          })}
        </nav>
      </aside>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <header
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
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
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
            <div style={{ position: 'relative', color: 'var(--text-muted)' }}>
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
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div
                style={{
                  width: 30,
                  height: 30,
                  borderRadius: '50%',
                  background: 'var(--brand-gradient)',
                  color: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 12,
                  fontWeight: 700,
                }}
              >
                {(user?.full_name || user?.username || '?').slice(0, 1).toUpperCase()}
              </div>
              <span style={{ fontSize: 13, fontWeight: 600 }}>{user?.full_name || user?.username}</span>
              <button
                onClick={handleLogout}
                style={{
                  background: 'none',
                  border: '1px solid var(--border-soft)',
                  borderRadius: 8,
                  padding: '6px 12px',
                  fontSize: 12,
                  cursor: 'pointer',
                  color: 'var(--text-muted)',
                }}
              >
                Sign Out
              </button>
            </div>
          </div>
        </header>

        <main style={{ flex: 1, padding: 24, background: 'var(--bg-app)' }}>
          <Outlet />
        </main>
      </div>

      <DialPad />
    </div>
  )
}