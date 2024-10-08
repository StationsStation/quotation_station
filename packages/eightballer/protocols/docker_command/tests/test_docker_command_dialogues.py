# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Test dialogues module for docker_command protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from aea.test_tools.test_protocol import BaseProtocolDialoguesTestCase

from packages.eightballer.protocols.docker_command.message import DockerCommandMessage
from packages.eightballer.protocols.docker_command.dialogues import (
    DockerCommandDialogue,
    DockerCommandDialogues,
)


class TestDialoguesDockerCommand(BaseProtocolDialoguesTestCase):
    """Test for the 'docker_command' protocol dialogues."""

    MESSAGE_CLASS = DockerCommandMessage

    DIALOGUE_CLASS = DockerCommandDialogue

    DIALOGUES_CLASS = DockerCommandDialogues

    ROLE_FOR_THE_FIRST_MESSAGE = DockerCommandDialogue.Role.DOCKER_ENGINE  # CHECK

    def make_message_content(self) -> dict:
        """Make a dict with message contruction content for dialogues.create."""
        return dict(
            performative=DockerCommandMessage.Performative.BUILD,
            image_name="some str",
            context="some str",
            dockerfile_path="some str",
            build_args={"some str": "some str"},
        )
