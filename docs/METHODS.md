# Methods

All conditions share scenario/version, candidate order, hard gates, current message, recent turns, model, output constraints, seed where supported, and repair cap.

| Method | Calls | Generator-visible memory |
|---|---:|---|
| no memory | 1 | none |
| similarity top-k | 1 | raw top-k direct-eligible cards selected by deterministic TF-IDF |
| one-pass selective | 1 | all direct-eligible cards plus “use carefully” instruction |
| relevance two-pass | 2 | raw cards selected only for topical relevance |
| Reconsider-Lite | 2 | newly allocated admitted views only |
| no physical separation | 2 | every direct-eligible full card plus Reconsider-Lite actions |

Reconsider-Lite uses a ladder: validity, relational utility, conversational warrant, scope, expression, then lexicographic priority. It never uses a weighted compensatory score. Optional surviving memories are dropped unless the user asks about remembered history. At most three direct views, one explicit callback, and one sanitized permission question are allowed by default.

Optional component ablations are configuration concepts and are intentionally not run in the default focused campaign.

