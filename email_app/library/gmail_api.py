# this file contains basic functions for interacting with google gmail api


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()

        print('Message Id: %s' % message['id'])

        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        raise e


def get_messages(service, user_id: str, pagination_param: int, page_token: str = None) -> dict:
    try:
        if page_token:
            return service.users().messages().list(userId=user_id, maxResults=pagination_param,
                                                   pageToken=page_token).execute()
        else:
            return service.users().messages().list(userId=user_id, maxResults=pagination_param).execute()
    except Exception as error:
        raise error


def get_profile(service, user_id):
    try:
        return service.users().getProfile(userId=user_id).execute()
    except Exception as e:
        raise e


def get_labels(service, user_id):
    try:
        return service.users().labels().list(userId=user_id).execute()
    except Exception as e:
        raise e


def get_message_with_metadata(service, user_id, msg_id):
    try:
        return service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
    except Exception as error:
        raise error


# todo finish this function
def get_message_attachments(service, user_id, msg_id, part):
    try:
        return service.users().messages().attachments().get(id=part['body']['attachmentId'],
                                                            userId=user_id, messageId=msg_id).execute()
    except Exception as error:
        raise error


def create_draft(service, user_id, message_body):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print("Draft id: %s\nDraft message: %s" % (draft['id'], draft['message']))

        return draft
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def trash_message():
    pass


def untrash_message():
    pass


def delete_message():
    pass


def show_sent_messages():
    pass
