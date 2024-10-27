import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

import phonenumbers

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PhoneNumber:
    """Value object for validated phone numbers"""

    value: str

    @classmethod
    def from_string(cls, phone_number: str, country: str = "KE") -> "PhoneNumber":
        error = f"'{phone_number}' is not a valid phone number"

        try:
            parsed_number = phonenumbers.parse(phone_number, country)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise InvalidPhoneNumber(error)

        if not phonenumbers.is_valid_number(parsed_number):
            raise InvalidPhoneNumber(error)

        e164_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
        return cls(e164_number)


@dataclass(frozen=True)
class Message:
    """Value object for SMS messages"""

    content: str

    @classmethod
    def from_string(cls, content: str) -> "Message":
        if not content:
            raise ValueError("Please provide a message to send")
        return cls(content)


@dataclass(frozen=True)
class SMSResponse:
    """Immutable response object replacing namedtuple"""

    status: bool
    response: Dict[str, Any]


class InvalidPhoneNumber(Exception):
    """Exception to raise when phone number provided is invalid."""

    pass


class SMSProviderError(Exception):
    """Base exception for SMS provider errors"""

    pass


class SMSProvider(Protocol):
    """Protocol defining the SMS provider interface"""

    def send_sms(self, phone_number: PhoneNumber, message: Message) -> SMSResponse:
        """Send an SMS message"""
        pass


class SMSConfig(ABC):
    """Base configuration class for SMS providers"""

    enabled: bool = False

    @abstractmethod
    def create_client(self) -> SMSProvider:
        """Create an SMS client from this configuration"""
        pass

    @classmethod
    @abstractmethod
    def from_settings(cls, settings_dict: Dict[str, Any]) -> Optional["SMSConfig"]:
        """Create config from settings dictionary"""
        pass
