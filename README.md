# Nyanger - simple logger

**Nyanger** is a simple logger designed to be simple to use and simple to modify.

Creation of Nyanger was motivated by the need of a simple logging facility for simple everyday scripts as well as simple logging solution for complex multiprocessing code.

Nyanger designed to be simultaneously: working solution, prototype, and code example.
So use Nyanger as is, extend it with **LogWriters**, or modify source code to fill your needs.

Nyanger consist of 3 modules:
- **async** (for the use with asyncio)
- **process** (for use with code of any complexity, but especially complex multiprocessing/multithreading code)
- **simple** (for plain simple scripts or multithreading code)

# Compatibility
Nyanger compatible with **Linux** (and probably any *NIX), and probably with **Windows** (feel free to test and report any issues)

# Usage
All 3 modules follow same pattern:
1. `Nyanger` is our logger class. You need to get instance of it ether by creating object manually or by calling `get_logger` method. 
2. You must provide list of `LogWriter` objects to `Nyanger` constructor, if `get_logger` called without this list then default console `LogWriter` will be created.
3. You can create your own log writes by implementing `LogWriter` abstract class.
4. You start logger by calling `start()` method.
5. You use it by calling `other()` `info()` `warning()` `error()` `debug()` or `log()` methods of `Nyanger` instance.
6. Before ending your program you're stopping logger by calling `stop()` method.

# Example
Init Nyanger directly:

```python
import nyanger.process as nya
import nyanger.process.log_writers.console_writer as cwr

log: nya.Nyanger

if __name__ == '__main__':
    # Init logger
    log = nya.Nyanger("pur", loging_level=nya.LogLevel.DEBUG, log_writers=[cwr.ConsoleWriter()])

    log.start()
    log.other("Other test pur")
    log.info("Info test put")
    log.warning("Warning test pur")
    log.error("Error test pur")
    log.debug("Debug test pur")
    log.stop()
```

Using get_logger helper:
```python
import nyanger.process.static as nya_stat

# Init logger
log = nya_stat.get_logger("nyan")

if __name__ == '__main__':
    log.start()
    log.other("Other test pur")
    log.info("Info test put")
    log.warning("Warning test pur")
    log.error("Error test pur")
    log.debug("Debug test pur")
    log.stop()
```
