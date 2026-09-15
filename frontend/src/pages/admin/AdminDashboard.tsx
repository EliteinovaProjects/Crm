import { useEffect, useState } from 'react'
import { api } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'
import { StatCard } from '../../components/dashboard/StatCard'
import { BarChartCard, DonutChartCard } from '../../components/dashboard/Charts'
import { BreakdownTable } from '../../components/dashboard/BreakdownTable'
import { LeadsIcon, PhoneIcon, AgentsIcon } from '../../components/icons'

interface DashboardStats {
  total_leads: number
  agent_wise_leads: Record<string, number>
  status_wise_leads: Record<string, number>
  source_wise_leads: Record<string, number>
  category_wise_leads: Record<string, number>
  recent_leads: any[]
  upcoming_followups: any[]
}

export function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [error, setError] = useState('')
  const { user } = useAuth()

  useEffect(() => {
    api
      .get<DashboardStats>('/admin/dashboard/stats')
      .then((res) => setStats(res.data))
      .catch(() => setError('Failed to load dashboard stats'))
  }, [])

  if (error) return <div style={{ color: '#e11d48' }}>{error}</div>
  if (!stats) return <div>Loading...</div>

  const sourceStatusRows = Object.entries(stats.source_wise_leads).map(([source, count]) => [
    source,
    count,
    stats.status_wise_leads['Follow Up'] ?? 0,
    stats.status_wise_leads['Missed'] ?? 0,
    stats.status_wise_leads['Active'] ?? 0,
  ])

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <div style={{ fontWeight: 700, fontSize: 20 }}>LMS Dashboard</div>
        <div style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          Good afternoon, {user?.full_name || user?.username} 👋
        </div>
      </div>

      <div style={{ display: 'flex', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
        <StatCard title="Total Leads" value={stats.total_leads} color="pink" icon={<LeadsIcon />} />
        <StatCard title="Total Calls" value={0} color="purple" icon={<PhoneIcon />} />
        <StatCard title="Missed Calls" value={0} color="orange" icon={<PhoneIcon />} />
        <StatCard
          title="Active Agents"
          value={Object.keys(stats.agent_wise_leads).length}
          color="green"
          icon={<AgentsIcon />}
        />
      </div>

      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginBottom: 16 }}>
        <BarChartCard title="Total Leads" data={stats.status_wise_leads} />
        <DonutChartCard title="Agent Wise Leads Allocation" data={stats.agent_wise_leads} />
      </div>

      <BreakdownTable
        title="Source/Status Leads"
        columns={['Lead Source', 'Fresh', 'Follow Up', 'Missed', 'Active']}
        rows={sourceStatusRows}
      />
    </div>
  )
}
