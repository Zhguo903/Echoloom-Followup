from bbi.domain.enums import MethodName
from bbi.methods.base import MethodSpec

METHOD_SPECS = {
    MethodName.NO_MEMORY: MethodSpec("one generation", "no memory"),
    MethodName.SIMILARITY_TOP_K: MethodSpec("one generation", "top-k raw eligible cards"),
    MethodName.ONE_PASS_SELECTIVE: MethodSpec("one generation", "all eligible cards"),
    MethodName.RELEVANCE_TWO_PASS: MethodSpec("selection + generation", "selected raw cards"),
    MethodName.RECONSIDER_LITE: MethodSpec(
        "deliberation + generation", "admitted reduced views only"
    ),
    MethodName.NO_PHYSICAL_SEPARATION: MethodSpec(
        "deliberation + generation", "all eligible cards plus decisions"
    ),
}

__all__ = ["METHOD_SPECS"]
