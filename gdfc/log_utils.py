import functools
from logging import config
from typing import Callable

DATE_FMT = "%Y-%m-%dT%H-%M-%S"


def set_log_conf() -> None:
    config.dictConfig(
        config={
            "version": 1,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(name)-30s %(levelname)-8s %(message)s",
                    "datefmt": DATE_FMT,
                }
            },
            "loggers": {
                "": {  # root logger
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "gdfc": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "__main__": {  # if __name__ == "__main__"
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "googleapiclient.discovery_cache": {
                    "level": "ERROR",
                    "propagate": False,
                }
            },
        }
    )


def log_setup(func: Callable):
    """wrapper to factorise the logger setup"""

    set_log_conf()

    @functools.wraps(wrapped=func)
    def wrapped_func(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapped_func
