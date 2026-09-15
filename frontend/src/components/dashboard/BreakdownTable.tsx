export function BreakdownTable({
  title,
  columns,
  rows,
}: {
  title: string
  columns: string[]
  rows: (string | number)[][]
}) {
  return (
    <div style={{ background: '#fff', borderRadius: 16, padding: 20, boxShadow: 'var(--shadow-card)' }}>
      <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 14 }}>{title}</div>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
        <thead>
          <tr>
            {columns.map((c) => (
              <th
                key={c}
                style={{
                  textAlign: 'left',
                  padding: '8px 10px',
                  background: 'var(--brand-gradient-soft)',
                  color: '#a855f7',
                  fontWeight: 600,
                }}
              >
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} style={{ borderBottom: '1px solid var(--border-soft)' }}>
              {row.map((cell, j) => (
                <td key={j} style={{ padding: '8px 10px' }}>
                  {cell}
                </td>
              ))}
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={columns.length} style={{ padding: 16, textAlign: 'center', color: 'var(--text-muted)' }}>
                No data available.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
