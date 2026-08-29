export type PublicAction = 'ignore' | 'scoped_implicit' | 'scoped_explicit' | 'ask_first'
export type MethodName =
  | 'no_memory'
  | 'similarity_top_k'
  | 'one_pass_selective'
  | 'relevance_two_pass'
  | 'reconsider_lite'
  | 'no_physical_separation'

export interface Qualifier {
  qualifier_id: string
  kind: string
  text: string
  required_if_used: boolean
}

export interface MemoryCard {
  memory_id: string
  content: string
  memory_type: string
  sensitivity: 'low' | 'medium' | 'high'
  permission_state: string
  currentness: string
  narrative_branch: string
  recent_callback_count: number
  scope_qualifiers: Qualifier[]
}

export interface Scenario {
  scenario_id: string
  family_id: string
  title: string
  set_name: string
  tags: string[]
  candidate_memories: MemoryCard[]
  conversation: {
    current_message: string
    active_branch: string
  }
}

export interface GateResult {
  memory_id: string
  eligible_for_deliberation: boolean
  rejected: boolean
  permission_only: boolean
  reason_codes: string[]
}

export interface AdmittedView {
  memory_id: string
  action: PublicAction
  allowed_content: string | null
  required_qualifiers: string[]
  sanitized_permission_topic: string | null
}

export interface RunRecord {
  run_id: string
  scenario_id: string
  method: MethodName
  visible_reply: string
  hard_gates: { results: GateResult[] }
  admitted_views: AdmittedView[]
  actions: Record<string, PublicAction>
  validator_issues: { code: string; message: string }[]
  repair_count: number
  fallback_type: string | null
  latency: Record<string, number>
  prompt_hashes: Record<string, string>
  generator_request_json: string
}
