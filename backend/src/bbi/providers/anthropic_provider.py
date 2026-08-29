class AnthropicProvider:
    name = "anthropic"

    def __init__(self, *_: object, **__: object) -> None:
        raise RuntimeError(
            "Install and configure the optional Anthropic runtime before using this adapter."
        )
