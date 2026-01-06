export type Role = 'candidate' | 'verifier' | 'employer' | 'admin'

export type ClaimStatus = 'draft' | 'pending' | 'verified' | 'rejected' | 'expired' | 'disputed'

export type Claim = {
  id: string
  title: string
  claim_type: string
  organization_name: string
  supervisor_name: string
  supervisor_contact: string
  start_date: string
  end_date: string
  description: string
  skill_tags?: string[]
  status: ClaimStatus
  credibility_score?: number
  credibility_breakdown?: { factor: string; score: number; reason: string }[]
  created_at: string
  updated_at: string
}

export type VerificationDecision = {
  outcome: 'approved' | 'rejected'
  notes?: string
  role_type?: string
  verified_start_date?: string
  verified_end_date?: string
  valid_until?: string
}

export type VerificationRecord = {
  id: string
  outcome: 'approved' | 'rejected'
  notes?: string
  role_type?: string
  verified_start_date?: string
  verified_end_date?: string
  valid_until?: string
  created_at: string
}

export type OrgRecord = {
  id: string
  name: string
  status: 'pending' | 'verified' | 'unverified'
  contact_email?: string
}

export type Dispute = {
  id: string
  claim_id: string
  status: 'open' | 'under_review' | 'resolved' | 'dismissed'
  reason: string
  resolution_notes?: string
}

export type AuditEntry = {
  id: number
  action: string
  actor_id?: string | null
  entity_type: string
  entity_id: string
  metadata?: Record<string, unknown> | null
  created_at: string
}
