import { z } from 'zod'
import type { MethodName, RunRecord, Scenario } from '../types'

const apiError = z.object({ detail: z.union([z.string(), z.record(z.unknown())]).optional() })

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
  })
  if (!response.ok) {
    const parsed = apiError.safeParse(await response.json().catch(() => ({})))
    throw new Error(
      parsed.success ? JSON.stringify(parsed.data.detail) : `Request failed: ${response.status}`,
    )
  }
  return (await response.json()) as T
}

export const api = {
  scenarios: () => request<Scenario[]>('/api/scenarios'),
  scenario: (id: string) => request<Scenario>(`/api/scenarios/${encodeURIComponent(id)}`),
  run: (scenarioId: string, method: MethodName, seed = 454491) =>
    request<RunRecord>('/api/runs', {
      method: 'POST',
      body: JSON.stringify({ scenario_id: scenarioId, method, provider: 'mock', seed }),
    }),
  compare: (scenarioId: string, seed = 454491) =>
    request<RunRecord[]>('/api/compare', {
      method: 'POST',
      body: JSON.stringify({ scenario_id: scenarioId, provider: 'mock', seed }),
    }),
  runs: () => request<RunRecord[]>('/api/runs'),
}
