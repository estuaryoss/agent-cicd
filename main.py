#!/usr/bin/env python3
from secrets import token_hex

import click

__author__ = "Catalin Dinuta"

from runners.config_sender import ConfigSender
from runners.status_checker import StatusChecker
from service.restapi_service import RestApiService
from utils.io_utils import IOUtils


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
@click.option('--endpoint', help='The endpoint to sent the request. Default is "/commanddetached"')
@click.option('--file', help='The yaml file path on disk. Default is "./config.yaml"')
def cli(ip, port, token, protocol, cert, endpoint, file):
    cmds_id = token_hex(8)
    connection = {
        "ip": ip,
        "port": port,
        "token": token,
        "protocol": protocol if protocol is not None else "http",
        "cert": cert if cert is not None else "https/cert.pem",
        "endpoint": endpoint if endpoint is not None else f"/commanddetached/{cmds_id}"
    }
    service = RestApiService(connection)
    file_path = file if not None else "./config.yaml"

    try:
        file_content = IOUtils.read_file(file_path)
    except Exception as e:
        print("\nFile does not exist ({})".format(e.__str__()))
        exit(1)

    # check if can connect
    try:
        service.send("ls")
    except Exception as e:
        print("\nCould not connect to the agent ({})".format(e.__str__()))
        exit(1)

    print(f"\nRunning commands from file '{file_path}'. Waiting for hash confirmation ...\n")
    ConfigSender.send_config(service=service, file_content=file_content)

    status_checker = StatusChecker(service)
    status_checker.check_progress(poll_interval=5)
    exit(0)


if __name__ == "__main__":
    cli()
