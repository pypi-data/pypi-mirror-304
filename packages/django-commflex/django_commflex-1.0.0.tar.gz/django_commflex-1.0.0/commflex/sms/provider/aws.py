from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
import botocore
from django.core.exceptions import ImproperlyConfigured

from commflex.sms.abstract import (
    Message,
    PhoneNumber,
    SMSConfig,
    SMSProvider,
    SMSResponse,
)


@dataclass
class AWSSMSConfig(SMSConfig):
    access_key: str
    secret_access_key: str
    region: str
    enabled: bool = False
    timeout: int = 30

    def create_client(self) -> SMSProvider:
        return AWSSMSClient(self)

    @classmethod
    def from_settings(cls, settings_dict: Dict[str, Any]) -> Optional["AWSSMSConfig"]:
        aws_settings = settings_dict.get("aws")
        if not aws_settings:
            return None

        required_fields = ["access_key", "secret_access_key", "region"]
        missing_fields = [
            field for field in required_fields if not aws_settings.get(field)
        ]

        if missing_fields:
            raise ImproperlyConfigured(
                f"Missing required AWS SMS settings: {', '.join(missing_fields)}"
            )

        return cls(
            access_key=aws_settings["access_key"],
            secret_access_key=aws_settings["secret_access_key"],
            region=aws_settings["region"],
            enabled=aws_settings.get("enabled", False),
            timeout=aws_settings.get("timeout", 30),
        )


class AWSSMSClient:
    def __init__(self, config: AWSSMSConfig):
        self.config = config
        boto_config = botocore.config.Config(
            connect_timeout=config.timeout, read_timeout=config.timeout
        )
        self.client = boto3.client(
            "sns",
            aws_secret_access_key=config.secret_access_key,
            aws_access_key_id=config.access_key,
            region_name=config.region,
            config=boto_config,
        )

    def send_sms(self, phone_number: PhoneNumber, message: Message) -> SMSResponse:
        try:
            resp = self.client.publish(
                PhoneNumber=phone_number.value, Message=message.content
            )
        except Exception as e:
            return SMSResponse(False, {"error": str(e)})

        status_code = resp.get("ResponseMetadata", {}).get("HTTPStatusCode", 0)
        return SMSResponse(status_code == 200, resp)
