import asyncio
import json
from pathlib import Path

import typer

from bbi.domain.enums import MethodName
from bbi.domain.runs import RunRecord
from bbi.evaluation.go_no_go import evaluate_go_no_go
from bbi.evaluation.runner import load_config, run_campaign
from bbi.evaluation.scenarios import coverage_matrix, discover_scenarios, lint_scenarios
from bbi.pipeline.reconsider_lite import run_method
from bbi.prompts.hashing import hash_prompt_files
from bbi.prompts.loader import repo_root
from bbi.providers.mock import RuleBasedMockProvider
from bbi.scenarios.coverage import coverage_report
from bbi.scenarios.manifests import (
    build_corpus_manifest,
    freeze_corpus,
    write_manifest,
)
from bbi.scenarios.migration import migrate_scenario_file
from bbi.scenarios.review import build_combined_review_queue, build_review_outputs
from bbi.scenarios.scaffold import scaffold_heldout, scaffold_separation

app = typer.Typer(no_args_is_help=True, help="Reconsider-Lite research and evaluation CLI")


def _scenario(scenario_id: str):  # type: ignore[no-untyped-def]
    scenarios = discover_scenarios([repo_root() / "data" / "scenarios"])
    for scenario in scenarios:
        if scenario.scenario_id == scenario_id:
            return scenario
    raise typer.BadParameter(f"scenario not found: {scenario_id}")


@app.command("scenario-lint")
def scenario_lint(path: Path = typer.Argument(Path("data/scenarios"))) -> None:
    target = path if path.is_absolute() else repo_root() / path
    errors = lint_scenarios([target])
    if errors:
        for error in errors:
            typer.echo(f"ERROR {error}")
        raise typer.Exit(1)
    scenarios = discover_scenarios([target])
    typer.echo(
        json.dumps(
            {
                "valid": True,
                "scenario_count": len(scenarios),
                "coverage": coverage_matrix(scenarios),
            },
            indent=2,
        )
    )


