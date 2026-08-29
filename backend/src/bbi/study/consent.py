ETHICS_WARNING = (
    "Do not collect participant data until the appropriate ethics and consent pathway is confirmed."
)


def may_start_session(*, study_mode: bool, adult_eligible: bool, consented: bool) -> bool:
    return study_mode and adult_eligible and consented
