import { FormEvent, useEffect, useState } from 'react'
import { api } from '../services/api'

type Section = 'reminders' | 'campaign-base' | 'coins' | 'toolbox' | 'c2c' | 'coin-admin'

const groups = {
  toolbox: ['Settings', 'Functionality', 'Accounts', 'Resources'],
  c2c: ['Create Campaign', 'Campaign List', 'Campaign Base', 'Manage Field'],
  'coin-admin': ['Monthly Coins', 'Top-Up Coins'],
}

export function WorkspaceSection({ section }: { section: Section }) {
  const [tab, setTab] = useState(section === 'reminders' ? 'Upcoming Reminder' : section === 'coins' || section === 'coin-admin' ? 'Monthly Coins' : section === 'toolbox' ? 'Settings' : 'Campaign Base')
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ title: '', due_at: '', description: '' })

  useEffect(() => {
    if (section !== 'reminders') return
    setLoading(true)
    api.get(tab === 'Reminder History' ? '/reminders/history' : '/reminders/upcoming')
      .then((res) => setItems(res.data))
      .catch(() => setError('Unable to load reminders.'))
      .finally(() => setLoading(false))
  }, [section, tab])

  async function createReminder(event: FormEvent) {
    event.preventDefault()
    try {
      await api.post('/reminders/', form)
      setForm({ title: '', due_at: '', description: '' })
      setTab('Upcoming Reminder')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Unable to create reminder.')
    }
  }

  const tabs: string[] = section === 'reminders'
    ? ['Upcoming Reminder', 'Reminder History']
    : section === 'campaign-base'
      ? ['Campaign Base']
      : groups[section === 'coins' ? 'coin-admin' : section]
  const title = section === 'reminders' ? 'Reminder List' : section === 'campaign-base' ? 'Campaign Base' : section === 'coins' ? 'Coins' : section === 'coin-admin' ? 'Coins' : section === 'toolbox' ? 'Tool Box' : 'C2C Settings'

  return <div>
    <h2 style={{ margin: '0 0 6px' }}>{title}</h2>
    <p style={{ color: 'var(--text-muted)', margin: '0 0 20px' }}>{section === 'reminders' ? 'Track upcoming and completed customer reminders.' : 'Manage this CRM workspace from the available sections.'}</p>
    <div style={{ display: 'flex', gap: 20, alignItems: 'flex-start' }}>
      <div style={{ width: 220, background: '#fff', borderRadius: 16, padding: 12, boxShadow: 'var(--shadow-card)' }}>{tabs.map((item) => <button key={item} onClick={() => setTab(item)} style={{ display: 'block', width: '100%', textAlign: 'left', border: 0, borderRadius: 9, padding: '11px 12px', marginBottom: 4, background: tab === item ? 'var(--brand-gradient-soft)' : 'transparent', color: tab === item ? '#ec4899' : 'var(--text-main)', fontWeight: 600, cursor: 'pointer' }}>{item}</button>)}</div>
      <div style={{ flex: 1 }}>
        {section === 'reminders' ? <>
          {tab === 'Upcoming Reminder' && <form onSubmit={createReminder} style={{ background: '#fff', padding: 20, borderRadius: 14, boxShadow: 'var(--shadow-card)', marginBottom: 16 }}><h3 style={{ marginTop: 0 }}>Add Reminder</h3><div style={{ display: 'grid', gap: 10 }}><input required placeholder="Reminder title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} style={{ padding: 10, border: '1px solid var(--border-soft)', borderRadius: 8 }} /><input required type="datetime-local" value={form.due_at} onChange={(e) => setForm({ ...form, due_at: e.target.value })} style={{ padding: 10, border: '1px solid var(--border-soft)', borderRadius: 8 }} /><textarea placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} style={{ padding: 10, border: '1px solid var(--border-soft)', borderRadius: 8 }} /></div><button style={{ marginTop: 12, padding: '10px 18px', border: 0, borderRadius: 8, color: '#fff', background: 'var(--brand-gradient)', fontWeight: 700 }}>Save Reminder</button></form>}
          <div style={{ background: '#fff', borderRadius: 14, padding: 20, boxShadow: 'var(--shadow-card)' }}>{loading ? 'Loading...' : error ? <span style={{ color: '#e05252' }}>{error}</span> : items.length === 0 ? <span style={{ color: 'var(--text-muted)' }}>No reminders found.</span> : items.map((item) => <div key={item.id} style={{ padding: '12px 0', borderBottom: '1px solid var(--border-soft)' }}><strong>{item.title || item.name}</strong><div style={{ color: 'var(--text-muted)', fontSize: 12 }}>{item.due_at || item.reminder_date || ''}</div></div>)}</div>
        </> : <div style={{ background: '#fff', borderRadius: 14, padding: 24, boxShadow: 'var(--shadow-card)' }}><h3 style={{ marginTop: 0 }}>{tab}</h3><p style={{ color: 'var(--text-muted)' }}>{section === 'coins' || section === 'coin-admin' ? 'Inbound, outbound, SMS, email, fax, and common coin balances will be shown here.' : section === 'campaign-base' || tab === 'Campaign Base' ? 'Campaign base details, contacts, and lead fields can be managed here.' : 'Use this section to manage CRM configuration and operations.'}</p></div>}
      </div>
    </div>
  </div>
}
