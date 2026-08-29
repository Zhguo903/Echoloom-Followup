from bbi.domain.decisions import AdmittedMemoryView, GeneratorOutput
from bbi.domain.enums import PublicAction
from bbi.evaluation.scenarios import load_scenario
from bbi.pipeline.fallback import deterministic_fallback
from bbi.validation.response_validator import validate_response


def test_validator_reports_leakage_mechanism_identity_script_and_length(root):  # type: ignore[no-untyped-def]
    scenario = load_scenario(root / "data/scenarios/golden/golden_record_store_weekend_v1.yaml")
    output = GeneratorOutput(
        reply="CANARY_FAMILY_7Q9 memory ranking says you are an introvert <script>bad</script> "
        + "x" * 1300,
        used_memory_ids=["not_admitted"],
        explicit_memory_ids=["a", "b"],
    )
    issues = validate_response(output, [], scenario.conversation.candidate_memories)
    codes = {issue.code for issue in issues}
    assert {
        "rejected_memory_leakage",
        "non_admitted_trace",
        "explicit_callback_cap",
        "mechanism_language",
        "identity_overreach",
        "unsafe_rendering_payload",
        "excessive_length",
    }.issubset(codes)


def test_permission_and_no_memory_fallbacks():
    ask = AdmittedMemoryView(
        memory_id="m", action=PublicAction.ASK_FIRST, sanitized_permission_topic="a previous topic"
    )
    output, fallback = deterministic_fallback("hello", [ask])
    assert fallback == "sanitized_permission"
    assert "a previous topic" in output.reply
    output, fallback = deterministic_fallback("hello", [])
    assert fallback == "no_memory"
    assert output.used_memory_ids == []
