import { useEffect, useMemo, useState } from 'react'
import {
  createClaim,
  decideVerification,
  fetchReport,
  getClaims,
  getInbox,
  login,
  register,
  requestVerification,
} from './api'
import { getAuditLogs, getDisputes, getOrgs, verifyOrg, decideDispute } from './adminApi'
import type { Claim, Role, OrgRecord, Dispute, AuditEntry } from './types'
import './App.css'

const defaultClaim = {
  title: '',
  claim_type: 'volunteering',
  organization_name: '',
  supervisor_name: '',
  supervisor_contact: '',
  start_date: '',
  end_date: '',
  description: '',
  skill_tags: '',
}

function App() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'))
  const [role, setRole] = useState<Role>(() => (localStorage.getItem('role') as Role) || 'candidate')
  const [claims, setClaims] = useState<Claim[]>([])
  const [inbox, setInbox] = useState<Claim[]>([])
  const [reportId, setReportId] = useState('')
  const [report, setReport] = useState<Claim | null>(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [showAuthOverlay, setShowAuthOverlay] = useState(!localStorage.getItem('access_token'))
  const [adminOrgs, setAdminOrgs] = useState<OrgRecord[]>([])
  const [adminDisputes, setAdminDisputes] = useState<Dispute[]>([])
  const [adminAudits, setAdminAudits] = useState<AuditEntry[]>([])

  const [loginEmail, setLoginEmail] = useState('')
  const [loginPassword, setLoginPassword] = useState('')
  const [registerForm, setRegisterForm] = useState({
    email: '',
    password: '',
    full_name: '',
    role: 'candidate' as Role,
  })

  const [claimForm, setClaimForm] = useState(defaultClaim)

  const isAuthed = useMemo(() => Boolean(token), [token])

  useEffect(() => {
    if (!token) return
    if (role === 'candidate') {
      getClaims(token)
        .then(setClaims)
        .catch((err) => setMessage(err.message || 'Failed to load claims'))
    }
    if (role === 'verifier') {
      getInbox(token)
        .then(setInbox)
        .catch((err) => setMessage(err.message || 'Failed to load inbox'))
    }
    if (role === 'admin') {
      Promise.all([getOrgs(token), getDisputes(token), getAuditLogs(token)])
        .then(([orgs, disputes, audits]) => {
          setAdminOrgs(orgs)
          setAdminDisputes(disputes)
          setAdminAudits(audits)
        })
        .catch((err) => setMessage(err.message || 'Failed to load admin data'))
    }
  }, [token, role])

  const handleLogin = async () => {
    try {
      setLoading(true)
      const res = await login(loginEmail, loginPassword)
      localStorage.setItem('access_token', res.access_token)
      localStorage.setItem('role', res.role)
      setRole(res.role as Role)
      setToken(res.access_token)
      setMessage(`Logged in as ${res.role}`)
      setShowAuthOverlay(false)
    } catch (err: any) {
      setMessage(err.message || 'Login failed. Check email, password, and role.')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async () => {
    try {
      setLoading(true)
      await register(registerForm)
      setMessage('Registered. Now login.')
    } catch (err: any) {
      setMessage(err.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateClaim = async () => {
    if (!token) return setMessage('Login first')
    try {
      setLoading(true)
      const payload = {
        ...claimForm,
        skill_tags: claimForm.skill_tags
          ? claimForm.skill_tags.split(',').map((s) => s.trim()).filter(Boolean)
          : [],
      }
      await createClaim(token, payload)
      const refreshed = await getClaims(token)
      setClaims(refreshed)
      setClaimForm(defaultClaim)
      setMessage('Claim created')
    } catch (err: any) {
      setMessage(err.message || 'Create claim failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRequestVerification = async (id: string) => {
    if (!token) return
    try {
      await requestVerification(token, id)
      const refreshed = await getClaims(token)
      setClaims(refreshed)
      setMessage('Verification requested')
    } catch (err: any) {
      setMessage(err.message || 'Request failed')
    }
  }

  const handleDecision = async (id: string, outcome: 'approved' | 'rejected') => {
    if (!token) return
    try {
      await decideVerification(token, id, { outcome })
      const refreshed = await getInbox(token)
      setInbox(refreshed)
      setMessage(`Claim ${outcome}`)
    } catch (err: any) {
      setMessage(err.message || 'Decision failed')
    }
  }

  const handleAdminReview = async (orgId: string, currentStatus: OrgRecord['status']) => {
    if (!token) return
    const nextStatus = currentStatus === 'verified' ? 'pending' : 'verified'
    try {
      await verifyOrg(token, orgId, nextStatus)
      const refreshed = await getOrgs(token)
      setAdminOrgs(refreshed)
      setMessage(`Org status updated to ${nextStatus}`)
    } catch (err: any) {
      setMessage(err.message || 'Org update failed')
    }
  }

  const handleAdminDispute = async (id: string, status: 'resolved' | 'dismissed') => {
    if (!token) return
    try {
      await decideDispute(token, id, status, 'Reviewed by admin')
      const refreshed = await getDisputes(token)
      setAdminDisputes(refreshed)
      setMessage(`Dispute ${id} marked ${status}`)
    } catch (err: any) {
      setMessage(err.message || 'Dispute update failed')
    }
  }

  const handleFetchReport = async () => {
    try {
      setLoading(true)
      const data = await fetchReport(token, reportId)
      setReport(data)
      setMessage('')
    } catch (err: any) {
      setMessage(err.message || 'Report not found')
      setReport(null)
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('role')
    setToken(null)
    setClaims([])
    setInbox([])
    setReport(null)
    setShowAuthOverlay(true)
  }

  if (showAuthOverlay) {
    return (
      <div className="overlay">
        <div className="overlay-card">
          <div>
            <div className="badge">VerifyLK</div>
            <h1>Sign in to continue</h1>
            <p className="muted">Use your role to access the dashboard. Accounts persist on this device until you log out.</p>
            {message && <div className="flash">{message}</div>}
          </div>

          <div className="form-grid">
            <label className="field">
              <span>Email</span>
              <input value={loginEmail} onChange={(e) => setLoginEmail(e.target.value)} placeholder="you@example.com" />
            </label>
            <label className="field">
              <span>Password</span>
              <input type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} placeholder="••••••••" />
            </label>
            <label className="field">
              <span>Role</span>
              <select value={role} onChange={(e) => setRole(e.target.value as Role)}>
                <option value="candidate">Candidate</option>
                <option value="verifier">Verifier</option>
                <option value="employer">Employer</option>
                <option value="admin">Admin</option>
              </select>
            </label>
          </div>
          <div className="cta-row">
            <button className="cta primary" onClick={handleLogin} disabled={loading}>Login</button>
          </div>

          <hr className="divider" />

          <div>
            <h3>Create account</h3>
            <div className="form-grid">
              <label className="field">
                <span>Full name</span>
                <input value={registerForm.full_name} onChange={(e) => setRegisterForm({ ...registerForm, full_name: e.target.value })} />
              </label>
              <label className="field">
                <span>Email</span>
                <input value={registerForm.email} onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })} />
              </label>
              <label className="field">
                <span>Password</span>
                <input type="password" value={registerForm.password} onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })} />
              </label>
              <label className="field">
                <span>Role</span>
                <select value={registerForm.role} onChange={(e) => setRegisterForm({ ...registerForm, role: e.target.value as Role })}>
                  <option value="candidate">Candidate</option>
                  <option value="verifier">Verifier</option>
                  <option value="employer">Employer</option>
                </select>
              </label>
            </div>
            <div className="cta-row">
              <button className="cta ghost" onClick={handleRegister} disabled={loading}>Register</button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <header className="hero">
        <div>
          <div className="badge">Sri Lanka · VerifyLK</div>
          <h1>Proof of experience with one launch command.</h1>
          <p>
            Start the stack with <code>./start.ps1</code>, register, login, create claims, request verification, and share reports—all from this UI.
          </p>
          <div className="cta-row">
            <button className="cta primary" onClick={logout}>Logout</button>
            <span className="cta-note">Logged in as {role}</span>
          </div>
          {message && <div className="flash">{message}</div>}
        </div>
        <div className="card report">
          <div className="report-header">
            <div>
              <p className="eyebrow">Auth & Roles</p>
              <h2>{isAuthed ? `Logged in as ${role}` : 'Not logged in'}</h2>
              <p className="muted">Tokens are stored locally while this tab is open.</p>
            </div>
            <div className="score">
              <span>Status</span>
              <strong>{isAuthed ? 'Live' : 'Offline'}</strong>
            </div>
          </div>
          <div className="form-grid">
            <label className="field">
              <span>Email</span>
              <input value={loginEmail} onChange={(e) => setLoginEmail(e.target.value)} placeholder="you@example.com" />
            </label>
            <label className="field">
              <span>Password</span>
              <input type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} placeholder="••••••••" />
            </label>
            <label className="field">
              <span>Role</span>
              <select value={role} onChange={(e) => setRole(e.target.value as Role)}>
                <option value="candidate">Candidate</option>
                <option value="verifier">Verifier</option>
                <option value="employer">Employer</option>
                <option value="admin">Admin</option>
              </select>
            </label>
            <div className="auth-actions">
              <button className="cta tiny ghost" onClick={logout}>Logout</button>
            </div>
          </div>
        </div>
      </header>

      <section className="grid">
        {role === 'candidate' && (
          <div className="panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">Candidate</p>
                <h3>Create experience claim</h3>
              </div>
              <button className="cta small ghost" onClick={() => setClaimForm(defaultClaim)}>Reset</button>
            </div>
            <div className="form-grid">
              <label className="field">
                <span>Title</span>
                <input value={claimForm.title} onChange={(e) => setClaimForm({ ...claimForm, title: e.target.value })} />
              </label>
              <label className="field">
                <span>Type</span>
                <select value={claimForm.claim_type} onChange={(e) => setClaimForm({ ...claimForm, claim_type: e.target.value })}>
                  <option value="volunteering">Volunteering</option>
                  <option value="internship">Internship</option>
                  <option value="apprenticeship">Apprenticeship</option>
                  <option value="informal">Informal</option>
                  <option value="freelance">Freelance</option>
                  <option value="training">Training</option>
                </select>
              </label>
              <label className="field">
                <span>Organization</span>
                <input value={claimForm.organization_name} onChange={(e) => setClaimForm({ ...claimForm, organization_name: e.target.value })} />
              </label>
              <label className="field">
                <span>Supervisor</span>
                <input value={claimForm.supervisor_name} onChange={(e) => setClaimForm({ ...claimForm, supervisor_name: e.target.value })} />
              </label>
              <label className="field">
                <span>Supervisor Contact</span>
                <input value={claimForm.supervisor_contact} onChange={(e) => setClaimForm({ ...claimForm, supervisor_contact: e.target.value })} />
              </label>
              <label className="field">
                <span>Start Date</span>
                <input type="date" value={claimForm.start_date} onChange={(e) => setClaimForm({ ...claimForm, start_date: e.target.value })} />
              </label>
              <label className="field">
                <span>End Date</span>
                <input type="date" value={claimForm.end_date} onChange={(e) => setClaimForm({ ...claimForm, end_date: e.target.value })} />
              </label>
              <label className="field wide">
                <span>Description</span>
                <textarea value={claimForm.description} onChange={(e) => setClaimForm({ ...claimForm, description: e.target.value })} />
              </label>
              <label className="field wide">
                <span>Skill Tags (comma separated)</span>
                <input value={claimForm.skill_tags} onChange={(e) => setClaimForm({ ...claimForm, skill_tags: e.target.value })} />
              </label>
            </div>
            <div className="panel-actions">
              <button className="cta primary" onClick={handleCreateClaim} disabled={loading || role !== 'candidate'}>
                Save claim
              </button>
            </div>
            <div className="claim-list">
              {claims.map((claim) => (
                <div className="claim" key={claim.id}>
                  <div>
                    <p className="claim-title">{claim.title}</p>
                    <p className="muted">{claim.organization_name}</p>
                    <div className="tag-row">
                      {(claim.skill_tags || []).map((t) => (
                        <span className="tag" key={t}>{t}</span>
                      ))}
                    </div>
                  </div>
                  <div className="claim-meta">
                    <span className={`status ${claim.status}`}>{claim.status}</span>
                    {claim.credibility_score != null && <span className="score-chip">{claim.credibility_score}</span>}
                    {claim.status === 'draft' && (
                      <button className="cta ghost tiny" onClick={() => handleRequestVerification(claim.id)}>Request verification</button>
                    )}
                  </div>
                </div>
              ))}
              {claims.length === 0 && <p className="muted">No claims yet.</p>}
            </div>
          </div>
        )}

        {role === 'verifier' && (
          <div className="panel">
            <div className="panel-head">
              <div>
                <p className="eyebrow">Verifier</p>
                <h3>Inbox</h3>
              </div>
              <span className="eyebrow">{inbox.length} pending</span>
            </div>
            <div className="inbox">
              {inbox.map((item) => (
                <div className="inbox-item" key={item.id}>
                  <div>
                    <p className="claim-title">{item.title}</p>
                    <p className="muted">{item.organization_name}</p>
                    <p className="eyebrow">{item.supervisor_name}</p>
                  </div>
                  <div className="action-col">
                    <button className="cta tiny primary" onClick={() => handleDecision(item.id, 'approved')}>Approve</button>
                    <button className="cta tiny ghost" onClick={() => handleDecision(item.id, 'rejected')}>Reject</button>
                  </div>
                </div>
              ))}
              {inbox.length === 0 && <p className="muted">No pending verifications.</p>}
            </div>
          </div>
        )}

        {role === 'employer' && (
          <div className="panel wide">
            <div className="panel-head">
              <div>
                <p className="eyebrow">Employer</p>
                <h3>Report lookup</h3>
              </div>
              <button className="cta small ghost" onClick={handleFetchReport} disabled={loading}>Fetch</button>
            </div>
            <div className="form-grid">
              <label className="field">
                <span>Report token (claim id for now)</span>
                <input value={reportId} onChange={(e) => setReportId(e.target.value)} placeholder="claim id or token" />
              </label>
            </div>
            {report && (
              <div className="report-details">
                <div className="report-row">
                  <div>
                    <p className="muted">Candidate claim</p>
                    <p className="claim-title">{report.title}</p>
                    <p className="muted">{report.organization_name}</p>
                  </div>
                  <div className="score">
                    <span>Credibility</span>
                    <strong>{report.credibility_score ?? 0}</strong>
                  </div>
                </div>
                <ul className="factor-list">
                  {(report.credibility_breakdown || []).map((b) => (
                    <li key={b.factor}>
                      <div>
                        <p className="factor">{b.factor}</p>
                        <p className="reason">{b.reason}</p>
                      </div>
                      <span className="score-chip">{b.score}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {role === 'admin' && (
          <div className="panel wide">
            <div className="panel-head">
              <div>
                <p className="eyebrow">Admin</p>
                <h3>Workspace</h3>
              </div>
              <span className="eyebrow">Moderation & org verification</span>
            </div>
            <div className="admin-grid">
              <div className="admin-card">
                <div className="admin-head">
                  <p className="eyebrow">Org verification</p>
                  <span className="eyebrow">Pending: {adminOrgs.filter((o) => o.status === 'pending').length}</span>
                </div>
                <div className="admin-list">
                  {adminOrgs.map((org) => (
                    <div className="admin-row" key={org.name}>
                      <div>
                        <p className="claim-title">{org.name}</p>
                        <p className="muted">{org.contact_email}</p>
                      </div>
                      <div className="admin-actions">
                        <span className={`status ${org.status === 'verified' ? 'verified' : 'pending'}`}>{org.status}</span>
                        <button className="cta tiny ghost" onClick={() => handleAdminReview(org.id, org.status)}>Toggle</button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="admin-card">
                <div className="admin-head">
                  <p className="eyebrow">Disputes</p>
                  <span className="eyebrow">Open: {adminDisputes.filter((d) => d.status !== 'resolved').length}</span>
                </div>
                <div className="admin-list">
                  {adminDisputes.map((d) => (
                    <div className="admin-row" key={d.id}>
                      <div>
                        <p className="claim-title">{d.id}</p>
                        <p className="muted">Claim: {d.claim_id}</p>
                        <p className="eyebrow">{d.reason}</p>
                      </div>
                      <div className="admin-actions">
                        <span className={`status ${d.status}`}>{d.status}</span>
                        <div className="cta-row">
                          <button className="cta tiny primary" onClick={() => handleAdminDispute(d.id, 'resolved')}>Resolve</button>
                          <button className="cta tiny ghost" onClick={() => handleAdminDispute(d.id, 'dismissed')}>Dismiss</button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="admin-card">
                <div className="admin-head">
                  <p className="eyebrow">Audit log</p>
                  <span className="eyebrow">Recent</span>
                </div>
                <div className="admin-list">
                  {adminAudits.map((a, idx) => (
                    <div className="admin-row" key={`${a.action}-${idx}`}>
                      <div>
                        <p className="claim-title">{a.action}</p>
                        <p className="muted">{a.actor_id || 'system'} → {a.entity_type}:{a.entity_id}</p>
                      </div>
                      <span className="eyebrow">{new Date(a.created_at).toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  )
}

export default App
