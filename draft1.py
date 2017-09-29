
from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.text import MIMEText
import base64

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.compose  https://www.googleapis.com/auth/gmail.send '
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage('storage.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_draft(service, user_id, message_body):
    """ Create and insert a draft email. Print and returns draft's message to id
    Args :
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message_body: The body of the email message, including headers.
    Returns:
    Draft object, including draft id and message meta data.
    """

    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()
        print("Draft id : {}\nDraft message: {}".format(draft['id'], draft['message']))
        return draft
    except Exception as e:
        print("Oh error!");
        print(e)

'''https://developers.google.com/gmail/api/guides/drafts'''
''' This is required because the message should comply with certain standard structure. see link above'''

def create_message(sender, to, subject, message_text):
     """Create a message for an email.
       Args:
           sender: Email address of the sender.
           to: Email address of the receiver.
           subject: The subject of the email message.
           message_text: The text of the email message.
     Returns:
         An object containing a url encoded email object.
     """

     message = MIMEText(message_text)
     message['to'] = to
     message['from'] = sender
     message['subject'] = subject
     return {'raw': base64.urlsafe_b64encode(message.as_string())}


def main():
    """Shows basic usage of the Gmail API.
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    my_message = create_message('me', "saar16cs@cmrit.ac.in", "hello", "hello!!! this is a test")
    drafts = create_draft(service, 'me', my_message)
    print("Draft created!!!")

    # send the drafts

    try:
        service.users().drafts().send(userId='me',body=drafts).execute()
        print("Draft sent!!!")
    except Exception as e:
        print("Oh another error")
        print(e)



if __name__ == '__main__':
    main()

