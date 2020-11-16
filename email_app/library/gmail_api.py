# this file contains basic functions for interacting with google gmail api
from typing import List


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


def get_attachment(service, user_id, msg_id, attachment_id):
    try:
        return service.users().messages().attachments().get(userId=user_id, messageId=msg_id,
                                                            id=attachment_id).execute()
    except Exception as error:
        raise error


def get_raw_message(service, user_id, msg_id):
    return get_message_with_param(service, user_id, msg_id, 'raw')


def get_full_message(service, user_id, msg_id):
    return get_message_with_param(service, user_id, msg_id, 'full')


def get_message_with_param(service, user_id, msg_id, param: str):
    try:
        return service.users().messages().get(userId=user_id, id=msg_id, format=param).execute()
    except Exception as error:
        raise error


# todo finish this function
def get_message_attachments(service, user_id, message_id, attachment_id):
    try:
        return service.users().messages().attachments().get(userId=user_id, messageId=message_id,
                                                            id=attachment_id).execute()
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


def trash_message(service, user_id: str, message_id: str):
    '''
    Moves the specified message to the trash.
    user_id: string
    The user's email address. The special value me can be used to indicate the authenticated user.
    id: string
    The ID of the message to Trash.
    '''
    try:
        message = service.users().messages().trash(userId=user_id, id=message_id).execute()
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def untrash_message(service, user_id: str, message_id: str):
    '''
    Moves the specified message from the trash.
    user_id: string
    The user's email address. The special value me can be used to indicate the authenticated user.
    id: string
    The ID of the message to Trash.
    '''
    try:
        message = service.users().messages().untrash(userId=user_id, id=message_id).execute()
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def delete_message(service, user_id: str, message_id: str):
    '''
    Immediately and permanently deletes the specified message. This operation cannot be undone.
    user_id: string
    The user's email address. The special value me can be used to indicate the authenticated user.
    message_id: string
    The ID of the message to delete.
    '''
    try:
        message = service.users().messages().delete(userId=user_id, id=message_id).execute()
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        raise e


def list_messages_with_label(service, user_id: str, label_ids: List[str]):
    try:
        messages = service.users().messages().list(userId=user_id, labelIds=label_ids, includeSpamTrash=True).execute()
        return messages
    except Exception as e:
        print('An error occurred: %s' % e)
        raise e


def get_attachment(service, user_id: str, message_id: str, attachment_id: str):
    try:
        attachment = service.users().messages().attachments().get(userId=user_id, messageId=message_id,
                                                                  id=attachment_id).execute()
        return attachment
    except Exception as e:
        print('An error occurred: %s' % e)
        raise e
