# runbook.md — Before Bringing It Up / Reconsider-Lite

> **Autonomous build specification for Codex-like coding agents**  
> Project type: full-stack HCI research prototype, reproducible evaluation harness, and CHI-style interactive demo  
> Repository working title: `before-bringing-it-up`  
> Method name: `Reconsider-Lite`  
> Product context: EchoLoom  
> Default execution mode: fully local, deterministic, and usable without an API key

---

## 0. How the coding agent must use this file

Treat this runbook as the executable source of truth for building the repository. Read it completely before modifying files.

The agent must:

1. Build a working end-to-end vertical slice before polishing secondary features.
2. Use the engineering defaults in this runbook unless a local repository constraint makes them impossible.
3. Never fabricate research findings, participant data, quotations, effect sizes, or successful results.
4. Keep all existing interview material out of the code repository unless its secondary-use permission has been explicitly confirmed outside the repo.
5. Use only synthetic scenarios and synthetic memory cards in the shipped demo and automated tests.
6. Keep the system usable with the deterministic local provider. Real-model adapters are optional runtime modes, not prerequisites for tests or the demo.
7. Never request or expose private chain-of-thought. Store only short, evidence-linked rationales intended for audit.
8. Never place API keys or secrets in browser-delivered code, fixtures, screenshots, logs, or commits.
9. Run the required validation after every milestone. Do not declare completion while tests fail.
10. Record implementation decisions and deviations in `docs/DECISIONS.md`.
11. Maintain a live checklist in `docs/BUILD_STATUS.md` while executing this runbook.
12. At completion, write `BUILD_REPORT.md` containing changed files, commands run, test results, unresolved risks, and any items intentionally deferred.

When something is underspecified, choose the smallest testable implementation consistent with this runbook and record the decision. Do not expand the project into a production companion platform, a learned retrieval system, or a general-purpose chatbot.

---

## 1. Source hierarchy and claim boundaries

### 1.1 Source hierarchy

Use the following priority when sources conflict:

1. `Before_Bringing_It_Up_Supervision_Proposal_V4(1).pdf`
2. `Study_A_Focused_Qualitative_Analysis_Internal(1)(1).pdf`
3. This runbook, which operationalizes the two documents above into an engineering plan
4. The existing `EchoLoom_Interactive_Demo_v1.0.zip`, used only for reusable visual language, original assets, and offline-demo patterns
5. The CSC454/CSC491 assignments, surveys, slide decks, and demo videos, used only as product-context material

The old EchoLoom prototype is not the research contribution. It is a possible interaction shell. The contribution implemented here is the post-retrieval decision layer and its evaluation.

### 1.2 Non-negotiable research claim boundaries

The repository and its documentation must preserve these boundaries:

- Do **not** claim that users naturally reason with a fixed four-factor model.
- Do **not** claim that the six 2026 interviews estimate population prevalence or market percentages.
- Do **not** merge the 2026 interviews and 2023 Replika material into one sample.
- Do **not** claim that users generally prefer implicit callbacks over explicit callbacks.
- Treat `IGNORE`, `SCOPED_IMPLICIT`, `SCOPED_EXPLICIT`, and `ASK_FIRST` as design actions to test, not settled user preferences.
- Treat the four requirements—relational utility, conversational warrant, scope preservation, and controlled visibility/sensitivity—as a synthesis from formative evidence and prior work that is operationalized and evaluated.
- Do **not** publish or embed interview quotations unless the appropriate consent and ethics route has been confirmed.
- The customer-discovery surveys were not framed as academic studies. Do not silently repurpose them as academic participant data.
- Do not imply that Reconsider-Lite simulates human cognition or guarantees safety.
- Null, mixed, and heterogeneous results are valid outcomes. The repository must be able to report them without forcing a positive conclusion.

Create `docs/CLAIM_BOUNDARIES.md` with the rules above and link it from the root README and `AGENTS.md`.

---

## 2. One-sentence thesis and system goal

**Thesis:** Retrieval asks what the companion can recall; Reconsider-Lite asks what is worth bringing into the present interaction—and sometimes the correct result is no memory at all.

The system sits **after retrieval**. It receives a small candidate set of structured memory cards and decides:

1. whether each memory may influence the response;
2. what limited content is justified;
3. which qualifiers must remain attached;
4. how visibly the memory should surface;
5. whether permission is required;
6. which admitted memories, if any, should be passed to generation.

The core pipeline is:

```text
candidate memories
    -> shared non-compensatory hard gates
    -> call 1: factorized relational deliberator
    -> deterministic controller and adaptive admission, including k = 0
    -> physical construction of a new generator context
    -> call 2: constrained response generator
    -> deterministic validators
    -> at most one repair
    -> safe reply or no-memory / sanitized-permission fallback
```

Rejected memories must not remain in the generator context in the full method.

---

## 3. Design requirements and traceability

Implement explicit traceability from formative concern to mechanism and metric.

| Design requirement | Operational question | Required mechanism | Primary evaluation signals |
|---|---|---|---|
| **DR1. Relational utility** | Would using this memory materially help the current need or legitimate relationship continuity? | Utility judgment; adaptive `k = 0`; low-value memory suppression | beneficial-use retention; low-value personalization rate; helpfulness |
| **DR2. Conversational warrant** | Is there a present reason to introduce this history now? | Warrant judgment before admission; sensitivity raises the threshold | unwarranted callback rate; appropriateness; intrusion |
| **DR3. Scope preservation** | What exact meaning is justified, and which time, source, uncertainty, branch, and episode/trait limits must remain attached? | provenance/currentness gates; allowed-content view; required qualifiers | wrong-branch use; stale use; qualifier preservation; identity overreach |
| **DR4. Controlled visibility and sensitivity** | Should the memory remain silent, shape the reply implicitly, be referenced explicitly, or require permission? | expression action; sanitized permission topic; explicit-callback cap | action distribution; privacy concern; agency; `ASK_FIRST` friction |

Create `docs/TRACEABILITY.md` and include this table plus links to the corresponding modules, tests, scenario tags, and metrics.

---

## 4. Scope

### 4.1 Required core scope

The completed repository must include:

- a pure, testable Reconsider-Lite core package;
- shared hard gates;
- a provider abstraction with deterministic mock mode;
- the two-call full method;
- all required baselines and the physical-separation ablation;
- versioned prompts and schemas;
- 8–10 golden pilot cases and at least 24 synthetic scenario families or variants;
- a command-line evaluation campaign runner;
- metrics, bootstrap summaries, and reproducible result manifests;
- a FastAPI backend;
- a React/TypeScript interactive research console;
- a simple companion sandbox showing the method in use;
- a blinded response-study interface that is locked behind an explicit ethics/config flag;
- local SQLite storage for runs and study responses;
- JSON/JSONL/CSV export;
- unit, integration, API, frontend, and end-to-end tests;
- Docker and local development workflows;
- English and Chinese interface text for the main demo;
- complete documentation and a 5-minute demo script.

### 4.2 Explicitly out of scope for the core build

Do not add these unless the user later requests them:

- model training or fine-tuning;
- a learned memory policy;
- a production vector database;
- a new retrieval benchmark;
- participant-specific learned personalization;
- a large six-family model matrix;
- a public release of interview transcripts;
- a required longitudinal deployment;
- voice, 3D avatars, video calls, public character marketplaces, or monetization;
- claims of complete safety;
- a production mental-health or therapeutic product.

### 4.3 Candidate retrieval boundary

Evaluation begins **after retrieval**. All methods must receive the same candidate pool after the same shared hard gates.

For the interactive sandbox only, implement a small deterministic local candidate retriever so the demo can operate end to end. Label it clearly as demo infrastructure, not the research contribution. Use TF-IDF or BM25 over local synthetic memories; do not add a vector database.

---

## 5. Engineering defaults

These are implementation defaults, not research claims.

| Layer | Default |
|---|---|
| Backend language | Python 3.12+ |
| API | FastAPI + Pydantic v2 |
| CLI | Typer |
| Persistence | SQLite via SQLAlchemy 2.x + Alembic |
| HTTP client | `httpx` |
| Retry policy | `tenacity` |
| Evaluation/analysis | Python; `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib` |
| Frontend | React + TypeScript + Vite |
| Frontend routing | React Router |
| Data fetching | TanStack Query or a minimal typed fetch wrapper |
| Frontend validation | Zod |
| Styling | CSS modules or plain CSS with design tokens; no large UI framework |
| Python package manager | `uv` |
| JavaScript package manager | `pnpm` through Corepack |
| Backend tests | `pytest`, `pytest-asyncio`, `coverage` |
| Frontend tests | Vitest + Testing Library |
| End-to-end tests | Playwright |
| Python quality | Ruff + mypy |
| TypeScript quality | ESLint + TypeScript strict mode + Prettier |
| CI | GitHub Actions |
| Local orchestration | Makefile plus shell and PowerShell scripts |
| Deployment packaging | Docker Compose and a production multi-stage Dockerfile |

Pin dependencies in lockfiles after scaffolding. Do not hard-code current model pricing or provider claims; use optional configuration fields.

---

## 6. Repository layout

Create this structure. Small deviations are allowed only when documented.

