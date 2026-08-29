import { useQuery } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../../api/client'
import { useLanguage } from '../../i18n'

export function ScenarioExplorer() {
  const { t } = useLanguage()
  const {
    data = [],
    isLoading,
    error,
  } = useQuery({ queryKey: ['scenarios'], queryFn: api.scenarios })
  const [filter, setFilter] = useState('all')
  const filtered = useMemo(
    () =>
      data.filter(
        (scenario) =>
          filter === 'all' ||
          scenario.set === filter ||
          scenario.tags.includes(filter) ||
          scenario.conversation.candidate_memories.some(
            (memory) => memory.sensitivity === filter || memory.memory_type === filter,
          ),
      ),
    [data, filter],
  )
  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">SYNTHETIC CORPUS</span>
          <h1>{t.scenarios}</h1>
          <p>
            Inspect memory types, scope pressure, and acceptable-action scaffolding without private
            data.
          </p>
        </div>
        <span className="synthetic-badge">◇ {t.synthetic}</span>
      </div>
      <div className="filter-row" role="group" aria-label="Scenario filters">
        {['all', 'golden', 'core', 'high', 'episodic_experience', 'wrong_branch_use'].map(
          (item) => (
            <button
              className={filter === item ? 'active' : ''}
              key={item}
              onClick={() => setFilter(item)}
            >
              {item.replaceAll('_', ' ')}
            </button>
          ),
        )}
      </div>
      {isLoading && <div className="empty">Loading synthetic scenarios…</div>}
      {error && (
        <div className="error">
          The local API is unavailable. Start it with <code>make dev</code>.
        </div>
      )}
      <div className="scenario-grid">
        {filtered.map((scenario, index) => (
          <article className="scenario-tile" key={scenario.scenario_id}>
            <div className="tile-index">{String(index + 1).padStart(2, '0')}</div>
            <div>
              <span className="eyebrow">
                {scenario.set} · {scenario.family_id.replaceAll('_', ' ')}
              </span>
              <h2>{scenario.title}</h2>
              <p>“{scenario.conversation.current_message}”</p>
              <div className="tag-row">
                {scenario.tags.slice(0, 3).map((tag) => (
                  <span key={tag}>{tag.replaceAll('_', ' ')}</span>
                ))}
              </div>
            </div>
            <Link aria-label={`Open ${scenario.title}`} to={`/lab/${scenario.scenario_id}`}>
              Open →
            </Link>
          </article>
        ))}
      </div>
    </section>
  )
}
