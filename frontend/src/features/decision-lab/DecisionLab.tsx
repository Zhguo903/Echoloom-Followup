import { useMutation, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../../api/client'
import { Ladder } from '../../components/Ladder'
import { MemoryCard } from '../../components/MemoryCard'
import { useLanguage } from '../../i18n'
import type { MethodName, RunRecord } from '../../types'

const methods: MethodName[] = [
  'no_memory',
  'similarity_top_k',
  'one_pass_selective',
  'relevance_two_pass',
  'reconsider_lite',
  'no_physical_separation',
]

function downloadRun(run: RunRecord) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(run, null, 2)], { type: 'application/json' }),
  )
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = `${run.run_id}.json`
  anchor.click()
  URL.revokeObjectURL(url)
}

export function DecisionLab() {
  const { scenarioId = 'golden_record_store_weekend_v1' } = useParams()
  const { t } = useLanguage()
  const [method, setMethod] = useState<MethodName>('reconsider_lite')
  const [seed, setSeed] = useState(454491)
  const scenario = useQuery({
    queryKey: ['scenario', scenarioId],
    queryFn: () => api.scenario(scenarioId),
  })
  const run = useMutation({ mutationFn: () => api.run(scenarioId, method, seed) })
  if (scenario.isLoading) return <div className="page empty">Loading decision lab…</div>
  if (!scenario.data)
    return (
      <div className="page error">
        Scenario unavailable. Start the local API with <code>make dev</code>.
      </div>
    )
  const gates = new Map(run.data?.hard_gates.results.map((gate) => [gate.memory_id, gate]))
  const admittedIds = new Set(run.data?.admitted_views.map((item) => item.memory_id))
  return (
    <section className="page lab-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">DECISION LAB · {scenario.data.set_name}</span>
          <h1>{scenario.data.title}</h1>
          <p className="current-message">“{scenario.data.conversation.current_message}”</p>
        </div>
        <Link className="text-link" to={`/compare/${scenarioId}`}>
          Compare all six →
        </Link>
      </div>
      <div className="control-bar">
        <label>
          Method
          <select value={method} onChange={(event) => setMethod(event.target.value as MethodName)}>
            {methods.map((item) => (
              <option key={item} value={item}>
                {item.replaceAll('_', ' ')}
              </option>
            ))}
          </select>
        </label>
        <label>
          Provider
          <select disabled>
            <option>mock · local</option>
          </select>
        </label>
        <label>
          Seed
          <input
            value={seed}
            onChange={(event) => setSeed(Number(event.target.value))}
            inputMode="numeric"
          />
        </label>
        <button className="button primary" disabled={run.isPending} onClick={() => run.mutate()}>
          {run.isPending ? 'Running…' : t.run}
        </button>
      </div>
      {run.error && <div className="error">Run failed: {run.error.message}</div>}
      <div className="lab-grid">
        <section className="lab-column">
          <div className="column-label">
            <span>01</span>
            <h2>Candidate memories</h2>
          </div>
          {scenario.data.candidate_memories.map((memory) => (
            <MemoryCard
              key={memory.memory_id}
              memory={memory}
              gate={gates.get(memory.memory_id)}
              action={run.data?.actions[memory.memory_id]}
            />
          ))}
        </section>
        <section className="lab-column decision-column">
          <div className="column-label">
            <span>02</span>
            <h2>Decision ladder</h2>
          </div>
          <Ladder hasRun={Boolean(run.data)} />
          <div className="context-box" aria-label="Generator context">
            <div className="context-header">
              <span>{t.generator}</span>
              <strong>{run.data?.admitted_views.length ?? 0} admitted</strong>
            </div>
            {!run.data && <p className="muted">Run a method to construct a new context.</p>}
            {run.data?.admitted_views.map((view) => (
              <article key={view.memory_id}>
                <span>{view.action.replaceAll('_', ' ')}</span>
                <p>{view.allowed_content ?? view.sanitized_permission_topic}</p>
                {view.required_qualifiers.map((qualifier) => (
                  <small key={qualifier}>Preserve: {qualifier}</small>
                ))}
              </article>
            ))}
          </div>
          {run.data && (
            <div className="outside-box">
              <strong>{t.outside}</strong>
              <p>
                {scenario.data.candidate_memories
                  .filter((item) => !admittedIds.has(item.memory_id))
                  .map((item) => item.memory_id)
                  .join(' · ') || 'None'}
              </p>
            </div>
          )}
        </section>
        <section className="lab-column response-column">
          <div className="column-label">
            <span>03</span>
            <h2>Visible response</h2>
          </div>
          <div className="response-card">
            {run.data ? (
              <>
                <div className="avatar">E</div>
                <p>{run.data.visible_reply}</p>
              </>
            ) : (
              <p className="muted">
                The final response will appear here—without scores or mechanism language.
              </p>
            )}
          </div>
          {run.data && (
            <>
              <div className="audit-stats">
                <div>
                  <span>Validation</span>
                  <strong>{run.data.validator_issues.length ? 'Issues' : 'Passed'}</strong>
                </div>
                <div>
                  <span>Repair</span>
                  <strong>{run.data.repair_count}</strong>
                </div>
                <div>
                  <span>Latency</span>
                  <strong>
                    {Math.round(Object.values(run.data.latency).reduce((a, b) => a + b, 0))} ms
                  </strong>
                </div>
              </div>
              <button className="button secondary wide" onClick={() => downloadRun(run.data)}>
                Export run JSON ↓
              </button>
            </>
          )}
        </section>
      </div>
    </section>
  )
}