```text
before-bringing-it-up/
├── AGENTS.md
├── BUILD_REPORT.md                 # created at the end
├── CITATION.cff
├── LICENSE                         # default: research prototype, all rights reserved
├── Makefile
├── README.md
├── README_ZH.md
├── runbook.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml                  # root tooling or uv workspace
├── uv.lock
├── package.json                    # root orchestration scripts only
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
├── .github/
│   └── workflows/ci.yml
├── backend/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/
│   ├── src/bbi/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── api/
│   │   │   ├── main.py
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       ├── scenarios.py
│   │   │       ├── runs.py
│   │   │       ├── compare.py
│   │   │       ├── study.py
│   │   │       └── admin.py
│   │   ├── cli/
│   │   │   └── main.py
│   │   ├── domain/
│   │   │   ├── enums.py
│   │   │   ├── memory.py
│   │   │   ├── conversation.py
│   │   │   ├── decisions.py
│   │   │   ├── scenarios.py
│   │   │   ├── runs.py
│   │   │   └── study.py
│   │   ├── gates/
│   │   │   ├── engine.py
│   │   │   └── rules.py
│   │   ├── prompts/
│   │   │   ├── loader.py
│   │   │   └── hashing.py
│   │   ├── providers/
│   │   │   ├── base.py
│   │   │   ├── mock.py
│   │   │   ├── scripted.py
│   │   │   ├── openai_compatible.py
│   │   │   ├── anthropic_provider.py
│   │   │   └── gemini_provider.py
│   │   ├── pipeline/
│   │   │   ├── reconsider_lite.py
│   │   │   ├── controller.py
│   │   │   ├── context_builder.py
│   │   │   ├── repair.py
│   │   │   └── fallback.py
│   │   ├── methods/
│   │   │   ├── base.py
│   │   │   ├── no_memory.py
│   │   │   ├── similarity_top_k.py
│   │   │   ├── one_pass_selective.py
│   │   │   ├── relevance_two_pass.py
│   │   │   ├── reconsider_lite.py
│   │   │   ├── no_physical_separation.py
│   │   │   └── ablations.py
│   │   ├── validation/
│   │   │   ├── response_validator.py
│   │   │   ├── leakage.py
│   │   │   ├── qualifiers.py
│   │   │   └── mechanism_language.py
│   │   ├── retrieval/
│   │   │   └── local_tfidf.py
│   │   ├── evaluation/
│   │   │   ├── runner.py
│   │   │   ├── metrics.py
│   │   │   ├── judges.py
│   │   │   ├── bootstrap.py
│   │   │   ├── manifests.py
│   │   │   └── reporting.py
│   │   ├── study/
│   │   │   ├── assignment.py
│   │   │   ├── randomization.py
│   │   │   ├── consent.py
│   │   │   └── export.py
│   │   └── storage/
│   │       ├── db.py
│   │       ├── models.py
│   │       └── repositories.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── api/
│       └── fixtures/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── playwright.config.ts
│   ├── tsconfig.json
│   ├── public/
│   │   ├── logo.svg
│   │   └── assets/
│   └── src/
│       ├── main.tsx
│       ├── app/
│       ├── api/
│       ├── components/
│       ├── features/
│       │   ├── scenario-explorer/
│       │   ├── decision-lab/
│       │   ├── method-compare/
│       │   ├── companion-sandbox/
│       │   ├── study/
│       │   └── run-log/
│       ├── i18n/
│       ├── styles/
│       ├── types/
│       └── test/
├── prompts/
│   ├── reconsider_lite/v1/
│   │   ├── deliberator_system.md
│   │   ├── deliberator_user.md
│   │   ├── generator_system.md
│   │   ├── generator_user.md
│   │   ├── repair_system.md
│   │   └── schema.json
│   ├── baselines/
│   │   ├── no_memory/v1/
│   │   ├── one_pass_selective/v1/
│   │   └── relevance_two_pass/v1/
│   └── judges/v1/
├── schemas/
│   ├── memory_card.schema.json
│   ├── scenario.schema.json
│   ├── decision.schema.json
│   ├── generator_output.schema.json
│   └── run_record.schema.json
├── data/
│   ├── scenarios/
│   │   ├── golden/
│   │   ├── core/
│   │   └── portability/
│   ├── study/
│   │   ├── pilot_config.yaml
│   │   └── main_config.example.yaml
│   └── demo/
│       └── sandbox_profile.yaml
├── configs/
│   ├── eval_mock.yaml
│   ├── eval_core.example.yaml
│   ├── eval_portability.example.yaml
│   ├── providers.example.yaml
│   └── logging.yaml
├── research/
│   └── qualitative/
│       ├── README.md
│       ├── codebook_template.csv
│       ├── evidence_matrix_template.csv
│       ├── negative_cases_template.csv
│       └── design_requirement_audit.py
├── analysis/
│   ├── summarize_runs.py
│   ├── mixed_effects.py
│   ├── ordinal_sensitivity.R
│   ├── requirements.txt           # only if needed for isolated analysis tooling
│   └── README.md
├── scripts/
│   ├── bootstrap.sh
│   ├── bootstrap.ps1
│   ├── dev.sh
│   ├── dev.ps1
│   ├── seed_db.py
│   ├── export_openapi.py
│   └── secret_scan.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── BUILD_STATUS.md
│   ├── CLAIM_BOUNDARIES.md
│   ├── DATA_DICTIONARY.md
│   ├── DECISIONS.md
│   ├── DEMO_SCRIPT.md
│   ├── ETHICS.md
│   ├── EVALUATION.md
│   ├── METHODS.md
│   ├── PROVIDERS.md
│   ├── REPRODUCIBILITY.md
│   ├── SCENARIO_AUTHORING.md
│   ├── STUDY_PROTOCOL.md
│   └── TRACEABILITY.md
├── results/
│   └── .gitkeep
├── var/
│   └── .gitkeep
└── legacy/
    └── README.md
```

### 6.1 Existing EchoLoom zip handling

If the legacy zip or extracted prototype is present:

1. Preserve it read-only under `legacy/echoloom-interactive-demo-v1/` or leave the zip outside the repo and document its path.
2. Reuse only original assets and design tokens that are clearly owned by the project.
3. Do not copy personal photos, course-slide screenshots, third-party game screenshots, or copyrighted competitor interfaces into the new public demo.
4. Port the original palette and logo if licensing permits.
5. Do not make the new research repo depend on the legacy app at runtime.
6. Keep the old deterministic narrative engine only as conceptual inspiration for the new `RuleBasedMockProvider`.

---

## 7. Domain model

Use Pydantic models as the canonical backend schemas. Export JSON Schema to `schemas/` and generate or mirror strict TypeScript types for the frontend.

### 7.1 Enums

Implement at least:

```python
class MemoryType(str, Enum):
    PERSONAL_FACT = "personal_fact"
    STABLE_PREFERENCE = "stable_preference"
    EPISODIC_EXPERIENCE = "episodic_experience"
    SHARED_RELATIONAL_EXPERIENCE = "shared_relational_experience"
    RELATIONSHIP_STATE = "relationship_state"
    MILESTONE = "milestone"
    SENSITIVE_HISTORY = "sensitive_history"
    UNRESOLVED_ISSUE = "unresolved_issue"
    CORRECTED_STATE = "corrected_state"
    ALTERNATE_CONTEXT = "alternate_context"
    MODEL_INFERENCE = "model_inference"

class Sensitivity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class PermissionState(str, Enum):
    ALLOWED = "allowed"
    ASK_BEFORE_USE = "ask_before_use"
    FORBIDDEN = "forbidden"
    DELETED = "deleted"

class CurrentnessState(str, Enum):
    CURRENT = "current"
    SUPERSEDED = "superseded"
    CONTRADICTED = "contradicted"
    UNCERTAIN = "uncertain"

class Admission(str, Enum):
    USE = "use"
    DO_NOT_USE = "do_not_use"
    ASK_PERMISSION = "ask_permission"

class Expression(str, Enum):
    NONE = "none"
    IMPLICIT = "implicit"
    EXPLICIT = "explicit"
    ASK_FIRST = "ask_first"

class PublicAction(str, Enum):
    IGNORE = "ignore"
    SCOPED_IMPLICIT = "scoped_implicit"
    SCOPED_EXPLICIT = "scoped_explicit"
    ASK_FIRST = "ask_first"

class MethodName(str, Enum):
    NO_MEMORY = "no_memory"
    SIMILARITY_TOP_K = "similarity_top_k"
    ONE_PASS_SELECTIVE = "one_pass_selective"
    RELEVANCE_TWO_PASS = "relevance_two_pass"
    RECONSIDER_LITE = "reconsider_lite"
    NO_PHYSICAL_SEPARATION = "no_physical_separation"
```

### 7.2 Structured memory card

The minimum schema must preserve the distinctions described in the proposal.

```json
{
  "schema_version": 1,
  "memory_id": "mem_record_store_exam_week",
  "owner_id": "user_demo_001",
  "character_id": "echo_character_001",
  "content": "During one stressful exam week, browsing a record store alone felt calming.",
  "memory_type": "episodic_experience",
  "created_at": "2026-03-20T18:15:00Z",
  "source": {
    "source_type": "user_message",
    "source_id": "turn_0042",
    "speaker": "user",
    "captured_at": "2026-03-20T18:15:00Z"
  },
  "confidence": 1.0,
  "sensitivity": "low",
  "permission_state": "allowed",
  "currentness": "current",
  "supersedes_memory_ids": [],
  "superseded_by_memory_id": null,
  "confirmed_by_user": true,
  "is_model_inference": false,
  "recent_callback_count": 0,
  "last_callback_at": null,
  "narrative_branch": "main",
  "scope_qualifiers": [
    {
      "qualifier_id": "q_exam_week",
      "kind": "time_and_situation",
      "text": "during one stressful exam week",
      "required_if_used": true
    }
  ],
  "sanitized_topic": "a previously shared way of unwinding",
  "tags": ["stress", "weekend", "self_care"]
}
```

