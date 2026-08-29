from pathlib import Path


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "prompts").is_dir() and (parent / "runbook.md").exists():
            return parent
    raise RuntimeError("repository root not found")


class PromptLoader:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or repo_root() / "prompts"

    def load(self, relative_path: str) -> str:
        path = (self.root / relative_path).resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError("prompt path escapes prompt root")
        return path.read_text(encoding="utf-8")
