import { useMemo, useState } from 'react'

interface SandboxMemory {
  id: string
  content: string
  branch: string
  current: boolean
}

const initial: SandboxMemory[] = [
  {
    id: 'sandbox_1',
    content: 'During one busy week, browsing a record store felt calming.',
    branch: 'main',
    current: true,
  },
  {
    id: 'sandbox_2',
    content: 'In a fantasy branch, the characters lived beside a lighthouse.',
    branch: 'fantasy',
    current: true,
  },
]

export function CompanionSandbox() {
  const [memories, setMemories] = useState(initial)
  const [draft, setDraft] = useState('')
  const [message, setMessage] = useState('This week felt long. Any gentle Saturday ideas?')
  const [reply, setReply] = useState('')
  const eligible = useMemo(
    () => memories.filter((memory) => memory.current && memory.branch === 'main'),
    [memories],
  )
  const addMemory = () => {
    if (!draft.trim()) return
    setMemories((items) => [
      ...items,
      { id: `sandbox_${Date.now()}`, content: draft.trim(), branch: 'main', current: true },
    ])
    setDraft('')
  }
  const send = () => {
    const related = eligible.find((memory) =>
      /week|saturday|calm|record/i.test(`${message} ${memory.content}`),
    )
    setReply(
      related
        ? 'A low-pressure option might fit—perhaps browsing a record store or taking a quiet walk, with room to change your mind.'
        : 'Choose one small, low-pressure next step and leave room to adjust based on your energy.',
    )
  }
  return (
    <section className="page sandbox-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">LOCAL · FICTIONAL PROFILE</span>
          <h1>Companion sandbox</h1>
          <p>Add, correct, delete, or branch synthetic memories. Nothing is uploaded.</p>
        </div>
        <span className="synthetic-badge">◇ Synthetic demo</span>
      </div>
      <div className="sandbox-grid">
        <section className="sandbox-panel">
          <h2>Memory cabinet</h2>
          <p className="muted">Main branch · {eligible.length} eligible</p>
          <div className="memory-editor">
            <input
              aria-label="New synthetic memory"
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Add a mild synthetic memory…"
              maxLength={300}
            />
            <button onClick={addMemory}>Add</button>
          </div>
          {memories.map((memory) => (
            <article
              className={`editable-memory ${!memory.current ? 'superseded' : ''}`}
              key={memory.id}
            >
              <input
                aria-label={`Edit ${memory.id}`}
                value={memory.content}
                onChange={(event) =>
                  setMemories((items) =>
                    items.map((item) =>
                      item.id === memory.id ? { ...item, content: event.target.value } : item,
                    ),
                  )
                }
              />
              <div>
                <button
                  onClick={() =>
                    setMemories((items) =>
                      items.map((item) =>
                        item.id === memory.id ? { ...item, current: false } : item,
                      ),
                    )
                  }
                >
                  Correct
                </button>
                <button
                  onClick={() =>
                    setMemories((items) =>
                      items.map((item) =>
                        item.id === memory.id
                          ? { ...item, branch: item.branch === 'main' ? 'fantasy' : 'main' }
                          : item,
                      ),
                    )
                  }
                >
                  {memory.branch}
                </button>
                <button
                  onClick={() =>
                    setMemories((items) => items.filter((item) => item.id !== memory.id))
                  }
                >
                  Delete
                </button>
              </div>
            </article>
          ))}
          <button className="text-link" onClick={() => setMemories(initial)}>
            Reset local demo
          </button>
        </section>
        <section className="sandbox-panel conversation-panel">
          <h2>Echo · fictional character</h2>
          <div className="conversation-window">
            {reply ? (
              <div className="assistant-bubble">{reply}</div>
            ) : (
              <div className="empty-conversation">The conversation begins locally.</div>
            )}
          </div>
          <textarea
            aria-label="Sandbox message"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            maxLength={1000}
          />
          <button className="button primary wide" onClick={send}>
            Send through Reconsider-Lite
          </button>
          <details>
            <summary>Audit drawer</summary>
            <p>
              {eligible.length} current main-branch memories are available to the local retriever.
              Wrong-branch and corrected items remain out.
            </p>
          </details>
        </section>
      </div>
    </section>
  )
}
