from unittest.mock import Mock

import pytest
import requests
from tenacity import RetryError

from commflex.sms.abstract import Message, PhoneNumber, SMSResponse
from commflex.sms.factory import RetryableClient
from tests.settings import TEST_MESSAGE, VALID_PHONE


class TestRetryableClient:
    @pytest.fixture
    def mock_client(self):
        return Mock()

    @pytest.fixture
    def retryable_client(self, mock_client):
        return RetryableClient(mock_client)

    def test_successful_send(self, retryable_client, mock_client):
        mock_client.send_sms.return_value = SMSResponse(True, {"message_id": "123"})

        phone = PhoneNumber.from_string(VALID_PHONE)
        message = Message.from_string(TEST_MESSAGE)
        response = retryable_client.send_sms(phone, message)

        assert response.status is True
        assert mock_client.send_sms.call_count == 1

    def test_retry_on_failure(self, retryable_client, mock_client):
        # Simulate network errors instead of SMS failures
        mock_client.send_sms.side_effect = [
            requests.exceptions.ConnectionError("Connection failed"),
            requests.exceptions.ConnectionError("Connection failed"),
            SMSResponse(True, {"message_id": "123"}),
        ]

        phone = PhoneNumber.from_string(VALID_PHONE)
        message = Message.from_string(TEST_MESSAGE)
        response = retryable_client.send_sms(phone, message)

        assert response.status is True
        assert mock_client.send_sms.call_count == 3

    def test_failure_after_max_retries(self, retryable_client, mock_client):
        # Simulate a network error to trigger retries
        mock_client.send_sms.side_effect = requests.exceptions.ConnectionError(
            "Connection failed"
        )

        phone = PhoneNumber.from_string(VALID_PHONE)
        message = Message.from_string(TEST_MESSAGE)

        # Catch RetryError, which wraps the original exception after max retries
        with pytest.raises(RetryError):
            retryable_client.send_sms(phone, message)

        # Ensure the client was retried the expected number of times (3)
        assert mock_client.send_sms.call_count == 3
