# Analysis

`summarize_runs.py` summarizes deterministic run manifests without mutating the campaign directory. `mixed_effects.py` expects an approved, de-identified long-format response export and fits condition as a fixed effect with participant and scenario intercepts. `ordinal_sensitivity.R` is optional and requires `ordinal` plus `jsonlite`; R is not part of core CI.

Create a new output directory for every analysis. Never commit participant-level data by default.

