export function StudyPage() {
  return (
    <section className="page study-lock">
      <span className="lock-icon">⌁</span>
      <span className="eyebrow">STUDY MODE · OFF</span>
      <h1>Participant collection is locked.</h1>
      <p>
        Do not collect participant data until the appropriate ethics and consent pathway is
        confirmed.
      </p>
      <div className="study-details">
        <div>
          <strong>Adult eligibility</strong>
          <span>Required when enabled</span>
        </div>
        <div>
          <strong>Blinded labels</strong>
          <span>Method and provider hidden</span>
        </div>
        <div>
          <strong>Withdrawal</strong>
          <span>Responses deletable</span>
        </div>
      </div>
      <code>BBI_STUDY_MODE=false</code>
    </section>
  )
}
