import time


class StatusChecker:

    def __init__(self, service):
        """ Progress checker for commands """
        self.service = service
        self.description = {}
        self.cmds_finished = {}

    def check_progress(self, poll_interval):
        while True:
            self.__poll_and_save()
            self.__check_if_scheduled()
            self.__mark_and_print_if_finished()
            if self.__check_finished():
                return self.__get_global_status()
            time.sleep(poll_interval)

    def __poll_and_save(self):
        try:
            self.description = self.service.get()
        except Exception as e:
            pass

    def __print_progress(self, cmd):
        details = self.description.get('commands').get(cmd).get('details')
        print(f">> {cmd}\n")
        print(details.get('out') if details.get('err') == "" else details.get('err') + "\n")
        print(f"Exit code: {details.get('code')}\n")

    def __mark_and_print_if_finished(self):
        commands = self.description.get('commands').keys()
        for cmd in commands:
            if self.description.get('commands').get(cmd).get('status') == 'finished' \
                    and cmd not in self.cmds_finished:
                self.cmds_finished[cmd] = self.description.get('commands').get(cmd).get('details').get('code')
                self.__print_progress(cmd)

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