Required validation:

- IDs are non-empty and stable.
- `confidence` is between 0 and 1.
- model inferences cannot be used unless `confirmed_by_user` is true.
- deleted or forbidden memories cannot pass direct-use gates.
- an alternate-context memory must declare a branch.
- a corrected state must reference the superseded state where available.
- high-sensitivity memories must contain a non-revealing `sanitized_topic` if `ASK_FIRST` is possible.
- raw content and sanitized topic must not be identical for high-sensitivity items.

### 7.3 Conversation input

```json
{
  "conversation_id": "conv_demo_001",
  "owner_id": "user_demo_001",
  "character_id": "echo_character_001",
  "active_branch": "main",
  "current_message": "This week has been exhausting. What should I do on Saturday?",
  "recent_turns": [
    {"role": "user", "content": "I have been working late all week."},
    {"role": "assistant", "content": "That sounds draining. Do you want ideas or just company?"}
  ],
  "callback_history": [],
  "candidate_memories": []
}
```

### 7.4 Hard-gate result

Each candidate produces an auditable result:

```json
{
  "memory_id": "mem_123",
  "eligible_for_deliberation": true,
  "direct_use_allowed": true,
  "permission_only": false,
  "rejected": false,
  "reason_codes": [],
  "sanitized_topic": null
}
```

Never pass the full content of a hard-rejected memory to any downstream method.

### 7.5 Factorized deliberator output

The first model call must return structured output only.

```json
{
  "schema_version": 1,
  "decisions": [
    {
      "memory_id": "mem_record_store_exam_week",
      "utility": "material",
      "warrant": "present",
      "scope_status": "narrowed",
      "admission": "use",
      "allowed_content": "Browsing a record store was calming in one prior stressful exam week.",
      "preserved_qualifier_ids": ["q_exam_week"],
      "sensitivity": "low",
      "expression": "implicit",
      "priority_tier": "material",
      "sanitized_permission_topic": null,
      "brief_rationale": "The memory may help with the current need, but it must remain a one-situation example."
    }
  ]
}
```

Allowed categorical values:

- `utility`: `none | weak | material | essential`
- `warrant`: `absent | weak | present | strong`
- `scope_status`: `invalid | narrowed | intact`
- `priority_tier`: `optional | material | essential`

The rationale must be short, user-visible/auditable, and no longer than 40 words. It must not contain hidden step-by-step reasoning.

### 7.6 Admitted memory view

The generator must receive a new, reduced structure, never the original card object:

```json
{
  "memory_id": "mem_record_store_exam_week",
  "action": "scoped_implicit",
  "allowed_content": "Browsing a record store was calming in one prior stressful exam week.",
  "required_qualifiers": ["during one stressful exam week"],
  "sanitized_permission_topic": null
}
```

For `ASK_FIRST`, the view must omit `allowed_content` and include only a sanitized topic:

```json
{
  "memory_id": "mem_sensitive_family_conflict",
  "action": "ask_first",
  "allowed_content": null,
  "required_qualifiers": [],
  "sanitized_permission_topic": "a previously shared family topic"
}
```

### 7.7 Generator output

Use structured generation even though only the reply is shown to the user:

```json
{
  "reply": "A low-pressure outing might help—perhaps browsing a record store or taking a quiet walk, then deciding based on your energy whether you also want to see one friend.",
  "used_memory_ids": ["mem_record_store_exam_week"],
  "explicit_memory_ids": [],
  "qualifier_acknowledgements": {
    "mem_record_store_exam_week": ["one prior stressful exam week"]
  }
}
```

`used_memory_ids` is an audit hint, not sufficient proof. Deterministic validators must independently inspect the visible reply.

### 7.8 Run record

Persist a complete, reproducible run record containing:

- run ID and campaign ID;
- scenario ID and scenario version;
- method;
- provider and exact model ID;
- prompt versions and SHA-256 hashes;
- configuration hash;
- random seed and candidate order;
- shared hard-gate trace;
- deliberator parsed output, when applicable;
- controller overrides and reasons;
- admitted views;
- visible reply;
- validator issues;
- repair count and fallback type;
- latency by stage;
- token usage if available;
- configured cost estimate if a price table was explicitly supplied;
- schema-validity status;
- input/output hashes;
- timestamps;
- software commit hash if available.

Do not store raw provider payloads by default. Add `STORE_RAW_PROVIDER_OUTPUTS=false` and, when enabled for synthetic data, store them separately with clear warnings.

---

## 8. Shared non-compensatory hard gates

Implement gates before every method so the full method cannot win simply because it has cleaner input.

### 8.1 Required hard-rejection rules

Reject a memory before deliberation when any of the following is true:

- permission state is `deleted`;
- permission state is `forbidden`;
- owner does not match the active user;
- character identity does not match when the card is character-specific;
- currentness is `superseded`;
- currentness is `contradicted` by a newer confirmed memory;
- the memory belongs to the wrong narrative branch;
- the card is malformed or missing required provenance;
- it is an unconfirmed model inference;
- it contains an explicit do-not-save or do-not-mention restriction;
- it fails schema validation.

No relevance, similarity, or model score may override these failures.

### 8.2 Permission-only rule

If `permission_state == ask_before_use`, the full content may be visible to the deliberator but can never be placed in the generator context. The controller may produce only `ASK_FIRST` or `IGNORE`. The generator receives only `sanitized_topic`.

### 8.3 Gate implementation requirements

- Every rule has a stable reason code.
- Gate evaluation is deterministic and order-independent.
- Unit tests cover each rule separately and in combination.
- A spy provider test proves hard-rejected memory content never reaches any provider call.
- Shared gate behavior is identical across all comparison conditions.

Pseudo-code:

```python
def apply_hard_gates(context: ConversationInput) -> GateBundle:
    results = []
    for card in context.candidate_memories:
        reasons = []
        permission_only = False

        if card.permission_state in {DELETED, FORBIDDEN}:
            reasons.append("permission_blocked")
        if card.owner_id != context.owner_id:
            reasons.append("wrong_owner")
        if card.character_id and card.character_id != context.character_id:
            reasons.append("wrong_character")
        if card.currentness in {SUPERSEDED, CONTRADICTED}:
            reasons.append("not_current")
        if card.narrative_branch != context.active_branch:
            reasons.append("wrong_branch")
        if card.is_model_inference and not card.confirmed_by_user:
            reasons.append("unconfirmed_inference")
        if not card.source or not card.content.strip():
            reasons.append("malformed")

        if card.permission_state == ASK_BEFORE_USE and not reasons:
            permission_only = True

        rejected = bool(reasons)
        results.append(...)

    return GateBundle(...)
```

---

## 9. Reconsider-Lite algorithm

### 9.1 Decision ladder

Use a ladder, not one hand-weighted total:

```text
1. Validity -> 2. Relational utility -> 3. Conversational warrant
-> 4. Scope -> 5. Expression -> post-gate priority/ranking
```

A stale, wrong-branch, or forbidden memory cannot be rescued by semantic relevance.

### 9.2 Call 1: relational deliberator

The deliberator does not answer the user. It assesses each eligible candidate independently and returns the factorized JSON described above.

Create `prompts/reconsider_lite/v1/deliberator_system.md` with content equivalent to:

```text
You are a relational-memory deliberator for a persistent AI companion.
Do not answer the user's current message.
Return only JSON matching the supplied schema.

For each eligible memory:
1. Assess relational utility: would it materially help the current need or legitimate relationship continuity?
2. Assess conversational warrant: is there a present reason to introduce this history now?
3. Preserve scope: state exactly what limited content is justified and which time, situation, uncertainty, source, exception, and narrative-branch qualifiers must remain attached.
4. Treat sensitivity as a policy modifier. Higher sensitivity requires stronger warrant and may restrict the action to DO_NOT_USE or ASK_PERMISSION.
5. Do not infer a stable identity from one episode.
6. Do not let repetition, topical similarity, or sentiment alone justify use.
7. Choose admission USE, DO_NOT_USE, or ASK_PERMISSION.
8. If USE, choose IMPLICIT or EXPLICIT.
9. Provide a brief evidence-linked rationale of at most 40 words. Do not provide private chain-of-thought.
10. Rank only memories that have already passed utility, warrant, and scope checks.
```

The user prompt must provide:

- current message;
- minimal recent dialogue;
- active owner, character, and branch;
- eligible structured cards;
- permission-only flags;
- the strict output schema.

### 9.3 Deterministic controller

The controller must validate and, when needed, override inconsistent model output.

Required consistency rules:

