# Providers

`mock-v1` is deterministic, local, keyless, and sufficient for CI/demo. It reads structured input and metadata only; it never reads gold annotations.

`ScriptedTestProvider` injects responses and records serialized requests for boundary/retry assertions. The OpenAI-compatible adapter uses a server-side base URL and key and attempts strict JSON schema output. Anthropic and Gemini are optional runtime adapters and intentionally unavailable until their dependencies and exact models are configured.

Never switch models inside a campaign. Freeze exact provider/model IDs, record unsupported seed/schema settings, and keep raw provider output storage and prompt-content logging off unless a synthetic-data audit explicitly enables them.

