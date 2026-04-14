# Copyright (c) 2026 Harness Solution Factory. All Rights Reserved.
#!/bin/python
"""
OpenAPI Path Filter — processes a normalized Harness OpenAPI spec, strips Beta
endpoints and tags, groups the surviving paths by root anchor, and writes the
artefacts needed by downstream agent-developer tooling.

Entry point: FilterManager.run()
Outputs (relative to OUTPUT_DIR env var, default ./openapi/tmp):
  - filtered-tags-valid.json
  - filtered-tags-rejected.json
  - filtered-paths-valid.json
  - filtered-paths-rejected.json
  - filtered-paths-missing.json
  - processed-paths-valid.json          ← organised by root anchor
  - ../normalized-api-payload.json      ← final merged payload
"""

import json
import logging
import sys
from os import environ
from pathlib import Path
from sys import stdout
from typing import Any


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class FilterBaseException(Exception):
    """Base for all filter-pipeline exceptions."""


class ConfigException(FilterBaseException):
    """Invalid or missing configuration."""


class InputException(FilterBaseException):
    """Input file cannot be located or parsed."""


class ProcessingException(FilterBaseException):
    """Unexpected state reached during processing."""


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_INPUT_FILE = "openapi/harness-openapi-normalized.json"
DEFAULT_OUTPUT_DIR = "openapi/logs"
DEFAULT_FINAL_OUTPUT = "openapi/normalized-api-payload.json"
BETA_MARKER = "[Beta]"


