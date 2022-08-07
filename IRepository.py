import abc

class IRepository(metaclass=abc.ABCMeta):
    """
    Abstract class for Agnes command CRUD functions.
    """
    @abc.abstractmethod
    def give_quote(self):
        pass

    @abc.abstractmethod
    def write_quote(self):
        pass

    @abc.abstractmethod
    def get_quote_info(self):
        pass

    @abc.abstractmethod
    def give_band_name(self):
        pass

    @abc.abstractmethod
    def write_band_name(self):
        pass

    @abc.abstractmethod
    def give_album_name(self):
        pass

    @abc.abstractmethod
    def write_album_name(self):
        pass

    @abc.abstractmethod
    def give_they_called_me(self):
        pass

    @abc.abstractmethod
    def write_they_called_me(self):
        pass
