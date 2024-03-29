import platform
import subprocess

from environment.environment import EnvironmentSingleton
from utils.command_hasher import CommandHasher
from utils.io_utils import IOUtils


class CmdUtils:

    @staticmethod
    def run_cmd_shell_true_get_str(command):
        if platform.system() == "Windows":
            response = CmdUtils.run_cmd_shell_true_to_file_list(list_cmd=command)
        else:
            response = CmdUtils.run_cmd_shell_true_to_file_list(list_cmd=[" ".join(command)])

        return response

    @staticmethod
    def start_cmd_detached(command):
        p = subprocess.Popen(command, env=EnvironmentSingleton.get_instance().get_env_and_virtual_env())

        print("Opened pid {} for command {}".format(p.pid, command))

        return p.pid

    @staticmethod
    def run_cmd_shell_true(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=EnvironmentSingleton.get_instance().get_env_and_virtual_env(), shell=True)
        return CmdUtils.__get_subprocess_data(p)

    @staticmethod
    def run_cmd_shell_true_to_file_list(list_cmd):
        file_path_out, file_path_err = CommandHasher.get_cmd_for_file_encode_list(command=list_cmd, suffix=".out"), \
                                       CommandHasher.get_cmd_for_file_encode_list(command=list_cmd, suffix=".err")
        IOUtils.recreate_files([file_path_out, file_path_err])
        with open(file_path_out, 'w') as fh_out, open(file_path_err, 'w') as fh_err:
            p = subprocess.Popen(list_cmd, stdout=fh_out, stderr=fh_err,
                                 env=EnvironmentSingleton.get_instance().get_env_and_virtual_env(), shell=True)

        return CmdUtils.__get_subprocess_data_file(p, file_out=file_path_out, file_err=file_path_err)

    @staticmethod
    def run_cmd_shell_true_to_file_str(str_cmd):
        file_path_out, file_path_err = \
            CommandHasher.get_cmd_for_file_encode_str(command=str_cmd, suffix=".out"), \
            CommandHasher.get_cmd_for_file_encode_str(command=str_cmd, suffix=".err")

        IOUtils.recreate_files([file_path_out, file_path_err])
        with open(file_path_out, 'w') as fh_out, open(file_path_err, 'w') as fh_err:
            p = subprocess.Popen(str_cmd, stdout=fh_out, stderr=fh_err,
                                 env=EnvironmentSingleton.get_instance().get_env_and_virtual_env(), shell=True)

        return CmdUtils.__get_subprocess_data_file(p, file_out=file_path_out, file_err=file_path_err)

    @staticmethod
    def run_cmd_shell_false(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=EnvironmentSingleton.get_instance().get_env_and_virtual_env())
        return CmdUtils.__get_subprocess_data(p)

    @staticmethod
    def __get_subprocess_data(p):
        out, err = p.communicate()

        return {
            "code": p.returncode,
            "out": out.decode("UTF-8", "replace"),
            "err": err.decode("UTF-8", "replace"),
            "pid": p.pid,
            "args": p.args
        }

    @staticmethod
    def __get_subprocess_data_file(p, file_out, file_err):
        p.communicate()

        return {
            "code": p.returncode,
            "out": IOUtils.read_file(file_out),
            "err": IOUtils.read_file(file_err),
            "pid": p.pid,
            "args": p.args
        }
