import type { Dispute, OrgRecord, AuditEntry } from './types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api/v1'

function authHeaders(token?: string) {
  const headers: Record<string, string> = {}
  if (token) headers.Authorization = `Bearer ${token}`
  return headers
}

export async function getOrgs(token: string) {
  const res = await fetch(`${API_BASE}/admin/orgs`, { headers: authHeaders(token) })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<OrgRecord[]>
}

export async function verifyOrg(token: string, orgId: string, status: 'verified' | 'pending' | 'unverified') {
  const res = await fetch(`${API_BASE}/admin/orgs/${orgId}/verify?status_value=${status}`, {
    method: 'POST',
    headers: authHeaders(token),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getDisputes(token: string) {
  const res = await fetch(`${API_BASE}/admin/disputes`, { headers: authHeaders(token) })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<Dispute[]>
}

export async function decideDispute(token: string, disputeId: string, status: 'resolved' | 'dismissed', notes?: string) {
  const res = await fetch(`${API_BASE}/admin/disputes/${disputeId}/decision?status_value=${status}&notes=${encodeURIComponent(notes || '')}`, {
    method: 'POST',
    headers: authHeaders(token),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getAuditLogs(token: string) {
  const res = await fetch(`${API_BASE}/admin/audit`, { headers: authHeaders(token) })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<AuditEntry[]>
}