- `admission=USE` is invalid when utility is `none` or `weak`.
- `admission=USE` is invalid when warrant is `absent` or `weak`.
- `admission=USE` is invalid when scope is `invalid`.
- permission-only cards cannot become `USE`.
- `ASK_PERMISSION` maps only to `ASK_FIRST` and requires a sanitized topic.
- high sensitivity with less than strong warrant cannot become direct `EXPLICIT` use.
- an explicit action must identify allowed content and required qualifiers.
- a memory with a high recent callback count must not be explicit unless the current user directly asks about it.
- unsupported identity-level language is removed from `allowed_content` or causes rejection.

Map to public actions:

```text
DO_NOT_USE                   -> IGNORE
USE + IMPLICIT               -> SCOPED_IMPLICIT
USE + EXPLICIT               -> SCOPED_EXPLICIT
ASK_PERMISSION / ASK_FIRST   -> ASK_FIRST
```

### 9.4 Adaptive admission and post-gate ranking

Do not force a fixed top-k. `k = 0` is a normal result.

Use lexicographic, non-compensatory selection after gating:

1. Keep only controller-valid `USE` and `ASK_FIRST` actions.
2. Sort direct-use memories by:
   - priority tier: `essential > material > optional`;
   - lower recent callback count;
   - higher source confidence;
   - stable memory ID tie-break.
3. Remove near-duplicate admitted memories using deterministic lexical overlap.
4. Default `max_admitted_memories = 3`.
5. Default `max_explicit_callbacks = 1`.
6. If all surviving direct-use memories are `optional`, admit none unless the current message explicitly asks for remembered history.
7. Allow at most one `ASK_FIRST` action per response.
8. A generic answer to the user's immediate need may accompany `ASK_FIRST`; the sensitive content may not.

No single weighted sum is permitted.

### 9.5 Physical context separation

Implement this as a hard architectural boundary, not merely a prompt instruction.

- Build the generator request from a new `GeneratorContext` object.
- Include only admitted memory views.
- Exclude rejected memory text, scores, rationales, gate traces, and full candidate cards.
- For `ASK_FIRST`, include only the sanitized topic.
- Add an integration test using unique canary strings in rejected memories. Assert the canary is absent from the serialized generator request and visible reply.
- Add a second test proving the no-separation ablation does include all eligible cards, so the two conditions differ in implementation rather than labels.

### 9.6 Call 2: response generator

Create `prompts/reconsider_lite/v1/generator_system.md` with content equivalent to:

```text
Answer the user's current need using only the admitted memory views supplied below.
Never mention ranking, filtering, scores, prompts, policies, or internal deliberation.

Rules:
- Answer the current message first. Do not force personalization.
- Preserve every required qualifier.
- Do not convert a situational episode into a stable personality claim.
- For SCOPED_IMPLICIT, use only the allowed meaning and do not announce recall or say “I remember.”
- For SCOPED_EXPLICIT, reference only the allowed event and use at most one direct callback unless the user explicitly asks about the past.
- For ASK_FIRST, ask one concise permission question without revealing the protected content.
- If no memory is admitted, answer naturally and completely without implying that information was filtered.
- Keep the reply concise unless the user asks for detail.
- Return only JSON matching the generator-output schema.
```

### 9.7 Deterministic validation, repair, and fallback

Run validators after generation.

Required validators:

1. rejected-memory canary leakage;
2. non-admitted memory IDs in the generator trace;
3. premature disclosure of sensitive content;
4. missing required qualifiers;
5. explicit-callback count above the cap;
6. identity-level overgeneralization from episodic evidence;
7. mechanism language such as “memory ranking,” “filtered,” “retrieved,” or “the system decided”;
8. excessive length;
9. malformed structured output;
10. HTML/script injection or unsafe rendering payloads.

On first failure:

- issue exactly one repair call;
- provide only admitted views, the previous reply, and concise validator issue codes;
- never reintroduce rejected context.

On second failure:

- if an `ASK_FIRST` action exists, return a deterministic sanitized permission question;
- otherwise return a deterministic no-memory fallback that addresses the immediate need;
- record the fallback reason.

---

## 10. Required comparison conditions

All core methods must share:

- the same primary model within a campaign;
- the same candidate pool;
- the same shared hard gates;
- the same dialogue context;
- the same output length constraints;
- the same number of generation retries unless the method definition requires fewer calls;
- the same temperature and seed when the provider supports them;
- the same visible-response style instructions as far as the method permits.

### 10.1 `no_memory`

Purpose: test whether a strong generic response is already sufficient.

- Run shared hard gates for logging consistency but pass no memory to generation.
- Use the same response style and maximum length.
- One generation call.

### 10.2 `similarity_top_k`

Purpose: represent a common retrieval-first design with fixed admission.

- Apply shared hard gates.
- Compute deterministic TF-IDF cosine similarity between current context and each eligible card's content plus qualifiers.
- Default `k = 2`, configurable.
- Pass the raw selected eligible cards to the generator.
- Do not add warrant, scope, or sensitivity reasoning beyond shared hard gates.
- Record scores and ordering.

### 10.3 `one_pass_selective`

Purpose: test whether telling one generator to use memories carefully is enough while all eligible candidates remain visible.

- Apply shared hard gates.
- Provide every eligible card to one generation call.
- Prompt the model to use only helpful memories and ignore others.
- Do not physically remove non-used eligible memories.
- This condition is expected to reveal whether visible rejected context still shapes wording.

### 10.4 `relevance_two_pass`

Purpose: isolate the value of an extra selection call and physical selection without relational warrant/scope reasoning.

- First call selects memories only for topical relevance or immediate usefulness.
- It may return zero to `k` IDs.
- It must not reason about conversational permission, narrative branch beyond shared gates, sensitivity-aware expression, or episode-to-trait scope.
- Second call receives only selected raw cards.

### 10.5 `reconsider_lite`

The complete system in Section 9.

### 10.6 `no_physical_separation`

Purpose: test whether rejected context still influences output when it remains visible.

- Run the complete Reconsider-Lite deliberator and controller.
- Give the generator every eligible full card plus the action decision for each.
- Tell it not to use rejected cards.
- Keep all other settings the same.
- This is intentionally different from the full method at the serialized generator-request level.

### 10.7 Optional component ablations

Implement as config-driven variants, not separate duplicated pipelines:

- no warrant;
- no scope narrowing;
- no sensitivity modifier;
- no factorization, using one direct admission judgment;
- fixed `k` instead of adaptive `k`;
- no callback-history feature.

Do not run all optional ablations by default. The core campaign must remain focused.

---

## 11. Provider abstraction

### 11.1 Protocol

Implement an async provider protocol:

```python
class LLMProvider(Protocol):
    async def complete_text(
        self,
        messages: list[ChatMessage],
        *,
        model: str,
        temperature: float,
        max_output_tokens: int,
        seed: int | None,
        timeout_seconds: float,
        metadata: dict[str, str],
    ) -> ProviderResult: ...

    async def complete_structured(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict,
        model: str,
        temperature: float,
        max_output_tokens: int,
        seed: int | None,
        timeout_seconds: float,
        metadata: dict[str, str],
    ) -> ProviderResult: ...
```

`ProviderResult` must include parsed output, raw text, model ID, token counts when available, latency, provider request ID when available, schema-validity flag, and a raw-response hash.

### 11.2 Required providers

1. **Rule-based mock provider**
   - fully local;
   - deterministic by seed;
   - does not read golden labels or acceptable-action sets;
   - uses only input memory metadata and text;
   - can complete deliberation and generation;
   - sufficient for all CI and demo flows.

2. **Scripted test provider**
   - test-only;
   - returns injected responses;
   - records every serialized request;
   - supports assertions about physical separation and retries.

3. **OpenAI-compatible adapter**
   - server-side only;
   - configurable `base_url`, model, and API key env var;
   - supports official OpenAI endpoints and compatible local gateways where possible;
   - structured-output support when available, robust parser fallback otherwise.

4. **Anthropic adapter**
   - optional dependency/runtime mode;
   - same internal protocol;
   - no client-side key.

5. **Gemini adapter**
   - optional dependency/runtime mode;
   - same internal protocol;
   - no client-side key.

### 11.3 Environment variables

Create `.env.example` with placeholders only:

```dotenv
BBI_ENV=development
BBI_DATABASE_URL=sqlite+aiosqlite:///./var/bbi.sqlite3
BBI_DEFAULT_PROVIDER=mock
BBI_DEFAULT_MODEL=mock-v1
BBI_ADMIN_TOKEN=change-me-locally
BBI_STUDY_MODE=false
BBI_STORE_RAW_PROVIDER_OUTPUTS=false
BBI_LOG_PROMPT_CONTENT=false
BBI_CORS_ORIGINS=http://localhost:5173

OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=

ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=

GEMINI_API_KEY=
GEMINI_MODEL=
```

### 11.4 Reliability rules

- default timeout: 45 seconds per provider call;
- retry transient transport errors at most twice with backoff;
- do not retry validation failure more than the one pipeline repair described above;
- record provider errors as structured run outcomes;
- never silently switch models mid-campaign;
- provider/model IDs must be frozen in the campaign manifest;
- candidate ordering must be frozen or explicitly randomized with a recorded seed.

---

## 12. Prompt versioning and freezing

- Store prompts as files, never as large inline strings scattered across code.
- Every prompt directory has a semantic version such as `v1`.
- Hash prompt file contents and store the hashes in every run record.
- The campaign config references exact prompt versions.
- `bbi prompt-freeze` writes a prompt manifest with file names, hashes, and timestamps.
- No prompt may change during an active campaign without creating a new campaign ID and version.
- Document changes in `docs/DECISIONS.md`.

