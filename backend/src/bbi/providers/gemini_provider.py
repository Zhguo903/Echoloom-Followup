class GeminiProvider:
    name = "gemini"

    def __init__(self, *_: object, **__: object) -> None:
        raise RuntimeError(
            "Install and configure the optional Gemini runtime before using this adapter."
        )
