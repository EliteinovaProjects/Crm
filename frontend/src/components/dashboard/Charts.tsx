export function BarChartCard({ title, data }: { title: string; data: Record<string, number> }) {
  const entries = Object.entries(data || {})
  const max = Math.max(1, ...entries.map(([, v]) => v))

  return (
    <div style={{ background: '#fff', borderRadius: 16, padding: 20, boxShadow: 'var(--shadow-card)', flex: 2, minWidth: 280 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div style={{ fontWeight: 700, fontSize: 14 }}>{title}</div>
        <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Last 7 Days</div>
      </div>
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: 12,
          height: 150,
          borderBottom: '1px solid var(--border-soft)',
          paddingBottom: 4,
        }}
      >
        {entries.length === 0 && <div style={{ color: 'var(--text-muted)', fontSize: 13 }}>No data</div>}
        {entries.map(([label, value]) => (
          <div key={label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6, flex: 1 }}>
            <div
              style={{
                width: '60%',
                maxWidth: 28,
                height: Math.max(6, (value / max) * 130),
                borderRadius: 6,
                background: 'var(--brand-gradient)',
              }}
            />
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
        {entries.map(([label]) => (
          <div key={label} style={{ flex: 1, textAlign: 'center', fontSize: 11, color: 'var(--text-muted)' }}>
            {label}
          </div>
        ))}
      </div>
    </div>
  )
}

const donutColors = ['#ec4899', '#a855f7', '#f0924a', '#2fae65', '#4aa3f0', '#e0c33f']

export function DonutChartCard({ title, data }: { title: string; data: Record<string, number> }) {
  const entries = Object.entries(data || {})
  const total = entries.reduce((sum, [, v]) => sum + v, 0) || 1

  let cursor = 0
  const stops = entries.map(([label, value], i) => {
    const pct = (value / total) * 100
    const start = cursor
    cursor += pct
    return `${donutColors[i % donutColors.length]} ${start}% ${cursor}%`
  })

  return (
    <div style={{ background: '#fff', borderRadius: 16, padding: 20, boxShadow: 'var(--shadow-card)', flex: 1, minWidth: 220 }}>
      <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 16 }}>{title}</div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
        <div
          style={{
            width: 110,
            height: 110,
            borderRadius: '50%',
            background: entries.length ? `conic-gradient(${stops.join(',')})` : '#eee',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}
        >
          <div
            style={{
              width: 66,
              height: 66,
              borderRadius: '50%',
              background: '#fff',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <div style={{ fontWeight: 700, fontSize: 16 }}>{total}</div>
            <div style={{ fontSize: 9, color: 'var(--text-muted)' }}>Total</div>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {entries.map(([label, value], i) => (
            <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12 }}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: donutColors[i % donutColors.length],
                  display: 'inline-block',
                }}
              />
              {label} ({Math.round((value / total) * 100)}%)
            </div>
          ))}
          {entries.length === 0 && <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>No data</div>}
        </div>
      </div>
    </div>
  )
}
