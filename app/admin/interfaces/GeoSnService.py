import abc


class GeoSnService(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass
