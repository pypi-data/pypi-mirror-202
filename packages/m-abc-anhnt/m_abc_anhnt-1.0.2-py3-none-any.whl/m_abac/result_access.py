class ResultAccess:
    def __init__(self):
        self.allow_access = False
        self.display_config = []
        self.filter_config = []

    def get_allow_access(self):
        return self.allow_access

    def set_allow_access(self, value: bool):
        self.allow_access = value

    def get_filter_config(self):
        return self.filter_config

    def add_filter_config(self, value):
        self.filter_config.append(value)

    def get_display_config(self):
        return self.display_config

    def add_display_config(self, value):
        self.display_config.append(value)
