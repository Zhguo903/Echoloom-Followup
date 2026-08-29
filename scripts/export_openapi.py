import json

from bbi.api.main import app
from bbi.prompts.loader import repo_root

destination = repo_root() / "frontend" / "src" / "api" / "openapi.json"
destination.write_text(
    json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
print(destination)