class FilterConfig:
    """Centralises runtime configuration for the filter pipeline."""

    def __init__(self) -> None:
        self.input_file = Path(environ.get("PLUGIN_INPUT_FILE", DEFAULT_INPUT_FILE))
        self.output_dir = Path(environ.get("PLUGIN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
        self.final_output = Path(environ.get("PLUGIN_FINAL_OUTPUT", DEFAULT_FINAL_OUTPUT))
        self.debug = environ.get("PLUGIN_DEBUG_MODE", "false").lower() == "true"

    def return_logging_instance(self, name: str) -> logging.Logger:
        """Create and return a configured logger for *name*."""
        logging.basicConfig(
            stream=stdout,
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger = logging.getLogger(name)
        if self.debug:
            logger.setLevel(logging.DEBUG)
        return logger

    def validate(self) -> None:
        """Raise ConfigException if any required path is not usable."""
        if not self.input_file.exists():
            raise ConfigException(
                f"Input file not found: {self.input_file}"
            )
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.final_output.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Entity: wraps a single raw tag object
# ---------------------------------------------------------------------------

class TagEntity:
    """Represents a single OpenAPI tag entry."""

    def __init__(self, raw: dict) -> None:
        self.raw = raw
        self.name: str = raw.get("name", "")
        self.display_name: str = raw.get("x-displayName", "")
        self.description: str = raw.get("description", "")

    def is_beta(self) -> bool:
        """Return True when this tag is marked as Beta in any field."""
        return (
            BETA_MARKER in self.display_name
            or BETA_MARKER in self.description
        )


# ---------------------------------------------------------------------------
# Manager: tag filtering
# ---------------------------------------------------------------------------

class TagFilterManager:
    """Filters OpenAPI tags into valid and rejected sets."""

    def __init__(self, config: FilterConfig) -> None:
        self.config = config
        self.logger = config.return_logging_instance(__name__)

    def filter(self, raw_tags: list[dict]) -> tuple[list[str], list[str]]:
        """
        Partition *raw_tags* into (valid_names, rejected_names).

        Returns two lists of tag name strings so downstream path filtering
        can use simple set membership checks.
        """
        valid_names: list[str] = []
        rejected: list[dict] = []

        for raw in raw_tags:
            entity = TagEntity(raw)
            if entity.is_beta():
                self.logger.debug("Rejecting beta tag: %s", entity.name)
                rejected.append(raw)
            else:
                valid_names.append(entity.name)

        self._write_json(
            self.config.output_dir / "filtered-tags-valid.json",
            valid_names,
        )
        self._write_json(
            self.config.output_dir / "filtered-tags-rejected.json",
            rejected,
        )

        rejected_names = [t.get("name", "") for t in rejected]

        self.logger.info(
            "Tags — accepted: %d  rejected: %d  total: %d",
            len(valid_names),
            len(rejected_names),
            len(valid_names) + len(rejected_names),
        )

        return valid_names, rejected_names

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _write_json(self, path: Path, data: Any) -> None:
        with open(path, mode="w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4, sort_keys=True, ensure_ascii=False)
        self.logger.debug("Wrote %s", path)


# ---------------------------------------------------------------------------
# Manager: path filtering
# ---------------------------------------------------------------------------

class PathFilterManager:
    """Filters OpenAPI paths against a set of rejected tag names."""

    def __init__(self, config: FilterConfig) -> None:
        self.config = config
        self.logger = config.return_logging_instance(__name__)

    def filter(
        self,
        raw_paths: dict[str, Any],
        rejected_tags: list[str],
    ) -> dict[str, Any]:
        """
        Return only the paths that are not Beta.

        A path is rejected when *any* HTTP-method block within it:
          - has BETA_MARKER in its summary or description, or
          - has a tag whose name contains BETA_MARKER, or
          - has all its tags in *rejected_tags*.
        """
        rejected_tag_set = set(rejected_tags)
        valid_paths: dict[str, Any] = {}
        rejected_paths: dict[str, Any] = {}

        self.logger.info("Processing %d raw paths", len(raw_paths))

        for path_key, path_value in raw_paths.items():
            if self._is_path_rejected(path_key, path_value, rejected_tag_set):
                rejected_paths[path_key] = path_value
            else:
                valid_paths[path_key] = path_value

        valid_paths = dict(sorted(valid_paths.items()))
        rejected_paths = dict(sorted(rejected_paths.items()))

        self._write_json(
            self.config.output_dir / "filtered-paths-valid.json",
            valid_paths,
        )
        self._write_json(
            self.config.output_dir / "filtered-paths-rejected.json",
            rejected_paths,
        )
        self._write_json(
            self.config.output_dir / "filtered-paths-missing.json",
            {},  # reserved for future gap-analysis
        )

        self.logger.info(
            "Paths — accepted: %d  rejected: %d  total: %d",
            len(valid_paths),
            len(rejected_paths),
            len(valid_paths) + len(rejected_paths),
        )

        return valid_paths

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_path_rejected(
        self,
        path_key: str,
        path_value: dict,
        rejected_tag_set: set[str],
    ) -> bool:
        """Return True if the path should be excluded from the output."""
        for method_block in path_value.values():
            if not isinstance(method_block, dict):
                continue

            if BETA_MARKER in method_block.get("summary", ""):
                self.logger.debug("Rejecting (summary) %s", path_key)
                return True

            if BETA_MARKER in method_block.get("description", ""):
                self.logger.debug("Rejecting (description) %s", path_key)
                return True

            tags: list[str] = method_block.get("tags", [])

            if any(BETA_MARKER in t for t in tags):
                self.logger.debug("Rejecting (beta tag literal) %s", path_key)
                return True

            if tags and set(tags).issubset(rejected_tag_set):
                self.logger.debug("Rejecting (all tags rejected) %s", path_key)
                return True

        return False

    def _write_json(self, path: Path, data: Any) -> None:
        with open(path, mode="w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4, sort_keys=True, ensure_ascii=False)
        self.logger.debug("Wrote %s", path)


# ---------------------------------------------------------------------------
# Manager: path organisation
# ---------------------------------------------------------------------------

class PathOrganiserManager:
    """Groups valid paths by root anchor and merges with API components."""

    def __init__(self, config: FilterConfig) -> None:
        self.config = config
        self.logger = config.return_logging_instance(__name__)

    def organise(
        self,
        payload: dict[str, Any],
        valid_paths: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Bucket *valid_paths* by the first URL segment (root anchor), attach
        the original *components* block, and return the merged object.
        """
        output_paths: dict[str, dict] = {}

        for path_key, path_value in valid_paths.items():
            parts = Path(path_key).parts
            root_anchor = parts[1] if len(parts) > 1 else path_key
            output_paths.setdefault(root_anchor, {}).update({path_key: path_value})

        output_object: dict[str, Any] = {
            "paths": output_paths,
            "components": payload.get("components", {}),
        }

        self._write_json(
            self.config.output_dir / "processed-paths-valid.json",
            output_object,
        )
        self._write_json(self.config.final_output, output_object)

        self.logger.info(
            "Organised %d paths across %d root anchors",
            len(valid_paths),
            len(output_paths),
        )

        return output_object

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _write_json(self, path: Path, data: Any) -> None:
        with open(path, mode="w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4, sort_keys=True, ensure_ascii=False)
        self.logger.debug("Wrote %s", path)


# ---------------------------------------------------------------------------
# Top-level pipeline manager
# ---------------------------------------------------------------------------

class FilterManager:
    """Orchestrates the full tag-and-path filter pipeline."""

    def __init__(self) -> None:
        self.config = FilterConfig()
        self.logger = self.config.return_logging_instance(__name__)

    def run(self) -> None:
        """Execute the complete filter pipeline."""
        try:
            self.config.validate()
            payload = self._load_input()

            tag_mgr = TagFilterManager(self.config)
            _valid_tag_names, rejected_tag_names = tag_mgr.filter(payload.get("tags", []))

            path_mgr = PathFilterManager(self.config)
            valid_paths = path_mgr.filter(payload.get("paths", {}), rejected_tag_names)

            organiser = PathOrganiserManager(self.config)
            organiser.organise(payload, valid_paths)

            self.logger.info("Pipeline complete — output written to %s", self.config.output_dir)

        except ConfigException as err:
            self.logger.error("Configuration error: %s", err)
            sys.exit(1)
        except InputException as err:
            self.logger.error("Input error: %s", err)
            sys.exit(1)
        except ProcessingException as err:
            self.logger.error("Processing error: %s", err)
            sys.exit(1)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_input(self) -> dict[str, Any]:
        """Load and return the raw OpenAPI JSON payload."""
        self.logger.info("Loading input file: %s", self.config.input_file)
        try:
            with open(self.config.input_file, mode="r", encoding="utf-8") as fh:
                data: dict = json.load(fh)
        except (OSError, json.JSONDecodeError) as err:
            raise InputException(
                f"Failed to read {self.config.input_file}: {err}"
            ) from err

        self.logger.debug("Top-level keys: %s", list(data.keys()))
        return data


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Script entry point."""
    FilterManager().run()


if __name__ == "__main__":
    main()
