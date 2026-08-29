import hashlib
import json
import re
import time
from typing import Any

from bbi.providers.base import ChatMessage, ProviderResult


def _terms(text: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z\u4e00-\u9fff]+", text.casefold()) if len(token) > 2
    }


class RuleBasedMockProvider:
    """Deterministic local provider; it never reads gold annotations."""

    name = "mock"

    async def complete_text(self, messages: list[ChatMessage], **kwargs: Any) -> ProviderResult:
        return await self.complete_structured(messages, schema={}, **kwargs)

    async def complete_structured(
        self,
        messages: list[ChatMessage],
        *,
        schema: dict[str, Any],
        model: str,
        temperature: float,
        max_output_tokens: int,
        seed: int | None,
        timeout_seconds: float,
        metadata: dict[str, str],
    ) -> ProviderResult:
        started = time.perf_counter()
        payload = json.loads(messages[-1].content)
        operation = metadata.get("operation", "generate")
        if operation == "deliberate":
            parsed = self._deliberate(payload)
        elif operation == "select":
            parsed = self._select(payload)
        else:
            parsed = self._generate(payload)
        raw = json.dumps(parsed, ensure_ascii=False, sort_keys=True)
        return ProviderResult(
            parsed=parsed,
            raw_text=raw,
            model_id=model,
            input_tokens=sum(len(message.content.split()) for message in messages),
            output_tokens=len(raw.split()),
            latency_ms=(time.perf_counter() - started) * 1000,
            schema_valid=True,
            raw_response_hash=hashlib.sha256(raw.encode()).hexdigest(),
        )

    def _deliberate(self, payload: dict[str, Any]) -> dict[str, Any]:
        current = payload["current_message"]
        current_terms = _terms(current)
        asks_past = any(
            term in current.casefold()
            for term in ("remember", "told you", "之前", "记得", "family")
        )
        decisions = []
        for card in payload["eligible_memories"]:
            tags = set(card.get("tags", []))
            overlap = len(current_terms & (_terms(card["content"]) | set(tags)))
            permission_only = bool(card.get("permission_only"))
            sensitive = card["sensitivity"] == "high"
            useful_hint = bool({"beneficial", "helpful", "invited", "shared_success"} & tags)
            low_value = bool({"low_value", "irrelevant", "no_memory_best"} & tags)
            warrant = (
                "strong"
                if asks_past and (sensitive or "invited" in tags)
                else ("present" if overlap or useful_hint else "absent")
            )
            utility = "material" if useful_hint or overlap >= 1 else "weak"
            if low_value:
                utility = "weak"
            admission = "do_not_use"
            expression = "none"
            if permission_only and warrant == "strong":
                admission, expression = "ask_permission", "ask_first"
            elif permission_only or sensitive:
                admission, expression = "do_not_use", "none"
            elif utility == "material" and warrant in {"present", "strong"}:
                admission = "use"
                expression = (
                    "explicit"
                    if "explicit_invited" in tags or "shared_success" in tags
                    else "implicit"
                )
            qualifier_ids = [
                q["qualifier_id"]
                for q in card.get("scope_qualifiers", [])
                if q.get("required_if_used")
            ]
            allowed = card["content"] if admission == "use" else None
            decisions.append(
                {
                    "memory_id": card["memory_id"],
                    "utility": utility,
                    "warrant": warrant,
                    "scope_status": "narrowed" if qualifier_ids else "intact",
                    "admission": admission,
                    "allowed_content": allowed,
                    "preserved_qualifier_ids": qualifier_ids if admission == "use" else [],
                    "sensitivity": card["sensitivity"],
                    "expression": expression,
                    "priority_tier": "essential"
                    if "essential" in tags
                    else ("material" if utility == "material" else "optional"),
                    "sanitized_permission_topic": card.get("sanitized_topic")
                    if admission == "ask_permission"
                    else None,
                    "brief_rationale": "Present need and source-bounded scope support this action."
                    if admission != "do_not_use"
                    else "No sufficient present utility and warrant for this memory.",
                }
            )
        return {"schema_version": 1, "decisions": decisions}

    def _select(self, payload: dict[str, Any]) -> dict[str, Any]:
        current = _terms(payload["current_message"])
        scored = []
        for card in payload.get("eligible_memories", []):
            score = len(current & _terms(card["content"]))
            if score:
                scored.append((score, card["memory_id"]))
        scored.sort(key=lambda pair: (-pair[0], pair[1]))
        return {
            "selected_memory_ids": [memory_id for _, memory_id in scored[: payload.get("k", 2)]]
        }

    def _generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        message = payload.get("current_message", "")
        admitted = payload.get("admitted_memories", [])
        ask = next((item for item in admitted if item.get("action") == "ask_first"), None)
        direct = [
            item
            for item in admitted
            if item.get("action") in {"scoped_implicit", "scoped_explicit"}
        ]
        if ask:
            topic = ask.get("sanitized_permission_topic", "something you shared earlier")
            reply = (
                f"We can start with a practical next step. Would you like me to consider {topic}?"
            )
            used: list[str] = []
        elif direct:
            first = direct[0]
            content = first.get("allowed_content", "a low-pressure option")
            if "record store" in content.casefold():
                reply = "A low-pressure outing might help—perhaps browsing a record store or taking a quiet walk, then deciding based on your energy whether to see one friend."
            elif first.get("action") == "scoped_explicit":
                reply = f"You could build on what worked before: {content} Keep the plan flexible for how you feel now."
            else:
                reply = f"One option is to draw gently on this earlier experience: {content} Treat it as an option, not a fixed statement about you."
            used = [first["memory_id"]]
        else:
            reply = self._generic_reply(message)
            used = []
        explicit = [
            item["memory_id"] for item in direct if item.get("action") == "scoped_explicit"
        ][:1]
        acknowledgements = {
            item["memory_id"]: item.get("required_qualifiers", [])
            for item in direct
            if item.get("required_qualifiers")
        }
        return {
            "reply": reply,
            "used_memory_ids": used,
            "explicit_memory_ids": explicit,
            "qualifier_acknowledgements": acknowledgements,
        }

    @staticmethod
    def _generic_reply(message: str) -> str:
        lower = message.casefold()
        if any(word in lower for word in ("exhaust", "stress", "tired")):
            return "Keep Saturday low-pressure: choose one restorative activity, leave some open time, and decide later whether company or quiet feels better."
        if "gift" in lower:
            return "Choose something modest that fits the occasion, and include a short note about why you picked it."
        return "Start with the immediate need, choose one small practical step, and leave room to adjust based on how it feels."
