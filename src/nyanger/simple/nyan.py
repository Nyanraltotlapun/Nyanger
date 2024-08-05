#     Nyanger is a simple logger designed to be simple to use and simple to modify.
#
#     Copyright (C) 2024  Kirill Harmatulla Shakirov  kirill.shakirov@protonmail.com
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """
    Enumerates logging levels.
    """
    OTHER = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    DEBUG = 4


class LogMessage:
    """
    Represents message to be logged.
    Contains time severity and text fields.
    """
    def __init__(self, time: datetime, severity: LogLevel, text: str):
        """
        Initialize LogMessage instance.
        :param time: message time.
        :param severity: severity level of the message.
        :param text: message content.
        """
        self.time = time
        self.severity = severity
        self.text = text


class LogWriter(ABC):
    """
    Abstract class representing log writer interface.
    Must be implemented by a concrete log writer class.
    Only write method must be implemented, start and stop methods one should implement as needed.
    Start method will be called by Nyanger on its start.
    And stop method will be called by Nyanger on its stop.
    """
    @abstractmethod
    def start(self):
        """
        This method called on logger start.
        """
        pass

    @abstractmethod
    def write(self, msg: LogMessage):
        """
        This method called when message need to be logged.
        :param msg: message to be logged.
        :return:
        """

    @abstractmethod
    def stop(self):
        """
        This method will be called on logger stop.
        """
        pass


class Nyanger:
    """
    Simple logger designed to be simple in use and simple in changing by its user.
    """

    def __init__(self, name: str, loging_level: LogLevel, log_writers: list[LogWriter]):
        """
        Initialize Nyanger instance.
        :param name: Logger name.
        :param loginlxcg_level: Logging level, messages with severity less than this field value will be filtered out.
        :param log_writers: List of log writers.
        """
        self.name = name
        """Logger name."""
        self.loging_level = loging_level
        """Logging level, messages with severity less than this field value will be filtered out."""
        self._log_writers = log_writers.copy()
        """List of log writers."""
        self._active = False
        self._stopped = False

    def is_active(self) -> bool:
        return self._active

    def is_stopped(self) -> bool:
        return self._stopped

    def start(self):
        """
        Starts Nyanger.
        """
        if not self._stopped:
            for log_writer in self._log_writers:
                log_writer.start()
            self._active = True

    def stop(self):
        """
        Stops Nyanger.
        """
        for log_writer in self._log_writers:
            log_writer.stop()
        self._active = False
        self._stopped = True

    def log(self, message: str, severity: LogLevel):
        """
        Writes message to log writers. This method captures time of the message.
        :param message: text to be logged.
        :param severity: severity of the message.
        """
        # Filter messages with severity lower than self.loging_level
        if severity.value <= self.loging_level.value:
            # Create and write LogMessage to log writers
            message = LogMessage(datetime.now(), severity, message)
            for log_writer in self._log_writers:
                log_writer.write(message)

    def other(self, message: str):
        """
        Log message with OTHER severity level.
        :param message: text to be logged.
        """
        self.log(message, LogLevel.OTHER)

    def info(self, message: str):
        """
        Log message with INFO severity level.
        :param message: text to be logged.
        """
        self.log(message, LogLevel.INFO)

    def warning(self, message: str):
        """
        Log message with WARNING severity level.
        :param message: text to be logged.
        """
        self.log(message, LogLevel.WARNING)

    def error(self, message: str):
        """
        Log message with ERROR severity level.
        :param message: text to be logged.
        """
        self.log(message, LogLevel.ERROR)

    def debug(self, message: str):
        """
        Log message with DEBUG severity level.
        :param message: text to be logged.
        """
        self.log(message, LogLevel.DEBUG)
