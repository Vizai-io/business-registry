"""Build deterministic manifests and snapshots for the public registry."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import tarfile
from pathlib import Path
from typing import Any, Iterable


MANIFEST_PATH = Path("manifest/registry-manifest.json")
SNAPSHOT_NAME = "registry-snapshot.tar.gz"
CHECKSUMS_NAME = "SHA256SUMS"
DIST_MANIFEST_NAME = "registry-manifest.json"
HASH_ALGORITHM = "sha256"
CANONICALIZATION = "vizai-canonical-json-v1"
PUBLIC_ROOT_ARTIFACTS = (
    "LICENSE",
    "LICENSE-CODE",
    "LICENSE-DATA",
    "NOTICE",
)


def sha256_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def raw_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize the registry's cross-language canonical JSON representation."""
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _media_type(path: Path) -> str:
    if path.suffix == ".json":
        return "application/json"
    if path.suffix == ".jsonl":
        return "application/x-ndjson"
    return "text/plain"


def discover_public_artifacts(root: Path | str) -> list[Path]:
    """Return the deterministic public artifact set, excluding the manifest."""
    root = Path(root).resolve()
    candidates: list[Path] = []
    for filename in PUBLIC_ROOT_ARTIFACTS:
        path = root / filename
        if path.is_file():
            candidates.append(path)

    patterns = (
        "schema/*.schema.json",
        "registry/*/profile.json",
        "provenance/*/publication-receipt.json",
        "index/*.json",
        "index/*.jsonl",
    )
    for pattern in patterns:
        candidates.extend(path for path in root.glob(pattern) if path.is_file())

    return sorted(
        set(candidates),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def build_manifest(root: Path | str) -> dict[str, Any]:
    root = Path(root).resolve()
    artifacts = []
    for path in discover_public_artifacts(root):
        relative = path.relative_to(root).as_posix()
        artifacts.append(
            {
                "path": relative,
                "mediaType": _media_type(path),
                "bytes": path.stat().st_size,
                "sha256": raw_sha256(path),
            }
        )
    return {
        "schemaVersion": "1.0",
        "manifestType": "vizai-public-registry",
        "hashAlgorithm": HASH_ALGORITHM,
        "canonicalization": CANONICALIZATION,
        "artifactCount": len(artifacts),
        "artifacts": artifacts,
    }


def manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def write_manifest(root: Path | str) -> Path:
    root = Path(root).resolve()
    target = root / MANIFEST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(manifest_bytes(build_manifest(root)))
    return target


def manifest_errors(root: Path | str) -> list[str]:
    root = Path(root).resolve()
    target = root / MANIFEST_PATH
    if not target.is_file():
        return [f"Missing deterministic manifest: {MANIFEST_PATH.as_posix()}."]
    expected = manifest_bytes(build_manifest(root))
    actual = target.read_bytes()
    if actual != expected:
        return [
            "Committed registry manifest differs from the deterministic "
            "public-artifact build."
        ]
    return []


def _tar_info(relative: str, size: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(relative)
    info.size = size
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    return info


def _write_reproducible_tar_gz(
    target: Path,
    entries: Iterable[tuple[str, bytes]],
) -> None:
    with target.open("wb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw,
            compresslevel=9,
            mtime=0,
        ) as compressed:
            with tarfile.open(
                fileobj=compressed,
                mode="w",
                format=tarfile.USTAR_FORMAT,
            ) as archive:
                for relative, data in sorted(entries):
                    archive.addfile(_tar_info(relative, len(data)), fileobj=_Bytes(data))


class _Bytes:
    """Minimal read-only byte stream accepted by TarFile.addfile."""

    def __init__(self, data: bytes):
        self._data = data
        self._offset = 0

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self._data) - self._offset
        start = self._offset
        end = min(len(self._data), start + size)
        self._offset = end
        return self._data[start:end]


def build_snapshot(
    root: Path | str,
    output_directory: Path | str,
) -> dict[str, str]:
    """Build a byte-reproducible snapshot plus checksums for attestation."""
    root = Path(root).resolve()
    output_directory = Path(output_directory).resolve()
    errors = manifest_errors(root)
    if errors:
        raise ValueError(" ".join(errors))

    output_directory.mkdir(parents=True, exist_ok=True)
    manifest_source = root / MANIFEST_PATH
    manifest_target = output_directory / DIST_MANIFEST_NAME
    shutil.copyfile(manifest_source, manifest_target)

    entries = [
        (path.relative_to(root).as_posix(), path.read_bytes())
        for path in discover_public_artifacts(root)
    ]
    entries.append((MANIFEST_PATH.as_posix(), manifest_source.read_bytes()))

    snapshot_path = output_directory / SNAPSHOT_NAME
    _write_reproducible_tar_gz(snapshot_path, entries)

    subjects = (snapshot_path, manifest_target)
    checksums_path = output_directory / CHECKSUMS_NAME
    checksums_path.write_text(
        "".join(
            f"{raw_sha256(path).removeprefix('sha256:')} *{path.name}\n"
            for path in subjects
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "snapshot": str(snapshot_path),
        "manifest": str(manifest_target),
        "checksums": str(checksums_path),
        "snapshotSha256": raw_sha256(snapshot_path),
    }
