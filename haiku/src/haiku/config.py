"""
Configuration file utilities
"""

import json
import logging
import sys

logger = logging.getLogger(__name__)


def load_config(filepath: str, conf_definition: dict = None) -> dict:
    """
    Load configuration file into memory

    :param str filepath: Path to config file
    :param dict conf_definition: Definition of expected configurations
    :return dict: Configuration object
    """
    try:
        with open(filepath) as f:
            conf = json.load(f)
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Could not load configuration file - {filepath}")
        logger.error(e)
        sys.exit(1)
    except FileNotFoundError as e:
        logging.warning(f"Configuration file could not be located - {filepath}. Using the default configuration")
        return {}

    if conf_definition or conf:
        check_config(conf, conf_definition)

    return conf


def check_config(conf, conf_definition):

    for key, key_type in conf_definition.items():
        if key not in conf:
            logger.warning(f"Expected configuration '{key}' was not specified in the configuration file")
        elif not isinstance(conf[key], key_type):
            logger.warning(f"Configuration '{key}' is not the expected type {key_type}")

    # check if config has an unexpected key
    for key in conf.keys():
        if key not in conf_definition:
            logger.warning(f"Configuration '{key}' was not expected and will be ignored")