@app.command("scenario-migrate-v2")
def scenario_migrate_v2(
    path: Path = typer.Argument(...),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Migrate v1 files to a separate v2 directory, or validate an existing v2 path."""

    source = path if path.is_absolute() else repo_root() / path
    files = sorted(source.rglob("*.yaml")) if source.is_dir() else [source]
    if not files:
        raise typer.BadParameter(f"no scenario files found: {source}")
    if output is None:
        scenarios = discover_scenarios([source])
        if any(scenario.schema_version != 2 for scenario in scenarios):
            raise typer.BadParameter("in-place migration is disabled; provide --output")
        typer.echo(json.dumps({"valid_v2": True, "scenario_count": len(scenarios)}, indent=2))
        return
    destination_root = output if output.is_absolute() else repo_root() / output
    migrated = []
    for source_file in files:
        destination = destination_root / source_file.name
        migrate_scenario_file(source_file, destination)
        migrated.append(str(destination.relative_to(repo_root())))
    typer.echo(json.dumps({"migrated": len(migrated), "files": migrated}, indent=2))


@app.command("scenario-scaffold-heldout")
def scenario_scaffold_heldout(
    matrix: Path = typer.Option(..., "--matrix"),
    output: Path = typer.Option(..., "--output"),
) -> None:
    matrix_path = matrix if matrix.is_absolute() else repo_root() / matrix
    output_path = output if output.is_absolute() else repo_root() / output
    paths = scaffold_heldout(matrix_path, output_path)
    typer.echo(json.dumps({"drafts_created": len(paths), "output": str(output_path)}, indent=2))


@app.command("scenario-scaffold-separation")
def scenario_scaffold_separation(output: Path = typer.Option(..., "--output")) -> None:
    output_path = output if output.is_absolute() else repo_root() / output
    paths = scaffold_separation(output_path)
    typer.echo(json.dumps({"drafts_created": len(paths), "output": str(output_path)}, indent=2))


@app.command("scenario-build-manifest")
def scenario_build_manifest(
    scenario_dir: Path = typer.Option(..., "--scenario-dir"),
    corpus_id: str = typer.Option(..., "--corpus-id"),
    output: Path = typer.Option(..., "--output"),
) -> None:
    root = repo_root()
    scenario_path = scenario_dir if scenario_dir.is_absolute() else root / scenario_dir
    output_path = output if output.is_absolute() else root / output
    manifest = build_corpus_manifest(root, scenario_path, corpus_id=corpus_id)
    write_manifest(manifest, output_path)
    typer.echo(str(output_path))


@app.command("scenario-coverage")
def scenario_coverage(
    manifest: Path = typer.Option(..., "--manifest"),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    root = repo_root()
    manifest_path = manifest if manifest.is_absolute() else root / manifest
    report = coverage_report(root, manifest_path)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if output is not None:
        output_path = output if output.is_absolute() else root / output
        if output_path.exists():
            raise typer.BadParameter(f"refusing to overwrite report: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    typer.echo(rendered, nl=False)
    if report["structural_status"] != "pass":
        raise typer.Exit(1)


@app.command("scenario-review-report")
def scenario_review_report(
    manifest: Path = typer.Option(..., "--manifest"),
    output: Path = typer.Option(..., "--output"),
    queue: Path = typer.Option(..., "--queue"),
) -> None:
    root = repo_root()
    manifest_path = manifest if manifest.is_absolute() else root / manifest
    output_path = output if output.is_absolute() else root / output
    queue_path = queue if queue.is_absolute() else root / queue
    for destination in (output_path, queue_path):
        if destination.exists():
            raise typer.BadParameter(f"refusing to overwrite review output: {destination}")
    build_review_outputs(root, manifest_path, output_path, queue_path)
    typer.echo(json.dumps({"report": str(output_path), "queue": str(queue_path)}, indent=2))


@app.command("corpus-freeze")
def corpus_freeze(manifest: Path = typer.Option(..., "--manifest")) -> None:
    root = repo_root()
    manifest_path = manifest if manifest.is_absolute() else root / manifest
    try:
        destination = freeze_corpus(root, manifest_path)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(str(destination))


@app.command("scenario-review-queue")
def scenario_review_queue(
    manifests: list[Path] = typer.Option(..., "--manifest"),
    output: Path = typer.Option(..., "--output"),
) -> None:
    root = repo_root()
    manifest_paths = [path if path.is_absolute() else root / path for path in manifests]
    output_path = output if output.is_absolute() else root / output
    if output_path.exists():
        raise typer.BadParameter(f"refusing to overwrite review queue: {output_path}")
    build_combined_review_queue(root, manifest_paths, output_path)
    typer.echo(str(output_path))


@app.command("run")
def run(config: Path = typer.Option(..., "--config")) -> None:
    path = config if config.is_absolute() else repo_root() / config
    output = asyncio.run(run_campaign(path))
    typer.echo(str(output))


@app.command("run-one")
def run_one(
    scenario: str = typer.Option(..., "--scenario"),
    method: MethodName = typer.Option(MethodName.RECONSIDER_LITE, "--method"),
    provider: str = typer.Option("mock", "--provider"),
) -> None:
    if provider != "mock":
        raise typer.BadParameter(
            "CLI demo supports mock by default; configure server-side adapters separately"
        )
    record = asyncio.run(run_method(_scenario(scenario), method, RuleBasedMockProvider()))
    typer.echo(record.model_dump_json(indent=2))


@app.command("compare")
def compare(
    scenario: str = typer.Option(..., "--scenario"),
    provider: str = typer.Option("mock", "--provider"),
) -> None:
    if provider != "mock":
        raise typer.BadParameter("mock is the local comparison provider")

    async def execute() -> list[RunRecord]:
        return [
            await run_method(_scenario(scenario), method, RuleBasedMockProvider())
            for method in MethodName
        ]

    records = asyncio.run(execute())
    typer.echo(
        json.dumps(
            [
                {
                    "method": record.method.value,
                    "reply": record.visible_reply,
                    "actions": record.actions,
                }
                for record in records
            ],
            indent=2,
            default=str,
        )
    )


@app.command("analyze")
def analyze(result_dir: Path) -> None:
    target = result_dir if result_dir.is_absolute() else repo_root() / result_dir
    report = target / "report.md"
    if not report.exists():
        raise typer.BadParameter("campaign report does not exist")
    typer.echo(report.read_text(encoding="utf-8"))


@app.command("export-runs")
def export_runs(result_dir: Path, format: str = typer.Option("jsonl", "--format")) -> None:
    if format not in {"jsonl", "json"}:
        raise typer.BadParameter("format must be jsonl or json")
    target = result_dir if result_dir.is_absolute() else repo_root() / result_dir
    source = target / "runs.jsonl"
    if format == "jsonl":
        typer.echo(str(source))
    else:
        rows = [
            json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line
        ]
        destination = target / "runs.json"
        destination.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        typer.echo(str(destination))


@app.command("prompt-freeze")
def prompt_freeze(config: Path = typer.Option(..., "--config")) -> None:
    path = config if config.is_absolute() else repo_root() / config
    data = load_config(path)
    manifest = {
        "campaign_id": data["campaign_id"],
        "prompts": hash_prompt_files(repo_root() / "prompts"),
    }
    destination = path.with_name(f"{data['campaign_id']}_prompts_manifest.json")
    destination.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    typer.echo(str(destination))


@app.command("estimate-calls")
def estimate_calls(config: Path = typer.Option(..., "--config")) -> None:
    path = config if config.is_absolute() else repo_root() / config
    data = load_config(path)
    scenarios = discover_scenarios([repo_root() / item for item in data["scenario_paths"]])
    calls = 0
    for method in map(MethodName, data["methods"]):
        per_run = (
            2
            if method
            in {
                MethodName.RELEVANCE_TWO_PASS,
                MethodName.RECONSIDER_LITE,
                MethodName.NO_PHYSICAL_SEPARATION,
            }
            else 1
        )
        calls += per_run * len(scenarios) * data["run"].get("repetitions", 1)
    typer.echo(
        json.dumps(
            {"estimated_provider_calls_before_repairs": calls, "scenarios": len(scenarios)},
            indent=2,
        )
    )


@app.command("go-no-go")
def go_no_go(result_dir: Path) -> None:
    target = result_dir if result_dir.is_absolute() else repo_root() / result_dir
    typer.echo(json.dumps(evaluate_go_no_go(target), indent=2))


if __name__ == "__main__":
    app()
