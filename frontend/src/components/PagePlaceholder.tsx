export function PagePlaceholder({ title }: { title: string }) {
  return (
    <div style={{ background: '#fff', borderRadius: 16, padding: 32, boxShadow: 'var(--shadow-card)' }}>
      <h3 style={{ margin: '0 0 8px' }}>{title}</h3>
      <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: 13.5 }}>This section is not yet implemented.</p>
    </div>
  )
}
