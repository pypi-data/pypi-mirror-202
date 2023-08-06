"""
A module implementing a configuration interface for the package.
"""

# built-in
from contextlib import suppress
from dataclasses import dataclass
from os.path import expandvars
from pathlib import Path
from shutil import copyfile
from typing import Any, Dict, List, Set, cast

# third-party
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io.types import JsonObject as _JsonObject
from vcorelib.logging import LoggerType
from vcorelib.paths import rel

# internal
from rcmpy.schemas import RcmpyDictCodec as _RcmpyDictCodec


@dataclass
class ManagedFile:
    """
    A data structure for managed files specified in the configuration data.
    """

    template: str
    extra_templates: Set[str]

    directory: Path
    name: str

    link: bool

    @property
    def output(self) -> Path:
        """Get the full output path."""
        return self.directory.joinpath(self.name)

    def update_root(self, root: Path) -> None:
        """
        If the output directory is a relative path, update it to be an
        absolute one based on the provided root directory.
        """

        if not self.directory.is_absolute():
            self.directory = root.joinpath(self.directory)
            assert self.directory.is_absolute(), self.directory

    def update(self, source: Path, logger: LoggerType) -> None:
        """Update this managed file based on the provided source file."""

        output = self.output

        # At some point this could be skipped for existing symlinks.
        with suppress(FileNotFoundError):
            output.unlink()

        # Ensure the output directory exists.
        self.directory.mkdir(parents=True, exist_ok=True)

        if self.link:
            output.symlink_to(source)
        else:
            copyfile(source, output)

        logger.info("'%s' -> '%s'.", rel(source), rel(output))


FilesConfig = List[Dict[str, Any]]


class Config(_RcmpyDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""

    def update_root(self, root: Path) -> None:
        """Call 'update_root' for each managed file."""

        for file in self.files:
            file.update_root(root)

    def init(self, data: _JsonObject) -> None:
        """Initialize this instance."""
        self.data = data

        # A set of templates that are used by this config.
        self.templates: Set[str] = set()

        self.files: List[ManagedFile] = []
        for file in cast(FilesConfig, data.get("files", [])):
            new = ManagedFile(
                file["template"],
                set(file.get("extra_templates", [])),
                # Resolve environment variables and any '~' here.
                Path(expandvars(file["directory"])).expanduser(),
                file.get("name", file["template"]),
                file["link"],
            )

            # Keep track of all templates used in any file.
            self.templates.add(new.template)
            for template in new.extra_templates:
                self.templates.add(template)

            self.files.append(new)

    def asdict(self) -> _JsonObject:
        """Obtain a dictionary representing this instance."""
        return self.data
