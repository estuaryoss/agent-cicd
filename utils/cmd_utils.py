import subprocess


class CmdUtils:

    @staticmethod
    def run_cmd_detached(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Opened pid {} for command {}".format(p.pid, command))

    @staticmethod
    def run_cmd_shell_true(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return CmdUtils.__get_subprocess_data(p)

    @staticmethod
    def run_cmd_shell_true_get_str(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        response = CmdUtils.__get_subprocess_data(p)
        if response.get("code") != 0:
            raise BaseException(response.get("err"))

        return response.get("out")

    @staticmethod
    def run_cmd_shell_false(command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return CmdUtils.__get_subprocess_data(p)

    @staticmethod
    def __get_subprocess_data(p):
        lines_to_slice = 500
        [out, err] = p.communicate()

        return {
            "out": "\n".join(out.decode("UTF-8", "replace").split("\n")[-lines_to_slice:]).rstrip(),
            "err": "\n".join(err.decode("UTF-8", "replace").split("\n")[-lines_to_slice:]).rstrip(),
            "code": p.returncode,
            "pid": p.pid,
            "args": p.args
        }
