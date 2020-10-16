import click


class ConfigSender:

    @staticmethod
    def send_config(service, file_content):
        try:
            response = service.send(file_content)
            click.echo(response)
        except Exception as e:
            print("\nException({})".format(e.__str__()))
