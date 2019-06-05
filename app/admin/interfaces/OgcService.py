import abc


class OgcService(abc.ABC):
    @abc.abstractmethod
    def createAllServices(self):
        pass

    @abc.abstractmethod
    def createSingleService(self, indicator, file_path=None):
        pass
