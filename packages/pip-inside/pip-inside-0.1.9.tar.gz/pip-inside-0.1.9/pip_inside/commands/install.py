import os
import shutil
import subprocess
import sys
from typing import List

import click
import tomlkit

from pip_inside.utils.pyproject import PyProject


def handle_install(groups: List[str]):
    _install_from_pi_lock(groups) or _install_from_pyproject_toml(groups)


def _install_from_pi_lock(groups: List[str]):
    if not os.path.exists('pi.lock'):
        return

    with open('pi.lock', 'r') as f:
        data = tomlkit.load(f)

    if '_all_' in groups:
        for group, deps in data.items():
            _install_group(group, deps)
    else:
        for group in groups:
            _install_group(group, data.get(group, []))


def _install_from_pyproject_toml(groups: List[str]):
    pyproject = PyProject.from_toml()

    if '_all_' in groups:
        for group, deps in pyproject.get_dependencies_for_install().items():
            _install_group(group, deps)

    else:
        for group in groups:
            deps = pyproject.get_for_install(group)
            _install_group(group, deps)


def _install_group(group: str, dependencies: list):
    if dependencies is None or len(dependencies) == 0:
        click.secho(f"Group: {group}, nothing to install", fg='cyan')
        return

    click.secho(f"Group: {group}", fg='cyan')
    try:
        cmd = [shutil.which('python'), '-m', 'pip', 'install', *dependencies]
        subprocess.run(cmd, stderr=sys.stderr, stdout=sys.stdout)
    except subprocess.CalledProcessError:
        pass
