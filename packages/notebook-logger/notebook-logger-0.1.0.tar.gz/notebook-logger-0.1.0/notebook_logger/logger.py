import logging

class SimpleLogger:

    def __init__(self):
        logging.basicConfig(
            filename='notebook_msg.log',
            level=logging.INFO,
            format='%(asctime)s || %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
        )

    def set_file(self, filepath):
        logging.basicConfig(filename=filepath)

    def log(self, message, only_file=False):
        if not only_file:
            print(message)
        logging.info(message)
        