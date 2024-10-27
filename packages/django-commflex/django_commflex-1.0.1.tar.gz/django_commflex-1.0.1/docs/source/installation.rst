Quick start
===========

.. _installation:

1. Install package

.. code-block:: python

   pip install django-commflex


2. Add "django-double-commflex" to your ``INSTALLED_APPS`` setting:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'commflex',
      ]

Configuration
------------

Add the SMS settings to your Django settings file:

.. code-block:: python

    SMS_SETTINGS = {
        'aws': {
            'access_key': 'your-access-key',
            'secret_access_key': 'your-secret-key',
            'region': 'aws-region',
            'enabled': True,  # Only one provider can be enabled at a time
            'timeout': 30,  # Optional, defaults to 30 seconds
        },
        'ait': {
            'username': 'your-username',
            'api_key': 'your-api-key',
            'sms_url': 'https://api.ait-provider.com/sms',
            'sender_id': 'YOUR_SENDER_ID',
            'enabled': False,
            'timeout': 30,  # Optional, defaults to 30 seconds
        }
    }

Usage
-----

Basic Usage
~~~~~~~~~~

.. code-block:: python

    from commflex.sms import send_sms

    # Send the SMS
    send_sms(phone_number, message)
