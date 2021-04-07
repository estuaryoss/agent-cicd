#!/usr/bin/env python3
import unittest

from about import properties
from utils.cmd_utils import CmdUtils


class FlaskServerTestCase(unittest.TestCase):
    ip = "localhost"
    port = "8080"
    token = ""
    batch = "true"
    file = "configs/config"
    exec = "python"
    main_path = "main.py"

    def test_cli_exit_status_0(self):
        response = CmdUtils.run_cmd_shell_true(f"{self.exec} {self.main_path} "
                                               f"--ip={self.ip} "
                                               f"--port={self.port} "
                                               f"--token=\"{self.token}\" "
                                               f"--batch={self.batch} "
                                               f"--file={self.file}.yml")

        print(response)
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("Global exit code: 0", response.get('out'))

    def test_cli_exit_status_1(self):
        response = CmdUtils.run_cmd_shell_true(f"{self.exec} {self.main_path} "
                                               f"--ip={self.ip} "
                                               f"--port={self.port} "
                                               f"--token=\"{self.token}\" "
                                               f"--batch={self.batch} "
                                               f"--file={self.file}_exit_1.yml")

        print(response)
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("Global exit code: 1", response.get('out'))

    def test_cli_execute_custom_uploaded_script(self):
        response = CmdUtils.run_cmd_shell_true(f"{self.exec} {self.main_path} "
                                               f"--ip={self.ip} "
                                               f"--port={self.port} "
                                               f"--token=\"{self.token}\" "
                                               f"--batch={self.batch} "
                                               f"--file={self.file}_custom.yml")

        print(f"{response}")
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("BIOS Version:", response.get('out'))
        self.assertIn("System Locale:", response.get('out'))
        self.assertNotIn("Error", response.get('out'))
        self.assertIn("Upload Success", response.get('out'))  # upload success
        self.assertIn("Global exit code: 0", response.get('out'))

    def test_cli_execute_cli_exits_on_first_client_error(self):
        response = CmdUtils.run_cmd_shell_true(f"{self.exec} {self.main_path} "
                                               f"--ip={self.ip} "
                                               f"--port={self.port} "
                                               f"--token=\"{self.token}\" "
                                               f"--batch={self.batch} "
                                               f"--file={self.file}_custom_exit_on_first_fail_client.yml")

        print(f"{response}")
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("BIOS Version:", response.get('out'))
        self.assertIn("System Locale:", response.get('out'))
        self.assertIn("is not recognized", response.get('out'))
        self.assertNotIn("Global exit code: 0", response.get('out'))

    def test_cli_execute_cli_exits_on_first_server_error(self):
        response = CmdUtils.run_cmd_shell_true(f"{self.exec} {self.main_path} "
                                               f"--ip={self.ip} "
                                               f"--port={self.port} "
                                               f"--token=\"{self.token}\" "
                                               f"--batch=false "
                                               f"--file={self.file}_custom_exit_on_first_fail_server.yml")

        print(f"{response}")
        self.assertIn(f"{properties.get('version')}", response.get('out'))
        self.assertIn("BIOS Version:", response.get('out'))
        self.assertIn("System Locale:", response.get('out'))
        self.assertNotIn("after invalid command", response.get('out'))
        self.assertNotIn("Global exit code: 0", response.get('out'))


if __name__ == '__main__':
    unittest.main()
