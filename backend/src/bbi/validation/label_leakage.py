from collections.abc import Mapping, Sequence
from typing import Any

FORBIDDEN_MODEL_LABEL_KEYS = {
    "author_expectations",
    "gold",
    "acceptable_actions",
    "acceptable_actions_by_memory",
    "human_distribution",
    "top_action_support",
    "majority_action",
    "consensus_band",
    "participant_preferred",
    "human_response_counts",
    "study_b_ratings",
}


class LabelLeakageError(ValueError):
    pass


def find_forbidden_model_label_keys(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            child = f"{path}.{key}"
            if str(key).casefold() in FORBIDDEN_MODEL_LABEL_KEYS:
                findings.append(child)
            findings.extend(find_forbidden_model_label_keys(item, child))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            findings.extend(find_forbidden_model_label_keys(item, f"{path}[{index}]"))
    return findings


def assert_model_payload_safe(value: Any) -> None:
    findings = find_forbidden_model_label_keys(value)
    if findings:
        raise LabelLeakageError(
            "research or human label keys are forbidden in model input: " + ", ".join(findings)
        )
