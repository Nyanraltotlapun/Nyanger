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

from multiprocessing import Process, Queue as ProcessQueue
from typing import Optional
from datetime import datetime
from abc import ABC, abstractmethod
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
    Start method will be called by Nyanger inside log precess on its start.
    And stop method will be called inside log process after exiting logging loop.
    """
    @abstractmethod
    def start(self):
        """
        This method called inside log precess after its start.
        """
        pass

    @abstractmethod
    def write(self, msg: LogMessage):
        """
        This method called by logging loop when message need to be logged.
        :param msg: message to be logged.
        :return:
        """

    @abstractmethod
    def stop(self):
        """
        This method will be called inside log process after exiting logging loop.
        """
        pass


class Nyanger:
    """
    Simple logger designed to be simple in use and simple in changing by its user.
    """

    def __init__(self, name: str, loging_level: LogLevel, log_writers: list[LogWriter]):
        self.name = name
        """Logger name."""
        self.loging_level = loging_level
        """Logging level, messages with severity less than this field value will be filtered out"""
        self._log_writers = log_writers.copy()
        """List of log writers."""
        self._log_queue: ProcessQueue[LogMessage | int] = ProcessQueue()
        """Queue of log messages used to pass them to log process."""
        self._nyan_process: Optional[Process] = None
        """Stores log process."""
        self._STOP_MESSAGE = 0
        """Constant representing message that need to be putted in self._log_queue in order to break logging loop."""

    def _logging_loop(self):
        for log_writer in self._log_writers:
            log_writer.start()

        while True:
            try:
                message = self._log_queue.get()
                if message == self._STOP_MESSAGE:
                    break

                for log_writer in self._log_writers:
                    log_writer.write(message)

            except KeyboardInterrupt:
                continue

        for log_writer in self._log_writers:
            log_writer.stop()

    def is_running(self):
        """
        Checks out logging process running status.
        :return: True if logging process is alive and False otherwise.
        """
        if self._nyan_process is None:
            return False
        return self._nyan_process.is_alive()

    def start(self):
        """
        Starts Nyanger.
        Creating and starts logging process.
        :return:
        """
        self._nyan_process = Process(target=self._logging_loop, name=f"{self.name}_logger", daemon=True)
        self._nyan_process.start()

    def stop(self, timeout: float = 5.0):
        """
        Stops Nyanger.
        Sending stop message to logging process and waits timeout seconds for process end.
        If process still active after timeout seconds - terminates it.
        :param timeout: Number of seconds to wait for process to terminate.
        :return:
        """
        self._log_queue.put(self._STOP_MESSAGE)
        self._nyan_process.join(timeout=timeout)
        self._nyan_process.terminate()

    def log(self, message: str, severity: LogLevel):
        """
        Puts message to logging queue. This method captures time of the message.
        :param message: text to be logged.
        :param severity: severity of the message.
        :return:
        """
        # Filter messages with severity lower than self.loging_level
        if severity.value <= self.loging_level.value:
            # Create and put LogMessage to log queue
            self._log_queue.put(LogMessage(datetime.now(), severity, message))

    def other(self, message: str):
        """
        Log message with OTHER severity level.
        :param message: text to be logged.
        :return:
        """
        self.log(message, LogLevel.OTHER)

    def info(self, message: str):
        """
        Log message with INFO severity level.
        :param message: text to be logged.
        :return:
        """
        self.log(message, LogLevel.INFO)

    def warning(self, message: str):
        """
        Log message with WARNING severity level.
        :param message: text to be logged.
        :return:
        """
        self.log(message, LogLevel.WARNING)

    def error(self, message: str):
        """
        Log message with ERROR severity level.
        :param message: text to be logged.
        :return:
        """
        self.log(message, LogLevel.ERROR)

    def debug(self, message: str):
        """
        Log message with DEBUG severity level.
        :param message: text to be logged.
        :return:
        """
        self.log(message, LogLevel.DEBUG)