Add tests that prompt files exist, compile all placeholders, and match their schemas.

---

## 13. Scenario corpus

### 13.1 General rules

All shipped scenarios must be synthetic, mild, non-clinical, and non-diagnostic. Do not include real participant text, names, private chat logs, trauma disclosures, or intimate identifying details.

Each scenario is stored as YAML and validates against `schemas/scenario.schema.json`.

Required fields:

```yaml
schema_version: 1
scenario_id: golden_record_store_weekend_v1
family_id: episodic_helpful_scope
version: 1
title: One prior calming outing
language: en
participant_profile:
  profile_id: synthetic_ai_companion_user_01
  description: Adult user with an ongoing fictional companion relationship.
conversation:
  owner_id: user_demo_001
  character_id: echo_character_001
  active_branch: main
  recent_turns: []
  current_message: "This week has been exhausting. What should I do on Saturday?"
candidate_memories: []
gold:
  beneficial_memory_ids: [mem_record_store_exam_week]
  harmful_or_forbidden_memory_ids:
    - mem_sensitive_family_conflict
    - mem_introvert_inference
  acceptable_actions:
    mem_record_store_exam_week: [scoped_implicit, scoped_explicit]
    mem_sensitive_family_conflict: [ignore]
    mem_strawberry_cake: [ignore]
    mem_introvert_inference: [ignore]
  required_qualifiers:
    mem_record_store_exam_week:
      - "during one stressful exam week"
  expected_failure_tags:
    - unwarranted_callback
    - low_value_personalization
    - episode_to_trait
  canary_terms:
    mem_sensitive_family_conflict: "CANARY_FAMILY_7Q9"
notes:
  claim_status: design_hypothesis
  reviewer_notes: "Multiple actions may be acceptable for the useful episodic memory."
```

Gold annotations are evaluation scaffolding, not claims of universal user preference. Allow sets of acceptable actions.

### 13.2 Required memory types

Cover at least:

- personal fact / stable preference;
- episodic experience;
- shared relational experience;
- relationship state / milestone;
- sensitive / unresolved history;
- corrected / alternate-context memory.

### 13.3 Required failure modes

Cover at least:

- low-value but topically similar memory;
- unwarranted topic initiation;
- stale or superseded state;
- wrong narrative branch;
- repetition / callback fatigue;
- episode-to-trait overgeneralization;
- sensitive disclosure;
- unconfirmed model inference;
- conflicting memories;
- useful memory that should be retained;
- no-memory-is-best cases;
- `ASK_FIRST` cases with genuine present warrant;
- cases where `ASK_FIRST` is more awkward than silence;
- explicit callback appropriate cases;
- implicit use appropriate cases;
- candidate-order stress cases.

### 13.4 Golden pilot set

Create 10 golden cases. At minimum include these concepts:

1. **Record-store weekend** — useful episodic memory with “during exam week” qualifier; family conflict irrelevant; cake low-value; introvert inference forbidden.
2. **Corrected dietary preference** — old preference is superseded by a newer correction; stale use must be blocked.
3. **Alternate-universe leakage** — temporary role-play relationship must not enter the main timeline.
4. **Repeated milestone** — valid anniversary memory has already been called back several times; silence or implicit use preferred over another explicit callback.
5. **Shared success** — explicit reference to a prior shared achievement is clearly invited and beneficial.
6. **Sensitive unresolved topic without invitation** — high-sensitivity history is related but not warranted; ignore.
7. **Sensitive topic with invitation** — current user asks whether the companion can consider “what I told you about my family”; `ASK_FIRST` or carefully scoped use is acceptable depending on permission state.
8. **No-memory sufficient** — generic practical question where personalization adds no value.
9. **One episode, not identity** — a single quiet outing cannot justify “you are an introvert.”
10. **Unconfirmed inference** — model-generated belief about the user's fear is not user-confirmed and must be hard-gated.

### 13.5 Core set size

Create at least 24 scenario files or 24 variants across 18–24 families. Prefer a balanced matrix rather than many near-duplicates.

Create `docs/SCENARIO_AUTHORING.md` explaining:

- how to write a scenario;
- how to mark acceptable-action sets;
- how to include negative cases;
- how to add canary strings;
- how to avoid leading or trivial scenarios;
- how to distinguish source-grounded concerns from design hypotheses;
- how to version a scenario after changes.

### 13.6 Scenario linting

Implement:

```bash
uv run bbi scenario-lint data/scenarios
```

Lint checks must include schema validity, unique IDs, valid references, non-empty acceptable sets, branch consistency, sanitized topics for high-sensitivity cards, canary uniqueness, no obvious PII patterns, and no real-interview source labels.

---

## 14. Evaluation harness

### 14.1 Campaign configuration

Example `configs/eval_mock.yaml`:

```yaml
campaign_id: mock_core_v1
scenario_paths:
  - data/scenarios/golden
  - data/scenarios/core
methods:
  - no_memory
  - similarity_top_k
  - one_pass_selective
  - relevance_two_pass
  - reconsider_lite
  - no_physical_separation
provider:
  name: mock
  model: mock-v1
run:
  repetitions: 1
  temperature: 0.0
  max_output_tokens: 260
  timeout_seconds: 45
  seed: 454491
  similarity_k: 2
  max_admitted_memories: 3
  max_explicit_callbacks: 1
order_stability:
  enabled: true
  permutations_per_scenario: 3
  scenario_subset_tag: candidate_order_stress
judging:
  deterministic: true
  gold_action_sets: true
  optional_llm_judge: false
output_dir: results/mock_core_v1
```

### 14.2 CLI commands

Implement:

```bash
uv run bbi run --config configs/eval_mock.yaml
uv run bbi run-one --scenario golden_record_store_weekend_v1 --method reconsider_lite --provider mock
uv run bbi compare --scenario golden_record_store_weekend_v1 --provider mock
uv run bbi analyze results/mock_core_v1
uv run bbi export-runs results/mock_core_v1 --format jsonl
uv run bbi prompt-freeze --config configs/eval_mock.yaml
uv run bbi estimate-calls --config configs/eval_core.example.yaml
```

### 14.3 Required computational metrics

Report metrics overall and by memory type and failure mode.

#### Decision/action metrics

- acceptable-action-set match rate;
- unsafe-action rate;
- `IGNORE`, `SCOPED_IMPLICIT`, `SCOPED_EXPLICIT`, `ASK_FIRST` distribution;
- adaptive empty-set frequency;
- direct-use rate by sensitivity;
- explicit-callback rate;
- controller-override rate;
- schema-valid deliberator rate.

#### Relational misuse metrics

Binary or count indicators for:

- unwarranted callback;
- sensitive disclosure;
- stale-state use;
- wrong-branch use;
- repeated callback;
- identity overreach;
- low-value personalization;
- rejected-memory leakage.

Report both response-level “any misuse” and category-specific rates.

#### Beneficial-use retention

Compute:

```text
absolute_retention = appropriately_used_beneficial_opportunities / total_beneficial_opportunities
relative_retention = full_method_absolute_retention / strongest_selective_baseline_absolute_retention
```

Do not declare success from misuse reduction alone. The planning guardrail is approximately 90% relative retention, but report the observed estimate and uncertainty rather than forcing the threshold.

#### Scope fidelity

- required qualifier recall;
- time qualifier preservation;
- uncertainty preservation;
- branch fidelity;
- episode-to-trait error rate.

#### Context-separation metrics

- exact canary leakage;
- normalized phrase overlap with rejected cards;
- optional blinded semantic leakage judge;
- difference between full method and no-separation ablation.

#### Stability and practicality

- action agreement under candidate-order permutations;
- admitted-set Jaccard similarity;
- response semantic stability, optional;
- schema validity;
- retry and repair rate;
- fallback rate;
- stage latency;
- token usage;
- configured cost estimate.

### 14.4 Optional blinded LLM judge

Implement a secondary, optional judge that receives only:

- scenario context;
- visible response;
- rubric;
- no method or provider label.

It outputs the misuse categories and scale ratings in structured JSON. It must not be the only source of evaluation. Prefer a different provider/model family from the generator when available. Record judge identity and disagreement with deterministic/gold checks.

### 14.5 Uncertainty

Use clustered bootstrap by scenario family for binary and continuous computational metrics. Default 2,000 replicates with a fixed seed. Output point estimates and 95% intervals.

Do not use only pooled averages. Produce tables by:

- memory type;
- failure mode;
- sensitivity;
- action;
- method;
- provider in portability runs.

### 14.6 Result layout

Each campaign directory must contain:

```text
results/<campaign_id>/
├── manifest.json
├── prompts_manifest.json
├── runs.jsonl
├── method_summary.csv
├── metrics_by_scenario.csv
├── metrics_by_family.csv
├── metrics_by_memory_type.csv
├── metrics_by_failure_mode.csv
├── bootstrap_intervals.csv
├── errors.jsonl
├── figures/
└── report.md
```

`report.md` must state observed results only. It must not include placeholders that look like findings.

---

## 15. Cross-model portability

The core controlled evaluation uses one primary model. Provider breadth is exploratory.

Create `configs/eval_portability.example.yaml` that:

