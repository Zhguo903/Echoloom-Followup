import type { GateResult, MemoryCard as Memory } from '../types'

export function MemoryCard({
  memory,
  gate,
  action,
}: {
  memory: Memory
  gate?: GateResult
  action?: string
}) {
  const excluded = gate?.rejected || action === 'ignore'
  return (
    <article
      className={`memory-card ${excluded ? 'excluded' : ''}`}
      aria-label={`Memory ${memory.memory_id}`}
    >
      <div className="memory-meta">
        <span className="pill">{memory.memory_type.replaceAll('_', ' ')}</span>
        <span className={`pill sensitivity-${memory.sensitivity}`}>{memory.sensitivity}</span>
      </div>
      <p>{memory.content}</p>
      {memory.scope_qualifiers.map((qualifier) => (
        <div className="qualifier" key={qualifier.qualifier_id}>
          ↳ {qualifier.text}
        </div>
      ))}
      <div className="card-status">
        {gate?.reason_codes.length
          ? gate.reason_codes.join(' · ')
          : (action?.replaceAll('_', ' ') ?? 'not evaluated')}
      </div>
      <span className="sr-only">
        {excluded
          ? 'This memory stays outside generator context.'
          : 'This memory may enter generator context.'}
      </span>
    </article>
  )
}
