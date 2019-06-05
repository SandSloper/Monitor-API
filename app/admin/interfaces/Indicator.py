import abc

class Indicator:
    @abc.abstractmethod
    def get_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def get_time(self):
        pass

    @abc.abstractmethod
    def get_spatial_extends(self):
        pass

    @abc.abstractmethod
    def get_units(self):
        pass

    @abc.abstractmethod
    def get_methodogy(self):
        pass

    @abc.abstractmethod
    def get_colors(self):
        pass

    @abc.abstractmethod
    def get_cat(self):
        pass