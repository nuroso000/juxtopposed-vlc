#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Created 2026-10-24 for the macOS redesign build.
"""Create a build-local Qt header view for moc on macOS; never edit the SDK."""
from pathlib import Path
import sys

library, headers, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
modules = {path.stem: path / "Headers" for path in library.glob("Qt*.framework")
           if (path / "Headers").is_dir()}
for path in headers.glob("Qt*"):
    if path.is_dir():
        modules.setdefault(path.name, path)
for name, target in modules.items():
    link = output / name
    if link.is_symlink():
        if link.resolve() == target.resolve():
            continue
        link.unlink()
    elif link.exists():
        raise SystemExit(f"Refusing to replace a non-symlink: {link}")
    link.symlink_to(target.resolve(), target_is_directory=True)
