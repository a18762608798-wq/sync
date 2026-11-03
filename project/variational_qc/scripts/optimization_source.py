"""Validate the single formal Exp04 parameter source and its identity."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

OPTIMIZATION_PROTOCOL = "independent-global-lbfgs-v1"


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def array_sha256(values) -> str:
    return hashlib.sha256(np.asarray(values, dtype="<f8").tobytes()).hexdigest()


def json_sha256(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def protocol_of(archive) -> str:
    if "optimization_protocol" not in archive:
        raise ValueError("Exp04 parameter source has no optimization protocol; retired data refused")
    return np.asarray(archive["optimization_protocol"], dtype=np.uint8).tobytes().decode("ascii")


def validate_s06(path: str | Path):
    path = Path(path)
    archive = np.load(path, allow_pickle=False)
    if protocol_of(archive) != OPTIMIZATION_PROTOCOL:
        archive.close()
        raise ValueError("Retired Exp04 optimization protocol refused")
    manifest_path = path.with_name("exp04_manifest.json")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema") != "exp04/v2" or manifest.get("optimization_protocol") != OPTIMIZATION_PROTOCOL:
        archive.close()
        raise ValueError("Exp04 manifest does not identify the current independent optimizer")
    return archive


def source_identity(s06_path: str | Path, s04_path: str | Path) -> dict:
    with validate_s06(s06_path):
        pass
    return {"optimization_protocol": OPTIMIZATION_PROTOCOL,
            "s06_sha256": file_sha256(s06_path),
            "s06_manifest_sha256": file_sha256(Path(s06_path).with_name("exp04_manifest.json")),
            "s04_sha256": file_sha256(s04_path)}


def require_same_provenance(actual: dict | None, expected: dict, where: str) -> None:
    if actual != expected:
        raise ValueError(f"{where}: batch or parameter provenance differs; resume refused")
