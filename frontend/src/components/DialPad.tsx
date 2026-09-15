import { useState } from 'react'
import { api } from '../services/api'
import { PhoneIcon } from './icons'

const KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']

type Tab = 'keypad' | 'settings'
type CallState = 'idle' | 'calling' | 'connected'

export function DialPad() {
  const [open, setOpen] = useState(false)
  const [tab, setTab] = useState<Tab>('keypad')
  const [number, setNumber] = useState('')
  const [callId, setCallId] = useState<string | null>(null)
  const [callState, setCallState] = useState<CallState>('idle')
  const [error, setError] = useState('')

  const [status, setStatus] = useState('available')
  const [mode, setMode] = useState('manual')
  const [readyForCampaign, setReadyForCampaign] = useState(false)
  const [permission] = useState('Inbound + Outbound')
  const [savingSettings, setSavingSettings] = useState(false)
  const [settingsSaved, setSettingsSaved] = useState(false)

  function press(key: string) {
    if (callState !== 'idle') return
    setNumber((n) => n + key)
  }

  function backspace() {
    if (callState !== 'idle') return
    setNumber((n) => n.slice(0, -1))
  }

  async function startCall() {
    if (!number) return
    setError('')
    setCallState('calling')
    try {
      const res = await api.post('/calls/initiate', null, { params: { phone_number: number } })
      setCallId(res.data.call_id)
      setCallState('connected')
    } catch {
      setError('Could not place the call.')
      setCallState('idle')
    }
  }

  async function endCall() {
    if (callId) {
      try {
        await api.put(`/calls/${callId}/end`)
      } catch {
        // ignore - still reset the UI
      }
    }
    setCallId(null)
    setCallState('idle')
    setNumber('')
  }

  async function saveSettings() {
    setSavingSettings(true)
    setSettingsSaved(false)
    try {
      await api.put('/calls/agent/status', null, { params: { status, mode } })
      await api.put('/calls/agent/campaign-ready', null, { params: { ready: readyForCampaign } })
      setSettingsSaved(true)
    } catch {
      setError('Could not save settings.')
    } finally {
      setSavingSettings(false)
    }
  }

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        aria-label="Open dial pad"
        style={{
          position: 'fixed',
          left: 24,
          bottom: 24,
          width: 54,
          height: 54,
          borderRadius: '50%',
          border: 'none',
          background: 'var(--brand-gradient)',
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 8px 20px rgba(168, 85, 247, 0.35)',
          cursor: 'pointer',
          zIndex: 40,
        }}
      >
        <PhoneIcon width={22} height={22} />
      </button>

      {open && (
        <div
          onClick={() => setOpen(false)}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(31, 32, 51, 0.35)',
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'flex-start',
            padding: 24,
            zIndex: 50,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: 300,
              background: '#fff',
              borderRadius: 20,
              boxShadow: 'var(--shadow-card)',
              overflow: 'hidden',
            }}
          >
            <div style={{ display: 'flex', background: 'var(--brand-gradient-soft)' }}>
              <button
                onClick={() => setTab('keypad')}
                style={{
                  flex: 1,
                  padding: '12px 0',
                  border: 'none',
                  background: tab === 'keypad' ? 'var(--brand-gradient)' : 'transparent',
                  color: tab === 'keypad' ? '#fff' : '#a855f7',
                  fontWeight: 700,
                  fontSize: 13,
                  cursor: 'pointer',
                }}
              >
                Dial Pad
              </button>
              <button
                onClick={() => setTab('settings')}
                style={{
                  flex: 1,
                  padding: '12px 0',
                  border: 'none',
                  background: tab === 'settings' ? 'var(--brand-gradient)' : 'transparent',
                  color: tab === 'settings' ? '#fff' : '#a855f7',
                  fontWeight: 700,
                  fontSize: 13,
                  cursor: 'pointer',
                }}
              >
                Settings
              </button>
            </div>

            {tab === 'keypad' && (
              <div style={{ padding: 20 }}>
                <div
                  style={{
                    textAlign: 'center',
                    fontSize: 22,
                    fontWeight: 700,
                    minHeight: 30,
                    marginBottom: 16,
                    letterSpacing: 1,
                  }}
                >
                  {number || <span style={{ color: 'var(--text-muted)', fontSize: 14, fontWeight: 400 }}>Enter number</span>}
                </div>

                {callState === 'connected' && (
                  <div style={{ textAlign: 'center', color: '#2fae65', fontSize: 12.5, marginBottom: 10, fontWeight: 600 }}>
                    ● Connected
                  </div>
                )}
                {callState === 'calling' && (
                  <div style={{ textAlign: 'center', color: '#a855f7', fontSize: 12.5, marginBottom: 10, fontWeight: 600 }}>
                    Calling…
                  </div>
                )}

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, marginBottom: 16 }}>
                  {KEYS.map((k) => (
                    <button
                      key={k}
                      onClick={() => press(k)}
                      disabled={callState !== 'idle'}
                      style={{
                        padding: '14px 0',
                        borderRadius: 12,
                        border: '1px solid var(--border-soft)',
                        background: '#fff',
                        fontSize: 16,
                        fontWeight: 600,
                        cursor: callState === 'idle' ? 'pointer' : 'default',
                        color: 'var(--text-main)',
                      }}
                    >
                      {k}
                    </button>
                  ))}
                </div>

                {error && <div style={{ color: '#e05252', fontSize: 12, marginBottom: 10, textAlign: 'center' }}>{error}</div>}

                <div style={{ display: 'flex', gap: 10 }}>
                  {callState === 'idle' && (
                    <>
                      <button
                        onClick={backspace}
                        disabled={!number}
                        style={{
                          flex: 1,
                          padding: '10px 0',
                          borderRadius: 10,
                          border: '1px solid var(--border-soft)',
                          background: '#fff',
                          fontSize: 13,
                          cursor: number ? 'pointer' : 'default',
                          color: 'var(--text-muted)',
                        }}
                      >
                        ⌫ Clear
                      </button>
                      <button
                        onClick={startCall}
                        disabled={!number}
                        style={{
                          flex: 1,
                          padding: '10px 0',
                          borderRadius: 10,
                          border: 'none',
                          background: 'var(--brand-gradient)',
                          color: '#fff',
                          fontSize: 13,
                          fontWeight: 700,
                          cursor: number ? 'pointer' : 'default',
                        }}
                      >
                        📞 Call
                      </button>
                    </>
                  )}
                  {callState !== 'idle' && (
                    <button
                      onClick={endCall}
                      style={{
                        flex: 1,
                        padding: '10px 0',
                        borderRadius: 10,
                        border: 'none',
                        background: '#e05252',
                        color: '#fff',
                        fontSize: 13,
                        fontWeight: 700,
                        cursor: 'pointer',
                      }}
                    >
                      Hang Up
                    </button>
                  )}
                </div>
              </div>
            )}

            {tab === 'settings' && (
              <div style={{ padding: 20, display: 'flex', flexDirection: 'column', gap: 14 }}>
                <label style={{ fontSize: 12.5, color: 'var(--text-muted)', fontWeight: 600 }}>
                  Status
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    style={{
                      display: 'block',
                      width: '100%',
                      marginTop: 6,
                      padding: '9px 10px',
                      borderRadius: 10,
                      border: '1px solid var(--border-soft)',
                      fontSize: 13,
                      color: 'var(--text-main)',
                    }}
                  >
                    <option value="available">Available</option>
                    <option value="busy">Busy</option>
                    <option value="offline">Offline</option>
                  </select>
                </label>

                <label style={{ fontSize: 12.5, color: 'var(--text-muted)', fontWeight: 600 }}>
                  Mode
                  <select
                    value={mode}
                    onChange={(e) => setMode(e.target.value)}
                    style={{
                      display: 'block',
                      width: '100%',
                      marginTop: 6,
                      padding: '9px 10px',
                      borderRadius: 10,
                      border: '1px solid var(--border-soft)',
                      fontSize: 13,
                      color: 'var(--text-main)',
                    }}
                  >
                    <option value="manual">Manual</option>
                    <option value="auto">Auto</option>
                  </select>
                </label>

                <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, fontWeight: 600 }}>
                  <input
                    type="checkbox"
                    checked={readyForCampaign}
                    onChange={(e) => setReadyForCampaign(e.target.checked)}
                  />
                  Ready For Campaign Calls
                </label>

                <div style={{ fontSize: 12.5, color: 'var(--text-muted)' }}>
                  Permission: <span style={{ color: 'var(--text-main)', fontWeight: 600 }}>{permission}</span>
                </div>

                {error && <div style={{ color: '#e05252', fontSize: 12 }}>{error}</div>}
                {settingsSaved && <div style={{ color: '#2fae65', fontSize: 12 }}>Settings saved.</div>}

                <button
                  onClick={saveSettings}
                  disabled={savingSettings}
                  style={{
                    padding: '10px 0',
                    borderRadius: 10,
                    border: 'none',
                    background: 'var(--brand-gradient)',
                    color: '#fff',
                    fontSize: 13,
                    fontWeight: 700,
                    cursor: 'pointer',
                  }}
                >
                  {savingSettings ? 'Saving…' : 'Save Settings'}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}