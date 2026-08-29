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
