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
