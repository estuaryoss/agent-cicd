#!/usr/bin/env python3
import unittest

from about import properties
from utils.cmd_utils import CmdUtils


class FlaskServerTestCase(unittest.TestCase):
    ip = "localhost"
    port = "8080"
    token = "None"
    file = "configs/config"

    def test_cli_exit_status_0(self):
        response = CmdUtils.run_cmd_shell_true(f"python main.py "
                                               f"--ip={FlaskServerTestCase.ip} "
                                               f"--port={FlaskServerTestCase.port} "
                                               f"--token={FlaskServerTestCase.token} "
                                               f"--file={FlaskServerTestCase.file}.yml")

        print(response.get("err"))
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("Global exit code: 0", response.get('out'))

    def test_cli_exit_status_1(self):
        response = CmdUtils.run_cmd_shell_true(f"python main.py "
                                               f"--ip={FlaskServerTestCase.ip} "
                                               f"--port={FlaskServerTestCase.port} "
                                               f"--token={FlaskServerTestCase.token} "
                                               f"--file={FlaskServerTestCase.file}_exit_1.yml")

        print(response.get("err"))
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("Global exit code: 1", response.get('out'))

    def test_cli_execute_custom_uploaded_script(self):
        response = CmdUtils.run_cmd_shell_true(f"python main.py "
                                               f"--ip={FlaskServerTestCase.ip} "
                                               f"--port={FlaskServerTestCase.port} "
                                               f"--token={FlaskServerTestCase.token} "
                                               f"--file={FlaskServerTestCase.file}_custom.yml")

        print(response.get("err"))
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("You executed custom CI/CD flow", response.get('out'))
        self.assertIn("Global exit code: 0", response.get('out'))

if __name__ == '__main__':
    unittest.main()
