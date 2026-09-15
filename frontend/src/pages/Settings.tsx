import { Link, Route, Routes, useLocation } from 'react-router-dom'
import { PagePlaceholder } from '../components/PagePlaceholder'
import { settingsLinks, employeeSettingsLinks } from '../config/sidebar'
import { useAuth } from '../contexts/AuthContext'

export function Settings() {
  const { user } = useAuth()
  const location = useLocation()
  const links = user?.role === 'employee' ? employeeSettingsLinks : settingsLinks
  const base = location.pathname.split('/settings')[0] + '/settings'

  return (
    <div>
      <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 20 }}>Settings</div>
      <div style={{ display: 'flex', gap: 24 }}>
        <div
          style={{
            width: 220,
            background: '#fff',
            borderRadius: 16,
            boxShadow: 'var(--shadow-card)',
            padding: 12,
            flexShrink: 0,
          }}
        >
          {links.map((link) => (
            <Link
              key={link.path}
              to={`${base}/${link.path}`}
              style={{
                display: 'block',
                padding: '10px 12px',
                borderRadius: 10,
                textDecoration: 'none',
                color: location.pathname.endsWith(link.path) ? '#ec4899' : 'var(--text-main)',
                background: location.pathname.endsWith(link.path) ? 'var(--brand-gradient-soft)' : 'transparent',
                fontSize: 13.5,
                fontWeight: 600,
                marginBottom: 4,
              }}
            >
              {link.label}
            </Link>
          ))}
        </div>
        <div style={{ flex: 1 }}>
          <Routes>
            {links.map((link) => (
              <Route key={link.path} path={link.path} element={<PagePlaceholder title={link.label} />} />
            ))}
            <Route path="*" element={<PagePlaceholder title={links[0].label} />} />
          </Routes>
        </div>
      </div>
    </div>
  )
}
