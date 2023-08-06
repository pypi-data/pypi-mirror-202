# -*- coding: utf-8 -*-
import email.message
import logging
import smtplib
import traceback

from kami_logging import benchmark_with, logging_with
from pydantic import validator

from kami_messenger.messenger import Messenger, RecipientFormatError
from kami_messenger.validator import DataValidator, EmailFormatError

email_messenger_logger = logging.getLogger('Email Messenger')


class EmailMessenger(Messenger):
    def _validate_message_recipients(message):
        for recipient in message.recipients:
            try:
                data = DataValidator(recipient)
                data.isEmail()
            except EmailFormatError:
                raise RecipientFormatError(
                    recipient,
                    f'Recipient {recipient} should be an valid e-mail address',
                )
            finally:
                return message

    @validator('messages', pre=True, each_item=True)
    @classmethod
    def recipientsValid(cls, message):
        cls._validate_message_recipients(message)

    @logging_with(email_messenger_logger)
    @benchmark_with(email_messenger_logger)
    def connect(self) -> int:
        try:
            engine = smtplib.SMTP('smtp.gmail.com: 587')
            engine.starttls()
            engine.login(
                self.credentials['login'], self.credentials['password']
            )
        except Exception as e:
            email_messenger_logger.error(traceback.format_exc())
            raise
        else:
            self.engine = engine
            email_messenger_logger.info(f'Success Connected')
            return 200

    @logging_with(email_messenger_logger)
    @benchmark_with(email_messenger_logger)
    def _sendMessage(self, message) -> int:
        try:
            self.connect()
            email_message = email.message.Message()
            email_message.add_header('Content-Type', 'text/html')
            email_message['Subject'] = message.subject
            email_message['From'] = message.sender
            email_message.set_payload(message.body)
            self.engine.sendmail(
                self.credentials['login'],
                message.recipients,
                email_message.as_string().encode('utf-8'),
            )
        except Exception as e:
            raise e
        finally:
            email_messenger_logger.info(
                f'Message Sucessufully Sent To {message.recipients}'
            )
            return 200
