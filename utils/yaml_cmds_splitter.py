class YamlCommandsSplitter:
    __in_order_fields = ["client_script"]

    def __init__(self, config):
        """ Generates list of commands in order from yaml """
        self.config = config

    def get_cmds_in_order(self):
        commands_list_in_order = []
        for section in self.__in_order_fields:
            if self.config.get(section) is not None:
                commands_list_in_order = [cmd for cmd in self.config.get(section)]

        return commands_list_in_order
