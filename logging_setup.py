import logging

def setup_logging(log_file="traces.log", level=logging.ERROR):

    logging.basicConfig(filename=log_file, level=level,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Log displayed in the console as well
    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info("Logging initialized.")


