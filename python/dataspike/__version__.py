import importlib.resources
import sys


def read_from_file(package: str, resource: str, encoding: str = "utf-8", errors: str = "strict") -> str:
    try:
        if sys.version_info >= (3, 9):
            with (importlib.resources.files(package) / resource).open("r", encoding=encoding, errors=errors) as f:
                return f.read().strip()
        else:
            return importlib.resources.read_text(package, resource, encoding, errors).strip()
    except FileNotFoundError:
        return "0.0.0"
    except AttributeError:
        return "0.0.0"


def read_version() -> str:
    try:
        from importlib.metadata import version, PackageNotFoundError

        try:
            return version(__package__ or "dataspike")
        except PackageNotFoundError:
            return read_from_file("dataspike", "VERSION")
    except ImportError:
        return read_from_file("dataspike", "VERSION")


__version__ = read_version()
