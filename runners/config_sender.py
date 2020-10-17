import click


class ConfigSender:

    @staticmethod
    def send_config(service, file_content):
        response = service.post(file_content)
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nHash: {description.get('description')} \n")
        click.echo(f"\nEnv vars set: {description.get('config').get('env')} \n")

