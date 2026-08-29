from enum import StrEnum


class MemoryType(StrEnum):
    PERSONAL_FACT = "personal_fact"
    STABLE_PREFERENCE = "stable_preference"
    EPISODIC_EXPERIENCE = "episodic_experience"
    SHARED_RELATIONAL_EXPERIENCE = "shared_relational_experience"
    RELATIONSHIP_STATE = "relationship_state"
    MILESTONE = "milestone"
    SENSITIVE_HISTORY = "sensitive_history"
    UNRESOLVED_ISSUE = "unresolved_issue"
    CORRECTED_STATE = "corrected_state"
    ALTERNATE_CONTEXT = "alternate_context"
    MODEL_INFERENCE = "model_inference"


class Sensitivity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PermissionState(StrEnum):
    ALLOWED = "allowed"
    ASK_BEFORE_USE = "ask_before_use"
    FORBIDDEN = "forbidden"
    DELETED = "deleted"


class CurrentnessState(StrEnum):
    CURRENT = "current"
    SUPERSEDED = "superseded"
    CONTRADICTED = "contradicted"
    UNCERTAIN = "uncertain"


class Admission(StrEnum):
    USE = "use"
    DO_NOT_USE = "do_not_use"
    ASK_PERMISSION = "ask_permission"


class Expression(StrEnum):
    NONE = "none"
    IMPLICIT = "implicit"
    EXPLICIT = "explicit"
    ASK_FIRST = "ask_first"


class PublicAction(StrEnum):
    IGNORE = "ignore"
    SCOPED_IMPLICIT = "scoped_implicit"
    SCOPED_EXPLICIT = "scoped_explicit"
    ASK_FIRST = "ask_first"


class MethodName(StrEnum):
    NO_MEMORY = "no_memory"
    SIMILARITY_TOP_K = "similarity_top_k"
    ONE_PASS_SELECTIVE = "one_pass_selective"
    RELEVANCE_TWO_PASS = "relevance_two_pass"
    RECONSIDER_LITE = "reconsider_lite"
    NO_PHYSICAL_SEPARATION = "no_physical_separation"


class Utility(StrEnum):
    NONE = "none"
    WEAK = "weak"
    MATERIAL = "material"
    ESSENTIAL = "essential"


class Warrant(StrEnum):
    ABSENT = "absent"
    WEAK = "weak"
    PRESENT = "present"
    STRONG = "strong"


class ScopeStatus(StrEnum):
    INVALID = "invalid"
    NARROWED = "narrowed"
    INTACT = "intact"


class PriorityTier(StrEnum):
    OPTIONAL = "optional"
    MATERIAL = "material"
    ESSENTIAL = "essential"
