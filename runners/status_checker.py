import os
import time

from utils.command_hasher import CommandHasher
from utils.io_utils import IOUtils


class StatusChecker:

    def __init__(self, service):
        """ Progress checker for commands """
        self.service = service
        self.description = {}
        self.was_cmd_printed = {}
        self.f_seek = {}
        self.cmd_hasher = CommandHasher()

    def check_progress_async(self, poll_interval):
        self.__poll_and_save()
        self.__check_if_scheduled()
        self.__init_f_seek()
        self.__init_was_cmd_printed()
        while True:
            self.__poll_and_save()
            self.__stream_out_err()
            if self.__check_finished_global():
                return self.__get_global_status()
            time.sleep(poll_interval)

    def check_progress_sync(self, description):
        self.__save(description)
        self.__check_if_scheduled()
        self.__init_f_seek()
        self.__init_was_cmd_printed()
        while True:
            self.__save(description)
            self.__stream_out_err()
            if self.__check_finished_global():
                return self.__get_global_status()

    def __poll_and_save(self):
        description = self.service.get().get('description')
        try:
            if isinstance(description, dict):
                self.description = description
            else:
                raise Exception(description)
        except Exception as e:
            pass

    def __save(self, description):
        if isinstance(description, dict):
            self.description = description

    def __print_progress(self, cmd):
        if len(self.f_seek[cmd]) == 0:
            self.f_seek[cmd] = [IOUtils.get_fh_for_read(self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".out")),
                                IOUtils.get_fh_for_read(self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".err"))]
        out, err = self.f_seek[cmd][0].read().rstrip(), self.f_seek[cmd][1].read().rstrip()
        self.f_seek[cmd][0].seek(0, os.SEEK_END), self.f_seek[cmd][1].seek(0, os.SEEK_END)
        self.__print_result(err, out)
        if self.__check_finished_cmd(cmd=cmd) and not self.was_cmd_printed[cmd]:
            self.was_cmd_printed[cmd] = True
            print(f"'{cmd}' exit code: {self.__get_cmd_exit_code(cmd=cmd)}\n")

    def __print_result(self, err, out):
        if err == "" and out == "":
            pass
        elif err == "":
            print(out)
        else:
            print(err)

    def __stream_out_err(self):
        commands = self.description.get('commands').keys()
        for cmd in commands:
            out_file = self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".out")
            err_file = self.cmd_hasher.get_cmd_for_file_encode_str(cmd, ".err")
            try:
                IOUtils.write_to_file(out_file, self.description.get('commands').get(cmd).get('details').get('out'))
                IOUtils.write_to_file(err_file, self.description.get('commands').get(cmd).get('details').get('err'))
                self.__print_progress(cmd=cmd)
            except:
                continue

    def __check_finished_global(self):
        return self.description.get('finished')

    def __check_finished_cmd(self, cmd):
        return self.description.get('commands').get(cmd).get('status') == "finished"

    def __get_global_status(self):
        commands = self.description.get('commands').keys()
        for cmd in commands:
            if self.description.get('commands').get(cmd).get('details').get('code') != 0:
                return 1
        return 0

    def __check_if_scheduled(self):
        if len(self.description.get('commands')) == 0:
            raise BaseException("Error in the agent.\n")

    def __init_f_seek(self):
        self.f_seek = {key: [] for key in self.description.get('commands').keys()}

    def __init_was_cmd_printed(self):
        self.was_cmd_printed = {key: False for key in self.description.get('commands').keys()}

    def __get_cmd_exit_code(self, cmd):
        return self.description.get('commands').get(cmd).get('details').get('code')
