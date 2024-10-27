from celery import shared_task

from commflex.sms.abstract import Message, PhoneNumber
from commflex.sms.factory import SMSClientFactory


@shared_task
def send_sms_helper(phone_number: str, message: str) -> None:
    """Celery task for sending SMS messages"""
    sms_client = SMSClientFactory.create_client()
    validated_number = PhoneNumber.from_string(phone_number)
    validated_message = Message.from_string(message)
    sms_client.send_sms(validated_number, validated_message)
