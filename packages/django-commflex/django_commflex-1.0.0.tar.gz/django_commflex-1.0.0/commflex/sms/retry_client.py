import logging

import botocore
import botocore.exceptions
import requests
import requests.exceptions
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from commflex.sms.abstract import (
    Message,
    PhoneNumber,
    SMSProvider,
    SMSProviderError,
    SMSResponse,
)

LOGGER = logging.getLogger(__name__)


class RetryableClient:
    def __init__(self, client: SMSProvider):
        self.delegate = client
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (
                requests.exceptions.RequestException,
                botocore.exceptions.BotoCoreError,
                botocore.exceptions.ClientError,
            )
        ),
        before_sleep=lambda retry_state: LOGGER.warning(
            f"Retrying SMS send after attempt {retry_state.attempt_number} due to: {retry_state.outcome.exception()}" # noqa
        ),
    )
    def send_sms(self, phone_number: PhoneNumber, message: Message) -> SMSResponse:
        try:
            result = self.delegate.send_sms(phone_number, message)
            if not result.status:
                error = result.response.get("error", "Unknown error")
                raise SMSProviderError(f"SMS sending failed: {error}")
            return result
        except Exception as e:
            self.logger.error(f"Error sending SMS: {str(e)}")
            raise
