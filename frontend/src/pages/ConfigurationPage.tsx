import { FormEvent, useEffect, useState } from 'react'
import { api } from '../services/api'

type ConfigKind = 'fields' | 'sources' | 'statuses' | 'categories' | 'sms-templates' | 'api-docs' | 'agents'

interface ConfigPageProps {
  kind: ConfigKind
}

interface Item {
  id?: string
  name?: string
  field_name?: string
  field_type?: string
  required?: boolean
  source_name?: string
  status_name?: string
  category_name?: string
  lead_type?: string
  template_name?: string
  username?: string
  full_name?: string
  role?: string
}

const definitions: Record<ConfigKind, { title: string; description: string; endpoint?: string; fields: { name: string; label: string; type?: string }[] }> = {
  fields: {
    title: 'Manage Fields', description: 'Create fields that appear on the lead form.', endpoint: '/fields/',
    fields: [{ name: 'field_name', label: 'Field Name' }, { name: 'field_type', label: 'Field Type', type: 'select' }, { name: 'required', label: 'Required', type: 'checkbox' }],
  },
  sources: {
    title: 'Add Source', description: 'Manage lead sources used by LMS lead forms.', endpoint: '/sources/',
    fields: [{ name: 'lead_type', label: 'Lead Type' }, { name: 'source_name', label: 'Source Name' }],
  },
  statuses: {
    title: 'Add Status', description: 'Manage lead statuses.', endpoint: '/statuses/',
    fields: [{ name: 'status_name', label: 'Status Name' }],
  },
  categories: {
    title: 'Add Category', description: 'Manage lead categories.', endpoint: '/categories/',
    fields: [{ name: 'lead_type', label: 'Lead Type' }, { name: 'category_name', label: 'Category Name' }],
  },
  'sms-templates': {
    title: 'SMS Templates', description: 'Create reusable SMS templates for customer communication.', endpoint: '/sms-templates/',
    fields: [{ name: 'template_name', label: 'Template Name' }, { name: 'content', label: 'Message Content', type: 'textarea' }],
  },
  agents: {
    title: 'Agents', description: 'Review agents and their current assignment status.', endpoint: '/agents/',
    fields: [],
  },
  'api-docs': {
    title: 'API Docs', description: 'Available CRM API endpoints for integrations.', endpoint: '/api-docs/',
    fields: [],
  },
}

export function ConfigurationPage({ kind }: ConfigPageProps) {
  const definition = definitions[kind]
  const [items, setItems] = useState<Item[]>([])
  const [form, setForm] = useState<Record<string, string | boolean>>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  function load() {
    if (!definition.endpoint) return
    setLoading(true)
    api.get(definition.endpoint)
      .then((res) => {
        const data = res.data
        setItems(Array.isArray(data) ? data : data.endpoints ? Object.entries(data.endpoints).flatMap(([group, endpoints]) => Object.entries(endpoints as Record<string, string>).map(([name, path]) => ({ id: `${group}-${name}`, name: `${group}: ${name}`, field_name: path }))) : [])
      })
      .catch(() => setError('Unable to load this section. Check the API and database migration.'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [definition.endpoint])

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!definition.endpoint) return
    setSaving(true)
    setError('')
    setMessage('')
    try {
      await api.post(definition.endpoint, form)
      setForm({})
      setMessage('Saved successfully.')
      load()
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Unable to save this item.')
    } finally {
      setSaving(false)
    }
  }

  const displayValue = (item: Item) => item.field_name || item.source_name || item.status_name || item.category_name || item.template_name || item.full_name || item.name || item.username || '-'

  return (
    <div>
      <h2 style={{ margin: '0 0 6px' }}>{definition.title}</h2>
      <p style={{ color: 'var(--text-muted)', margin: '0 0 20px' }}>{definition.description}</p>
      {definition.fields.length > 0 && (
        <form onSubmit={submit} style={{ background: '#fff', borderRadius: 14, padding: 20, boxShadow: 'var(--shadow-card)', marginBottom: 20 }}>
          <h3 style={{ margin: '0 0 14px' }}>Create New</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12 }}>
            {definition.fields.map((field) => (
              <label key={field.name} style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, color: 'var(--text-muted)' }}>
                {field.type === 'checkbox' ? (
                  <span><input type="checkbox" checked={Boolean(form[field.name])} onChange={(e) => setForm({ ...form, [field.name]: e.target.checked })} /> Required</span>
                ) : field.type === 'textarea' ? (
                  <><span>{field.label}</span><textarea required value={String(form[field.name] || '')} onChange={(e) => setForm({ ...form, [field.name]: e.target.value })} style={{ minHeight: 82, border: '1px solid var(--border-soft)', borderRadius: 8, padding: 10 }} /></>
                ) : field.type === 'select' ? (
                  <><span>{field.label}</span><select required value={String(form[field.name] || '')} onChange={(e) => setForm({ ...form, [field.name]: e.target.value })} style={{ padding: 10, border: '1px solid var(--border-soft)', borderRadius: 8 }}><option value="">Select type</option><option value="text">Text</option><option value="number">Number</option><option value="date">Date</option><option value="select">Select</option></select></>
                ) : (
                  <><span>{field.label}</span><input required value={String(form[field.name] || '')} onChange={(e) => setForm({ ...form, [field.name]: e.target.value })} style={{ padding: 10, border: '1px solid var(--border-soft)', borderRadius: 8 }} /></>
                )}
              </label>
            ))}
          </div>
          <button disabled={saving} style={{ marginTop: 16, padding: '10px 18px', border: 0, borderRadius: 8, color: '#fff', background: 'var(--brand-gradient)', fontWeight: 700 }}>{saving ? 'Saving...' : 'Save'}</button>
          {message && <span style={{ color: '#2fae65', marginLeft: 12, fontSize: 13 }}>{message}</span>}
        </form>
      )}
      {error && <div style={{ color: '#e05252', marginBottom: 12 }}>{error}</div>}
      <div style={{ background: '#fff', borderRadius: 14, padding: 20, boxShadow: 'var(--shadow-card)' }}>
        <h3 style={{ margin: '0 0 14px' }}>{kind === 'api-docs' ? 'Available Endpoints' : 'Existing Records'}</h3>
        {loading ? <div>Loading...</div> : items.length === 0 ? <div style={{ color: 'var(--text-muted)' }}>No records found.</div> : <div style={{ display: 'grid', gap: 8 }}>{items.map((item) => <div key={item.id || displayValue(item)} style={{ borderBottom: '1px solid var(--border-soft)', padding: '10px 0', display: 'flex', justifyContent: 'space-between' }}><strong>{displayValue(item)}</strong><span style={{ color: 'var(--text-muted)', fontSize: 12 }}>{item.field_type || item.role || item.field_name || ''}</span></div>)}</div>}
      </div>
    </div>
  )
}
