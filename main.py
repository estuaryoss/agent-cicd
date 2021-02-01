#!/usr/bin/env python3
import time
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
def cli(ip, port, token, protocol, cert, endpoint, file, interval):
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

    try:
        file_content = IOUtils.read_file(file_path)
    except Exception as e:
        print("File does not exist ({})\n".format(e.__str__()))
        exit(1)

    # check if can connect
    try:
        service.ping()
    except Exception as e:
        print("Could not connect to the agent ({})\n".format(e.__str__()))
        exit(1)

    config_loader = ConfigLoader(yaml.safe_load(IOUtils.read_file(file=file_path, type='r')))
    yaml_splitter = YamlCommandsSplitter(config_loader.get_config())
    client_cmds = yaml_splitter.get_cmds_in_order()
    for cmd in client_cmds:
        print(f"Running client command: '{cmd}'\n")
        click.echo(CommandHolder.run_cmd(service=service, command=cmd))

    print(f"Running commands from file '{file_path}'. Waiting for response confirmation ...\n")
    description = Sender.send_config(service=service, file_content=file_content)
    Sender.get_agent_info(service=service)

    poll_interval = int(interval) if interval is not None else 5
    time.sleep(2)
    status_checker = StatusChecker(service)
    # if default then check progress of the cmd in background
    if endpoint == f"/commanddetachedyaml/{cmds_id}":
        exit_code = status_checker.check_progress_async(poll_interval=poll_interval)
    # otherwise check the command already executed
    elif endpoint == "/commandyaml":
        exit_code = status_checker.check_progress_sync(description=description.get("description"))
    else:
        raise BaseException(f"Unknown endpoint {endpoint}")

    print(f"Global exit code: {exit_code}\n")
    exit(exit_code)


if __name__ == "__main__":
    cli()
