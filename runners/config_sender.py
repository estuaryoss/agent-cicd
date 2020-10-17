import click


class ConfigSender:

    @staticmethod
    def send_config(service, file_content):
        try:
            response = service.post(file_content)
            click.echo(response.get('description'))
            click.echo(f"\nEnv vars set: {response.get('config').get('env')} \n")
        except Exception as e:
            print("\nException({})".format(e.__str__()))