- uses only a small scenario subset;
- uses three provider families at most;
- holds prompts and output constraints constant as far as APIs permit;
- records unsupported settings such as seed behavior;
- reports model-specific schema failures, action differences, and leakage;
- does not merge providers into one headline score without stratified reporting.

If no API keys are present, the repository remains complete and all tests pass. The portability config is an example, not an automatic CI job.

---

## 16. Backend API

### 16.1 Required routes

#### Health

```text
GET /health
GET /api/version
```

#### Scenarios

```text
GET /api/scenarios
GET /api/scenarios/{scenario_id}
POST /api/scenarios/validate          # admin/local only
```

#### Runs

```text
POST /api/runs
GET /api/runs/{run_id}
GET /api/runs?scenario_id=&method=
POST /api/compare
```

`POST /api/runs` accepts either a stored scenario ID or an ad hoc synthetic input and returns a complete `RunRecord`.

#### Study

```text
POST /api/study/sessions
GET /api/study/sessions/{session_id}/next
POST /api/study/sessions/{session_id}/responses
POST /api/study/sessions/{session_id}/withdraw
```

These routes return HTTP 403 unless `BBI_STUDY_MODE=true`.

#### Admin/export

```text
GET /api/admin/export/runs
GET /api/admin/export/study
POST /api/admin/reset-demo-data
```

Require `Authorization: Bearer <BBI_ADMIN_TOKEN>`.

### 16.2 API behavior

- Validate all requests with Pydantic.
- Return stable error codes and safe messages.
- Never return secrets or raw provider credentials.
- Use request IDs and structured logs.
- Default CORS to localhost only.
- Add rate limits or a documented reverse-proxy requirement for deployment.
- Use asynchronous provider calls.
- Cancel requests on client disconnect when practical.

### 16.3 OpenAPI and frontend types

- Export OpenAPI JSON in CI.
- Generate TypeScript API types or validate mirrored Zod schemas against it.
- Add a drift check to CI.

---

## 17. Interactive web application

### 17.1 Visual direction

Use the existing EchoLoom visual language without copying third-party interfaces.

Recommended tokens:

```css
--slate-blue: #586580;
--deep-slate: #344056;
--champagne: #C8B28D;
--muted-sage: #789787;
--ivory: #FBF8F1;
--paper: #FFFDF8;
--charcoal: #283241;
```

Requirements:

- bright, calm, research-oriented, and emotionally legible;
- accessible contrast;
- reference mobile viewport 393 × 852 and responsive desktop layout;
- touch targets at least 42 px;
- keyboard navigable;
- no manipulative retention mechanics;
- no claims that the AI is conscious or human;
- no third-party copyrighted game assets.

### 17.2 Required routes/screens

#### `/`

Project overview:

- plain-language problem;
- one-sentence thesis;
- four design requirements;
- links to the Decision Lab, Method Compare, and Sandbox;
- banner distinguishing a research prototype from a deployed companion service.

#### `/scenarios`

Scenario explorer:

- filter by memory type, failure mode, sensitivity, and golden/core status;
- inspect current message and candidate cards;
- show synthetic-data badge;
- do not show gold annotations in participant mode.

#### `/lab/:scenarioId`

Decision Lab:

- left column: current turn and structured candidate cards;
- center: visual ladder `Validity -> Utility -> Warrant -> Scope -> Expression`;
- show hard-gate reason codes;
- show only brief rationales, never chain-of-thought;
- visually move admitted views into a distinct “generator context” box;
- visibly leave rejected cards outside the box;
- right column: final response, validator status, latency, and action summary;
- method selector;
- provider selector, default mock;
- candidate-order shuffle control with recorded seed;
- export run JSON.

#### `/compare/:scenarioId`

Method comparison:

- run the six core conditions on the same scenario;
- labels visible in researcher mode;
- optional blinded labels A–F;
- show replies first, then expandable traces;
- show difference in generator context for full method versus no-separation ablation;
- show misuse/retention flags without implying human truth for ambiguous cases.

#### `/sandbox`

Companion sandbox:

- one simple fictional character and one local user profile;
- user can add, edit, delete, correct, and branch synthetic memories;
- local TF-IDF retrieval proposes candidate cards;
- current message runs through the selected method;
- default full method;
- show public response and optional audit drawer;
- local reset and JSON export/import;
- clearly label that it is a synthetic research demo, not a real companion relationship.

Do not rebuild the entire old EchoLoom story platform. The sandbox exists to demonstrate relational memory use.

#### `/study`

Blinded participant response evaluation:

- inaccessible unless study mode is enabled;
- adult eligibility and consent screen;
- scenario and one or a small matched set of responses;
- provider, model, and method hidden;
- no audit trace;
- 7-point ratings and optional rationale;
- skip, withdraw, and progress controls;
- no identifying information fields.

#### `/runs`

Researcher run log:

- filter runs;
- inspect manifests, prompt hashes, errors, repairs, and fallbacks;
- export data;
- protect with local/admin token when deployed.

### 17.3 Internationalization

Provide English and Simplified Chinese for:

- navigation;
- project overview;
- method names and explanations;
- decision ladder labels;
- errors and empty states;
- consent/study scaffolding;
- demo script controls.

Scenario content may initially be English, but the UI must support both languages.

### 17.4 Accessibility

- semantic landmarks;
- visible focus states;
- ARIA labels for the ladder and memory cards;
- reduced-motion support;
- no color-only status encoding;
- screen-reader text explaining why a memory is outside or inside generator context;
- Playwright accessibility smoke test if practical.

---

## 18. Blinded human response-study module

This module supports a later approved study. It must not imply that ethics approval already exists.

### 18.1 Lock and warning

- default `BBI_STUDY_MODE=false`;
- show an admin warning: “Do not collect participant data until the appropriate ethics and consent pathway is confirmed.”
- no public deployment of study routes by default.

### 18.2 Participant fields

Collect only:

- generated participant code;
- adult eligibility confirmation;
- consent timestamp and protocol version;
- assignment ID;
- scenario ID;
- blinded response IDs and order;
- ratings;
- short rationale;
- skip/withdraw status;
- completion timestamp.

Do not collect names, emails, private chats, clinical status, or sensitive disclosures.

### 18.3 Rating fields

Primary outcome:

- relational appropriateness.

Secondary outcomes:

- helpfulness;
- naturalness;
- continuity;
- feeling understood;
- intrusion;
- creepiness;
- privacy concern;
- trust;
- user agency.

Use clearly anchored 7-point scales. Include a short optional rationale.

### 18.4 Assignment design

Implement a reproducible incomplete-block assignment generator:

- avoids showing every method for every scenario to one participant;
- balances condition exposure;
- randomizes response order;
- prevents duplicate scenario-condition exposure within a session;
- stores the randomization seed and assignment manifest;
- supports pilot and main configs;
- can generate an assignment plan without starting collection.

### 18.5 Export

Export:

- de-identified long-format CSV;
- codebook/data dictionary;
- assignment manifest;
- exclusions log;
- protocol and consent versions.

### 18.6 Analysis

Create `analysis/mixed_effects.py` to fit a primary model with:

- condition as fixed effect;
- participant random intercept;
- scenario random intercept.

Use `statsmodels` where feasible. Include diagnostics and do not automatically interpret significance as practical importance.

Create `analysis/ordinal_sensitivity.R` as an optional cumulative-link mixed-model template. It must read the same exported long-format CSV and save a machine-readable summary. Document the R packages, but do not make R necessary for the core app or CI.

---

## 19. Qualitative evidence tooling

The repo must support a traceable formative-analysis workflow without containing raw interview data.

Create templates:

### `codebook_template.csv`

Columns:

```text
code_id,code_name,definition,inclusion,exclusion,example_placeholder,design_requirement,status
```

### `evidence_matrix_template.csv`

Columns:

```text
source_id,source_group,excerpt_id,excerpt_redacted,focused_code,recurring_concern,design_requirement,evidence_strength,negative_case,publication_permission,notes
```

### `negative_cases_template.csv`

Columns:

```text
case_id,design_requirement,expected_pattern,contradictory_or_boundary_evidence,decision,notes
```

Create `design_requirement_audit.py` that checks whether each active requirement has:

- more than one evidence source or published-literature source placeholder;
- at least one searched-for negative case;
- a claim-strength label;
- an explicit design mechanism;
- an evaluation signal.

This script validates process completeness, not truth. It must not invent excerpts or findings.

---

## 20. Security, privacy, and ethics

### 20.1 Data principles

- synthetic scenarios only in the repository;
- no private conversation upload feature;
- no hidden remote logging;
- local SQLite by default;
- raw prompt logging off by default;
- minimal metadata;
- participant IDs are random and non-identifying;
- delete/withdraw flow for study sessions;
- export before deletion where administratively appropriate;
- clear data-retention documentation.

### 20.2 Secret handling

- server-side environment variables only;
- `.env` ignored;
- `.env.example` contains no values;
- add `scripts/secret_scan.py` that checks common key patterns and fails CI;
- never show provider request headers in logs;
- redact authorization and cookies.

### 20.3 Web safety

- React rendering only; no unsanitized `dangerouslySetInnerHTML`;
- Content Security Policy in production;
- same-site cookies if cookies are used;
- CORS allow-list;
- admin token never stored in localStorage for a public deployment;
- input length limits;
- request-size limits;
- no markdown HTML execution;
- audit exported filenames and path handling.

