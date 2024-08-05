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

from typing import Optional
import asyncio
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
    Start method will be called by Nyanger inside log precess on its start.
    And stop method will be called inside log process after exiting logging loop.
    """
    @abstractmethod
    async def start(self, loop: asyncio.AbstractEventLoop):
        """writers
        This method called before start of logging loop.
        """
        pass

    @abstractmethod
    async def write(self, msg: LogMessage):
        """
        This method called by logging loop when message need to be logged.
        :param msg: message to be logged.
        :return:
        """

    @abstractmethod
    async def stop(self):
        """
        This method will be called after exiting logging loop.
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
        """Logging level, messages with severity less than this field value will be filtered out."""
        self._log_writers = log_writers.copy()
        """List of log writers."""
        self._log_queue: Optional[asyncio.Queue[LogMessage | int]] = None
        """Queue of log messages used to pass them to logging loop."""
        self._logging_loop_task: Optional[asyncio.Task] = None
        """Logging loop asyncio task"""
        self._STOP_MESSAGE = 0
        """Constant representing message that need to be putted in self._log_queue in order to break logging loop."""

    async def _logging_loop(self, loop: asyncio.AbstractEventLoop):
        for log_writer in self._log_writers:
            await log_writer.start(loop)

        while True:
            try:
                message = await self._log_queue.get()
                self._log_queue.task_done()
                if message == self._STOP_MESSAGE:
                    break

                for log_writer in self._log_writers:
                    await log_writer.write(message)

                self._log_queue.task_done()

            except asyncio.CancelledError:
                break

        for log_writer in self._log_writers:
            await log_writer.stop()

    def is_running(self):
        """
        Checks out if logging loop is running.
        :return: True if logging loop is running, False otherwise.
        """
        return not self._logging_loop_task.done()

    async def start(self, loop: asyncio.AbstractEventLoop):
        """
        Starts Nyanger.
        Create logging task.
        :return:
        """
        self._log_queue = asyncio.Queue()
        self._logging_loop_task = asyncio.Task(self._logging_loop(loop))

    async def stop(self, timeout: float = 5.0, supress_timeout_error: bool = True):
        """
        Stops Nyanger.
        Sending stop message to logging process and waits timeout seconds for process end.
        If process still active after timeout seconds - terminates it.
        :param timeout: Number of seconds to wait for process to terminate.
        :param supress_timeout_error: Pum
        :return:
        """
        await self._log_queue.put(self._STOP_MESSAGE)
        # Wait for at most timeout seconds
        try:
            await asyncio.wait_for(self._logging_loop_task, timeout=timeout)
        except TimeoutError as ex:
            if not supress_timeout_error:
                raise ex

    async def log(self, message: str, severity: LogLevel):
        """
        Puts message to logging queue. This method captures time of the message.
        :param message: text to be logged.
        :param severity: severity of the message.
        :return:
        """
        # Filter messages with severity lower than self.loging_level
        if severity.value <= self.loging_level.value:
            # Create and put LogMessage to log queue
            await self._log_queue.put(LogMessage(datetime.now(), severity, message))

    async def other(self, message: str):
        """
        Log message with OTHER severity level.
        :param message: text to be logged.
        """
        await self.log(message, LogLevel.OTHER)

    async def info(self, message: str):
        """
        Log message with INFO severity level.
        :param message: text to be logged.
        """
        await self.log(message, LogLevel.INFO)

    async def warning(self, message: str):
        """
        Log message with WARNING severity level.
        :param message: text to be logged.
        """
        await self.log(message, LogLevel.WARNING)

    async def error(self, message: str):
        """
        Log message with ERROR severity level.
        :param message: text to be logged.
        """
        await self.log(message, LogLevel.ERROR)

    async def debug(self, message: str):
        """
        Log message with DEBUG severity level.
        :param message: text to be logged.
        """
        await self.log(message, LogLevel.DEBUG)
