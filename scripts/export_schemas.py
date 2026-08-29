import json

from bbi.domain.decisions import DeliberationBundle, GeneratorOutput
from bbi.domain.memory import MemoryCard
from bbi.domain.runs import RunRecord
from bbi.domain.scenarios import Scenario
from bbi.prompts.loader import repo_root

SCHEMAS = {
    "memory_card.schema.json": MemoryCard.model_json_schema(),
    "scenario.schema.json": Scenario.model_json_schema(),
    "decision.schema.json": DeliberationBundle.model_json_schema(),
    "generator_output.schema.json": GeneratorOutput.model_json_schema(),
    "run_record.schema.json": RunRecord.model_json_schema(),
}

for name, schema in SCHEMAS.items():
    destination = repo_root() / "schemas" / name
    destination.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(destination)
