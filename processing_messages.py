import base64
import email
import re

from googleapiclient.discovery import build
from authorize import gmail_authorisation
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests
import json

from helpers import create_necessary_tables


class GmailMessages:
    def __init__(self):
        # Getting the credentials of gmail OAuth Authorisation
        self.creds = gmail_authorisation()
        self.access_token = self.creds.token
        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_inbox_mails(self, count=1):
        # Retrieving the mails based on the count
        results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=count).execute()
        messages = results.get('messages', [])
        return messages

    def store_messages_in_db(self, count=3):
        message_table, files_table = create_necessary_tables()
        mails = self.get_inbox_mails(count)

        COLUMNS = ["threadId", "labels", "from_email", "to_email", "action_date", "subject", "messageBody",
                   "attachment"]
        DATA_TUPLE = list()
        for mail in mails:
            mail_info = self.service.users().messages().get(userId='me', id=mail['id'], format='full').execute()
            headers = mail_info['payload']['headers']
            attachments = mail_info.get('attachments', None)
            mail_payload = mail_info['payload']

            from_value = next((header['value'] for header in headers if header['name'] == 'From'), '')
            to_value = next((header['value'] for header in headers if header['name'] == 'To'), '')
            date_value = next((header['value'] for header in headers if header['name'] == 'Date'), '')
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')
            datetime_obj = None
            date_string = ""
            date_value = date_value.split('(')[0].strip()
            l = date_value.split(" ")
            l.pop()
            date_value = " ".join(l)

            # Handling different date formats
            if len(l) == 5:
                datetime_obj = datetime.strptime(date_value, "%a, %d %b %Y %H:%M:%S")
            elif len(l) == 4:
                datetime_obj = datetime.strptime(date_value, "%d %b %Y %H:%M:%S")

            # Extract the date component
            if datetime_obj:
                date_obj = datetime_obj.date()
                date_string = date_obj.strftime("%Y-%m-%d")

            # Extract the emails alone from the fields "from" and "to"
            if from_value != "":
                if len(re.findall(r'<([^>]+)>', from_value)) != 0:
                    from_address = re.findall(r'<([^>]+)>', from_value)[0]
                else:
                    from_address = from_value

            else:
                from_address = ""

            if to_value != "":
                if len(re.findall(r'<([^>]+)>', to_value)) != 0:
                    to_address = re.findall(r'<([^>]+)>', to_value)[0]
                else:
                    to_address = to_value
            else:
                to_address = ""

            # Iterate over attachments, if any
            if attachments:
                for attachment in attachments:
                    attachment_name = attachment['filename']

            # Decode and parse the message body
            if "data" in mail_payload['body']:
                body_data = mail_payload['body']['data']
                body_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
                parsed_message = email.message_from_string(body_text)
                html_content = ''
                for part in parsed_message.walk():
                    if part.get_content_type() == 'text/plain':
                        html_content = part.get_payload()

                # Extract the text content from the parsed message
                soup = BeautifulSoup(html_content, 'html.parser')
                text_content = soup.get_text()
            else:
                text_content = "Nill"

            labels = ",".join(mail_info["labelIds"])

            DATA_TUPLE.append((mail_info["threadId"], labels, from_address, to_address,
                               date_string, subject, text_content, attachments
                               ))

        message_table.insert_rows(COLUMNS, DATA_TUPLE)
        msg = f"Inserted {len(DATA_TUPLE)} rows!"
        print(msg)

    def mark_as_read(self, message_id):
        # Marking the message of the given id as read
        url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "removeLabelIds": ["UNREAD"]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"Message {message_id} marked as read.")
        else:
            print(f"Failed to mark message {message_id} as read. Error: {response.text}")

    def move_to_inbox(self, message_id):
        # Moving the message of the given id to inbox
        url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "addLabelIds": ["INBOX"]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"Message {message_id} moved to inbox.")
        else:
            print(f"Failed to move message {message_id} to inbox. Error: {response.text}")
