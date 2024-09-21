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

"""This module contains docker_command's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message  # type: ignore

from packages.eightballer.protocols.docker_command.custom_types import (
    ContainerStatus as CustomContainerStatus,
)
from packages.eightballer.protocols.docker_command.custom_types import (
    ErrorCode as CustomErrorCode,
)
from packages.eightballer.protocols.docker_command.custom_types import (
    PsResponse as CustomPsResponse,
)
from packages.eightballer.protocols.docker_command.custom_types import (
    PsResponses as CustomPsResponses,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.docker_command.message")

DEFAULT_BODY_SIZE = 4


class DockerCommandMessage(Message):
    """A protocol for managing Docker containers through interactions between an agent and a local manager."""

    protocol_id = PublicId.from_str("eightballer/docker_command:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/docker_management:0.1.0")

    ContainerStatus = CustomContainerStatus

    ErrorCode = CustomErrorCode

    PsResponse = CustomPsResponse

    PsResponses = CustomPsResponses

    class Performative(Message.Performative):
        """Performatives for the docker_command protocol."""

        BUILD = "build"
        BUILD_RESPONSE = "build_response"
        ERROR = "error"
        KILL = "kill"
        KILL_RESPONSE = "kill_response"
        LOGS = "logs"
        LOGS_RESPONSE = "logs_response"
        PS = "ps"
        PS_ALL_RESPONSE = "ps_all_response"
        PS_CONTAINER_RESPONSE = "ps_container_response"
        RUN = "run"
        RUN_RESPONSE = "run_response"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "build",
        "build_response",
        "error",
        "kill",
        "kill_response",
        "logs",
        "logs_response",
        "ps",
        "ps_all_response",
        "ps_container_response",
        "run",
        "run_response",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "all",
            "args",
            "build_args",
            "command",
            "container",
            "container_id",
            "container_name",
            "containers",
            "context",
            "detach",
            "dialogue_reference",
            "dockerfile_path",
            "entrypoint",
            "environment",
            "error_code",
            "error_msg",
            "id",
            "image_id",
            "image_name",
            "logs",
            "message_id",
            "performative",
            "ports",
            "status",
            "stream",
            "target",
            "volumes",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of DockerCommandMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        :param **kwargs: extra options.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=DockerCommandMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(DockerCommandMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def all(self) -> bool:
        """Get the 'all' content from the message."""
        enforce(self.is_set("all"), "'all' content is not set.")
        return cast(bool, self.get("all"))

    @property
    def args(self) -> Optional[Tuple[str, ...]]:
        """Get the 'args' content from the message."""
        return cast(Optional[Tuple[str, ...]], self.get("args"))

    @property
    def build_args(self) -> Optional[Dict[str, str]]:
        """Get the 'build_args' content from the message."""
        return cast(Optional[Dict[str, str]], self.get("build_args"))

    @property
    def command(self) -> Optional[str]:
        """Get the 'command' content from the message."""
        return cast(Optional[str], self.get("command"))

    @property
    def container(self) -> CustomPsResponse:
        """Get the 'container' content from the message."""
        enforce(self.is_set("container"), "'container' content is not set.")
        return cast(CustomPsResponse, self.get("container"))

    @property
    def container_id(self) -> Optional[str]:
        """Get the 'container_id' content from the message."""
        return cast(Optional[str], self.get("container_id"))

    @property
    def container_name(self) -> Optional[str]:
        """Get the 'container_name' content from the message."""
        return cast(Optional[str], self.get("container_name"))

    @property
    def containers(self) -> CustomPsResponses:
        """Get the 'containers' content from the message."""
        enforce(self.is_set("containers"), "'containers' content is not set.")
        return cast(CustomPsResponses, self.get("containers"))

    @property
    def context(self) -> Optional[str]:
        """Get the 'context' content from the message."""
        return cast(Optional[str], self.get("context"))

    @property
    def detach(self) -> Optional[bool]:
        """Get the 'detach' content from the message."""
        return cast(Optional[bool], self.get("detach"))

    @property
    def dockerfile_path(self) -> Optional[str]:
        """Get the 'dockerfile_path' content from the message."""
        return cast(Optional[str], self.get("dockerfile_path"))

    @property
    def entrypoint(self) -> Optional[str]:
        """Get the 'entrypoint' content from the message."""
        return cast(Optional[str], self.get("entrypoint"))

    @property
    def environment(self) -> Optional[Dict[str, str]]:
        """Get the 'environment' content from the message."""
        return cast(Optional[Dict[str, str]], self.get("environment"))

    @property
    def error_code(self) -> CustomErrorCode:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomErrorCode, self.get("error_code"))

    @property
    def error_msg(self) -> str:
        """Get the 'error_msg' content from the message."""
        enforce(self.is_set("error_msg"), "'error_msg' content is not set.")
        return cast(str, self.get("error_msg"))

    @property
    def id(self) -> str:
        """Get the 'id' content from the message."""
        enforce(self.is_set("id"), "'id' content is not set.")
        return cast(str, self.get("id"))

    @property
    def image_id(self) -> str:
        """Get the 'image_id' content from the message."""
        enforce(self.is_set("image_id"), "'image_id' content is not set.")
        return cast(str, self.get("image_id"))

    @property
    def image_name(self) -> str:
        """Get the 'image_name' content from the message."""
        enforce(self.is_set("image_name"), "'image_name' content is not set.")
        return cast(str, self.get("image_name"))

    @property
    def logs(self) -> Tuple[str, ...]:
        """Get the 'logs' content from the message."""
        enforce(self.is_set("logs"), "'logs' content is not set.")
        return cast(Tuple[str, ...], self.get("logs"))

    @property
    def ports(self) -> Optional[Dict[str, str]]:
        """Get the 'ports' content from the message."""
        return cast(Optional[Dict[str, str]], self.get("ports"))

    @property
    def status(self) -> CustomContainerStatus:
        """Get the 'status' content from the message."""
        enforce(self.is_set("status"), "'status' content is not set.")
        return cast(CustomContainerStatus, self.get("status"))

    @property
    def stream(self) -> Optional[bool]:
        """Get the 'stream' content from the message."""
        return cast(Optional[bool], self.get("stream"))

    @property
    def volumes(self) -> Optional[Dict[str, str]]:
        """Get the 'volumes' content from the message."""
        return cast(Optional[Dict[str, str]], self.get("volumes"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the docker_command protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(type(self.message_id)),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(type(self.target)),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, DockerCommandMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == DockerCommandMessage.Performative.BUILD:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.image_name, str),
                    "Invalid type for content 'image_name'. Expected 'str'. Found '{}'.".format(type(self.image_name)),
                )
                if self.is_set("context"):
                    expected_nb_of_contents += 1
                    context = cast(str, self.context)
                    enforce(
                        isinstance(context, str),
                        "Invalid type for content 'context'. Expected 'str'. Found '{}'.".format(type(context)),
                    )
                if self.is_set("dockerfile_path"):
                    expected_nb_of_contents += 1
                    dockerfile_path = cast(str, self.dockerfile_path)
                    enforce(
                        isinstance(dockerfile_path, str),
                        "Invalid type for content 'dockerfile_path'. Expected 'str'. Found '{}'.".format(
                            type(dockerfile_path)
                        ),
                    )
                if self.is_set("build_args"):
                    expected_nb_of_contents += 1
                    build_args = cast(Dict[str, str], self.build_args)
                    enforce(
                        isinstance(build_args, dict),
                        "Invalid type for content 'build_args'. Expected 'dict'. Found '{}'.".format(type(build_args)),
                    )
                    for key_of_build_args, value_of_build_args in build_args.items():
                        enforce(
                            isinstance(key_of_build_args, str),
                            "Invalid type for dictionary keys in content 'build_args'. Expected 'str'. Found '{}'.".format(
                                type(key_of_build_args)
                            ),
                        )
                        enforce(
                            isinstance(value_of_build_args, str),
                            "Invalid type for dictionary values in content 'build_args'. Expected 'str'. Found '{}'.".format(
                                type(value_of_build_args)
                            ),
                        )
            elif self.performative == DockerCommandMessage.Performative.RUN:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.image_name, str),
                    "Invalid type for content 'image_name'. Expected 'str'. Found '{}'.".format(type(self.image_name)),
                )
                if self.is_set("container_name"):
                    expected_nb_of_contents += 1
                    container_name = cast(str, self.container_name)
                    enforce(
                        isinstance(container_name, str),
                        "Invalid type for content 'container_name'. Expected 'str'. Found '{}'.".format(
                            type(container_name)
                        ),
                    )
                if self.is_set("environment"):
                    expected_nb_of_contents += 1
                    environment = cast(Dict[str, str], self.environment)
                    enforce(
                        isinstance(environment, dict),
                        "Invalid type for content 'environment'. Expected 'dict'. Found '{}'.".format(
                            type(environment)
                        ),
                    )
                    for key_of_environment, value_of_environment in environment.items():
                        enforce(
                            isinstance(key_of_environment, str),
                            "Invalid type for dictionary keys in content 'environment'. Expected 'str'. Found '{}'.".format(
                                type(key_of_environment)
                            ),
                        )
                        enforce(
                            isinstance(value_of_environment, str),
                            "Invalid type for dictionary values in content 'environment'. Expected 'str'. Found '{}'.".format(
                                type(value_of_environment)
                            ),
                        )
                if self.is_set("command"):
                    expected_nb_of_contents += 1
                    command = cast(str, self.command)
                    enforce(
                        isinstance(command, str),
                        "Invalid type for content 'command'. Expected 'str'. Found '{}'.".format(type(command)),
                    )
                if self.is_set("args"):
                    expected_nb_of_contents += 1
                    args = cast(Tuple[str, ...], self.args)
                    enforce(
                        isinstance(args, tuple),
                        "Invalid type for content 'args'. Expected 'tuple'. Found '{}'.".format(type(args)),
                    )
                    enforce(
                        all(isinstance(element, str) for element in args),
                        "Invalid type for tuple elements in content 'args'. Expected 'str'.",
                    )
                if self.is_set("entrypoint"):
                    expected_nb_of_contents += 1
                    entrypoint = cast(str, self.entrypoint)
                    enforce(
                        isinstance(entrypoint, str),
                        "Invalid type for content 'entrypoint'. Expected 'str'. Found '{}'.".format(type(entrypoint)),
                    )
                if self.is_set("ports"):
                    expected_nb_of_contents += 1
                    ports = cast(Dict[str, str], self.ports)
                    enforce(
                        isinstance(ports, dict),
                        "Invalid type for content 'ports'. Expected 'dict'. Found '{}'.".format(type(ports)),
                    )
                    for key_of_ports, value_of_ports in ports.items():
                        enforce(
                            isinstance(key_of_ports, str),
                            "Invalid type for dictionary keys in content 'ports'. Expected 'str'. Found '{}'.".format(
                                type(key_of_ports)
                            ),
                        )
                        enforce(
                            isinstance(value_of_ports, str),
                            "Invalid type for dictionary values in content 'ports'. Expected 'str'. Found '{}'.".format(
                                type(value_of_ports)
                            ),
                        )
                if self.is_set("detach"):
                    expected_nb_of_contents += 1
                    detach = cast(bool, self.detach)
                    enforce(
                        isinstance(detach, bool),
                        "Invalid type for content 'detach'. Expected 'bool'. Found '{}'.".format(type(detach)),
                    )
                if self.is_set("volumes"):
                    expected_nb_of_contents += 1
                    volumes = cast(Dict[str, str], self.volumes)
                    enforce(
                        isinstance(volumes, dict),
                        "Invalid type for content 'volumes'. Expected 'dict'. Found '{}'.".format(type(volumes)),
                    )
                    for key_of_volumes, value_of_volumes in volumes.items():
                        enforce(
                            isinstance(key_of_volumes, str),
                            "Invalid type for dictionary keys in content 'volumes'. Expected 'str'. Found '{}'.".format(
                                type(key_of_volumes)
                            ),
                        )
                        enforce(
                            isinstance(value_of_volumes, str),
                            "Invalid type for dictionary values in content 'volumes'. Expected 'str'. Found '{}'.".format(
                                type(value_of_volumes)
                            ),
                        )
            elif self.performative == DockerCommandMessage.Performative.KILL:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.id, str),
                    "Invalid type for content 'id'. Expected 'str'. Found '{}'.".format(type(self.id)),
                )
            elif self.performative == DockerCommandMessage.Performative.LOGS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.id, str),
                    "Invalid type for content 'id'. Expected 'str'. Found '{}'.".format(type(self.id)),
                )
                if self.is_set("stream"):
                    expected_nb_of_contents += 1
                    stream = cast(bool, self.stream)
                    enforce(
                        isinstance(stream, bool),
                        "Invalid type for content 'stream'. Expected 'bool'. Found '{}'.".format(type(stream)),
                    )
            elif self.performative == DockerCommandMessage.Performative.PS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.all, bool),
                    "Invalid type for content 'all'. Expected 'bool'. Found '{}'.".format(type(self.all)),
                )
                if self.is_set("container_id"):
                    expected_nb_of_contents += 1
                    container_id = cast(str, self.container_id)
                    enforce(
                        isinstance(container_id, str),
                        "Invalid type for content 'container_id'. Expected 'str'. Found '{}'.".format(
                            type(container_id)
                        ),
                    )
            elif self.performative == DockerCommandMessage.Performative.LOGS_RESPONSE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.logs, tuple),
                    "Invalid type for content 'logs'. Expected 'tuple'. Found '{}'.".format(type(self.logs)),
                )
                enforce(
                    all(isinstance(element, str) for element in self.logs),
                    "Invalid type for tuple elements in content 'logs'. Expected 'str'.",
                )
            elif self.performative == DockerCommandMessage.Performative.BUILD_RESPONSE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.image_id, str),
                    "Invalid type for content 'image_id'. Expected 'str'. Found '{}'.".format(type(self.image_id)),
                )
            elif self.performative == DockerCommandMessage.Performative.RUN_RESPONSE:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.status, CustomContainerStatus),
                    "Invalid type for content 'status'. Expected 'ContainerStatus'. Found '{}'.".format(
                        type(self.status)
                    ),
                )
                if self.is_set("container_id"):
                    expected_nb_of_contents += 1
                    container_id = cast(str, self.container_id)
                    enforce(
                        isinstance(container_id, str),
                        "Invalid type for content 'container_id'. Expected 'str'. Found '{}'.".format(
                            type(container_id)
                        ),
                    )
                enforce(
                    isinstance(self.logs, tuple),
                    "Invalid type for content 'logs'. Expected 'tuple'. Found '{}'.".format(type(self.logs)),
                )
                enforce(
                    all(isinstance(element, str) for element in self.logs),
                    "Invalid type for tuple elements in content 'logs'. Expected 'str'.",
                )
            elif self.performative == DockerCommandMessage.Performative.KILL_RESPONSE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.status, CustomContainerStatus),
                    "Invalid type for content 'status'. Expected 'ContainerStatus'. Found '{}'.".format(
                        type(self.status)
                    ),
                )
            elif self.performative == DockerCommandMessage.Performative.PS_ALL_RESPONSE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.containers, CustomPsResponses),
                    "Invalid type for content 'containers'. Expected 'PsResponses'. Found '{}'.".format(
                        type(self.containers)
                    ),
                )
            elif self.performative == DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.container, CustomPsResponse),
                    "Invalid type for content 'container'. Expected 'PsResponse'. Found '{}'.".format(
                        type(self.container)
                    ),
                )
            elif self.performative == DockerCommandMessage.Performative.ERROR:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.error_code, CustomErrorCode),
                    "Invalid type for content 'error_code'. Expected 'ErrorCode'. Found '{}'.".format(
                        type(self.error_code)
                    ),
                )
                enforce(
                    isinstance(self.error_msg, str),
                    "Invalid type for content 'error_msg'. Expected 'str'. Found '{}'.".format(type(self.error_msg)),
                )

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(self.target),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
