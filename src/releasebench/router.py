#!/usr/bin/env python3
"""Deterministic, side-effect-free ReleaseBench family dispatcher."""

from __future__ import annotations

import hashlib
import json
import sys
from typing import Any


CONTRACT_VERSION = "releasebench.route-request/v1"
RECEIPT_VERSION = "releasebench.route-receipt/v1"
ROUTER_ID = "releasebench-route"

INTENT_TO_LEAF = {
    "prepare-repository": "releasebench-prepare-repository",
    "audit-repository": "releasebench-audit-repository",
    "scan-secrets": "releasebench-scan-secrets",
    "scaffold-governance": "releasebench-scaffold-governance",
    "showcase-readme": "releasebench-showcase-readme",
    "publish-repository": "releasebench-publish-repository",
    "release-version": "releasebench-release-version",
    "prepare-package": "releasebench-prepare-package",
    "document-config": "releasebench-document-config",
}

DISPATCHABLE_LEAVES = tuple(INTENT_TO_LEAF.values())
FULL_FLOW_ORDER = (
    "releasebench-prepare-repository",
    "releasebench-showcase-readme",
    "releasebench-release-version",
    "releasebench-publish-repository",
    "releasebench-prepare-package",
)

CLOSED_ACTIONS = (
    "remote-project-creation-and-first-push",
    "host-visibility-metadata-topics-avatar-writes",
    "host-public-api-and-network-verification",
    "local-tag-creation-and-outward-tag-push",
    "host-release-creation-or-backfill",
    "package-registry-name-availability-reads",
    "package-publication",
    "remote-image-reachability-checks",
)


class ContractError(ValueError):
    """A malformed request that cannot produce a trustworthy receipt."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _validate_request(request: dict[str, Any]) -> None:
    allowed = {
        "contract_version",
        "request_id",
        "intents",
        "explicit_leaf",
        "full_flow",
        "completed_leaves",
        "not_applicable_leaves",
    }
    extra = sorted(set(request) - allowed)
    if extra:
        raise ContractError("UNDECLARED_FIELD", ",".join(extra))
    if request.get("contract_version") != CONTRACT_VERSION:
        raise ContractError("CONTRACT_VERSION_MISMATCH", "unsupported contract_version")
    if not isinstance(request.get("request_id"), str) or not request["request_id"].strip():
        raise ContractError("INVALID_REQUEST_ID", "request_id must be a non-empty string")

    intents = request.get("intents", [])
    if not isinstance(intents, list) or any(not isinstance(item, str) for item in intents):
        raise ContractError("INVALID_INTENTS", "intents must be a string array")
    unknown_intents = sorted(set(intents) - set(INTENT_TO_LEAF))
    if unknown_intents:
        raise ContractError("UNKNOWN_INTENT", ",".join(unknown_intents))
    if len(intents) != len(set(intents)):
        raise ContractError("DUPLICATE_INTENT", "intents must be unique")

    explicit_leaf = request.get("explicit_leaf")
    if explicit_leaf is not None and explicit_leaf not in DISPATCHABLE_LEAVES:
        raise ContractError("UNKNOWN_OR_RECURSIVE_LEAF", str(explicit_leaf))

    for field in ("completed_leaves", "not_applicable_leaves"):
        leaves = request.get(field, [])
        if not isinstance(leaves, list) or any(not isinstance(item, str) for item in leaves):
            raise ContractError("INVALID_LEAF_SET", field)
        unknown = sorted(set(leaves) - set(DISPATCHABLE_LEAVES))
        if unknown:
            raise ContractError("UNKNOWN_LEAF_STATE", f"{field}:{','.join(unknown)}")
        if len(leaves) != len(set(leaves)):
            raise ContractError("DUPLICATE_LEAF_STATE", field)

    if set(request.get("completed_leaves", [])) & set(request.get("not_applicable_leaves", [])):
        raise ContractError("CONFLICTING_LEAF_STATE", "a leaf cannot be complete and not applicable")
    if not isinstance(request.get("full_flow", False), bool):
        raise ContractError("INVALID_FULL_FLOW", "full_flow must be boolean")


def _receipt(
    request: dict[str, Any],
    *,
    leaf_id: str | None,
    reason_code: str,
    considered: list[str],
) -> dict[str, Any]:
    decision = "selected" if leaf_id else "no-safe-route"
    payload: dict[str, Any] = {
        "receipt_version": RECEIPT_VERSION,
        "request_id": request["request_id"],
        "router_id": ROUTER_ID,
        "decision": decision,
        "leaf_id": leaf_id,
        "reason_code": reason_code,
        "considered_leaves": considered,
        "authority_state": "candidate-inactive",
        "visibility_state": "private-prepublic",
        "outward_actions_authorized": False,
        "outward_actions_executed": False,
        "closed_actions": list(CLOSED_ACTIONS),
    }
    payload["receipt_sha256"] = canonical_sha256(payload)
    return payload


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ContractError("REQUEST_NOT_OBJECT", "request must be a JSON object")
    _validate_request(request)

    explicit_leaf = request.get("explicit_leaf")
    intents = request.get("intents", [])
    full_flow = request.get("full_flow", False)

    if explicit_leaf is not None:
        inferred = {INTENT_TO_LEAF[item] for item in intents}
        if inferred and inferred != {explicit_leaf}:
            return _receipt(
                request,
                leaf_id=None,
                reason_code="AMBIGUOUS_EXPLICIT_AND_INTENT",
                considered=sorted({explicit_leaf, *inferred}),
            )
        return _receipt(
            request,
            leaf_id=explicit_leaf,
            reason_code="EXPLICIT_LEAF",
            considered=[explicit_leaf],
        )

    if full_flow:
        if intents:
            return _receipt(
                request,
                leaf_id=None,
                reason_code="AMBIGUOUS_FULL_FLOW_AND_DIRECT_INTENT",
                considered=sorted({INTENT_TO_LEAF[item] for item in intents}),
            )
        completed = set(request.get("completed_leaves", []))
        not_applicable = set(request.get("not_applicable_leaves", []))
        remaining = [leaf for leaf in FULL_FLOW_ORDER if leaf not in completed | not_applicable]
        if not remaining:
            return _receipt(
                request,
                leaf_id=None,
                reason_code="FULL_FLOW_LOCAL_STAGES_COMPLETE",
                considered=list(FULL_FLOW_ORDER),
            )
        return _receipt(
            request,
            leaf_id=remaining[0],
            reason_code="FIRST_INCOMPLETE_FULL_FLOW_STAGE",
            considered=remaining,
        )

    inferred = sorted({INTENT_TO_LEAF[item] for item in intents})
    if len(inferred) == 1:
        return _receipt(
            request,
            leaf_id=inferred[0],
            reason_code="ONE_DIRECT_INTENT",
            considered=inferred,
        )
    if len(inferred) > 1:
        return _receipt(
            request,
            leaf_id=None,
            reason_code="AMBIGUOUS_MULTIPLE_INTENTS",
            considered=inferred,
        )
    return _receipt(
        request,
        leaf_id=None,
        reason_code="INSUFFICIENT_ROUTING_EVIDENCE",
        considered=[],
    )


def main() -> int:
    try:
        raw = sys.stdin.buffer.read() if len(sys.argv) == 1 or sys.argv[1] == "-" else open(sys.argv[1], "rb").read()
        request = json.loads(raw.decode("utf-8"))
        result = dispatch(request)
    except ContractError as exc:
        sys.stderr.write(f"{exc.code}: {exc}\n")
        return 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"INVALID_JSON: {exc}\n")
        return 2
    sys.stdout.buffer.write(canonical_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
