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

"""Test messages module for docker_command protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os
from typing import Any, List

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.docker_command.message import DockerCommandMessage
from packages.eightballer.protocols.docker_command.custom_types import (
    ErrorCode,
    PsResponse,
    PsResponses,
    ContainerStatus,
)


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageDockerCommand(BaseProtocolMessagesTestCase):
    """Test for the 'docker_command' protocol message."""

    MESSAGE_CLASS = DockerCommandMessage

    def build_messages(self) -> List[DockerCommandMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.BUILD,
                image_name="some str",
                context="some str",
                dockerfile_path="some str",
                build_args={"some str": "some str"},
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.RUN,
                image_name="some str",
                container_name="some str",
                environment={"some str": "some str"},
                command="some str",
                args=("some str",),
                entrypoint="some str",
                ports={"some str": "some str"},
                detach=True,
                volumes={"some str": "some str"},
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.KILL,
                id="some str",
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.LOGS,
                id="some str",
                stream=True,
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.PS,
                all=True,
                container_id="some str",
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.LOGS_RESPONSE,
                logs=("some str",),
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.BUILD_RESPONSE,
                image_id="some str",
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.RUN_RESPONSE,
                status=ContainerStatus(0),  # check it please!
                container_id="some str",
                logs=("some str",),
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.KILL_RESPONSE,
                status=ContainerStatus(0),  # check it please!
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.PS_ALL_RESPONSE,
                containers=PsResponses(**load_data("PsResponses")),  # check it please!
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE,
                container=PsResponse(**load_data("PsResponse")),  # check it please!
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
            ),
        ]

    def build_inconsistent(self) -> List[DockerCommandMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.BUILD,
                # skip content: image_name
                context="some str",
                dockerfile_path="some str",
                build_args={"some str": "some str"},
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.RUN,
                # skip content: image_name
                container_name="some str",
                environment={"some str": "some str"},
                command="some str",
                args=("some str",),
                entrypoint="some str",
                ports={"some str": "some str"},
                detach=True,
                volumes={"some str": "some str"},
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.KILL,
                # skip content: id
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.LOGS,
                # skip content: id
                stream=True,
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.PS,
                # skip content: all
                container_id="some str",
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.LOGS_RESPONSE,
                # skip content: logs
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.BUILD_RESPONSE,
                # skip content: image_id
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.RUN_RESPONSE,
                # skip content: status
                container_id="some str",
                logs=("some str",),
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.KILL_RESPONSE,
                # skip content: status
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.PS_ALL_RESPONSE,
                # skip content: containers
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE,
                # skip content: container
            ),
            DockerCommandMessage(
                performative=DockerCommandMessage.Performative.ERROR,
                # skip content: error_code
                error_msg="some str",
            ),
        ]
