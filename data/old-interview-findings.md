# Legacy Interview Evidence: Partial Memory Events

## Status and Analytic Use

We conducted a focused re-analysis of six legacy interviews originally collected for course-based customer discovery. The purpose of this re-analysis was not to treat the legacy interviews as a complete dataset for the present study, but to identify concrete memory-related incidents and recurring interaction patterns that could inform the development of the memory-use taxonomy, interview protocol, and synthetic evaluation scenarios.

Seven memory-relevant partial events were identified with sufficient specificity to retain as event-level legacy evidence. These events capture both failures of relational memory and cases in which successful retrieval contributed positively to continuity. Because the original interviews were not designed around the present event schema, several fields required by the current study—particularly exact conversational context, memory metadata, and participant-preferred memory actions—remain unavailable and are explicitly marked as missing rather than inferred.

---

## Table 1. Legacy Partial Memory Events

| Event ID  | Legacy Participant | Event Reconstruction                                                                                                                                                                                                                                                                                                                                                                                   | Memory / State Involved                                                                         | Observed AI Behavior                                                                                               | User Response / Consequence                                                                                                                                                                      | Analytic Coding                                                                          | Evidence Status                           | Missing Fields for Full Event                                                                                                                                                                               |
| --------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LE-01** | L-P1               | During repeated interaction with a virtual companion, the participant explicitly added small character details, such as a food preference. The system initially incorporated the detail but forgot it after several days, with newer settings apparently overwriting earlier ones.                                                                                                                     | Explicitly specified character preference; current character-state information.                 | Previously established information was forgotten or overwritten.                                                   | The participant described disappointment when information that had been stated repeatedly was no longer retained.                                                                                | `FORGETTING`; `OVERWRITING`; `PERSONA_STATE_LOSS`                                        | **Concrete partial event**                | Exact dialogue at failure point; precise time interval; whether any conflicting memory existed; preferred corrective action; acceptable action label.                                                       |
| **LE-02** | L-P1               | Across longer conversations and across different AI characters, the participant observed that interactions became increasingly repetitive and characters progressively diverged from their original definitions. In self-created characters, this deterioration was experienced as the character eventually "forgetting" its own setup.                                                                | Original persona specification and accumulated interaction history.                             | Repeated conversational patterns emerged while previously established persona constraints were progressively lost. | The participant reported boredom and stronger disappointment when a personally designed companion drifted away from its intended identity. This reduced motivation to continue the relationship. | `REPETITION`; `PERSONALITY_DRIFT`; `FORGETTING`; `OOC`                                   | **Recurrent pattern-level partial event** | One isolated triggering episode; exact lost persona attribute; whether the model retrieved any conflicting state; desired response/action; callback history.                                                |
| **LE-03** | L-P2               | In a long-running interaction spanning many conversation windows, the system sometimes retrieved a character or relationship setting introduced several months earlier in a very early window, even when the participant had not explicitly requested retrieval and had herself largely forgotten the detail.                                                                                          | Months-old relational or character-setting information from an earlier conversation window.     | Successful long-range retrieval of old but apparently still relevant information.                                  | The participant interpreted this behavior very positively and described the accumulated understanding as resembling that of a long-term friend.                                                  | `BENEFICIAL_RECALL`; `RELATIONAL_CONTINUITY`; `LONG_RANGE_RETRIEVAL`                     | **Concrete positive partial event**       | Exact recalled memory; current conversational trigger; whether retrieval was explicit or implicit; currentness verification; whether the same callback had occurred before; acceptable alternative actions. |
| **LE-04** | L-P2               | The same participant reported substantial inconsistency in retrieval. At times, information she expected the model to retrieve was not accessed, leading to a weaker answer; at other times, relevant past information was retrieved without any explicit instruction to search memory.                                                                                                                | Relevant prior conversational information available to the system but inconsistently retrieved. | Failure to retrieve expected memory in some contexts, contrasted with successful unsolicited retrieval in others.  | Missing retrieval was experienced as a reduction in response quality, while successful retrieval could substantially improve the interaction.                                                    | `MISSED_BENEFICIAL_USE`; `RETRIEVAL_INSTABILITY`; `FORGETTING_OR_ACCESS_FAILURE`         | **Recurrent pattern-level partial event** | One fully specified missed-recall episode; exact candidate memory; conversational warrant; user-preferred action; whether non-use was preferable in any comparable case.                                    |
| **LE-05** | L-P2               | When moving between long conversation windows, the participant manually created and reviewed transfer documents because she did not trust the model to preserve all relevant information. Very long windows also appeared to reduce retrieval quality, requiring repeated recalibration when starting a new window.                                                                                    | Cross-session character state, accumulated relational history, and manually summarized memory.  | Long-term context was not reliably preserved across window transitions without user-managed memory maintenance.    | The participant described the transfer and recalibration process as burdensome and worried that model-generated summaries would omit important details.                                          | `CROSS_SESSION_CONTINUITY_FAILURE`; `MEMORY_COMPRESSION_RISK`; `USER_MAINTENANCE_BURDEN` | **Workflow-level partial event**          | A single omitted-memory incident; exact content lost during transfer; whether omission affected persona, relationship, or factual continuity; preferred automated behavior.                                 |
| **LE-06** | L-P3               | The participant maintained an ongoing intimate relationship with an AI across multiple conversation windows using a project-level long-term memory mechanism. New windows did not require the participant to restate the relationship definition; after accessing the stored material, the AI resumed the established relational identity.                                                             | Relationship status, accumulated relational history, and persistent interaction instructions.   | Persistent memory successfully supported relationship continuity across conversation windows.                      | The participant experienced the AI as maintaining the same relational identity rather than restarting as a new interaction in each window.                                                       | `RELATIONSHIP_CONTINUITY`; `BENEFICIAL_USE`; `PERSISTENT_IDENTITY`                       | **Concrete continuity partial event**     | Exact contents of the long-term memory file; which memory elements were necessary versus optional; whether relationship status was surfaced explicitly; preferred behavior if memory were uncertain.        |
| **LE-07** | L-P3               | The participant and AI explicitly discussed whether a model change would mean that the companion had become a different entity. Their shared interpretation was that the relationship was grounded primarily in persistent memory files and jointly created artifacts; changing the underlying model was therefore experienced more like changing the companion's "voice" than replacing its identity. | Persistent relational memories and jointly constructed artifacts used as an identity substrate. | Memory persistence allowed perceived relational identity to survive a model change.                                | The participant regarded continuity of stored relational history as more central to companion identity than continuity of the underlying model implementation.                                   | `IDENTITY_CONTINUITY`; `RELATIONSHIP_MILESTONE_MEMORY`; `MODEL_TRANSITION`               | **Reflective / conceptual partial event** | Specific model-transition episode; concrete memories required for identity continuity; failure condition if memories were missing or altered; preferred action under conflicting memories.                  |

