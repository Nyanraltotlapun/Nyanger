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

from nyanger.process.log_writers.console_writer import ConsoleWriter
from nyanger.process.nyan import *

_loggers: dict[str, Nyanger] = {}
"""Dictionary containing loggers"""


def get_logger(name: str, loging_level: LogLevel = LogLevel.DEBUG,
               log_writers: Optional[list[LogWriter]] = None) -> Nyanger:
    """
    Creating new or retrieving existing logger by its name.
    If log_writers parameter is not provided than default console writer will be attached to new logger.
    :param name: logger name.
    :param loging_level: logging level for the logger, messages with severity less than this value will be filtered out.
    :param log_writers: list of log writers to use with this logger.
    :return: instance of Nyanger
    """

    if name in _loggers:
        return _loggers[name]

    if log_writers is None or len(log_writers) == 0:
        log_writers = [ConsoleWriter()]

    new_logger = Nyanger(name, loging_level=loging_level, log_writers=log_writers)
    _loggers[name] = new_logger
    return new_logger
