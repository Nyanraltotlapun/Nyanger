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
