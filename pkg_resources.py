"""
Compatibility shim for environments where setuptools no longer provides
pkg_resources (for example newer Python build setups).

Provides a minimal subset required by:
- adbutils (resource_filename, get_distribution, parse_version)
- PyInstaller runtime hook pyi_rth_pkgres (NullProvider and registration APIs)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from importlib import metadata
from importlib import resources


class DistributionNotFound(Exception):
    """Raised when a distribution cannot be located."""


@dataclass(frozen=True)
class Distribution:
    version: str


_loader_type_registry = {}
_finder_registry = {}


def get_distribution(dist_name: str) -> Distribution:
    """Return an object with a .version attribute, like pkg_resources."""
    try:
        return Distribution(version=metadata.version(dist_name))
    except metadata.PackageNotFoundError as exc:
        raise DistributionNotFound(str(exc)) from exc


def parse_version(version: str):
    """
    Parse a version for comparisons.
    Uses stdlib fallback to avoid extra dependency requirements.
    """
    try:
        from packaging.version import parse as _parse

        return _parse(version)
    except Exception:
        # Fallback parser that keeps comparison working in simple cases.
        chunks = []
        for part in version.replace("-", ".").split("."):
            chunks.append(int(part) if part.isdigit() else part.lower())
        return tuple(chunks)


class NullProvider:
    """
    Basic provider compatible with PyInstaller's runtime hook expectations.
    """

    def __init__(self, module):
        self.module = module
        module_file = getattr(module, "__file__", "") or ""
        self.module_path = os.path.dirname(module_file)
        self.loader = getattr(module, "__loader__", None)

    def _get(self, path: str) -> bytes:
        if self.loader and hasattr(self.loader, "get_data"):
            return self.loader.get_data(path)
        with open(path, "rb") as f:
            return f.read()

    def _has(self, path: str) -> bool:
        return os.path.exists(path)

    def _isdir(self, path: str) -> bool:
        return os.path.isdir(path)

    def _listdir(self, path: str):
        if os.path.isdir(path):
            return os.listdir(path)
        return []


def register_loader_type(loader_type, provider_factory):
    _loader_type_registry[loader_type] = provider_factory


def register_finder(importer_type, finder):
    _finder_registry[importer_type] = finder


def find_on_path(*_args, **_kwargs):
    return []


def _initialize_master_working_set():
    # Hook compatibility no-op.
    return None


def resource_filename(package_or_requirement: str, resource_name: str) -> str:
    """
    Return a file-system path to a package resource.
    """
    return str(resources.files(package_or_requirement).joinpath(resource_name))
