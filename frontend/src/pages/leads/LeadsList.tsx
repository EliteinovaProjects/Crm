import { useEffect, useState } from 'react'
import { api } from '../../services/api'
import { StatCard } from '../../components/dashboard/StatCard'
import { LeadsIcon, PhoneIcon, AgentsIcon } from '../../components/icons'

interface Lead {
  id: string
  account?: string
  name: string
  mobile_number: string
  email?: string
  status_id?: string
  source_id?: string
  category_id?: string
  follow_up_date?: string
  created_at: string
}

interface LeadListResponse {
  leads: Lead[]
  total: number
  page: number
  page_size: number
}

const statusColors: Record<string, { bg: string; fg: string }> = {
  Fresh: { bg: '#fde3ef', fg: '#ec4899' },
  'Follow Up': { bg: '#fdeadd', fg: '#f0924a' },
  Missed: { bg: '#fde0e0', fg: '#e05252' },
  Active: { bg: '#e1f6ea', fg: '#2fae65' },
}

function StatusBadge({ label }: { label: string }) {
  const c = statusColors[label] || { bg: '#f1f1f6', fg: '#6b6b83' }
  return (
    <span
      style={{
        background: c.bg,
        color: c.fg,
        padding: '3px 12px',
        borderRadius: 999,
        fontSize: 12,
        fontWeight: 600,
      }}
    >
      {label}
    </span>
  )
}

export function LeadsList() {
  const [data, setData] = useState<LeadListResponse | null>(null)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState<string[]>([])
  const [source, setSource] = useState('')
  const [status, setStatus] = useState('')

  function load() {
    api
      .get<LeadListResponse>('/leads/')
      .then((res) => setData(res.data))
      .catch(() => setError('Failed to load leads'))
  }

  useEffect(load, [])

  function toggleSelect(id: string) {
    setSelected((prev) => (prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]))
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: 20 }}>Leads & Logs</div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: 10, border: '1px solid var(--border-soft)', fontSize: 13 }}
          >
            <option value="">Source</option>
          </select>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: 10, border: '1px solid var(--border-soft)', fontSize: 13 }}
          >
            <option value="">Status</option>
          </select>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              padding: '8px 14px',
              borderRadius: 10,
              border: '1px solid var(--border-soft)',
              fontSize: 13,
              color: 'var(--text-muted)',
            }}
          >
            Total Leads: {data?.total ?? 0}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
        <StatCard title="Total Leads" value={data?.total ?? 0} color="pink" icon={<LeadsIcon />} />
        <StatCard title="Follow-Ups" value={0} color="purple" icon={<PhoneIcon />} />
        <StatCard title="Missed Follow-Ups" value={0} color="orange" icon={<PhoneIcon />} />
        <StatCard title="Active In-Active Agents" value="NA" color="green" icon={<AgentsIcon />} />
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginBottom: 12 }}>
        <button
          disabled={selected.length === 0}
          style={{
            padding: '8px 16px',
            borderRadius: 8,
            border: '1px solid var(--border-soft)',
            background: '#fff',
            fontSize: 13,
            cursor: selected.length ? 'pointer' : 'default',
          }}
        >
          Assign
        </button>
        <button
          disabled={selected.length === 0}
          style={{
            padding: '8px 16px',
            borderRadius: 8,
            border: '1px solid var(--border-soft)',
            background: '#fff',
            fontSize: 13,
            cursor: selected.length ? 'pointer' : 'default',
          }}
        >
          Bulk Update
        </button>
        <button
          disabled={selected.length === 0}
          style={{
            padding: '8px 16px',
            borderRadius: 8,
            border: '1px solid var(--border-soft)',
            background: '#fff',
            fontSize: 13,
            cursor: selected.length ? 'pointer' : 'default',
          }}
        >
          Delete
        </button>
        <button
          style={{
            padding: '8px 16px',
            borderRadius: 8,
            border: 'none',
            background: 'var(--brand-gradient)',
            color: '#fff',
            fontSize: 13,
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Download Excel
        </button>
      </div>

      {error && <div style={{ color: '#e11d48' }}>{error}</div>}
      {!data && !error && <div>Loading...</div>}
      {data && (
        <div style={{ background: '#fff', borderRadius: 16, overflow: 'hidden', boxShadow: 'var(--shadow-card)' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13.5 }}>
            <thead>
              <tr>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7' }}></th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>S No.</th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>Lead Source</th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>Mobile/Name</th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>Account</th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>Action</th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>Followup Date</th>
                <th style={{ padding: '12px 14px', background: 'var(--brand-gradient-soft)', color: '#a855f7', textAlign: 'left' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {data.leads.map((lead, i) => (
                <tr key={lead.id} style={{ borderTop: '1px solid var(--border-soft)' }}>
                  <td style={{ padding: '12px 14px' }}>
                    <input
                      type="checkbox"
                      checked={selected.includes(lead.id)}
                      onChange={() => toggleSelect(lead.id)}
                    />
                  </td>
                  <td style={{ padding: '12px 14px' }}>{i + 1}</td>
                  <td style={{ padding: '12px 14px' }}>{lead.source_id || '-'}</td>
                  <td style={{ padding: '12px 14px' }}>
                    <div style={{ fontWeight: 600 }}>{lead.mobile_number}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: 12 }}>{lead.name}</div>
                  </td>
                  <td style={{ padding: '12px 14px' }}>{lead.account || '-'}</td>
                  <td style={{ padding: '12px 14px' }}>
                    <div style={{ display: 'flex', gap: 10, color: '#ec4899' }}>
                      <PhoneIcon width={16} height={16} />
                      📱
                    </div>
                  </td>
                  <td style={{ padding: '12px 14px' }}>
                    {lead.follow_up_date ? new Date(lead.follow_up_date).toLocaleDateString() : 'Set Followup'}
                  </td>
                  <td style={{ padding: '12px 14px' }}>
                    <StatusBadge label="Fresh" />
                  </td>
                </tr>
              ))}
              {data.leads.length === 0 && (
                <tr>
                  <td colSpan={7} style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
                    No leads found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
