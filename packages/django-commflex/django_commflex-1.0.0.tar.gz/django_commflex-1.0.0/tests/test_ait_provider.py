from unittest.mock import patch

import pytest

from commflex.sms.abstract import Message, PhoneNumber
from commflex.sms.provider.ait import AITSMSClient, AITSMSConfig
from tests.settings import TEST_MESSAGE, VALID_PHONE


class TestAITSMSClient:
    @pytest.fixture
    def client(self, ait_settings):
        config = AITSMSConfig.from_settings(ait_settings)
        return AITSMSClient(config)

    @pytest.fixture
    def phone_number(self):
        return PhoneNumber.from_string(VALID_PHONE)

    @pytest.fixture
    def message(self):
        return Message.from_string(TEST_MESSAGE)

    @patch("africastalking.SMS.SMSService.send")
    def test_send_sms_success(self, mock_send, client, phone_number, message):
        mock_send.return_value = {
            "SMSMessageData": {
                "Message": "Sent to 1/1 Total Cost: KES 0.8000 Message parts: 1",
                "Recipients": [
                    {
                        "cost": "KES 0.8000",
                        "messageId": "ATXid_e9fa657cc8e4fe0e7244e3cd0bcdf77a",
                        "number": "+254703499071",
                        "status": "Success",
                        "statusCode": 101,
                    }
                ],
            }
        }

        response = client.send_sms(phone_number, message)
        assert response.status == "success"
        assert "SMSMessageData" in response.response
        assert (
            response.response["SMSMessageData"]["Recipients"][0]["status"] == "Success"
        )

    @patch("africastalking.SMS.SMSService.send")
    def test_send_sms_failure(self, mock_send, client, phone_number, message):
        mock_send.return_value = {
            "SMSMessageData": {"Message": "InvalidSenderId", "Recipients": []}
        }

        response = client.send_sms(phone_number, message)
        assert not response.status
        assert (
            response.response["error"]["SMSMessageData"]["Message"] == "InvalidSenderId"
        )

    @patch("africastalking.SMS.SMSService.send")
    def test_send_sms_no_recipients(self, mock_send, client, phone_number, message):
        mock_send.return_value = {
            "SMSMessageData": {"Message": "Sent to 0/1", "Recipients": []}
        }
        response = client.send_sms(phone_number, message)
        assert not response.status
        assert "error" in response.response
        assert response.response["error"]["SMSMessageData"]["Message"] == "Sent to 0/1"
