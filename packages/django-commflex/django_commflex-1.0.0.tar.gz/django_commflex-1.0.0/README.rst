Django Commflex Library
=======================

A flexible and reliable Django library for sending SMS messages through multiple providers with built-in retry capabilities.

Key Features
-----------
- Multiple SMS provider support (AWS SNS and AIT)
- Automatic phone number validation
- Configurable retry mechanism with exponential backoff

Quick Start
----------

1. Install the package:

   .. code-block:: bash

       pip install django-commflex


2. Add "django-double-commflex" to your ``INSTALLED_APPS`` setting:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'commflex',
      ]

3. Add SMS settings to your Django settings:

   .. code-block:: python

       SMS_SETTINGS = {
           'aws': {
               'access_key': 'your-access-key',
               'secret_access_key': 'your-secret-key',
               'region': 'aws-region',
               'enabled': True,
               'timeout': 30,
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

3. Send an SMS:

   .. code-block:: python

      from commflex.sms import send_sms
      send_sms(phone_number, message)

Supported Providers
-----------------

AWS SNS
~~~~~~~
Amazon Simple Notification Service integration with support for all regions.

AIT SMS
~~~~~~~
Africa's Talking SMS service integration with custom sender ID support.


Testing
-------

Run the test suite:

.. code-block:: bash

    python -m pytest

For development, install test dependencies:

.. code-block:: bash

    pip install -e ".[test]"


Documentation
-------------

https://django-commflex.readthedocs.io/en/latest/index.html
