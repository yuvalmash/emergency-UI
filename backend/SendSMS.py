from twilio.rest import Client

ACCOUNT_SID = 'AC5f1460f752c9e622a921b909e70dba6e'
AUTH_TOKEN = 'd7c0cbf61857b3cc1ed640febfb22dbf'
SENDER_PHONE = '+972525835074'


def send_sms(message, receiver_phone):
    """
    This function receives a message and receiver phone, and sends SMS using twilio services.
    :param message: Message to be sent (str)
    :param receiver_phone: Receiver's phone (str)
    :return: SMS id if successfully sent, or error message if failed
    """
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages \
            .create(
            body=message,
            from_=SENDER_PHONE,
            to=receiver_phone
        )
        return message.sid
    except:
        return 'An error ocurred, message was not sent. Please re-send or contact your system administrator.'
