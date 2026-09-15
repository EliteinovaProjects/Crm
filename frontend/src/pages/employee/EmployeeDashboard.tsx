import { useEffect, useState } from 'react'
import { api } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'
import { StatCard } from '../../components/dashboard/StatCard'
import { BarChartCard, DonutChartCard } from '../../components/dashboard/Charts'
import { BreakdownTable } from '../../components/dashboard/BreakdownTable'
import { PhoneIcon } from '../../components/icons'

interface EmployeeStats {
  total_leads: number
  my_leads: number
  status_wise_leads: Record<string, number>
  source_wise_leads: Record<string, number>
  category_wise_leads: Record<string, number>
  today_followups: any[]
  recent_calls: any[]
}

export function EmployeeDashboard() {
  const [stats, setStats] = useState<EmployeeStats | null>(null)
  const [error, setError] = useState('')
  const [tab, setTab] = useState<'incoming' | 'outgoing'>('incoming')
  const { user } = useAuth()

  useEffect(() => {
    api
      .get<EmployeeStats>('/employee/dashboard/stats')
      .then((res) => setStats(res.data))
      .catch(() => setError('Failed to load dashboard stats'))
  }, [])

  if (error) return <div style={{ color: '#e11d48' }}>{error}</div>
  if (!stats) return <div>Loading...</div>

  const sourceStatusRows = Object.entries(stats.source_wise_leads).map(([source, count]) => [source, count])

  return (
    <div>
      <div style={{ marginBottom: 20, display: 'flex', alignItems: 'center', gap: 24 }}>
        <div style={{ fontWeight: 700, fontSize: 20 }}>Dashboard</div>
        <div style={{ display: 'flex', gap: 20, fontSize: 13 }}>
          {(['incoming', 'outgoing'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                background: 'none',
                border: 'none',
                padding: '4px 0',
                cursor: 'pointer',
                fontWeight: 600,
                color: tab === t ? '#ec4899' : 'var(--text-muted)',
                borderBottom: tab === t ? '2px solid #ec4899' : '2px solid transparent',
                textTransform: 'capitalize',
              }}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
        <StatCard title="Total No Of Calls" value={0} color="pink" icon={<PhoneIcon />} />
        <StatCard title="Connected With Agent" value={0} color="purple" icon={<PhoneIcon />} />
        <StatCard title="Missed Calls on IVR" value={0} color="orange" icon={<PhoneIcon />} />
        <StatCard title="Missed Calls on Agent" value={0} color="green" icon={<PhoneIcon />} />
        <StatCard title="Active In-Active Agents" value="NA" color="pink" icon={<PhoneIcon />} />
      </div>

      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginBottom: 16 }}>
        <BarChartCard title="Event Wise Call Traffic" data={stats.status_wise_leads} />
        <DonutChartCard title="Agent Wise Leads Allocation" data={{ [user?.full_name || user?.username || 'Me']: stats.my_leads }} />
      </div>

      <BreakdownTable title="Source/Status Leads" columns={['Lead Source', 'Fresh']} rows={sourceStatusRows} />
    </div>
  )
}
