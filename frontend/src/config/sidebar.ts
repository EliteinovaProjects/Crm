import {
  DashboardIcon,
  PhoneIcon,
  AgentsIcon,
  LeadsIcon,
  ReportsIcon,
  SettingsIcon,
} from '../components/icons'

export interface NavItem {
  label: string
  path: string
  icon: typeof DashboardIcon
}

export const adminNav: NavItem[] = [
  { label: 'Dashboard', path: '/admin/dashboard', icon: DashboardIcon },
  { label: 'Live Calls', path: '/admin/live-calls', icon: PhoneIcon },
  { label: 'Agents', path: '/admin/agents', icon: AgentsIcon },
  { label: 'Leads & Logs', path: '/admin/leads', icon: LeadsIcon },
  { label: 'Reports', path: '/admin/reports', icon: ReportsIcon },
  { label: 'Settings', path: '/admin/settings', icon: SettingsIcon },
]

export const employeeNav: NavItem[] = [
  { label: 'Dashboard', path: '/employee/dashboard', icon: DashboardIcon },
  { label: 'Live Calls', path: '/employee/live-calls', icon: PhoneIcon },
  { label: 'Agents', path: '/employee/agents', icon: AgentsIcon },
  { label: 'Leads & Logs', path: '/employee/leads', icon: LeadsIcon },
  { label: 'Reports', path: '/employee/reports', icon: ReportsIcon },
  { label: 'Settings', path: '/employee/settings', icon: SettingsIcon },
]

export const settingsLinks = [
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

export const employeeSettingsLinks = [
  { label: 'Reminder List', path: 'reminders' },
  { label: 'Campaign Base', path: 'campaign-base' },
  { label: 'Coins', path: 'coins' },
]
