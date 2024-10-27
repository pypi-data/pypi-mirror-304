from unittest.mock import patch

import pytest
from django.core.exceptions import ImproperlyConfigured

from commflex.sms.factory import RetryableClient, SMSClientFactory
from commflex.sms.provider.ait import AITSMSClient
from commflex.sms.provider.aws import AWSSMSClient


class TestSMSClientFactory:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        # This fixture will run automatically for all tests in this class
        settings.SMS_SETTINGS = {}
        return settings

    def test_create_client_with_aws_config(self, aws_settings, settings):
        settings.SMS_SETTINGS = aws_settings
        with patch("boto3.client"):  # Mock boto3.client to prevent AWS calls
            client = SMSClientFactory.create_client()
            assert isinstance(client, RetryableClient)
            assert isinstance(client.delegate, AWSSMSClient)

    def test_create_client_with_ait_config(self, ait_settings, settings):
        settings.SMS_SETTINGS = ait_settings
        client = SMSClientFactory.create_client()
        assert isinstance(client, RetryableClient)
        assert isinstance(client.delegate, AITSMSClient)

    def test_missing_settings_raises_exception(self, settings):
        settings.SMS_SETTINGS = None
        with pytest.raises(ImproperlyConfigured):
            SMSClientFactory.create_client()

    def test_multiple_enabled_providers_raises_exception(
        self, aws_settings, ait_settings, settings
    ):
        combined_settings = aws_settings.copy()
        combined_settings.update(ait_settings)
        settings.SMS_SETTINGS = combined_settings
        with pytest.raises(ImproperlyConfigured):
            SMSClientFactory.create_client()
