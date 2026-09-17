import { Link, Route, Routes, useLocation } from 'react-router-dom'
import { PagePlaceholder } from '../components/PagePlaceholder'
import { 
  toolboxSettingsLinks, 
  toolboxFunctionalityLinks, 
  toolboxAccountsLinks, 
  toolboxResourcesLinks,
  c2cSettingsLinks,
  coinsLinks,
  reminderLinks
} from '../config/sidebar'
import { useAuth } from '../contexts/AuthContext'

interface LinkItem {
  label: string
  path: string
}

export function Settings() {
  const { user } = useAuth()
  const location = useLocation()
  
  // Determine which links to show based on user role and current path
  let links: LinkItem[] = []
  
  if (user?.role === 'employee') {
    // Employee settings - simpler structure
    if (location.pathname.includes('reminders')) {
      links = reminderLinks
    } else if (location.pathname.includes('coins')) {
      links = coinsLinks
    } else {
      links = [
        { label: 'Reminder List', path: 'reminders' },
        { label: 'Campaign Base', path: 'campaign-base' },
        { label: 'Coins', path: 'coins' },
      ]
    }
  } else {
    // Admin settings - more complex structure
    if (location.pathname.includes('toolbox-settings')) {
      links = toolboxSettingsLinks
    } else if (location.pathname.includes('toolbox-functionality')) {
      links = toolboxFunctionalityLinks
    } else if (location.pathname.includes('toolbox-accounts')) {
      links = toolboxAccountsLinks
    } else if (location.pathname.includes('toolbox-resources')) {
      links = toolboxResourcesLinks
    } else if (location.pathname.includes('c2c')) {
      links = c2cSettingsLinks
    } else if (location.pathname.includes('coins')) {
      links = coinsLinks
    } else {
      // Main admin settings page
      links = [
        { label: 'Manage Fields', path: 'fields' },
        { label: 'Add Source', path: 'sources' },
        { label: 'Add Status', path: 'statuses' },
        { label: 'Add Category', path: 'categories' },
        { label: 'SMS Templates', path: 'sms-templates' },
        { label: 'API Docs', path: 'api-docs' },
        { label: 'Tool Box - Settings', path: 'toolbox-settings' },
        { label: 'Tool Box - Functionality', path: 'toolbox-functionality' },
        { label: 'Tool Box - Accounts', path: 'toolbox-accounts' },
        { label: 'Tool Box - Resources', path: 'toolbox-resources' },
        { label: 'C2C Settings', path: 'c2c' },
        { label: 'Coins', path: 'coins' },
      ]
    }
  }
  
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
          {links.map((link: LinkItem) => (
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
            {links.map((link: LinkItem) => (
              <Route key={link.path} path={link.path} element={<PagePlaceholder title={link.label} />} />
            ))}
            <Route path="*" element={<PagePlaceholder title={links[0]?.label || 'Settings'} />} />
          </Routes>
        </div>
      </div>
    </div>
  )
}
