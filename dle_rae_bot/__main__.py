"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
import sys

from dle_rae_bot.controller import TelegramDefinitionController
from dle_rae_bot.repository import HttpDefinitionRepository
from dle_rae_bot.repository.definition import DefinitionRepository

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

if __name__ == '__main__':
    token = os.getenv("TG_TOKEN")
    log_level = os.getenv("LOG_LEVEL") or logging.ERROR

    if not token:
        logging.error("Missing telegram token. May forgive to set TG_TOKEN?")
        sys.exit(1)

    # Enable logger
    logging.basicConfig(level=log_level)

    repo: DefinitionRepository = HttpDefinitionRepository()
    ctrl = TelegramDefinitionController(token, repo)
    ctrl.run()
