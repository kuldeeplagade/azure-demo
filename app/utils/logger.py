from fastapi import FastAPI, HTTPException
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import colorlog

class ROSLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        # Create a rotating file handler for access logs (delete every day)
        access_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, "access.log"),
            when="midnight",
            interval=1,
            backupCount=1,  # Do not keep old logs
        )
        access_handler.setLevel(logging.INFO)

        # Create a rotating file handler for error logs (delete every day)
        error_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, "error.log"),
            when="midnight",
            interval=1,
            backupCount=1,  # Do not keep old logs
        )
        error_handler.setLevel(logging.ERROR)

        # Create a console handler for debug, info, warning, error, and critical logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a colored formatter
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p",
            log_colors={
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            reset=True,
            secondary_log_colors={},
            style='%'
        )

        # Create a non-colored formatter for file handlers
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p"
        )

        # Set formatter for the handlers
        access_handler.setFormatter(file_formatter)
        error_handler.setFormatter(file_formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.addHandler(access_handler)
        self.addHandler(error_handler)
        self.addHandler(console_handler)

# Create FastAPI instance
app = FastAPI()

# Initialize ROSLogger instance
logger = ROSLogger(__name__)
