from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from commflex.sms.provider.constants import PROVIDER_CONFIGS
from commflex.sms.retry_client import RetryableClient


class SMSClientFactory:

    @classmethod
    def create_client(cls) -> RetryableClient:
        """Create and return the configured SMS client"""
        sms_settings = getattr(settings, "SMS_SETTINGS", None)
        if not sms_settings:
            raise ImproperlyConfigured(
                "SMS_SETTINGS is not configured in Django settings"
            )

        # Load all available configurations
        configs = []
        for config_class in PROVIDER_CONFIGS:
            config = config_class.from_settings(sms_settings)
            if config and config.enabled:
                configs.append(config)

        if len(configs) > 1:
            raise ImproperlyConfigured("Only one SMS provider can be enabled at a time")
        elif not configs:
            raise ImproperlyConfigured(
                "At least one SMS provider must be enabled in SMS_SETTINGS"
            )

        # Create the client with the enabled configuration
        client = configs[0].create_client()
        return RetryableClient(client)
