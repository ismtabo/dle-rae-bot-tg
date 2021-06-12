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
from uuid import uuid4

from telegram import InlineQueryResultArticle, Update
from telegram.ext import (CallbackContext, CommandHandler, InlineQueryHandler,
                          Updater)
from telegram.inline.inputtextmessagecontent import InputTextMessageContent

from .rae import get_definitions

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    definition = get_definitions(query)
    logging.debug('definition obtained: %s' % repr(definition))
    if definition is None:
        results = []
    else:
        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title=definition.word,
                description=definition.description,
                input_message_content=InputTextMessageContent(str(definition))
            )
        ]
    update.inline_query.answer(results)


def main(token: str) -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)
    me = updater.bot.get_me()
    logging.info('Starting updater for bot: %s' % me)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    token = os.getenv("TG_TOKEN")
    log_level = os.getenv("LOG_LEVEL") or logging.ERROR

    if not token:
        logging.error("Missing telegram token. May forgive to set TG_TOKEN?")
        sys.exit(1)

    # Enable logger
    logging.basicConfig(level=log_level)

    main(token)