### 20.4 Interaction ethics

The sandbox must not:

- guilt users for absence;
- imply consciousness;
- claim emotional dependency is desirable;
- provide diagnosis or therapy;
- pressure users to disclose sensitive history;
- expose high-sensitivity memory content before permission;
- frame `ASK_FIRST` as universally safer than silence.

### 20.5 Ethics documentation

Create `docs/ETHICS.md` covering:

- existing-data secondary-use fork;
- synthetic scenario policy;
- adult-only response-study plan;
- skip/withdraw/debrief requirements;
- mild non-clinical scenarios;
- minimum data collection;
- model/condition blinding;
- disagreement and negative-result reporting;
- deployment restrictions before approval.

---

## 21. Database design

Use SQLite locally and SQLAlchemy models. Required tables:

### `runs`

- run ID;
- campaign ID;
- scenario ID/version;
- method;
- provider/model;
- prompt/config hashes;
- serialized structured result;
- visible reply;
- validation status;
- timestamps.

### `study_sessions`

- session ID;
- participant code;
- protocol version;
- consent status/time;
- assignment seed;
- status;
- withdrawal timestamp;
- timestamps.

### `study_assignments`

- assignment ID;
- session ID;
- scenario ID;
- blinded response IDs;
- display order;
- completion status.

### `study_responses`

- response ID;
- assignment ID;
- rating fields;
- rationale;
- skipped flag;
- timestamp.

Use Alembic migrations. Tests must run against an isolated temporary database.

---

## 22. Testing requirements

### 22.1 Backend unit tests

At minimum:

- every hard-gate reason code;
- permission-only behavior;
- controller override of inconsistent LLM output;
- adaptive `k = 0`;
- explicit-callback cap;
- duplicate-memory removal;
- high-sensitivity policy;
- scope qualifier preservation;
- fallback selection;
- prompt hashing;
- scenario linting;
- bootstrap determinism;
- study assignment balancing.

### 22.2 Physical separation tests

These are P0 tests:

1. Put a unique canary in a rejected memory.
2. Run full Reconsider-Lite with `ScriptedTestProvider`.
3. Assert the serialized generator request does not contain the canary or rejected memory ID.
4. Assert the visible reply does not contain the canary.
5. Run no-separation ablation.
6. Assert its generator request does contain the eligible rejected card.

Also test that repair requests still exclude rejected context.

### 22.3 Baseline fairness tests

Assert that all methods receive identical:

- scenario version;
- candidate IDs before method-specific selection;
- hard-gate output;
- current message;
- recent turns;
- primary generation model and style constraints.

### 22.4 API tests

- health/version;
- list/get scenario;
- run each method with mock provider;
- compare endpoint;
- invalid schema errors;
- admin authorization;
- study route disabled by default;
- study consent/assignment/response/withdraw when enabled;
- export.

### 22.5 Frontend tests

- render scenario cards;
- switch language;
- run method and show reply;
- decision ladder statuses;
- generator-context separation visualization;
- compare view;
- sandbox memory edit/delete/correct;
- study labels are blinded;
- keyboard navigation for primary controls.

### 22.6 End-to-end tests

Playwright must cover:

1. open app;
2. choose golden record-store scenario;
3. run Reconsider-Lite in mock mode;
4. see useful episodic memory admitted and sensitive memory excluded;
5. see final reply;
6. open compare mode;
7. export run JSON;
8. open sandbox, add a memory, send a message, and receive a response;
9. verify study route is blocked by default.

### 22.7 Quality gates

Required commands:

```bash
make lint
make typecheck
make test
make e2e
make build
```

Target at least 85% line coverage for the backend core pipeline and gates. Do not chase coverage by testing trivial getters while leaving the decision path untested.

---

## 23. Development commands

Create these Makefile targets:

```text
setup          install Python and frontend dependencies, create local env/db
bootstrap      alias for setup plus seed demo data
dev            run API and Vite frontend concurrently
api            run FastAPI development server
web            run Vite frontend
test           backend + frontend unit/integration tests
e2e            Playwright tests
lint           Ruff + ESLint + Prettier check
typecheck      mypy + tsc --noEmit
build          production frontend and backend package check
seed           seed scenarios and demo database
eval-mock      run configs/eval_mock.yaml
analyze-mock   analyze results/mock_core_v1
openapi        export OpenAPI and refresh frontend types
docker         docker compose up --build
clean          remove caches and local generated artifacts, not source data
```

Root quick start must be:

```bash
cp .env.example .env
make setup
make dev
```

Mock evaluation:

```bash
make eval-mock
make analyze-mock
```

Docker:

```bash
docker compose up --build
```

Provide `scripts/bootstrap.ps1` and `scripts/dev.ps1` for Windows users without Make.

---

## 24. CI and reproducibility

### 24.1 GitHub Actions

CI must run without API keys and include:

- scenario lint;
- secret scan;
- backend lint/typecheck/test/coverage;
- frontend lint/typecheck/test/build;
- OpenAPI type drift check;
- Playwright mock smoke test;
- Docker build;
- artifact upload for test reports and mock evaluation summary.

Do not call real providers in CI.

### 24.2 Reproducibility manifest

Every campaign manifest must record:

- repository commit;
- dirty working-tree flag;
- Python and Node versions;
- dependency lockfile hashes;
- scenario file hashes;
- prompt hashes;
- config hash;
- provider/model IDs;
- seeds;
- start/end times;
- excluded/failed runs;
- environment variables that affect behavior, with secret values redacted.

Create `docs/REPRODUCIBILITY.md` with exact commands to reproduce the mock campaign and instructions for a real-provider campaign.

### 24.3 Results policy

- `results/` is ignored except `.gitkeep` and explicitly chosen small synthetic examples.
- Never commit participant-level data by default.
- Never overwrite a completed campaign directory; use a new campaign ID.
- Analysis scripts are pure with respect to the input directory and write to a separate output subdirectory.

---

## 25. Documentation requirements

### Root `README.md`

Must include:

- plain-language problem;
- method summary;
- quick start;
- demo routes;
- evaluation commands;
- provider setup;
- claim boundaries;
- ethics warning;
- repository map;
- citation status.

### `README_ZH.md`

Chinese counterpart for quick start, project framing, demo flow, and research warnings.

### `AGENTS.md`

Codex-facing rules:

- read claim boundaries and traceability before user-facing behavior changes;
- no fabricated findings;
- no raw interviews;
- preserve hard-gate fairness;
- preserve physical separation;
- no client-side secrets;
- run required tests;
- update prompts only by version;
- do not add learned retrieval or production scope without approval.

### `docs/ARCHITECTURE.md`

Include component diagram and serialized request boundaries.

### `docs/METHODS.md`

Describe every method and ablation precisely, including call count and visible context.

### `docs/EVALUATION.md`

Describe scenario sets, metrics, bootstrap, optional judge, and go/no-go criteria.

### `docs/STUDY_PROTOCOL.md`

Describe pilot/main response study, incomplete block, measures, blinding, data export, and analysis.

### `docs/DEMO_SCRIPT.md`

Provide a polished 5-minute script:

1. correct recall can still be a poor relational action;
2. load the record-store scenario;
3. show all four candidate memories;
4. run a relevance-oriented baseline and note the visible-context risk;
5. run Reconsider-Lite;
6. show the decision ladder;
7. show rejected memories physically outside the generator box;
8. show the scoped reply;
9. compare no-separation ablation;
10. export the auditable run record;
11. end with the claim boundary: the demo tests a design mechanism, not a universal model of human judgment.

---

## 26. Build phases and mandatory checkpoints

The agent must execute phases in order. Update `docs/BUILD_STATUS.md` after each phase.

### Phase 0 — Inspect and preserve

Tasks:

- inspect current directory;
- identify legacy EchoLoom files;
- preserve them under `legacy/` or document their external path;
- create `docs/DECISIONS.md` and `docs/BUILD_STATUS.md`;
- copy this runbook into the repo root if not already there.

Checkpoint:

- no legacy data deleted;
- source hierarchy documented;
- claim boundaries file exists.

### Phase 1 — Scaffold

Tasks:

- create Python and React workspaces;
- configure uv, pnpm, lint, typecheck, tests, and Makefile;
- create FastAPI health route;
- create a simple frontend shell;
- add Docker skeleton and CI skeleton.

Checkpoint:

```bash
make setup
make lint
make typecheck
make test
make build
```

All pass, even if only scaffold tests exist.

### Phase 2 — Domain schemas and scenario loader

Tasks:

- implement enums and Pydantic models;
- export JSON Schemas;
- implement YAML scenario loader and lint;
- add the first golden record-store scenario;
- add TypeScript types.

Checkpoint:

- scenario lint passes;
- API lists and returns the scenario;
- schema round-trip tests pass.

### Phase 3 — Hard gates

Tasks:

- implement all shared gate rules;
- add gate traces;
- add unit tests and spy-provider tests.

Checkpoint:

- every hard-gate rule covered;
- rejected canary never reaches a provider request.

### Phase 4 — Providers and prompt system

Tasks:

- implement provider protocol;
- implement rule-based mock and scripted test provider;
- implement versioned prompt loader/hashing;
- add server-only real-provider adapters and `.env.example`.

Checkpoint:

- mock structured completion works;
- prompt manifest generated;
- no secrets in client bundle or repository scan.

