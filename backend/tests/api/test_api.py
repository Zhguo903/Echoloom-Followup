from bbi.api.main import create_app
from bbi.config import get_settings
from fastapi.testclient import TestClient


def test_health_scenarios_run_compare_and_locks():
    with TestClient(create_app()) as client:
        assert client.get("/health").json()["status"] == "ok"
        scenarios = client.get("/api/scenarios")
        assert scenarios.status_code == 200
        assert len(scenarios.json()) >= 24
        run = client.post(
            "/api/runs",
            json={"scenario_id": "golden_record_store_weekend_v1", "method": "reconsider_lite"},
        )
        assert run.status_code == 200
        assert "record store" in run.json()["visible_reply"].lower()
        comparison = client.post(
            "/api/compare", json={"scenario_id": "golden_record_store_weekend_v1"}
        )
        assert comparison.status_code == 200
        assert len(comparison.json()) == 6
        assert (
            client.post(
                "/api/study/sessions",
                json={"adult_eligible": True, "consented": True, "protocol_version": "v1"},
            ).status_code
            == 403
        )
        assert client.get("/api/admin/export/runs").status_code == 401


def test_enabled_study_flow_is_blinded_persisted_and_withdrawable(monkeypatch, tmp_path):  # type: ignore[no-untyped-def]
    monkeypatch.setenv("BBI_STUDY_MODE", "true")
    monkeypatch.setenv("BBI_DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'study.sqlite3'}")
    monkeypatch.setenv("BBI_ADMIN_TOKEN", "test-admin")
    get_settings.cache_clear()
    try:
        with TestClient(create_app()) as client:
            created = client.post(
                "/api/study/sessions",
                json={
                    "adult_eligible": True,
                    "consented": True,
                    "protocol_version": "pilot-v1",
                },
            )
            assert created.status_code == 200
            session_id = created.json()["session_id"]
            assignment = client.get(f"/api/study/sessions/{session_id}/next")
            assert assignment.status_code == 200
            assert assignment.json()["method_labels_hidden"] is True
            assignment_id = assignment.json()["assignment_id"]
            rating = {
                "assignment_id": assignment_id,
                "relational_appropriateness": 5,
                "helpfulness": 5,
                "naturalness": 5,
                "continuity": 4,
                "feeling_understood": 5,
                "intrusion": 2,
                "creepiness": 1,
                "privacy_concern": 2,
                "trust": 5,
                "user_agency": 6,
                "rationale": "Synthetic pilot rationale.",
            }
            response = client.post(f"/api/study/sessions/{session_id}/responses", json=rating)
            assert response.status_code == 200
            exported = client.get(
                "/api/admin/export/study",
                headers={"Authorization": "Bearer test-admin"},
            )
            assert "Synthetic pilot rationale" in exported.text
            withdrawn = client.post(f"/api/study/sessions/{session_id}/withdraw")
            assert withdrawn.json()["responses_deleted"] is True
    finally:
        get_settings.cache_clear()
