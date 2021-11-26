import click
import yaml


class Sender:

    @staticmethod
    def send_config(service, file_content):
        response = service.post(file_content)
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nEnvironment variables:\n{description.get('config').get('env')}\n")

        return description

    @staticmethod
    def get_agent_info(service):
        description = service.about()
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nAgent Info\n{description}\n")

    @staticmethod
    def send_config_for_cmd(service, cmd):
        data = """
        env:
            FOO: "BAR"
        script:
            - echo "script"
        """
        yaml_content = yaml.safe_load(data)
        yaml_content.get("script")[0] = cmd
        response = service.post(yaml_content.__str__())
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        # click.echo(f"\nEnvironment variables:\n{description.get('config').get('env')}\n")

        return description
