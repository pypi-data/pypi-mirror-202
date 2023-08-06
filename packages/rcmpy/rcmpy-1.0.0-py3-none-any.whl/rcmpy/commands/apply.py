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
from vcorelib.paths import rel

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

        is_new = env.state.is_new()

        # Check if this file has any updated templates.
        if is_new or env.is_updated(file):
            template = env.templates_by_name[file.template]

            # If a template doesn't require rendering, use it as-is.
            source = template.path

            if template.template is not None:
                # Render the template to the build directory.
                source = env.build.joinpath(file.template)
                with source.open("w") as path_fd:
                    path_fd.write(template.template.render(env.state.configs))
                    env.logger.info("Rendered '%s'.", rel(source))

                # Update the output file.
            file.update(source, env.logger)

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