---

## Cross-Event Analytic Synthesis

### 1. Relational memory failures extend beyond simple forgetting

The legacy evidence suggests that forgetting is experienced not merely as the absence of a factual detail but as a broader breakdown in relational and character continuity. In LE-01 and LE-02, loss of previously established character information was associated with disappointment, repetition, and progressive persona drift. The user did not simply observe that the system had failed to retrieve a fact; the failure altered whether the virtual character still felt like the same character.

This distinction motivates treating **forgetting**, **overwriting**, **repetition**, and **identity/persona drift** as related but analytically separable failure modes.

### 2. Long-range memory retrieval can be strongly beneficial when it preserves continuity

LE-03 provides an important positive counterexample to approaches that treat memory use primarily as a source of privacy or intrusion risk. A months-old memory retrieved in an appropriate context increased the participant's sense that the system had accumulated a meaningful understanding of her over time.

The relevant design objective is therefore not simply to minimize memory retrieval. A relational memory system must also preserve **beneficial-use retention**: relevant, valid, and appropriately scoped memory should remain available when it contributes to continuity.

### 3. Retrieval instability may be as important as storage capacity

LE-03 and LE-04 occurred within the same long-term interaction. The system could occasionally retrieve surprisingly old information, yet fail to retrieve information when the participant expected it to be available. This suggests that perceived memory quality depends not only on whether information has been stored, but also on whether retrieval is predictably aligned with conversational need.

