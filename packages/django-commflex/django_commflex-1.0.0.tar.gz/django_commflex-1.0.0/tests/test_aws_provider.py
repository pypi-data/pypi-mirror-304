from unittest.mock import Mock, patch

import pytest

from commflex.sms.abstract import Message, PhoneNumber
from commflex.sms.provider.aws import AWSSMSClient, AWSSMSConfig
from tests.settings import TEST_MESSAGE, VALID_PHONE


class TestAWSSMSClient:
    @pytest.fixture
    def aws_client(self, aws_settings):
        with patch("boto3.client") as mock_boto:
            mock_sns = Mock()
            mock_boto.return_value = mock_sns
            config = AWSSMSConfig.from_settings(aws_settings)
            client = AWSSMSClient(config)
            client.client = mock_sns
            return client, mock_sns

    def test_successful_sms_send(self, aws_client):
        client, mock_sns = aws_client
        mock_sns.publish.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200},
            "MessageId": "test_id",
        }

        phone = PhoneNumber.from_string(VALID_PHONE)
        message = Message.from_string(TEST_MESSAGE)
        response = client.send_sms(phone, message)

        assert response.status is True
        mock_sns.publish.assert_called_once_with(
            PhoneNumber=VALID_PHONE, Message=TEST_MESSAGE
        )

    def test_failed_sms_send(self, aws_client):
        client, mock_sns = aws_client
        mock_sns.publish.side_effect = Exception("Test AWS Error")

        phone = PhoneNumber.from_string(VALID_PHONE)
        message = Message.from_string(TEST_MESSAGE)
        response = client.send_sms(phone, message)

        assert response.status is False
        assert "Test AWS Error" in response.response["error"]
