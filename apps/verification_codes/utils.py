from django.conf import settings
from twilio.rest import Client

"""Send_sms via Twilio"""


def send_sms(phone, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Your verification code is: {verification_code}", from_=settings.TWILIO_NUMBER, to=str(phone)
    )

    return message.sid
