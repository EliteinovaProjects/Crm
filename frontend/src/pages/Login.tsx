import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { UserIcon, LockIcon, EyeIcon } from '../components/icons'

export function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loginType, setLoginType] = useState<'admin' | 'employee'>('admin')
  const [error, setError] = useState('')
  const [portalMismatch, setPortalMismatch] = useState<{ role: 'admin' | 'employee'; message: string } | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const { login, user } = useAuth()
  const navigate = useNavigate()

  if (user) {
    // Redirect based on the role returned by the backend.
    navigate(user.role === 'employee' ? '/employee/dashboard' : '/admin/dashboard', { replace: true })
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setPortalMismatch(null)
    setSubmitting(true)
    try {
      await login(username, password, loginType)
      // The redirect is based on the role returned by the backend.
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      if (detail?.code === 'wrong_portal') {
        setPortalMismatch({ role: detail.role === 'employee' ? 'employee' : 'admin', message: detail.message })
      } else {
        setError(typeof detail === 'string' ? detail : 'Invalid username or password')
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #f5e9fb 0%, #fbe7f1 100%)',
        padding: 24,
      }}
    >
      <div
        style={{
          display: 'flex',
          width: '100%',
          maxWidth: 920,
          minHeight: 560,
          background: '#fff',
          borderRadius: 28,
          overflow: 'hidden',
          boxShadow: '0 20px 60px rgba(150, 60, 160, 0.18)',
        }}
      >
        {/* Left branding panel */}
        <div
          style={{
            flex: 1,
            background:
              'radial-gradient(circle at 20% 20%, rgba(255,255,255,0.35), transparent 40%), linear-gradient(160deg, #f3c9e0 0%, #d9b7f0 45%, #c7a4ec 100%)',
            padding: '48px 40px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            position: 'relative',
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
              <div
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: 10,
                  background: 'var(--brand-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#fff',
                  fontWeight: 800,
                }}
              >
                E
              </div>
              <div>
                <div style={{ fontWeight: 800, fontSize: 20, letterSpacing: 0.5 }}>
                  ELITEINOVA <span style={{ color: '#ec4899' }}>CRM</span>
                </div>
                <div style={{ fontSize: 10, color: '#7a5f8f', letterSpacing: 1 }}>
                  CRM PORTAL
                </div>
              </div>
            </div>
          </div>

          <div>
            <h1 style={{ fontSize: 32, lineHeight: 1.2, color: '#3a2450', margin: '0 0 12px' }}>
              Better
              <br />
              Conversations
              <br />
              Brighter Business
            </h1>
          </div>

          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div
              style={{
                width: 140,
                height: 140,
                borderRadius: '50%',
                background: 'rgba(255,255,255,0.35)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 56,
              }}
            >
              🎧
            </div>
          </div>
        </div>

        {/* Right form panel */}
        <div style={{ flex: 1, padding: '48px 44px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h2 style={{ margin: '0 0 4px', fontSize: 24 }}>Hey, welcome!</h2>
          <p style={{ margin: '0 0 18px', color: 'var(--text-muted)', fontSize: 14 }}>
            Sign in to your {loginType === 'admin' ? 'Admin' : 'Employee'} account to continue
          </p>

          <div style={{ display: 'flex', gap: 8, marginBottom: 18, padding: 4, background: '#f8f4fc', borderRadius: 10 }}>
            {(['admin', 'employee'] as const).map((type) => (
              <button
                key={type}
                type="button"
                onClick={() => {
                  setLoginType(type)
                  setError('')
                  setUsername('')
                  setPassword('')
                }}
                style={{
                  flex: 1,
                  border: 'none',
                  borderRadius: 8,
                  padding: '9px 8px',
                  cursor: 'pointer',
                  fontWeight: 700,
                  fontSize: 13,
                  color: loginType === type ? '#fff' : '#6b5b7a',
                  background: loginType === type ? 'var(--brand-gradient)' : 'transparent',
                }}
              >
                {type === 'admin' ? 'Admin Login' : 'Employee Login'}
              </button>
            ))}
          </div>

          <div style={{ marginBottom: 20, padding: '12px', background: '#f8f4fc', borderRadius: 8, fontSize: 12, color: '#6b5b7a' }}>
            <strong>Access includes:</strong>
            <div style={{ marginTop: 4 }}>
              • LMS (Learning Management System)
              <br />
              • CMS (Context Management System)
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                border: '1px solid var(--border-soft)',
                borderRadius: 12,
                padding: '12px 14px',
                marginBottom: 14,
              }}
            >
              <UserIcon color="#c084c9" />
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                required
                style={{ border: 'none', outline: 'none', flex: 1, fontSize: 14 }}
              />
            </div>


            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                border: '1px solid var(--border-soft)',
                borderRadius: 12,
                padding: '12px 14px',
                marginBottom: 18,
              }}
            >
              <LockIcon color="#c084c9" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                style={{ border: 'none', outline: 'none', flex: 1, fontSize: 14 }}
              />
              <button
                type="button"
                onClick={() => setShowPassword((s) => !s)}
                style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#c084c9', padding: 0 }}
              >
                <EyeIcon />
              </button>
            </div>

            {error && <div style={{ color: '#e11d48', fontSize: 13, marginBottom: 14 }}>{error}</div>}

            <button
              type="submit"
              disabled={submitting}
              style={{
                width: '100%',
                padding: 14,
                border: 'none',
                borderRadius: 12,
                background: 'var(--brand-gradient)',
                color: '#fff',
                fontSize: 15,
                fontWeight: 600,
                cursor: submitting ? 'default' : 'pointer',
                opacity: submitting ? 0.8 : 1,
              }}
            >
              {submitting ? 'Please wait...' : 'Sign In'}
            </button>
          </form>
        </div>
      </div>

      {portalMismatch && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(15, 23, 42, 0.68)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 20, padding: 20 }}>
          <div role="dialog" aria-modal="true" style={{ width: '100%', maxWidth: 390, background: '#111a2e', color: '#fff', borderRadius: 16, borderTop: '4px solid #f59e0b', padding: 28, boxShadow: '0 24px 70px rgba(0,0,0,.35)', textAlign: 'center' }}>
            <div style={{ width: 58, height: 58, margin: '0 auto 16px', borderRadius: 16, background: 'rgba(245,158,11,.12)', display: 'grid', placeItems: 'center', fontSize: 30 }}>⚠</div>
            <h3 style={{ margin: '0 0 10px', fontSize: 20 }}>Wrong Login Portal</h3>
            <p style={{ margin: '0 auto 20px', color: '#cbd5e1', lineHeight: 1.6, fontSize: 13 }}>{portalMismatch.message}</p>
            <div style={{ textAlign: 'left', padding: 14, border: '1px solid rgba(245,158,11,.35)', borderRadius: 12, background: 'rgba(245,158,11,.08)', marginBottom: 16 }}><strong style={{ color: '#fbbf24', fontSize: 11 }}>RECOMMENDED</strong><div style={{ marginTop: 4, fontWeight: 700 }}>{portalMismatch.role === 'employee' ? 'Employee Login' : 'Admin Login'}</div></div>
            <button onClick={() => { setLoginType(portalMismatch.role); setPortalMismatch(null); setError('') }} style={{ width: '100%', padding: 12, border: 0, borderRadius: 10, background: '#d8890b', color: '#fff', fontWeight: 700, cursor: 'pointer', marginBottom: 8 }}>Switch to {portalMismatch.role === 'employee' ? 'Employee' : 'Admin'} Login</button>
            <button onClick={() => setPortalMismatch(null)} style={{ width: '100%', padding: 12, border: '1px solid #334155', borderRadius: 10, background: 'transparent', color: '#cbd5e1', fontWeight: 600, cursor: 'pointer' }}>Stay on Current Login</button>
          </div>
        </div>
      )}
    </div>
  )
}
