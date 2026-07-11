#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sys
import os

# LOCAL PATHS
LOG_PATH = os.getenv("LOG_PATH", "/tmp/logs")

def script_run(func, log_file=None, log_level=logging.INFO, arguments=()):
    """
    Basic function for running Automation scripts. Can be used in __main__ part of script.
    Initializes logging to a single folder in a unified format.
    """
    if not log_file:
        log_file = "default_logs.log"
    
    logging.basicConfig(
        filename = f"{LOG_PATH}/{log_file}",
        level    = log_level, 
        format   = "[%(asctime)s] FILE: %(filename)-25s LINE: #%(lineno)d | %(levelname)-8s | %(message)s"
    )
    
    try:
        logging.warning("Script started.")
        func(*arguments)
        logging.warning("Script finished.")
    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit(1)