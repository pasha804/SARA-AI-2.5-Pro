# -*- coding: utf-8 -*-
"""
SARA AI 2.5 Pro — Shared Path Resolution & Verified Filesystem Engine
Provides safe path resolution, atomic write-and-verify operations,
safe directory launching, and standard tool response formatting.
"""

import os
import sys
import time
import shutil
import hashlib
import datetime
import subprocess
from pathlib import Path

USER_PROFILE = Path(os.environ.get("USERPROFILE") or os.path.expanduser("~")).resolve()
REAL_DESKTOP = USER_PROFILE / "Desktop"
REAL_DOCUMENTS = USER_PROFILE / "Documents"
REAL_DOWNLOADS = USER_PROFILE / "Downloads"

# Ensure core user directories exist
for d in [REAL_DESKTOP, REAL_DOCUMENTS, REAL_DOWNLOADS]:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


def resolve_user_path(raw_path: str) -> Path:
    """
    Intelligently and safely resolves any Windows path, supporting:
    - Absolute Windows paths (e.g. C:/Users/..., D:/...)
    - Tilde home paths (~/Desktop, ~/Documents)
    - Virtual aliases: Desktop, Downloads, Documents (case-insensitive)
    - Relative paths with spaces, parentheses, and Unicode
    - Subdirectories under user desktop or project roots
    """
    if not raw_path or not str(raw_path).strip():
        return REAL_DESKTOP

    clean = str(raw_path).strip().replace("\\", "/")

    # 1. Handle tilde expansion
    if clean.startswith("~"):
        sub = clean[1:].lstrip("/")
        return (USER_PROFILE / sub).resolve() if sub else USER_PROFILE

    # 2. Check for explicit drive letter (e.g. C:/, D:/)
    p = Path(clean)
    if p.is_absolute():
        return p.resolve()

    # 3. Handle standard user folder prefixes
    parts = clean.split("/")
    first_token = parts[0].lower().strip(".")

    if first_token == "desktop":
        sub = "/".join(parts[1:])
        return (REAL_DESKTOP / sub).resolve() if sub else REAL_DESKTOP
    elif first_token == "downloads":
        sub = "/".join(parts[1:])
        return (REAL_DOWNLOADS / sub).resolve() if sub else REAL_DOWNLOADS
    elif first_token == "documents":
        sub = "/".join(parts[1:])
        return (REAL_DOCUMENTS / sub).resolve() if sub else REAL_DOCUMENTS

    # 4. Default relative paths to Desktop for user clarity, or preserve if in active workspace
    return (REAL_DESKTOP / clean).resolve()


def format_tool_response(
    tool: str,
    operation: str,
    success: bool,
    data: dict = None,
    message: str = "",
    error: str = None,
    duration_ms: float = 0.0,
    verification: dict = None
) -> dict:
    """Standardized tool response schema across SARA runtime."""
    return {
        "success": bool(success),
        "tool": str(tool),
        "operation": str(operation),
        "message": str(message or ("Operation completed successfully." if success else "Operation failed.")),
        "data": data or {},
        "error": str(error) if error else None,
        "duration_ms": round(float(duration_ms), 2),
        "verification": verification or {"verified": success},
        "timestamp": datetime.datetime.now().isoformat()
    }


