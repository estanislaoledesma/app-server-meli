from pyfcm import FCMNotification

push_service = FCMNotification(api_key = "AAAA3PJvsf4:APA91bFz41ZEzoN8ixbc-tptmNq_vmzgWCi2hKxbvt0lVoTfqq2o5mCoWa1Ch7PWypVPhlBS8LbDgyV0c_WaL1MIN0PNDw5qxxS7SDwRAnSLGe6t7Gmy9h7eU7gfuaGaRee9UK2jF6ir")

def sendPushNotification(registration_id, message_title, message_body):
    result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title,
                                               message_body = message_body)
    return result
