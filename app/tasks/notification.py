import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationStrategy():

    def send_email(self, message: str):
        # Write send email function here
        logger.info("Write function to send email")

    def send_sms(self, message: str):
        # Write send email function here
        logger.info("Write function to send sms")

    def console_notification(self, message: str):
        # Write send email function here
        logger.info(message)
