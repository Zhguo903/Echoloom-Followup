import { useMutation, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../../api/client'

export function MethodCompare() {
  const { scenarioId = 'golden_record_store_weekend_v1' } = useParams()
  const [blinded, setBlinded] = useState(false)
  const scenario = useQuery({
    queryKey: ['scenario', scenarioId],
    queryFn: () => api.scenario(scenarioId),
  })
  const comparison = useMutation({ mutationFn: () => api.compare(scenarioId) })
  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">SAME INPUT · SIX CONDITIONS</span>
          <h1>Method comparison</h1>
          <p>{scenario.data?.conversation.current_message ?? 'Loading scenario…'}</p>
        </div>
        <label className="toggle">
          <input
            type="checkbox"
            checked={blinded}
            onChange={(event) => setBlinded(event.target.checked)}
          />{' '}
          Blind labels A–F
        </label>
      </div>
      <button
        className="button primary"
        disabled={comparison.isPending}
        onClick={() => comparison.mutate()}
      >
        {comparison.isPending ? 'Running six conditions…' : 'Run comparison'}
      </button>
      {comparison.error && (
        <div className="error">Comparison failed: {comparison.error.message}</div>
      )}
      <div className="comparison-grid">
        {comparison.data?.map((run, index) => (
          <article
            className={`comparison-card ${run.method === 'reconsider_lite' ? 'featured' : ''}`}
            key={run.run_id}
          >
            <header>
              <span>
                {blinded ? String.fromCharCode(65 + index) : run.method.replaceAll('_', ' ')}
              </span>
              <small>{run.admitted_views.length} admitted</small>
            </header>
            <p>{run.visible_reply}</p>
            <details>
              <summary>Audit trace</summary>
              <div className="mini-actions">
                {Object.entries(run.actions).map(([id, action]) => (
                  <span key={id}>
                    {id}: <b>{action}</b>
                  </span>
                ))}
              </div>
              <p className="request-boundary">
                Generator payload contains{' '}
                {run.generator_request_json.includes('eligible_full_cards')
                  ? 'eligible full cards'
                  : 'reduced admitted views only'}
                .
              </p>
            </details>
          </article>
        ))}
      </div>
    </section>
  )
}
