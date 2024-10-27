from commflex.sms.task import send_sms_helper


def send_sms(phone_number, message):
    send_sms_helper.delay(phone_number, message)
    return True
