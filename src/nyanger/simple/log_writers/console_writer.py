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
import sys
from nyanger.simple.nyan import LogLevel, LogMessage, LogWriter


class Colors:
    """Console color codes."""
    RESET = '\033[0m'
    BOLD = '\033[01m'
    DISABLE = '\033[02m'
    UNDERLINE = '\033[04m'
    REVERSE = '\033[07m'
    STRIKETHROUGH = '\033[09m'
    INVISIBLE = '\033[08m'

    class FColor:
        """Foreground colors."""
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        ORANGE = '\033[33m'
        BLUE = '\033[34m'
        PURPLE = '\033[35m'
        CYAN = '\033[36m'
        LIGHT_GRAY = '\033[37m'
        DARK_GRAY = '\033[90m'
        LIGHT_RED = '\033[91m'
        LIGHT_GREEN = '\033[92m'
        YELLOW = '\033[93m'
        LIGHT_BLUE = '\033[94m'
        PINK = '\033[95m'
        LIGHT_CYAN = '\033[96m'

    class BColor:
        """Background colors."""
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        ORANGE = '\033[43m'
        BLUE = '\033[44m'
        PURPLE = '\033[45m'
        CYAN = '\033[46m'
        LIGHT_GRAY = '\033[47m'


class ConsoleWriter(LogWriter):
    """
    Simple implementation of LogWriter.
    Writes colored formatted messages to console.
    """
    def __init__(self, loging_level: LogLevel = LogLevel.DEBUG, color_map: Optional[dict[LogLevel, str]] = None):
        """
        Initialize ConsoleWriter instance.
        :param loging_level: messages with severity less than this field value will be filtered out.
        :param color_map: dictionary mapping console color codes to logging levels.
        """
        self._loging_level = loging_level

        if color_map is None:
            self._color_map = {
                LogLevel.OTHER: Colors.FColor.YELLOW,
                LogLevel.INFO: Colors.FColor.GREEN,
                LogLevel.WARNING: Colors.FColor.BLUE,
                LogLevel.ERROR: Colors.BOLD + Colors.FColor.RED,
                LogLevel.DEBUG: Colors.FColor.CYAN}
        else:
            self._color_map = color_map

    def start(self):
        """Doing nothing"""
        pass

    def write(self, msg: LogMessage):
        """
        Formats and writes msg to (sys.stdout).
        :param msg: message to be logged.
        """
        if msg.severity.value <= self._loging_level.value:
            log_text = f"{self._color_map[msg.severity]}{msg.time.isoformat()} {msg.severity.name}: {msg.text}\n{Colors.RESET}"
            sys.stdout.write(log_text)

    def stop(self):
        """Doing nothing"""
        pass
