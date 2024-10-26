from abc import ABC, abstractmethod
from time import sleep
from typing import override

from loguru import logger
from serial import Serial
from serial.threaded import LineReader, Protocol, ReaderThread
from serial.tools import list_ports


class Connection(ABC):
    """Abstract base class for a connection."""

    def __init__(self):
        pass

    @abstractmethod
    def send(self, data: str) -> str:
        """Send data over the connection."""
        pass

    @abstractmethod
    def receive(self) -> str:
        """Receive data from the connection."""
        pass

    @abstractmethod
    def get_wled_status(self) -> str:
        """Get the status of the connected device."""
        pass

    def start(self):
        """Start the connection."""
        pass

    def stop(self):
        """Stop the connection."""
        pass


class SerialReader(LineReader):
    """Serial reader class for reading lines from a serial connection."""

    def __init__(self):
        super(SerialReader, self).__init__()
        self.received_data: list[str] = []

    def connection_made(self, transport):
        super(SerialReader, self).connection_made(transport)
        logger.info("port opened")

    def handle_line(self, data):
        logger.trace("line received: {}\n".format(repr(data)))
        self.received_data.append(data)

    def connection_lost(self, exc):
        if exc:
            logger.error(exc)
        logger.info("port closed")


class SerialConnection(Connection):
    """Serial connection class for communicating with a device over a serial port."""

    TIMEOUT = 0.05
    COMMAND_WAIT = 0.005

    @override
    def __init__(self, port: str, baudrate: int):
        super(SerialConnection, self).__init__()
        self._port = port
        self._baudrate = baudrate
        self._serial: Serial = None
        self._protocol: Protocol = None
        self.start()

    @override
    def send(self, data: str) -> None:
        """Send data over the serial connection."""
        self._clear_buffer()
        self._send_string(data)
        sleep(self.COMMAND_WAIT)

    @override
    def receive(self) -> str:
        """Receive data from the serial connection."""
        return self._retrieve_response()

    def _send_string(self, data: str) -> None:
        """Send a string over the serial connection."""
        self._protocol.write_line(data)

    def _retrieve_response(self):
        """Retrieve the response from the serial connection."""
        timeout = 20
        while not self._protocol.received_data and timeout > 0:
            timeout -= 1
            sleep(self.COMMAND_WAIT)
        ret = self._protocol.received_data.pop()
        return ret

    def _clear_buffer(self):
        """Clear the buffer of received data."""
        self._protocol.received_data.clear()

    @classmethod
    def available_ports(cls, regexp: str = None, include_links=True) -> list[any]:
        """Get a list of available serial ports."""
        return list_ports.grep(regexp, include_links)

    @override
    def get_wled_status(self) -> str:
        """Get the status of the serial connection."""
        status_request = '{"v":true}'
        self._clear_buffer()
        self._send_string(status_request)
        return self._retrieve_response()

    @override
    def start(self):
        """Start the serial connection."""
        self._serial = Serial(
            self._port, baudrate=self._baudrate, timeout=SerialConnection.TIMEOUT
        )
        self._protocol = ReaderThread(self._serial, SerialReader).__enter__()

    @override
    def stop(self):
        """Stop the serial connection."""
        self._protocol.__exit__(None, None, None)
