import logging
import logging.config
import os


def setup_logger():
    # Default values if environment variables are not set
    log_folder = "logs"
    log_file = os.environ.get("LOG_FILE", "webhunter.log")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    backups = int(os.environ.get("LOG_BACKUPS", 7))

    # Dictionary configuration for logging
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            },
        },
        'handlers': {
            'default': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f"{log_folder}/{log_file}",
                'backupCount': backups,
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default'],
                'level': log_level,
                'propagate': True
            },
        }
    }

    logging.config.dictConfig(log_config)
