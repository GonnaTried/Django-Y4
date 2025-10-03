# yourapp/management/commands/sendtelegram.py

import asyncio

import telegram
from decouple import config
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sends a test message to a specified Telegram chat."

    def add_arguments(self, parser):
        parser.add_argument("message", type=str, help="The message to be sent.")

    def handle(self, *args, **options):
        """
        The main entry point for the Django command.
        It remains a synchronous method.
        """
        # We use asyncio.run() to call our asynchronous logic
        try:
            asyncio.run(self.main(*args, **options))
        except Exception as e:
            # Catch any other unexpected errors from the async part
            self.stdout.write(self.style.ERROR(f"An overall error occurred: {e}"))

    async def main(self, *args, **options):
        """
        This is where all our asynchronous logic lives.
        """
        # Get token and chat_id from .env file
        try:
            bot_token = config("TELEGRAM_BOT_TOKEN")
            chat_id = config("TELEGRAM_CHAT_ID")
            message = options["message"]
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Configuration error: Could not find TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in your .env file. {e}"
                )
            )
            return

        self.stdout.write(
            self.style.NOTICE(f"Attempting to send message to chat ID: {chat_id}")
        )

        try:
            # Initialize the bot
            bot = telegram.Bot(token=bot_token)

            # Send the message (and properly await it)
            await bot.send_message(chat_id=chat_id, text=message)

            self.stdout.write(self.style.SUCCESS("Message sent successfully!"))

        except telegram.error.Unauthorized:
            self.stdout.write(
                self.style.ERROR(
                    "Unauthorized: Invalid bot token. Please check your .env file."
                )
            )
        except telegram.error.BadRequest as e:
            self.stdout.write(
                self.style.ERROR(f"Bad Request: {e}. Is the chat_id correct?")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
