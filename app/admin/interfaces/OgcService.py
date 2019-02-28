import abc

class OgcService(abc.ABC):
    @abc.abstractmethod
    def createAllServices(self):
        pass
    @abc.abstractmethod
    def createSingleService(self,indicator,file_path=None):
        pass

    @abc.abstractmethod
    def writeFile(self,file_path=None):
        pass