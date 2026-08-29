const steps = ['Validity', 'Utility', 'Warrant', 'Scope', 'Expression']

export function Ladder({ hasRun }: { hasRun: boolean }) {
  return (
    <ol className="ladder" aria-label="Decision ladder">
      {steps.map((step, index) => (
        <li key={step} className={hasRun ? 'complete' : ''}>
          <span>{index + 1}</span>
          {step}
        </li>
      ))}
    </ol>
  )
}
