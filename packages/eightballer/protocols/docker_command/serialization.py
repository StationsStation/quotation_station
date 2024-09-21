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

"""Serialization module for docker_command protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.docker_command import (  # type: ignore
    docker_command_pb2,
)
from packages.eightballer.protocols.docker_command.custom_types import (  # type: ignore
    ContainerStatus,
    ErrorCode,
    PsResponse,
    PsResponses,
)
from packages.eightballer.protocols.docker_command.message import (  # type: ignore
    DockerCommandMessage,
)


class DockerCommandSerializer(Serializer):
    """Serialization for the 'docker_command' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'DockerCommand' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(DockerCommandMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        docker_command_msg = docker_command_pb2.DockerCommandMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == DockerCommandMessage.Performative.BUILD:
            performative = docker_command_pb2.DockerCommandMessage.Build_Performative()  # type: ignore
            image_name = msg.image_name
            performative.image_name = image_name
            if msg.is_set("context"):
                performative.context_is_set = True
                context = msg.context
                performative.context = context
            if msg.is_set("dockerfile_path"):
                performative.dockerfile_path_is_set = True
                dockerfile_path = msg.dockerfile_path
                performative.dockerfile_path = dockerfile_path
            if msg.is_set("build_args"):
                performative.build_args_is_set = True
                build_args = msg.build_args
                performative.build_args.update(build_args)
            docker_command_msg.build.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.RUN:
            performative = docker_command_pb2.DockerCommandMessage.Run_Performative()  # type: ignore
            image_name = msg.image_name
            performative.image_name = image_name
            if msg.is_set("container_name"):
                performative.container_name_is_set = True
                container_name = msg.container_name
                performative.container_name = container_name
            if msg.is_set("environment"):
                performative.environment_is_set = True
                environment = msg.environment
                performative.environment.update(environment)
            if msg.is_set("command"):
                performative.command_is_set = True
                command = msg.command
                performative.command = command
            if msg.is_set("args"):
                performative.args_is_set = True
                args = msg.args
                performative.args.extend(args)
            if msg.is_set("entrypoint"):
                performative.entrypoint_is_set = True
                entrypoint = msg.entrypoint
                performative.entrypoint = entrypoint
            if msg.is_set("ports"):
                performative.ports_is_set = True
                ports = msg.ports
                performative.ports.update(ports)
            if msg.is_set("detach"):
                performative.detach_is_set = True
                detach = msg.detach
                performative.detach = detach
            if msg.is_set("volumes"):
                performative.volumes_is_set = True
                volumes = msg.volumes
                performative.volumes.update(volumes)
            docker_command_msg.run.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.KILL:
            performative = docker_command_pb2.DockerCommandMessage.Kill_Performative()  # type: ignore
            id = msg.id
            performative.id = id
            docker_command_msg.kill.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.LOGS:
            performative = docker_command_pb2.DockerCommandMessage.Logs_Performative()  # type: ignore
            id = msg.id
            performative.id = id
            if msg.is_set("stream"):
                performative.stream_is_set = True
                stream = msg.stream
                performative.stream = stream
            docker_command_msg.logs.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.PS:
            performative = docker_command_pb2.DockerCommandMessage.Ps_Performative()  # type: ignore
            all = msg.all
            performative.all = all
            if msg.is_set("container_id"):
                performative.container_id_is_set = True
                container_id = msg.container_id
                performative.container_id = container_id
            docker_command_msg.ps.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.LOGS_RESPONSE:
            performative = docker_command_pb2.DockerCommandMessage.Logs_Response_Performative()  # type: ignore
            logs = msg.logs
            performative.logs.extend(logs)
            docker_command_msg.logs_response.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.BUILD_RESPONSE:
            performative = docker_command_pb2.DockerCommandMessage.Build_Response_Performative()  # type: ignore
            image_id = msg.image_id
            performative.image_id = image_id
            docker_command_msg.build_response.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.RUN_RESPONSE:
            performative = docker_command_pb2.DockerCommandMessage.Run_Response_Performative()  # type: ignore
            status = msg.status
            ContainerStatus.encode(performative.status, status)
            if msg.is_set("container_id"):
                performative.container_id_is_set = True
                container_id = msg.container_id
                performative.container_id = container_id
            logs = msg.logs
            performative.logs.extend(logs)
            docker_command_msg.run_response.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.KILL_RESPONSE:
            performative = docker_command_pb2.DockerCommandMessage.Kill_Response_Performative()  # type: ignore
            status = msg.status
            ContainerStatus.encode(performative.status, status)
            docker_command_msg.kill_response.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.PS_ALL_RESPONSE:
            performative = docker_command_pb2.DockerCommandMessage.Ps_All_Response_Performative()  # type: ignore
            containers = msg.containers
            PsResponses.encode(performative.containers, containers)
            docker_command_msg.ps_all_response.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE:
            performative = docker_command_pb2.DockerCommandMessage.Ps_Container_Response_Performative()  # type: ignore
            container = msg.container
            PsResponse.encode(performative.container, container)
            docker_command_msg.ps_container_response.CopyFrom(performative)
        elif performative_id == DockerCommandMessage.Performative.ERROR:
            performative = docker_command_pb2.DockerCommandMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            docker_command_msg.error.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = docker_command_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'DockerCommand' message.

        :param obj: the bytes object.
        :return: the 'DockerCommand' message.
        """
        message_pb = ProtobufMessage()
        docker_command_pb = docker_command_pb2.DockerCommandMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        docker_command_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = docker_command_pb.WhichOneof("performative")
        performative_id = DockerCommandMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == DockerCommandMessage.Performative.BUILD:
            image_name = docker_command_pb.build.image_name
            performative_content["image_name"] = image_name
            if docker_command_pb.build.context_is_set:
                context = docker_command_pb.build.context
                performative_content["context"] = context
            if docker_command_pb.build.dockerfile_path_is_set:
                dockerfile_path = docker_command_pb.build.dockerfile_path
                performative_content["dockerfile_path"] = dockerfile_path
            if docker_command_pb.build.build_args_is_set:
                build_args = docker_command_pb.build.build_args
                build_args_dict = dict(build_args)
                performative_content["build_args"] = build_args_dict
        elif performative_id == DockerCommandMessage.Performative.RUN:
            image_name = docker_command_pb.run.image_name
            performative_content["image_name"] = image_name
            if docker_command_pb.run.container_name_is_set:
                container_name = docker_command_pb.run.container_name
                performative_content["container_name"] = container_name
            if docker_command_pb.run.environment_is_set:
                environment = docker_command_pb.run.environment
                environment_dict = dict(environment)
                performative_content["environment"] = environment_dict
            if docker_command_pb.run.command_is_set:
                command = docker_command_pb.run.command
                performative_content["command"] = command
            if docker_command_pb.run.args_is_set:
                args = docker_command_pb.run.args
                args_tuple = tuple(args)
                performative_content["args"] = args_tuple
            if docker_command_pb.run.entrypoint_is_set:
                entrypoint = docker_command_pb.run.entrypoint
                performative_content["entrypoint"] = entrypoint
            if docker_command_pb.run.ports_is_set:
                ports = docker_command_pb.run.ports
                ports_dict = dict(ports)
                performative_content["ports"] = ports_dict
            if docker_command_pb.run.detach_is_set:
                detach = docker_command_pb.run.detach
                performative_content["detach"] = detach
            if docker_command_pb.run.volumes_is_set:
                volumes = docker_command_pb.run.volumes
                volumes_dict = dict(volumes)
                performative_content["volumes"] = volumes_dict
        elif performative_id == DockerCommandMessage.Performative.KILL:
            id = docker_command_pb.kill.id
            performative_content["id"] = id
        elif performative_id == DockerCommandMessage.Performative.LOGS:
            id = docker_command_pb.logs.id
            performative_content["id"] = id
            if docker_command_pb.logs.stream_is_set:
                stream = docker_command_pb.logs.stream
                performative_content["stream"] = stream
        elif performative_id == DockerCommandMessage.Performative.PS:
            all = docker_command_pb.ps.all
            performative_content["all"] = all
            if docker_command_pb.ps.container_id_is_set:
                container_id = docker_command_pb.ps.container_id
                performative_content["container_id"] = container_id
        elif performative_id == DockerCommandMessage.Performative.LOGS_RESPONSE:
            logs = docker_command_pb.logs_response.logs
            logs_tuple = tuple(logs)
            performative_content["logs"] = logs_tuple
        elif performative_id == DockerCommandMessage.Performative.BUILD_RESPONSE:
            image_id = docker_command_pb.build_response.image_id
            performative_content["image_id"] = image_id
        elif performative_id == DockerCommandMessage.Performative.RUN_RESPONSE:
            pb2_status = docker_command_pb.run_response.status
            status = ContainerStatus.decode(pb2_status)
            performative_content["status"] = status
            if docker_command_pb.run_response.container_id_is_set:
                container_id = docker_command_pb.run_response.container_id
                performative_content["container_id"] = container_id
            logs = docker_command_pb.run_response.logs
            logs_tuple = tuple(logs)
            performative_content["logs"] = logs_tuple
        elif performative_id == DockerCommandMessage.Performative.KILL_RESPONSE:
            pb2_status = docker_command_pb.kill_response.status
            status = ContainerStatus.decode(pb2_status)
            performative_content["status"] = status
        elif performative_id == DockerCommandMessage.Performative.PS_ALL_RESPONSE:
            pb2_containers = docker_command_pb.ps_all_response.containers
            containers = PsResponses.decode(pb2_containers)
            performative_content["containers"] = containers
        elif performative_id == DockerCommandMessage.Performative.PS_CONTAINER_RESPONSE:
            pb2_container = docker_command_pb.ps_container_response.container
            container = PsResponse.decode(pb2_container)
            performative_content["container"] = container
        elif performative_id == DockerCommandMessage.Performative.ERROR:
            pb2_error_code = docker_command_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = docker_command_pb.error.error_msg
            performative_content["error_msg"] = error_msg
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return DockerCommandMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content,
        )
