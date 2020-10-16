import sys

from utils.sftp import Sftp


class CommandHolder:
    commands = {
        "-quit": {
            "--method": sys.exit,
            "--args": [0]
        },
        "-trump": {
            "--method": sys.exit,
            "--args": [0]
        },
        "-put": {
            "--method": Sftp.upload_file,
            "--args": []
        },
        "-get": {
            "--method": Sftp.download_file,
            "--args": []
        },
    }

    @classmethod
    def cmd_check(cls, service, command):
        for key in cls.commands.keys():
            if key in command:
                cls.commands.get(key)["--args"] = list(
                    map(lambda x: x.strip(), command.partition("--args")[2].split(";"))) if \
                    command.partition("--args")[2] else [0]
                cls.commands.get(key)["--args"].insert(0, service) if command.partition("--args")[2] else None
                print(f"Executed {command}")
                return cls.commands.get(key).get("--method")(*CommandHolder.commands.get(key).get("--args"))

        return None