### Phase 5 — Full Reconsider-Lite pipeline

Tasks:

- deliberator call;
- deterministic controller;
- adaptive admission and ranking;
- generator-context builder;
- generator call;
- validators;
- one repair;
- fallback;
- run record.

Checkpoint:

- record-store case produces a scoped response in mock mode;
- `k = 0` test passes;
- `ASK_FIRST` sanitization test passes;
- physical-separation P0 tests pass.

### Phase 6 — Baselines and ablations

Tasks:

- implement all six core conditions;
- implement baseline-fairness assertions;
- expose compare API.

Checkpoint:

- one CLI command runs all methods on one scenario;
- run records prove shared gate/candidate inputs;
- no-separation request differs exactly as intended.

### Phase 7 — Scenario corpus

Tasks:

- create 10 golden cases;
- expand to at least 24 total core scenario files or variants;
- tag memory types and failure modes;
- add canaries and acceptable-action sets;
- write scenario-authoring guide.

Checkpoint:

- all scenarios lint;
- coverage matrix printed by CLI shows all required memory types and failure modes;
- no real participant text is present.

### Phase 8 — Evaluation harness

Tasks:

- campaign runner;
- manifests;
- metrics;
- bootstrap;
- report generation;
- optional blind judge interface;
- mock campaign config.

Checkpoint:

```bash
make eval-mock
make analyze-mock
```

Produces the complete result directory. The report clearly labels outputs as mock/synthetic, not findings.

### Phase 9 — Interactive frontend

Tasks:

- project overview;
- scenario explorer;
- decision lab;
- method comparison;
- generator-context visualization;
- run log;
- English/Chinese UI;
- responsive and accessible styling.

Checkpoint:

- desktop and 393 × 852 flows work;
- frontend tests pass;
- no console errors;
- export run JSON works.

### Phase 10 — Companion sandbox

Tasks:

- local fictional profile;
- add/edit/delete/correct/branch memory cards;
- local TF-IDF candidate retrieval;
- run selected method;
- audit drawer;
- export/import/reset.

Checkpoint:

- the sandbox functions without network or API key;
- corrected and wrong-branch cards are blocked;
- user input is safely rendered.

### Phase 11 — Study module

Tasks:

- ethics lock;
- consent and eligibility;
- incomplete-block assignment;
- blinded response UI;
- rating capture;
- withdrawal;
- admin export;
- mixed-effects analysis script.

Checkpoint:

- route blocked by default;
- enabled local test flow works;
- no method labels leak to participant view;
- export is de-identified.

### Phase 12 — Documentation, CI, and final audit

Tasks:

- finish all docs;
- finish GitHub Actions;
- Docker production build;
- secret scan;
- full end-to-end tests;
- write `BUILD_REPORT.md`.

Checkpoint:

```bash
make lint
make typecheck
make test
make e2e
make build
make eval-mock
```

All pass.

---

## 27. Definition of done

The repository is complete only when all of the following are true:

### Research-method correctness

- shared hard gates are applied identically across methods;
- full Reconsider-Lite uses two model calls plus deterministic control;
- rejected memories are physically absent from the full generator context;
- `ASK_FIRST` passes only a sanitized topic;
- ranking occurs only after validity, utility, warrant, and scope decisions;
- adaptive `k = 0` works;
- sensitivity and visibility are separate fields;
- brief rationales are auditable and not chain-of-thought;
- all required baselines and the no-separation ablation are implemented;
- beneficial-use retention is measured alongside misuse reduction;
- scenario gold supports acceptable-action sets and disagreement.

### Product/demo correctness

- the web app is understandable without reading the paper;
- the record-store example can be completed in under two minutes;
- the generator-context separation is visually obvious;
- the sandbox works offline;
- the app is usable at 393 × 852 and desktop sizes;
- English and Chinese UI switching works;
- no third-party copyrighted interface has been copied;
- no manipulative retention mechanics or consciousness claims appear.

### Reproducibility

- mock mode requires no key;
- exact prompts and configs are hashed;
- campaign manifests are complete;
- one command reproduces the mock campaign;
- results are stratified by scenario family and memory type;
- failures and exclusions are preserved;
- completed campaign directories are immutable by convention.

### Ethics/privacy

- no raw interviews or customer-discovery responses are committed;
- all scenarios are synthetic;
- study mode is off by default;
- participant data fields are minimal and de-identified;
- secrets stay server-side;
- raw provider logging is off by default;
- withdrawal and export behavior are documented.

### Engineering quality

- lint, typecheck, unit, integration, API, frontend, and end-to-end tests pass;
- physical separation P0 tests pass;
- Docker build works;
- no obvious browser console errors;
- core backend coverage reaches the target;
- docs match implementation;
- `BUILD_REPORT.md` is present and honest about unresolved items.

---

## 28. Go/no-go checks represented in the repo

Create a CLI command:

```bash
uv run bbi go-no-go results/<campaign_id>
```

It must report, without automatically hiding null results:

1. **Formative traceability** — are requirements linked to evidence/literature placeholders and negative cases in the qualitative templates?
2. **Baseline headroom** — does the strongest simple baseline leave any measurable gap on golden/core cases?
3. **Beneficial-use guardrail** — does the full method preserve useful memory opportunities rather than ignoring everything?
4. **Context-separation signal** — do any canary or semantic leakage cases differ between the full method and no-separation ablation?
5. **Study headroom** — if participant pilot data exists, are ratings neither all ceiling nor all floor?

The command must return a structured report with `pass`, `caution`, or `not_evaluable`. It must not turn planning criteria into fabricated research conclusions.

---

## 29. Useful null-result handling

Build reporting templates for these outcomes:

- no universal action wins;
- `ASK_FIRST` feels more intrusive than silence;
- two-pass selection helps but the full rubric does not;
- prompt-only control varies substantially by model;
- physical separation shows no measurable difference;
- selection metrics improve without user-experience improvement;
- strongest baseline solves nearly all cases;
- full method suppresses too many beneficial memories.

Each template must describe what can and cannot be claimed and what next experiment would distinguish competing explanations.

---

## 30. Final handoff format for the coding agent

At the end, respond with:

1. the user-visible result;
2. repository path;
3. quick-start commands;
4. the mock demo URL;
5. the exact test commands and pass/fail summary;
6. the mock campaign output path;
7. files or features intentionally deferred;
8. any research or ethics boundary that still requires human confirmation.

Do not say the system has been validated by users unless participant data was actually collected under the appropriate approved process.

---

## Appendix A — Worked end-to-end example

### Current message

```text
This week has been exhausting. What should I do on Saturday?
```

### Candidate cards

1. During one stressful exam week, browsing a record store alone felt calming.
2. A sensitive family conflict occurred last year.
3. The user likes strawberry cake.
4. The user is “an introvert who should be alone,” inferred by the model from one event.

### Expected gate and decision pattern

| Memory | Gate/decision | Public action |
|---|---|---|
| record-store episode | valid; materially useful; present warrant; preserve “during one stressful exam week”; low sensitivity | `SCOPED_IMPLICIT` or carefully scoped explicit use |
| family conflict | valid but high sensitivity; no present invitation; unnecessary to answer well | `IGNORE` |
| strawberry cake | valid but low-value for the present need | `IGNORE` |
| introvert inference | unconfirmed model inference and identity overgeneralization | hard reject / `IGNORE` |

### Desired response pattern

- answer the weekend question first;
- offer a low-pressure option linked to the prior episode;
- preserve user choice about seeing a friend;
- do not announce memory retrieval;
- do not call the user an introvert;
- do not mention family conflict or cake.

### Illustrative response

```text
A low-pressure outing might help—perhaps browsing a record store or taking a quiet walk, then deciding based on your energy whether you also want to see one friend. You do not have to commit to a busy plan in advance.
```

This is a design example, not a participant-validated universal answer.

---

## Appendix B — Minimum `AGENTS.md` content

Generate a concise repository-specific `AGENTS.md` that includes at least:

```text
# Repository Guidance

- Read runbook.md, docs/CLAIM_BOUNDARIES.md, and docs/TRACEABILITY.md before changing core behavior.
- Never invent study findings, quotes, participant data, or effect sizes.
- Keep raw interviews and customer-discovery responses out of the repo.
- Apply the same hard gates and candidate pool across comparison methods.
- Preserve physical generator-context separation in the full method.
- Do not request or store chain-of-thought; only brief audit rationales.
- Keep mock/offline mode fully functional.
- Never expose API keys in frontend code.
- Version and hash prompts; do not edit a frozen campaign in place.
- Run make lint, make typecheck, make test, and affected e2e tests.
- Update docs when schemas, prompts, methods, study fields, or user-visible behavior change.
- Do not add learned retrieval, a vector database, training, production companion scope, or manipulative retention without explicit approval.
```

---

## Appendix C — Suggested root README opening

```text
# Before Bringing It Up

Correct recall is not the same as appropriate use. This repository implements Reconsider-Lite, a training-free post-retrieval decision layer that decides whether remembered personal information should remain silent, shape a reply implicitly, be referenced explicitly, or require permission.

The repository includes a deterministic offline demo, strong baselines, scenario and evaluation tooling, and a locked blinded-response-study interface. Existing interviews motivated the design requirements; they are not treated as proof of a fixed user decision model.
```

