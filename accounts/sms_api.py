from django.conf import settings


def send_otp(otp):

    body = {
        'receptor': otp.phone,
        'template': '',
        'type': 1,
        'param1': otp.code
    }
    print(body)
    return (body,)
