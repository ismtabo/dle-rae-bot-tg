import logging
from uuid import uuid4

from dle_rae_bot.repository import HttpDefinitionRepository
from telegram import InlineQueryResultArticle, ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, InlineQueryHandler,
                          Updater)
from telegram.inline.inputtextmessagecontent import InputTextMessageContent


class TelegramDefinitionController:

    def __init__(self, token: str, repository: HttpDefinitionRepository) -> None:
        self.token=token
        self.repository=repository

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def inlinequery(self, update: Update, context: CallbackContext) -> None:
        """Handle the inline query."""
        query=update.inline_query.query
        definition=self.repository.get_definitions(query)
        logging.debug('definition obtained: %s' % repr(definition))
        if definition is None:
            results=[]
        else:
            results=[
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=definition.word,
                    description=definition.description,
                    input_message_content=InputTextMessageContent(
                        definition.markdown(), parse_mode=ParseMode.MARKDOWN
                    )
                )
            ]
        update.inline_query.answer(results)

    def start(self) -> None:
        """Run the bot."""
        # Create the Updater and pass it your bot's token.
        updater = Updater(self.token)
        me = updater.bot.get_me()
        logging.info('Starting updater for bot: %s' % me)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help_command))

        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(InlineQueryHandler(self.inlinequery))

        # Start the Bot
        updater.start_polling()

        # Block until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
