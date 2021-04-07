#!/usr/bin/env python3
import sys
import time
from distutils.util import strtobool
from secrets import token_hex

import click

__author__ = "Catalin Dinuta"

import yaml

from about import properties
from constants.env_init import EnvInit
from model.config_loader import ConfigLoader
from runners.config_sender import Sender
from runners.status_checker import StatusChecker
from service.restapi_service import RestApiService
from utils.command_holder import CommandHolder
from utils.io_utils import IOUtils
from utils.yaml_cmds_splitter import YamlCommandsSplitter


@click.command()
@click.option('--ip', prompt='ip/hostname',
              help='The IP/hostname of the target machine where estuary-agent is deployed')
@click.option('--port', prompt='port',
              help='The port number of the target machine where estuary-agent is deployed')
@click.option('--token', prompt='token', hide_input=True,
              help='The authentication token that will be sent via \'Token\' header. '
                   'Use \'None\' if estuary-agent is deployed unsecured')
@click.option('--protocol', help='The protocol with which the estuary-agent was deployed. Default is http. E.g. https')
@click.option('--cert', help='The certificate with which the estuary-agent was deployed. E.g. https/cert.pem')
@click.option('--endpoint', help='The endpoint to sent the request. Default is "/commanddetachedyaml"')
@click.option('--file', help='The yaml file path on disk. Default is "./config.yaml"')
@click.option('--interval', help='The poll interval in seconds. Default is 5.')
@click.option('--batch',
              help='If batch is "true", the server will execute all commands in batch. '
                   'If batch is "false" the commands will be executed one by one and the CLI exits '
                   'when the first failure is detected. Default is "false"')
def cli(ip, port, token, protocol, cert, endpoint, file, interval, batch):
    IOUtils.create_dir(EnvInit.CMD_DETACHED_STREAMS)
    print(f"CLI version: {properties.get('version')}\n")
    cmds_id = token_hex(8)
    connection = {
        "ip": ip,
        "port": port,
        "token": token,
        "protocol": protocol if protocol is not None else "http",
        "cert": cert if cert is not None else "https/cert.pem",
        "endpoint": endpoint if endpoint is not None else f"/commanddetachedyaml/{cmds_id}"
    }

    service = RestApiService(connection)
    file_path = file if file is not None else "config.yaml"
    batch_option = bool(strtobool(batch)) if batch is not None else False
    poll_interval = int(interval) if interval is not None else 5

    try:
        file_content = IOUtils.read_file(file_path)
    except Exception as e:
        raise BaseException("File does not exist ({})\n".format(e.__str__()))

    # check if can connect
    try:
        service.ping()
    except Exception as e:
        raise BaseException(f"Could not connect to the agent "
                            f"{connection.get('protocol')}://{connection.get('ip')}:{connection.get('port')}. Error: {e.__str__()}")

    config_loader = ConfigLoader(yaml.safe_load(IOUtils.read_file(file=file_path, type='r')))
    yaml_splitter = YamlCommandsSplitter(config_loader.get_config())
    client_cmds = yaml_splitter.get_client_cmds_in_order()
    server_cmds = yaml_splitter.get_server_cmds_in_order()

    for cmd in client_cmds:
        print(f"Running client command: '{cmd}'\n")
        result = CommandHolder.run_cmd(service=service, command=cmd)
        if result.get("code") != 0:
            click.echo(result.get('err'))
            sys.exit(result.get("code"))

        click.echo(result.get('out'))

    Sender.get_agent_info(service=service)

    print(f"Running commands from file '{file_path}' on agent "
          f"{connection.get('protocol')}://{connection.get('ip')}:{connection.get('port')} on endpoint {connection.get('endpoint')}\n")
    status_checker = StatusChecker(service)

    if batch_option:
        description = Sender.send_config(service=service, file_content=file_content)

        time.sleep(2)
        # if default then check progress of the cmd in background
        if connection.get("endpoint") == f"/commanddetachedyaml/{cmds_id}":
            exit_code = status_checker.check_progress_async(poll_interval=poll_interval)
        # otherwise check the command already executed
        elif connection.get("endpoint") == "/commandyaml":
            exit_code = status_checker.check_progress_sync(description=description.get("description"))
        else:
            raise BaseException(f"Unknown endpoint {endpoint}")
    else:
        for cmd in server_cmds:
            description = Sender.send_config_for_cmd(service=service, cmd=cmd)

            time.sleep(2)
            # if default then check progress of the cmd in background
            if connection.get("endpoint") == f"/commanddetachedyaml/{cmds_id}":
                exit_code = status_checker.check_progress_async(poll_interval=poll_interval)
            # otherwise check the command already executed
            elif connection.get("endpoint") == "/commandyaml":
                exit_code = status_checker.check_progress_sync(description=description.get("description"))
            else:
                raise BaseException(f"Unknown endpoint {endpoint}")
            if exit_code != 0:
                sys.exit(exit_code)
    print(f"Global exit code: {exit_code}\n")


if __name__ == "__main__":
    cli()
