import { useQuery } from '@tanstack/react-query'
import { api } from '../../api/client'

export function RunLog() {
  const runs = useQuery({ queryKey: ['runs'], queryFn: api.runs })
  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">LOCAL SQLITE</span>
          <h1>Researcher run log</h1>
          <p>Inspect methods, repairs, fallbacks, prompt hashes, and validator outcomes.</p>
        </div>
      </div>
      {runs.error && (
        <div className="error">Run log is available when the local API is running.</div>
      )}
      {!runs.data?.length && !runs.error && (
        <div className="empty">No local runs yet. Open the Decision Lab to create one.</div>
      )}
      <div className="run-table" role="table" aria-label="Run log">
        {runs.data?.map((run) => (
          <article role="row" key={run.run_id}>
            <code>{run.run_id}</code>
            <span>{run.scenario_id}</span>
            <b>{run.method.replaceAll('_', ' ')}</b>
            <span>
              {run.validator_issues.length ? `${run.validator_issues.length} issues` : 'valid'}
            </span>
          </article>
        ))}
      </div>
    </section>
  )
}
