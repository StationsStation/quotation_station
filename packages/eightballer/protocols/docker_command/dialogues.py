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

"""
This module contains the classes required for docker_command dialogue management.

- DockerCommandDialogue: The dialogue class maintains state of a dialogue and manages it.
- DockerCommandDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Dict, Type, Callable, FrozenSet, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues, DialogueLabel

from packages.eightballer.protocols.docker_command.message import DockerCommandMessage


class DockerCommandDialogue(Dialogue):
    """The docker_command dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            DockerCommandMessage.Performative.BUILD,
            DockerCommandMessage.Performative.RUN,
            DockerCommandMessage.Performative.PS,
            DockerCommandMessage.Performative.KILL,
            DockerCommandMessage.Performative.LOGS,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            DockerCommandMessage.Performative.BUILD_RESPONSE,
            DockerCommandMessage.Performative.RUN_RESPONSE,
            DockerCommandMessage.Performative.PS_ALL_RESPONSE,
            DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE,
            DockerCommandMessage.Performative.KILL_RESPONSE,
            DockerCommandMessage.Performative.LOGS_RESPONSE,
            DockerCommandMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        DockerCommandMessage.Performative.BUILD: frozenset(
            {DockerCommandMessage.Performative.BUILD_RESPONSE, DockerCommandMessage.Performative.ERROR}
        ),
        DockerCommandMessage.Performative.BUILD_RESPONSE: frozenset(),
        DockerCommandMessage.Performative.ERROR: frozenset(),
        DockerCommandMessage.Performative.KILL: frozenset(
            {DockerCommandMessage.Performative.KILL_RESPONSE, DockerCommandMessage.Performative.ERROR}
        ),
        DockerCommandMessage.Performative.KILL_RESPONSE: frozenset(),
        DockerCommandMessage.Performative.LOGS: frozenset(
            {DockerCommandMessage.Performative.LOGS_RESPONSE, DockerCommandMessage.Performative.ERROR}
        ),
        DockerCommandMessage.Performative.LOGS_RESPONSE: frozenset(),
        DockerCommandMessage.Performative.PS: frozenset(
            {
                DockerCommandMessage.Performative.PS_ALL_RESPONSE,
                DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE,
                DockerCommandMessage.Performative.ERROR,
            }
        ),
        DockerCommandMessage.Performative.PS_ALL_RESPONSE: frozenset(),
        DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE: frozenset(),
        DockerCommandMessage.Performative.RUN: frozenset(
            {DockerCommandMessage.Performative.RUN_RESPONSE, DockerCommandMessage.Performative.ERROR}
        ),
        DockerCommandMessage.Performative.RUN_RESPONSE: frozenset(),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a docker_command dialogue."""

        DOCKER_ENGINE = "docker_engine"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a docker_command dialogue."""

        BUILD_RESPONSE = 0
        RUN_RESPONSE = 1
        PS_CONTAINER_RESPONSE = 2
        KILL_RESPONSE = 3
        LOGS_RESPONSE = 4
        ERROR = 5

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[DockerCommandMessage] = DockerCommandMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :param message_class: the message class used
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class DockerCommandDialogues(Dialogues, ABC):
    """This class keeps track of all docker_command dialogues."""

    END_STATES = frozenset(
        {
            DockerCommandDialogue.EndState.BUILD_RESPONSE,
            DockerCommandDialogue.EndState.RUN_RESPONSE,
            DockerCommandDialogue.EndState.PS_CONTAINER_RESPONSE,
            DockerCommandDialogue.EndState.KILL_RESPONSE,
            DockerCommandDialogue.EndState.LOGS_RESPONSE,
            DockerCommandDialogue.EndState.ERROR,
        }
    )

    _keep_terminal_state_dialogues = True

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[DockerCommandDialogue] = DockerCommandDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=DockerCommandMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