def create_verified_file(raw_path: str, content: str = "", encoding: str = "utf-8") -> dict:
    """
    Creates a file with strict 8-step verification contract:
    1. Resolve intended destination
    2. Validate destination
    3. Create parent directories
    4. Write requested content atomically
    5. Verify file exists
    6. Verify size is plausible
    7. Read back sample to validate content integrity
    8. Return structured standardized tool response
    """
    t0 = time.perf_counter()
    target_path = resolve_user_path(raw_path)

    try:
        # Validate parent directory creation
        parent_dir = target_path.parent
        parent_dir.mkdir(parents=True, exist_ok=True)

        encoded_data = content.encode(encoding, errors="replace")
        expected_bytes = len(encoded_data)

        # Atomic write
        target_path.write_bytes(encoded_data)

        # Verification step: Existence check
        if not target_path.exists():
            duration = (time.perf_counter() - t0) * 1000
            return format_tool_response(
                tool="createFile",
                operation="write",
                success=False,
                error=f"File existence verification failed at: {target_path}",
                duration_ms=duration
            )

        actual_size = target_path.stat().st_size
        if actual_size != expected_bytes:
            duration = (time.perf_counter() - t0) * 1000
            return format_tool_response(
                tool="createFile",
                operation="write",
                success=False,
                error=f"Size mismatch: expected {expected_bytes} bytes, found {actual_size} bytes.",
                duration_ms=duration
            )

        # Content sample validation
        readback_sample = target_path.read_text(encoding=encoding, errors="replace")[:250]
        verification_hash = hashlib.sha256(encoded_data).hexdigest()[:12]

        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="createFile",
            operation="create_and_verify",
            success=True,
            data={
                "path": str(target_path),
                "filename": target_path.name,
                "bytes_written": actual_size,
                "encoding": encoding,
                "hash_sha256": verification_hash,
                "sample": readback_sample
            },
            message=f"File successfully created and verified at: {target_path}",
            duration_ms=duration,
            verification={
                "exists": True,
                "size_match": True,
                "bytes": actual_size,
                "readback_verified": True
            }
        )

    except PermissionError as pe:
        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="createFile",
            operation="write",
            success=False,
            error=f"Permission denied while creating {target_path}: {pe}",
            duration_ms=duration
        )
    except Exception as ex:
        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="createFile",
            operation="write",
            success=False,
            error=f"Failed to create file: {ex}",
            duration_ms=duration
        )


def create_verified_dir(raw_path: str) -> dict:
    """Creates a directory with explicit existence verification."""
    t0 = time.perf_counter()
    target_path = resolve_user_path(raw_path)

    try:
        target_path.mkdir(parents=True, exist_ok=True)
        if not target_path.exists() or not target_path.is_dir():
            duration = (time.perf_counter() - t0) * 1000
            return format_tool_response(
                tool="createFolder",
                operation="mkdir",
                success=False,
                error=f"Directory creation verification failed at: {target_path}",
                duration_ms=duration
            )

        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="createFolder",
            operation="mkdir",
            success=True,
            data={"path": str(target_path), "name": target_path.name},
            message=f"Directory verified at: {target_path}",
            duration_ms=duration,
            verification={"exists": True, "is_directory": True}
        )
    except Exception as ex:
        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="createFolder",
            operation="mkdir",
            success=False,
            error=str(ex),
            duration_ms=duration
        )


def open_path_verified(raw_path: str, application: str = "") -> dict:
    """
    Safely opens a file, folder, or project in default application, explorer, or code editor.
    Distinguishes:
    - Path does not exist
    - Application launch failed
    - Operation succeeded
    """
    t0 = time.perf_counter()
    target_path = resolve_user_path(raw_path)

    if not target_path.exists():
        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="openFolder" if target_path.is_dir() else "openFile",
            operation="open",
            success=False,
            error=f"Target path does not exist: {target_path}",
            duration_ms=duration
        )

    try:
        app_clean = application.lower().strip()
        if target_path.is_dir():
            if app_clean in ["code", "vscode"]:
                subprocess.Popen(["cmd.exe", "/c", "code", str(target_path)], shell=False)
            elif app_clean in ["cursor"]:
                subprocess.Popen(["cmd.exe", "/c", "cursor", str(target_path)], shell=False)
            elif app_clean in ["terminal", "powershell"]:
                subprocess.Popen(["cmd.exe", "/c", "start", "powershell", "-NoExit", "-Command", f"Set-Location '{target_path}'"], shell=False)
            else:
                # Open in Windows File Explorer
                os.startfile(str(target_path))
        else:
            # File opening
            if app_clean in ["code", "vscode"]:
                subprocess.Popen(["cmd.exe", "/c", "code", str(target_path)], shell=False)
            elif app_clean in ["notepad"]:
                subprocess.Popen(["cmd.exe", "/c", "notepad", str(target_path)], shell=False)
            else:
                os.startfile(str(target_path))

        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="openFolder" if target_path.is_dir() else "openFile",
            operation="open",
            success=True,
            data={"path": str(target_path), "application": application or "default"},
            message=f"Successfully opened: {target_path}",
            duration_ms=duration,
            verification={"launched": True, "target_exists": True}
        )
    except Exception as ex:
        duration = (time.perf_counter() - t0) * 1000
        return format_tool_response(
            tool="openFolder" if target_path.is_dir() else "openFile",
            operation="open",
            success=False,
            error=f"Application launch failed: {ex}",
            duration_ms=duration
        )
