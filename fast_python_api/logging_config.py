"""
Logging configuration
--------------------

Basic logging configuration for FastAPI application.

"""


import logging


#: Format string for logging output.
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_logging() -> None:
    """
    Configure logging.

    Configure logging to output to console with level INFO.
    """
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
    )


logger = logging.getLogger("fastapi_debug")
