import pytest
from django.core.exceptions import ImproperlyConfigured

from commflex.sms.abstract import InvalidPhoneNumber, Message, PhoneNumber
from commflex.sms.provider.ait import AITSMSConfig
from commflex.sms.provider.aws import AWSSMSConfig
from tests.settings import INVALID_PHONE, TEST_MESSAGE, VALID_PHONE


class TestPhoneNumber:
    def test_valid_phone_number_creation(self):
        phone = PhoneNumber.from_string(VALID_PHONE)
        assert phone.value == VALID_PHONE

    def test_invalid_phone_number_raises_exception(self):
        with pytest.raises(InvalidPhoneNumber):
            PhoneNumber.from_string(INVALID_PHONE)

    def test_phone_number_immutability(self):
        phone = PhoneNumber.from_string(VALID_PHONE)
        with pytest.raises(AttributeError):
            phone.value = "new_value"


class TestMessage:
    def test_valid_message_creation(self):
        message = Message.from_string(TEST_MESSAGE)
        assert message.content == TEST_MESSAGE

    def test_empty_message_raises_exception(self):
        with pytest.raises(ValueError):
            Message.from_string("")

    def test_message_immutability(self):
        message = Message.from_string(TEST_MESSAGE)
        with pytest.raises(AttributeError):
            message.content = "new content"


class TestAWSSMSConfig:
    def test_valid_config_creation(self, aws_settings):
        config = AWSSMSConfig.from_settings(aws_settings)
        assert config.access_key == "test_key"
        assert config.secret_access_key == "test_secret"
        assert config.region == "us-east-1"
        assert config.enabled is True
        assert config.timeout == 10

    def test_missing_required_fields(self):
        with pytest.raises(ImproperlyConfigured):
            AWSSMSConfig.from_settings({"aws": {"access_key": "test"}})

    def test_missing_aws_settings(self):
        assert AWSSMSConfig.from_settings({}) is None


class TestAITSMSConfig:
    def test_valid_config_creation(self, ait_settings):
        config = AITSMSConfig.from_settings(ait_settings)
        assert config.username == "sandbox"
        assert (
            config.api_key == "atsk_b7c3bb6a929415688f7d10b1b16b3453102cd1625be517519b655893f9b280b3ed54b2aa" # noqa
        )
        assert config.sms_url == "http://test.com/sms"
        assert config.sender_id == "mashaa"
        assert config.enabled is True
        assert config.timeout == 10

    def test_missing_required_fields(self):
        with pytest.raises(ImproperlyConfigured):
            AITSMSConfig.from_settings({"ait": {"username": "test"}})

    def test_missing_ait_settings(self):
        assert AITSMSConfig.from_settings({}) is None
