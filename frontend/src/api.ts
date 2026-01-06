import type { Claim, VerificationDecision } from './types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api/v1'

function authHeaders(token?: string, contentType = 'application/json') {
  const headers: Record<string, string> = {}
  if (contentType) headers['Content-Type'] = contentType
  if (token) headers.Authorization = `Bearer ${token}`
  return headers
}

export async function register(payload: {
  email: string
  password: string
  full_name: string
  role: string
}) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function login(email: string, password: string) {
  const body = new URLSearchParams()
  body.append('username', email)
  body.append('password', password)
  body.append('grant_type', 'password')
  body.append('scope', '')
  body.append('client_id', 'frontend')
  body.append('client_secret', '')
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  })
  if (!res.ok) {
    const msg = await res.text()
    throw new Error(msg || 'Login failed')
  }
  return res.json() as Promise<{ access_token: string; refresh_token: string; role: string }>
}

export async function getClaims(token: string) {
  const res = await fetch(`${API_BASE}/claims`, { headers: authHeaders(token) })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<Claim[]>
}

export async function createClaim(token: string, payload: Record<string, unknown>) {
  const res = await fetch(`${API_BASE}/claims`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function requestVerification(token: string, claimId: string) {
  const res = await fetch(`${API_BASE}/claims/${claimId}/request-verification`, {
    method: 'POST',
    headers: authHeaders(token),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getInbox(token: string) {
  const res = await fetch(`${API_BASE}/verifications/inbox`, {
    headers: authHeaders(token),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<Claim[]>
}

export async function decideVerification(token: string, claimId: string, decision: VerificationDecision) {
  const res = await fetch(`${API_BASE}/verifications/${claimId}/decision`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(decision),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function fetchReport(token: string | null, reportToken: string) {
  const res = await fetch(`${API_BASE}/reports/${reportToken}`, {
    headers: authHeaders(token || undefined),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<Claim>
}
