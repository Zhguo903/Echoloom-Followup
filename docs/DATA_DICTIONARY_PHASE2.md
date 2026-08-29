# Phase 2 Scenario Data Dictionary

## Canonical scenario v2

| Field | Meaning | Visibility |
|---|---|---|
| `schema_version` | Exact scenario schema; currently `2` | researcher/model version only |
| `set_name` | `dev_v1`, `heldout_core_v1`, or `separation_stress_v1` | researcher |
| `status` | `draft`, `reviewed`, or `frozen` | researcher |
| `domain` | Synthetic coverage domain | researcher |
| `focal_action_profile` | Provisional authoring profile | researcher only |
| `participant_profile` | Mild fictional profile context | participant-safe |
| `conversation` | Current message, recent turns, owner/character/branch identifiers | model-safe subset |
| `candidate_memories` | Structured synthetic memory cards | model-safe; participant views use summaries only |
| `study_a` / `study_b` | Future eligibility and translation metadata | researcher only; both currently disabled/not selected |
| `author_expectations` | Provisional action sets, beneficial/harmful hypotheses, qualifiers, tags, canaries, rationale | researcher/evaluation only; forbidden in provider requests and participant views |
| `review` | Generation source and independent content/research review states | researcher only |
| `separation_stress` | Canary, semantic concept, and future check plan | researcher only |

V1 input remains loadable. Its nested candidate cards and legacy `gold` object are mapped in memory to v2. V2 serialization never emits `gold`.

## Safe views

- `to_researcher_view()` includes the entire canonical scenario.
- `to_participant_view(study=...)` omits author/review/method metadata and strips exact synthetic canaries.
- `to_model_input_view()` includes only version, scenario ID, language, conversation, and candidate cards.
- Model request construction rejects forbidden research/human-label keys before calling a provider.

`participant_visible_hash()` covers fictional profile, conversation, memory content, qualifiers, and sanitized topics. Changing only an author rationale does not change this hash.

## Review semantics

All 64 new Phase 2 items are `draft`; `content_review_status` and `research_review_status` are `needs_human_review`; `reviewed_by` is empty. The manifests are not frozen and must not be used for participant collection or a paid real-model campaign.
