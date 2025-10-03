# yourapp/management/commands/sendtestemail.py

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sends a test email to confirm email configuration."

    def add_arguments(self, parser):
        # This allows you to specify the recipient's email on the command line
        # It's an optional argument
        parser.add_argument(
            "recipient_email",
            nargs="?",  # '?' means it's optional
            type=str,
            default="default.recipient@example.com",  # A default if none is provided
            help="The email address of the recipient.",
        )

    def handle(self, *args, **options):
        # --- ADD THESE LINES FOR DEBUGGING ---
        self.stdout.write("--- Verifying Django Settings ---")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write("---------------------------------")
        # --- END OF DEBUGGING LINES ---

        recipient = options["recipient_email"]

        self.stdout.write(
            self.style.NOTICE(f"Attempting to send a test email to {recipient}...")
        )

        try:
            send_mail(
                # Subject
                "Django Test Email",
                # Message
                "Hello! This is a test email sent from a Django management command.",
                # From
                settings.EMAIL_HOST_USER,
                # To
                [recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("Test email sent successfully!"))
            self.stdout.write(self.style.SUCCESS(f"Check the inbox for {recipient}."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
            self.stdout.write(
                self.style.ERROR(
                    "Please check your EMAIL_* settings in your .env or settings.py file."
                )
            )
