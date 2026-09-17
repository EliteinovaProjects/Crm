import {
  DashboardIcon,
  PhoneIcon,
  AgentsIcon,
  LeadsIcon,
  ReportsIcon,
  SettingsIcon,
  ToolBoxIcon,
  C2CIcon,
  CoinsIcon,
  ReminderIcon,
  CampaignIcon,
} from '../components/icons'

export interface NavItem {
  label: string
  path: string
  icon: typeof DashboardIcon
}

// LMS (Learning Management System) Navigation for Admin
export const adminLMSNav: NavItem[] = [
  { label: 'Dashboard', path: '/admin/dashboard', icon: DashboardIcon },
  { label: 'Leads & Logs', path: '/admin/leads', icon: LeadsIcon },
  { label: 'Manage Fields', path: '/admin/fields', icon: SettingsIcon },
  { label: 'Add Source', path: '/admin/sources', icon: SettingsIcon },
  { label: 'Add Status', path: '/admin/statuses', icon: SettingsIcon },
  { label: 'Add Category', path: '/admin/categories', icon: SettingsIcon },
  { label: 'SMS Templates', path: '/admin/sms-templates', icon: SettingsIcon },
  { label: 'API Docs', path: '/admin/api-docs', icon: SettingsIcon },
  { label: 'Agents', path: '/admin/agents', icon: AgentsIcon },
]

// CMS (Context Management System) Navigation for Admin
export const adminCMSNav: NavItem[] = [
  { label: 'Tool Box', path: '/admin/toolbox', icon: ToolBoxIcon },
  { label: 'C2C Settings', path: '/admin/c2c', icon: C2CIcon },
  { label: 'Coins', path: '/admin/coins', icon: CoinsIcon },
]

// Combined Admin Navigation
export const adminNav: NavItem[] = [
  { label: 'Dashboard', path: '/admin/dashboard', icon: DashboardIcon },
  { label: 'Leads & Logs', path: '/admin/leads', icon: LeadsIcon },
  { label: 'Manage Fields', path: '/admin/fields', icon: SettingsIcon },
  { label: 'Add Source', path: '/admin/sources', icon: SettingsIcon },
  { label: 'Add Status', path: '/admin/statuses', icon: SettingsIcon },
  { label: 'Add Category', path: '/admin/categories', icon: SettingsIcon },
  { label: 'SMS Templates', path: '/admin/sms-templates', icon: SettingsIcon },
  { label: 'API Docs', path: '/admin/api-docs', icon: SettingsIcon },
  { label: 'Agents', path: '/admin/agents', icon: AgentsIcon },
  { label: 'Tool Box', path: '/admin/toolbox', icon: ToolBoxIcon },
  { label: 'C2C Settings', path: '/admin/c2c', icon: C2CIcon },
  { label: 'Coins', path: '/admin/coins', icon: CoinsIcon },
]

// LMS (Learning Management System) Navigation for Employee
export const employeeLMSNav: NavItem[] = [
  { label: 'Dashboard', path: '/employee/dashboard', icon: DashboardIcon },
  { label: 'Leads & Logs', path: '/employee/leads', icon: LeadsIcon },
]

// CMS (Context Management System) Navigation for Employee
export const employeeCMSNav: NavItem[] = [
  { label: 'Reminder List', path: '/employee/reminders', icon: ReminderIcon },
  { label: 'Campaign Base', path: '/employee/campaign-base', icon: CampaignIcon },
  { label: 'Coins', path: '/employee/coins', icon: CoinsIcon },
]

// Combined Employee Navigation
export const employeeNav: NavItem[] = [
  { label: 'Dashboard', path: '/employee/dashboard', icon: DashboardIcon },
  { label: 'Leads & Logs', path: '/employee/leads', icon: LeadsIcon },
  { label: 'Reminder List', path: '/employee/reminders', icon: ReminderIcon },
  { label: 'Campaign Base', path: '/employee/campaign-base', icon: CampaignIcon },
  { label: 'Coins', path: '/employee/coins', icon: CoinsIcon },
]

// Tool Box Settings Sub-navigation
export const toolboxSettingsLinks = [
  { label: 'Design IVR Flow', path: 'ivr-flow' },
  { label: 'Sub-Admin', path: 'sub-admin' },
]

// Tool Box Functionality Sub-navigation
export const toolboxFunctionalityLinks = [
  { label: 'Contacts', path: 'contacts' },
  { label: 'Agent Groups', path: 'agent-groups' },
  { label: 'Export', path: 'export' },
  { label: 'Black List', path: 'blacklist' },
  { label: 'System Logs', path: 'system-logs' },
  { label: 'TopUp History', path: 'topup-history' },
  { label: 'Renewal History', path: 'renewal-history' },
  { label: 'Api Integration', path: 'api-integration' },
  { label: 'Holidays', path: 'holidays' },
  { label: 'Reminder', path: 'reminder' },
  { label: 'Break Reason', path: 'break-reason' },
  { label: 'Agent Call Type', path: 'agent-call-type' },
  { label: 'Disposition List', path: 'disposition-list' },
  { label: 'Text To Speech', path: 'text-to-speech' },
  { label: 'Configuration', path: 'configuration' },
]

// Tool Box Accounts Sub-navigation
export const toolboxAccountsLinks = [
  { label: 'Preferences', path: 'preferences' },
  { label: 'Payment History', path: 'payment-history' },
  { label: 'DID Configuration', path: 'did-configuration' },
]

// Tool Box Resources Sub-navigation
export const toolboxResourcesLinks = [
  { label: 'Agents', path: 'agents' },
  { label: 'Sound Library', path: 'sound-library' },
  { label: 'SMS Templates', path: 'sms-templates' },
]

// C2C Settings Sub-navigation
export const c2cSettingsLinks = [
  { label: 'Create Campaign', path: 'create-campaign' },
  { label: 'Campaign List', path: 'campaign-list' },
  { label: 'Campaign Base', path: 'campaign-base' },
  { label: 'Manage Field', path: 'manage-field' },
]

// Coins Sub-navigation
export const coinsLinks = [
  { label: 'Monthly Coins', path: 'monthly-coins' },
  { label: 'Top-Up Coins', path: 'topup-coins' },
]

// Reminder List Sub-navigation
export const reminderLinks = [
  { label: 'Upcoming Reminder', path: 'upcoming' },
  { label: 'Reminder History', path: 'history' },
]
