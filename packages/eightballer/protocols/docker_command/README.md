# Docker Command Protocol

## Description

...

## Specification

```yaml
name: docker_command
author: eightballer
version: 0.1.0
description: A protocol for managing Docker containers through interactions between an agent and a local manager.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/docker_management:0.1.0
speech_acts:
  build:
    image_name: pt:str
    context: pt:optional[pt:str]
    dockerfile_path: pt:optional[pt:str]
    build_args: pt:optional[pt:dict[pt:str, pt:str]]
  run:
    image_name: pt:str
    container_name: pt:optional[pt:str]
    environment: pt:optional[pt:dict[pt:str, pt:str]]
    command: pt:optional[pt:str]
    args: pt:optional[pt:list[pt:str]]
    entrypoint: pt:optional[pt:str]
    ports: pt:optional[pt:dict[pt:str, pt:str]]
    detach: pt:optional[pt:bool]
    volumes: pt:optional[pt:dict[pt:str, pt:str]]
  kill:
    id: pt:str
  logs:
    id: pt:str
    stream: pt:optional[pt:bool]
  ps:
    all: pt:bool
    container_id: pt:optional[pt:str]
  logs_response:
    logs: pt:list[pt:str]
  build_response:
    image_id: pt:str
  run_response:
    status: ct:ContainerStatus
    container_id: pt:optional[pt:str]
    logs: pt:list[pt:str]
  kill_response:
    status: ct:ContainerStatus
  ps_all_response:
    containers: ct:PsResponses
  ps_container_response:
    container: ct:PsResponse
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      BUILD_ERROR = 0;
      RUN_ERROR = 1;
      STATUS_ERROR = 2;
      INVALID_REQUEST = 3;
    }
  ErrorCodeEnum error_code = 1;
ct:ContainerStatus: |
  enum ContainerStatusEnum{
      CREATED = 0;
      RUNNING = 1;
      PAUSED = 2;
      RESTARTING = 3;
      REMOVING = 4;
      EXITED = 5;
      DEAD = 6;
      NOT_FOUND = 7;
    }
  ContainerStatusEnum container_status = 1;
ct:PsResponse: |
  string container_id = 1;
  string image = 2;
  string command = 3;
  string created = 4;
  ContainerStatus status = 5;
  map<string, string> ports = 6;
  repeated string names = 7;
ct:PsResponses: |
  repeated PsResponse containers = 1;
---
initiation: [build, run, ps, kill, logs]
reply:
  build: [build_response, error]
  run: [run_response, error]
  ps: [ps_all_response, ps_container_response, error]
  kill: [kill_response, error]
  logs: [logs_response, error]
  build_response: [ ]
  run_response: [ ]
  ps_all_response: [ ]
  ps_container_response: [ ]
  kill_response: [ ]
  logs_response: [ ]
  error: [ ]
termination: [build_response, run_response, ps_all_response, ps_container_response,
 kill_response, logs_response, error]
roles: { docker_engine }
end_states: [ build_response, run_response, ps_container_response, kill_response, logs_response, error ]
keep_terminal_state_dialogues: true
```