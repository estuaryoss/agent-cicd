class YamlCommandsSplitter:
    __in_order_fields_client = ["client_script"]
    __in_order_fields_server = ["before_install", "install", "after_install", "before_script", "script", "after_script"]

    def __init__(self, config):
        """ Generates list of commands in order from yaml """
        self.config = config

    def get_client_cmds_in_order(self):
        commands_list_in_order = []
        for section in self.__in_order_fields_client:
            if self.config.get(section) is not None:
                [commands_list_in_order.append(cmd) for cmd in self.config.get(section)]

        return commands_list_in_order

    def get_server_cmds_in_order(self):
        commands_list_in_order = []
        for section in self.__in_order_fields_server:
            if self.config.get(section) is not None:
                [commands_list_in_order.append(cmd) for cmd in self.config.get(section)]

        return commands_list_in_order
