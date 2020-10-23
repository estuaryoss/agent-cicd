import os
import time

from utils.command_hasher import CommandHasher
from utils.io_utils import IOUtils


class StatusChecker:

    def __init__(self, service):
        """ Progress checker for commands """
        self.service = service
        self.description = {}
        self.cmds_finished = {}
        self.f_seek = {}
        self.cmd_hasher = CommandHasher()

    def check_progress(self, poll_interval):
        self.__poll_and_save()
        self.__check_if_scheduled()
        self.__init_f_seek()
        while True:
            self.__poll_and_save()
            self.__stream_out_err()
            if self.__check_finished():
                return self.__get_global_status()
            time.sleep(poll_interval)

    def __poll_and_save(self):
        try:
            self.description = self.service.get()
        except Exception as e:
            pass

    def __print_progress(self, cmd):
        if len(self.f_seek[cmd]) == 0:
            self.f_seek[cmd] = [IOUtils.get_fh_for_read(self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".out")),
                                IOUtils.get_fh_for_read(self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".err"))]
        out, err = self.f_seek[cmd][0].read(), self.f_seek[cmd][1].read()
        self.f_seek[cmd][0].seek(0, os.SEEK_END), self.f_seek[cmd][1].seek(0, os.SEEK_SET)
        if out == "" and err == "":
            return
        print(out if err == "" else err)

    def __stream_out_err(self):
        commands = self.description.get('commands').keys()
        for cmd in commands:
            out_file = self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".out")
            err_file = self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".err")
            try:
                IOUtils.write_to_file(out_file, self.description.get('commands').get(cmd).get('details').get('out'))
                IOUtils.write_to_file(err_file, self.description.get('commands').get(cmd).get('details').get('err'))
                self.__print_progress(cmd=cmd)
            except Exception as e:
                continue

    def __check_finished(self):
        return self.description.get('finished')

    def __get_global_status(self):
        commands = self.cmds_finished.keys()
        for cmd in commands:
            if self.cmds_finished.get(cmd) != 0:
                return 1
        return 0

    def __check_if_scheduled(self):
        if len(self.description.get('commands')) == 0:
            raise Exception("Exception: ({})".format("Error in the agent. The commands are not scheduled. "
                                                     "Check if you have 'start.py' in the path\n"))

    def __init_f_seek(self):
        self.f_seek = {key: [] for key in self.description.get('commands').keys()}
