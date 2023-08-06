"""
An entry-point for the 'apply' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from logging import getLogger

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.logging import log_time

# internal
from rcmpy.environment import Environment, load_environment


def apply_env(env: Environment) -> int:
    """Apply pending changes from the environment."""

    result = 0

    for file in env.config.files:
        # Check if a template is found for this file.
        if file.template not in env.templates_by_name:
            result += 1
            env.logger.error("Template '%s' not found!", file.template)
            continue

        # Check if this file has any updated templates.
        if env.is_updated(file):
            template = env.templates_by_name[file.template]

            # If a template doesn't require rendering, link or
            # copy it.
            if template.template is None:
                file.update(template.path, env.logger)

    return result


def apply_cmd(_: _Namespace) -> int:
    """Execute the apply command."""

    result = 1

    with log_time(getLogger(__name__), "Command"):
        with load_environment() as env:
            if env.config_loaded:
                result = apply_env(env)

    return result


def add_apply_cmd(_: _ArgumentParser) -> _CommandFunction:
    """Add apply-command arguments to its parser."""

    return apply_cmd
