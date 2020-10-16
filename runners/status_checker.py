import time


class StatusChecker:

    def __init__(self, service):
        """ Progress checker for commands """
        self.service = service
        self.response = {}
        self.cmds_finished = []

    def check_progress(self, poll_interval):
        while True:
            self.__poll_and_save()
            self.__mark_if_finished()
            self.__print_progress()
            self.__check_finished()
            time.sleep(poll_interval)

    def __poll_and_save(self):
        try:
            self.response = self.service.get()
        except Exception as e:
            pass

    def __print_progress(self):
        print("in progress")

    def __mark_if_finished(self):
        pass

    def __check_finished(self):
        return True
