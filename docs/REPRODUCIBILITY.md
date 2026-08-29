# Reproducibility

```bash
cp .env.example .env
make setup
uv run bbi scenario-lint data/scenarios
make eval-mock
make analyze-mock
```

The campaign manifest records commit/dirty state, Python and Node versions, lockfile, scenario, prompt and config hashes, provider/model, seed, timestamps, failures, exclusions, and behavior-affecting environment names with secret values redacted.

Completed campaign directories are immutable by convention and the runner refuses to overwrite one containing a manifest. Change `campaign_id` and `output_dir` for a new run. Real-provider campaigns must copy the example config, set exact server-side model variables, freeze prompts, and remain stratified by provider.

