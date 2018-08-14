import json
import logging
import os

from datetime import datetime


class Global:
    def __init__(self):
        pass

    @staticmethod
    def get_logger(name, local_file, local_dir):
        log = logging.getLogger(name)
        log_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s '%(message)s'")

        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)

        handler_console = logging.StreamHandler()
        handler_console.setFormatter(log_formatter)
        # handler_file = logging.FileHandler(local_file)
        # handler_file.setFormatter(log_formatter)

        if len(log.handlers) == 0:
            log.addHandler(handler_console)
            # log.addHandler(handler_file)

        log.setLevel(logging.INFO)
        return log

    @staticmethod
    def get_files(path):
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return files

    @staticmethod
    def get_json(data_file):
        with open(data_file, 'r') as infile:
            data = json.load(infile)
            return json.dumps(data)

    @staticmethod
    def get_timestamp():
        """ Generate a timestamp

        :return: timestamp string
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

