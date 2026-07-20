"""ReleaseBench: a deterministic, side-effect-free release-readiness routing toolkit.

The package wraps the ReleaseBench family router. It reads one typed JSON routing
request and emits one canonical routing receipt; it performs no outward action.
"""

from releasebench.router import (
    CLOSED_ACTIONS,
    CONTRACT_VERSION,
    DISPATCHABLE_LEAVES,
    FULL_FLOW_ORDER,
    INTENT_TO_LEAF,
    RECEIPT_VERSION,
    ROUTER_ID,
    ContractError,
    canonical_bytes,
    canonical_sha256,
    dispatch,
    main,
)

__version__ = "0.1.1"

__all__ = [
    "CLOSED_ACTIONS",
    "CONTRACT_VERSION",
    "DISPATCHABLE_LEAVES",
    "FULL_FLOW_ORDER",
    "INTENT_TO_LEAF",
    "RECEIPT_VERSION",
    "ROUTER_ID",
    "ContractError",
    "canonical_bytes",
    "canonical_sha256",
    "dispatch",
    "main",
    "__version__",
]
