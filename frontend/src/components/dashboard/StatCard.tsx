import { ReactNode } from 'react'

const palettes: Record<string, { bg: string; fg: string }> = {
  pink: { bg: '#fde3ef', fg: '#ec4899' },
  purple: { bg: '#ede3fb', fg: '#a855f7' },
  orange: { bg: '#fdeadd', fg: '#f0924a' },
  green: { bg: '#e1f6ea', fg: '#2fae65' },
}

export function StatCard({
  title,
  value,
  delta,
  color = 'pink',
  icon,
}: {
  title: string
  value: number | string
  delta?: string
  color?: keyof typeof palettes
  icon: ReactNode
}) {
  const p = palettes[color]
  return (
    <div
      style={{
        background: '#fff',
        borderRadius: 16,
        padding: 18,
        flex: 1,
        minWidth: 190,
        boxShadow: 'var(--shadow-card)',
        display: 'flex',
        alignItems: 'center',
        gap: 14,
      }}
    >
      <div
        style={{
          width: 44,
          height: 44,
          borderRadius: 12,
          background: p.bg,
          color: p.fg,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}
      >
        {icon}
      </div>
      <div>
        <div style={{ fontSize: 12.5, color: 'var(--text-muted)' }}>{title}</div>
        <div style={{ fontSize: 22, fontWeight: 700 }}>{value}</div>
        {delta && <div style={{ fontSize: 11, color: '#2fae65' }}>▲ {delta} vs last month</div>}
      </div>
    </div>
  )
}
