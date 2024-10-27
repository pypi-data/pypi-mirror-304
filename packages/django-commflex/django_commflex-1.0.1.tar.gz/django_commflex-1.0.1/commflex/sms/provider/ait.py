from dataclasses import dataclass
from typing import Any, Dict, Optional

import africastalking
from django.core.exceptions import ImproperlyConfigured

from commflex.sms.abstract import (
    Message,
    PhoneNumber,
    SMSConfig,
    SMSProvider,
    SMSResponse,
)


@dataclass
class AITSMSConfig(SMSConfig):
    username: str
    api_key: str
    sms_url: str
    sender_id: str
    timeout: int = 30
    enabled: bool = False

    def create_client(self) -> SMSProvider:
        return AITSMSClient(self)

    @classmethod
    def from_settings(cls, settings_dict: Dict[str, Any]) -> Optional["AITSMSConfig"]:
        ait_settings = settings_dict.get("ait")
        if not ait_settings:
            return None

        required_fields = ["username", "api_key", "sms_url", "sender_id"]
        missing_fields = [
            field for field in required_fields if not ait_settings.get(field)
        ]

        if missing_fields:
            raise ImproperlyConfigured(
                f"Missing required AIT SMS settings: {', '.join(missing_fields)}"
            )

        return cls(
            username=ait_settings["username"],
            api_key=ait_settings["api_key"],
            sms_url=ait_settings["sms_url"],
            sender_id=ait_settings["sender_id"],
            timeout=ait_settings.get("timeout", 30),
            enabled=ait_settings.get("enabled", False),
        )


class AITSMSClient:
    def __init__(self, config: AITSMSConfig):
        self.config = config

    def send_sms(self, phone_number: PhoneNumber, message: Message) -> SMSResponse:
        africastalking.initialize(
            username=self.config.username, api_key=self.config.api_key
        )
        sms = africastalking.SMS
        data = sms.send(message.content, [phone_number.value], self.config.sender_id)
        recipients = data["SMSMessageData"]["Recipients"]
        if not recipients:
            return SMSResponse(False, {"error": data})

        return SMSResponse("success", data)
