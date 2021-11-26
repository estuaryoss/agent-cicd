#!/usr/bin/env python3
import sys
import time
from distutils.util import strtobool

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
              help='The IP/hostname of the target machine where Estuary Agent is deployed')
@click.option('--port', prompt='port',
              help='The port number of the target machine where Estuary Agent is deployed')
@click.option('--username', prompt='username',
              help='The username used for the Basic authentication')
@click.option('--password', prompt='password', hide_input=True,
              help='The password used for the Basic authentication')
@click.option('--protocol', help='The protocol with which the estuary-agent was deployed. Default is http. E.g. https')
@click.option('--cert', help='The certificate with which the estuary-agent was deployed. E.g. https/cert.pem')
@click.option('--endpoint', help='The endpoint to sent the request. Default is "/commandsyaml"')
@click.option('--file', help='The yaml file path on disk. Default is "./config.yaml"')
@click.option('--batch',
              help='If batch is "true", the server will execute all commands in batch. '
                   'If batch is "false" the commands will be executed one by one and the CLI exits '
                   'when the first failure is detected. Default is "false"')
def cli(ip, port, username, password, protocol, cert, endpoint, file, batch):
    IOUtils.create_dir(EnvInit.CMD_DETACHED_STREAMS)
    print(f"CLI version: {properties.get('version')}\n")
    connection = {
        "ip": ip,
        "port": port,
        "username": username,
        "password": password,
        "protocol": protocol if protocol is not None else "http",
        "cert": cert if cert is not None else "https/cert.pem",
        "endpoint": endpoint if endpoint is not None else f"/commandsyaml"
    }

    service = RestApiService(connection)
    file_path = file if file is not None else "config.yaml"
    batch_option = bool(strtobool(batch)) if batch is not None else False

    try:
        file_content = IOUtils.read_file(file_path)
    except Exception as e:
        raise BaseException("File does not exist ({})\n".format(e.__str__()))

    # check if can connect
    try:
        service.about()
    except Exception as e:
        raise BaseException(f"Could not connect to the agent "
                            f"{connection.get('protocol')}://{connection.get('ip')}:{connection.get('port')}. Error: {e.__str__()}")

    config_loader = ConfigLoader(yaml.safe_load(IOUtils.read_file(file=file_path, type='r')))
    yaml_splitter = YamlCommandsSplitter(config_loader.get_config())
    client_commands = yaml_splitter.get_client_cmds_in_order()
    server_commands = yaml_splitter.get_server_cmds_in_order()

    for cmd in client_commands:
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
        exit_code = status_checker.check_progress_sync(description=description.get("description"))
    else:
        for cmd in server_commands:
            response = Sender.send_config_for_cmd(service=service, cmd=cmd)

            time.sleep(2)
            exit_code = status_checker.check_progress_sync(description=response.get("description"))
            if exit_code != 0:
                sys.exit(exit_code)
    print(f"Global exit code: {exit_code}\n")


if __name__ == "__main__":
    cli()
