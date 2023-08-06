import Handlers.files_handler
import os
from enum import Enum
from datetime import datetime

class KLog():

    _instances = {}

    class LogSeverity(Enum):
        WARNING = 'WARNING'
        DEBUG = 'DEBUG'
        ERROR = 'ERROR'
        CRITICAL = 'CRITICAL'
        INFO = 'INFO'

    """
        This method initialize a new instance if no exists one before
    """
    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
            return instance
        return cls._instances[cls]
    
    """
        This method initialize the log and, if not exists creates one

        Arguments:
            folder:     string  |   Path where Log file is located
            log_name:   srting  |   Name of the log
            max_size:   int     |   Max size the log can reach (MB)
            is_zip:     bool    |   Flag to set if zip and save the logs or not
            max_zip:    int     |   Max number of zips saved in folder
    """
    def __init__(self, folder='', log_name='', max_size=10, is_zip=True, max_zip=10):
        self.folder = folder
        self.log_name = log_name
        self.max_size = max_size
        self.is_zip = is_zip
        self.max_zip = max_zip

        log_file = os.path.join(self.folder, self.log_name)

        Handlers.files_handler.file_exists(log_file)

    """
        This method writes one log line
    
        Arguments:
        where:      string  |   Class/method where message calls
        severity:   Enum    |   Default value "DEBUG"
        msg:        string  |   Log line to print
    """
    def write(self, where='', msg='', severity=LogSeverity.DEBUG):
        time = datetime.now()
        self.time = time
        self.where = where
        self.severity = severity.value
        self.msg = msg

        Handlers.files_handler.write(self)
