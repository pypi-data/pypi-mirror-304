import pytest


@pytest.fixture
def ait_settings():
    return {
        "ait": {
            "username": "sandbox",
            "api_key": "atsk_b7c3bb6a929415688f7d10b1b16b3453102cd1625be517519b655893f9b280b3ed54b2aa", # noqa
            "sms_url": "http://test.com/sms",
            "sender_id": "mashaa",
            "enabled": True,
            "timeout": 10,
        }
    }


@pytest.fixture
def aws_settings():
    return {
        "aws": {
            "access_key": "test_key",
            "secret_access_key": "test_secret",
            "region": "us-east-1",
            "enabled": True,
            "timeout": 10,
        }
    }
