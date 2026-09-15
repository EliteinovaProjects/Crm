import { useEffect, useMemo, useState } from 'react'
import { api } from '../../services/api'
import { StatCard } from '../../components/dashboard/StatCard'
import { BarChartCard, DonutChartCard } from '../../components/dashboard/Charts'
import { BreakdownTable } from '../../components/dashboard/BreakdownTable'
import { PhoneIcon, AgentsIcon } from '../../components/icons'

interface CallLogItem {
  id: string
  phone_number: string
  call_direction: 'inbound' | 'outbound' | string
  call_status: string
  duration?: number | null
  disposition?: string | null
  started_at?: string | null
  ended_at?: string | null
}

type Direction = 'incoming' | 'outgoing'

function formatDuration(seconds?: number | null) {
  if (!seconds) return '-'
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

export function LiveCalls() {
  const [calls, setCalls] = useState<CallLogItem[] | null>(null)
  const [error, setError] = useState('')
  const [direction, setDirection] = useState<Direction>('incoming')

  useEffect(() => {
    api
      .get<CallLogItem[]>('/calls/agent/me', { params: { limit: 200 } })
      .then((res) => setCalls(res.data))
      .catch(() => setError('Failed to load call activity'))
  }, [])

  const filtered = useMemo(() => {
    if (!calls) return []
    const wantDirection = direction === 'incoming' ? 'inbound' : 'outbound'
    return calls.filter((c) => (c.call_direction || 'outbound') === wantDirection)
  }, [calls, direction])

  const stats = useMemo(() => {
    const total = filtered.length
    const connectedWithAgent = filtered.filter((c) => c.call_status === 'ended' || c.call_status === 'connected').length
    const missedOnIvr = filtered.filter((c) => c.call_status === 'missed').length
    const missedOnAgent = filtered.filter((c) => c.call_status === 'failed').length
    return { total, connectedWithAgent, missedOnIvr, missedOnAgent }
  }, [filtered])

  const trafficByDay = useMemo(() => {
    const buckets: Record<string, number> = {}
    const now = new Date()
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now)
      d.setDate(d.getDate() - i)
      const label = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
      buckets[label] = 0
    }
    filtered.forEach((c) => {
      if (!c.started_at) return
      const label = new Date(c.started_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
      if (label in buckets) buckets[label] += 1
    })
    return buckets
  }, [filtered])

  const statusBreakdown = useMemo(() => {
    const buckets: Record<string, number> = {}
    filtered.forEach((c) => {
      const label = c.call_status.charAt(0).toUpperCase() + c.call_status.slice(1)
      buckets[label] = (buckets[label] || 0) + 1
    })
    return buckets
  }, [filtered])

  const tableRows = filtered
    .slice(0, 10)
    .map((c) => [
      c.phone_number,
      c.call_direction === 'inbound' ? 'Incoming' : 'Outgoing',
      c.call_status,
      formatDuration(c.duration),
      c.started_at ? new Date(c.started_at).toLocaleString() : '-',
      c.disposition || '-',
    ])

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20, flexWrap: 'wrap', gap: 12 }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: 20 }}>Live Calls</div>
          <div style={{ display: 'flex', gap: 4, marginTop: 10 }}>
            {(['incoming', 'outgoing'] as Direction[]).map((d) => (
              <button
                key={d}
                onClick={() => setDirection(d)}
                style={{
                  padding: '7px 18px',
                  borderRadius: 999,
                  border: 'none',
                  fontSize: 13,
                  fontWeight: 600,
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                  background: direction === d ? 'var(--brand-gradient)' : '#fff',
                  color: direction === d ? '#fff' : 'var(--text-muted)',
                  boxShadow: direction === d ? 'none' : 'var(--shadow-card)',
                }}
              >
                {d}
              </button>
            ))}
          </div>
        </div>
        <div
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
          }}
        >
          <PhoneIcon width={15} height={15} />
          Live Calls
          <span style={{ background: 'rgba(255,255,255,0.25)', padding: '1px 8px', borderRadius: 999 }}>
            {stats.total}
          </span>
          <span style={{ background: 'rgba(255,255,255,0.25)', padding: '1px 8px', borderRadius: 999 }}>
            {stats.connectedWithAgent}
          </span>
        </div>
      </div>

      {error && <div style={{ color: '#e11d48', marginBottom: 16 }}>{error}</div>}
      {!calls && !error && <div>Loading...</div>}

      {calls && (
        <>
          <div style={{ display: 'flex', gap: 16, marginBottom: 20, flexWrap: 'wrap' }}>
            <StatCard title="Total No Of Calls" value={stats.total} color="pink" icon={<PhoneIcon />} />
            <StatCard title="Connected With Agent" value={stats.connectedWithAgent} color="green" icon={<PhoneIcon />} />
            <StatCard title="Missed Calls on IVR" value={stats.missedOnIvr} color="orange" icon={<PhoneIcon />} />
            <StatCard title="Missed Calls on Agent" value={stats.missedOnAgent} color="purple" icon={<PhoneIcon />} />
            <StatCard title="Active In-Active Agents" value="NA" color="pink" icon={<AgentsIcon />} />
          </div>

          <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginBottom: 16 }}>
            <BarChartCard title="Event Wise Call Traffic" data={trafficByDay} />
            <DonutChartCard title="Call Status Breakdown" data={statusBreakdown} />
          </div>

          <BreakdownTable
            title={`Recent ${direction === 'incoming' ? 'Incoming' : 'Outgoing'} Calls`}
            columns={['Phone Number', 'Direction', 'Status', 'Duration', 'Started At', 'Disposition']}
            rows={tableRows}
          />
        </>
      )}
    </div>
  )
}