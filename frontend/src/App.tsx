import './App.css'

type Claim = {
  title: string
  org: string
  status: 'draft' | 'pending' | 'verified' | 'rejected'
  score?: number
  tags: string[]
}

type VerificationItem = {
  candidate: string
  role: string
  org: string
  submitted: string
}

const sampleClaims: Claim[] = [
  { title: 'Volunteer Coordinator', org: 'Community Bridge', status: 'verified', score: 86, tags: ['coordination', 'youth'] },
  { title: 'Apprentice Technician', org: 'TechWorks Jaffna', status: 'pending', tags: ['hardware', 'support'] },
  { title: 'Field Trainer', org: 'AgriReach', status: 'draft', tags: ['training', 'field'] },
]

const verificationInbox: VerificationItem[] = [
  { candidate: 'Malsha Perera', role: 'Apprentice Technician', org: 'TechWorks Jaffna', submitted: '2h ago' },
  { candidate: 'Ruwan Jayasuriya', role: 'Volunteer Lead', org: 'GreenHands', submitted: '1d ago' },
]

const reportFactors = [
  { factor: 'Verified org account', score: '+20', reason: 'TechWorks Jaffna verified' },
  { factor: 'Recency', score: '+15', reason: 'Completed in last 12 months' },
  { factor: 'Evidence', score: '+10', reason: 'Public letter + hours log' },
  { factor: 'Multiple verifications', score: '+20', reason: 'Supervisor + HR' },
  { factor: 'Expiry', score: '-0', reason: 'Valid until 2026-06-01' },
]

function App() {
  return (
    <div className="page">
      <header className="hero">
        <div>
          <div className="badge">Sri Lanka · Trust Infrastructure</div>
          <h1>Proof of real work, verified by humans.</h1>
          <p>
            Candidates capture evidence, verifiers endorse with audit trails, and employers see a clear
            credibility score they can trust. No blockchain, no black boxes—just accountable verification.
          </p>
          <div className="cta-row">
            <button className="cta primary">Start as Candidate</button>
            <button className="cta ghost">Join as Verifier</button>
            <span className="cta-note">Signed, shareable reports ready in minutes.</span>
          </div>
          <div className="metrics">
            <div><strong>12</strong><span>claims verified this week</span></div>
            <div><strong>4.2 hrs</strong><span>median time to verify</span></div>
            <div><strong>3</strong><span>pilot orgs onboarded</span></div>
          </div>
        </div>
        <div className="card report">
          <div className="report-header">
            <div>
              <p className="eyebrow">Verification Report</p>
              <h2>Malsha Perera</h2>
              <p className="muted">Apprentice Technician · TechWorks Jaffna</p>
            </div>
            <div className="score">
              <span>Credibility</span>
              <strong>86</strong>
            </div>
          </div>
          <ul className="factor-list">
            {reportFactors.map((f) => (
              <li key={f.factor}>
                <div>
                  <p className="factor">{f.factor}</p>
                  <p className="reason">{f.reason}</p>
                </div>
                <span className="score-chip">{f.score}</span>
              </li>
            ))}
          </ul>
          <div className="link-row">
            <div>
              <p className="eyebrow">Share link</p>
              <p className="muted">verify.lk/report/4f1d-92ef</p>
            </div>
            <button className="cta small">Copy</button>
          </div>
        </div>
      </header>

      <section className="grid">
        <div className="panel">
          <div className="panel-head">
            <div>
              <p className="eyebrow">Candidate</p>
              <h3>Experience claims</h3>
            </div>
            <button className="cta small">Add claim</button>
          </div>
          <div className="claim-list">
            {sampleClaims.map((claim) => (
              <div className="claim" key={claim.title}>
                <div>
                  <p className="claim-title">{claim.title}</p>
                  <p className="muted">{claim.org}</p>
                  <div className="tag-row">
                    {claim.tags.map((t) => (
                      <span className="tag" key={t}>{t}</span>
                    ))}
                  </div>
                </div>
                <div className="claim-meta">
                  <span className={`status ${claim.status}`}>{claim.status}</span>
                  {claim.score && <span className="score-chip">{claim.score}</span>}
                  <button className="cta ghost tiny">Share</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-head">
            <div>
              <p className="eyebrow">Verifier</p>
              <h3>Verification inbox</h3>
            </div>
            <button className="cta small ghost">View history</button>
          </div>
          <div className="inbox">
            {verificationInbox.map((item) => (
              <div className="inbox-item" key={item.candidate}>
                <div>
                  <p className="claim-title">{item.candidate}</p>
                  <p className="muted">{item.role} · {item.org}</p>
                  <p className="eyebrow">{item.submitted}</p>
                </div>
                <div className="action-col">
                  <button className="cta tiny primary">Approve</button>
                  <button className="cta tiny ghost">Reject</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel wide">
          <div className="panel-head">
            <div>
              <p className="eyebrow">Employer</p>
              <h3>Report validation</h3>
            </div>
            <button className="cta small ghost">Request follow-up</button>
          </div>
          <div className="report-row">
            <div>
              <p className="muted">Link status</p>
              <p className="status-pill ok">Valid · Expires 2026-06-01</p>
            </div>
            <div>
              <p className="muted">Org badge</p>
              <p className="status-pill badge">Org verified</p>
            </div>
            <div>
              <p className="muted">Evidence</p>
              <p className="status-pill">Public letter · Hours log</p>
            </div>
          </div>
        </div>
      </section>

      <section className="info">
        <div>
          <p className="eyebrow">Why it works</p>
          <h3>Human verification, audit trails, time-bound validity.</h3>
          <p className="muted">
            Every action is logged. Claims expire unless refreshed. Scores are explainable so employers and programs
            see why a candidate is credible.
          </p>
        </div>
        <div className="pillars">
          <div>
            <h4>Evidence-backed</h4>
            <p>Upload letters, photos, certificates. Control what’s public vs verifier-only.</p>
          </div>
          <div>
            <h4>Org-first</h4>
            <p>Verifiers use org accounts; future tiers add badges and domain verification.</p>
          </div>
          <div>
            <h4>Disputes</h4>
            <p>Flag, review, and resolve—keeping a clear audit history for trust.</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default App