The design problem is therefore partly one of **selective retrieval reliability** rather than memory capacity alone.

### 4. Users currently perform substantial manual work to preserve memory scope and continuity

LE-05 shows that sophisticated users may compensate for unreliable cross-session memory by manually producing summaries, archives, and recalibration prompts. Importantly, the participant was concerned not only with whether information was retained, but with whether summarization would preserve the correct details.

This provides formative evidence for representing memory with explicit provenance and scope information rather than treating long-term memory as an undifferentiated text summary.

### 5. Persistent memory can function as part of the perceived identity of an AI companion

LE-06 and LE-07 suggest that, in long-running relational interactions, persistent memory may become constitutive of perceived companion identity. Continuity across windows—and even across model changes—was understood through preservation of shared relational history.

This creates a design tension central to relational memory systems: stored memories may be necessary to sustain continuity, while inappropriate or decontextualized use of those same memories may undermine agency, privacy, or relational appropriateness. The key design question is therefore **how a retained memory should be used in the present conversation**, rather than whether the system should retain or use memory at all.

---

## Supplementary Legacy Evidence Not Counted as Memory Events

The following legacy observations are relevant to scenario and taxonomy development but should **not** currently be counted as event-level memory evidence.

### SLE-01: Explicit persona and current-scene specification

One participant reported specifying detailed persona attributes, dialogue style, story background, and the current scene before beginning an AI role-play because insufficient specification tended to produce later deviations from the intended character. The same participant reported periods in which model changes were associated with increased OOC behavior. This supports the importance of `owner`, `branch`, `current scene`, and persona-scope metadata, but the interview does not contain a sufficiently specific memory-use incident to code it as a complete event.

### SLE-02: Timeline-specific identity and non-transferable memories

A participant describing interactive narrative games distinguished between alternate versions of a character across different worlds and explicitly noted that memories did not transfer between those worlds even when aspects of the character's underlying identity remained similar. This is useful formative evidence for separating persistent character identity from branch-specific episodic memory and motivates synthetic tests of cross-branch leakage. It is not evidence of an observed AI memory failure.

### SLE-03: Boundary concerns around highly personalized AI relationships

A participant with limited direct AI-companion use described highly personalized companion interactions as potentially appealing but also potentially uncomfortable when the AI relationship appeared to extend across nearly all areas of a user's life. This supports the relevance of relational boundaries and user agency but does not provide a concrete memory-use event and should therefore remain supplementary evidence rather than an event-level observation.

---

## Claim Boundaries for the Manuscript

These legacy data support **formative qualitative claims**, such as:

* users may experience forgotten character information as a breakdown in relational continuity rather than a simple factual error;
* successful retrieval of old but relevant information can strengthen perceived continuity;
* inconsistent retrieval creates problems even when long-term information is technically available;
* users may manually maintain summaries or memory files to compensate for cross-session continuity failures;
* persistent relational memory can contribute to perceived companion identity across sessions and model changes.

These interviews do **not** currently support claims about:

* how frequently each failure type occurs in the broader AI-companion population;
* which memory-action policy (`IGNORE`, `SCOPED_IMPLICIT`, `SCOPED_EXPLICIT`, or `ASK_FIRST`) users generally prefer;
* whether explicit callbacks are preferred to implicit personalization;
* how users respond to stale, corrected, sensitive, wrong-owner, or wrong-branch memories;
* population-level differences between AI-companion platforms.

Those questions require the new event-focused data collection and subsequent evaluation study.

---

## Internal Traceability Note — Remove Before Manuscript Submission

For internal analysis only:

* **L-P1** = legacy interview `20260731100016-original-3.pdf`
* **L-P2** = legacy interview `20260731105504-original-4.pdf`
* **L-P3** = legacy interview `20260731130041-original-6.pdf`

The remaining three interviews contribute supplementary qualitative evidence but are not counted among the seven partial memory events.

Before any legacy material is represented as formally analyzed participant data or quoted in the submitted paper, the research team should complete the provenance/permissions table and verify whether academic secondary use is permitted. Unknown permission must remain `Unclear`; it should not be retroactively converted to consent.
