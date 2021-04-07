import click


class Sender:

    @staticmethod
    def send_config(service, file_content):
        response = service.post(file_content)
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nResponse:\n{description.get('description')}\n")
        click.echo(f"\nEnvironment variables:\n{description.get('config').get('env')}\n")

        return description

    @staticmethod
    def get_agent_info(service):
        response = service.about()
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nAgent Info\n{description}\n")

    @staticmethod
    def send_config_for_cmd(service, cmd):
        file_content = ""
        response = service.post(file_content)
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nResponse:\n{description.get('description')}\n")
        click.echo(f"\nEnvironment variables:\n{description.get('config').get('env')}\n")

        return description
