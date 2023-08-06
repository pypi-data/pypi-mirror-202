"""Define package contents."""
import importlib.resources
import json
import typing


class PackageMetadata(typing.TypedDict):
    """Define keys and types of corresponding values for package metadata."""

    Name: str
    Version: str


METADATA_CONTENTS: str = (
    importlib.resources.files("package_name_to_import_with").joinpath("metadata.json").read_text()
)
METADATA: PackageMetadata = json.loads(METADATA_CONTENTS)
