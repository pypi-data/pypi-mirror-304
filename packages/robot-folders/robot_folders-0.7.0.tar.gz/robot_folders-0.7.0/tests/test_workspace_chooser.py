#
# Copyright (c) 2024 FZI Forschungszentrum Informatik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os

import pytest
from click.testing import CliRunner

from robot_folders.commands.change_environment import EnvironmentChooser
from robot_folders.helpers.directory_helpers import get_checkout_dir
from robot_folders.helpers.workspace_chooser import WorkspaceChooser


def test_workspace_chooser(fs):
    env_name = "sckgdfh"
    env_dir = os.path.join(get_checkout_dir(), env_name)
    fs.create_dir(env_dir)
    fs.create_dir(os.path.join(env_dir, "colcon_ws"))
    fs.create_dir(os.path.join(env_dir, "catkin_ws"))
    fs.create_dir(os.path.join(env_dir, "misc_ws"))

    runner = CliRunner()
    result = runner.invoke(EnvironmentChooser(), [env_name])
    assert result.exit_code == 0
    result = runner.invoke(WorkspaceChooser())
    assert result.exit_code == 0
    print(result.output)
