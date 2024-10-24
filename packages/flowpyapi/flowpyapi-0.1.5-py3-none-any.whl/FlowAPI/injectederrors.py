from enum import Enum


class ErrorsToInject(Enum):
    """A class for errors that can be injected to aid testing"""

    RESPONSE_SOCKET_ERROR = 1  # raise a socket.expcetion data is the error number
    RESPONSE_CANNOTSEND_ERROR = 2  # raise a http.client.CannotSendRequest exception
    RESPONSE_BADSTATUS_ERROR = 3  # raise a http.client.BadStatusLine exception


class InjectedError:
    """A class type for injected errors"""

    def __init__(self, type, data={}) -> None:
        self._type = type
        self._data = data

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data
