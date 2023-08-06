"""Scratch Cache."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.0.1"

import logging
import hashlib
import os
import shutil
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)
# Set default logging handler to avoid "No handler found" warnings.
logger.addHandler(logging.NullHandler())


def local_machine_cache(
    fname: Union[str, Path], local_machine_cache_dir: Union[str, Path]
) -> Path:
    """Local disk read cache for network drive files.
    Replace a network drive filename with a local cached version if it exists.
    Create or update local cached version as needed.
    For reading only; don't use for writing."""

    # Defensive cast
    fname = Path(fname)
    local_machine_cache_dir = Path(local_machine_cache_dir)

    if not fname.exists():
        raise FileNotFoundError(f"{fname} does not exist.")

    # Create local cached filename
    hashed_fname = hashlib.sha224(str(fname).encode()).hexdigest()
    # Preserve entire file extension, because some libraries will vary how they read a file based on file extension
    all_file_extensions = "".join(
        fname.suffixes
    )  # might be empty string if no dot in name
    local_machine_cache_dir.mkdir(exist_ok=True, parents=True)
    local_fname = local_machine_cache_dir / f"{hashed_fname}{all_file_extensions}"

    def do_mtimes_match(f1, f2):
        # alternative: path.stat().st_mtime
        return os.path.getmtime(f1) == os.path.getmtime(f2)

    needs_update = False
    if not local_fname.exists():
        needs_update = True
    else:
        if not do_mtimes_match(fname, local_fname):
            needs_update = True

    if needs_update:
        # Cache miss. Need to update local cache
        # Copy file while preserving mtime:
        logger.info(
            f"Caching network file to local machine cache: {fname} -> {local_fname}"
        )
        shutil.copy2(fname, local_fname)
        if not do_mtimes_match(fname, local_fname):
            # sanity check
            logger.warning(
                f"Copied network file to local machine cache but mtime changed: {fname} -> {local_fname}"
            )
    else:
        logger.info(
            f"Reading network file from local machine cache: {fname} -> {local_fname}"
        )

    return local_fname
