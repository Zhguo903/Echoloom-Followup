import { Link } from 'react-router-dom'
import { useLanguage } from '../i18n'

const requirements = [
  [
    '01',
    'Relational utility',
    'Does this memory materially help the present need or legitimate continuity?',
  ],
  ['02', 'Conversational warrant', 'Is there a present reason to introduce this history now?'],
  [
    '03',
    'Scope preservation',
    'What exact meaning, time, source, and limits must remain attached?',
  ],
  [
    '04',
    'Controlled visibility',
    'Should it stay silent, shape the reply, be named, or require permission?',
  ],
]

export function OverviewPage() {
  const { t, language } = useLanguage()
  return (
    <>
      <section className="hero">
        <div className="eyebrow">RECONSIDER-LITE · CHI RESEARCH PROTOTYPE</div>
        <h1>{t.thesis}</h1>
        <p className="hero-copy">
          {language === 'en'
            ? 'Retrieval asks what a companion can recall. This decision layer asks what is worth bringing into the present interaction—and sometimes the correct result is no memory at all.'
            : '检索回答“系统能想起什么”。这个决策层进一步判断：此刻什么值得进入对话——有时正确答案是不使用任何记忆。'}
        </p>
        <div className="hero-actions">
          <Link className="button primary" to="/lab/golden_record_store_weekend_v1">
            Open Decision Lab
          </Link>
          <Link className="button secondary" to="/compare/golden_record_store_weekend_v1">
            {t.compare}
          </Link>
        </div>
        <div className="hero-flow" aria-label="System flow">
          <span>Candidate memories</span>
          <b>→</b>
          <span>Hard gates</span>
          <b>→</b>
          <span>Deliberate</span>
          <b>→</b>
          <span>New context</span>
          <b>→</b>
          <span>Reply</span>
        </div>
      </section>
      <section className="section">
        <div className="section-heading">
          <span>THE FOUR QUESTIONS</span>
          <h2>Before bringing it up</h2>
        </div>
        <div className="requirement-grid">
          {requirements.map(([number, title, description]) => (
            <article className="requirement" key={number}>
              <span>{number}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>
      <section className="boundary-callout">
        <div>
          <span className="eyebrow">CLAIM BOUNDARY</span>
          <h2>A mechanism to test, not a model of human truth.</h2>
        </div>
        <p>
          The four actions are design hypotheses. The shipped scenarios and outputs are synthetic;
          no user validation or universal preference is claimed.
        </p>
      </section>
    </>
  )
}
