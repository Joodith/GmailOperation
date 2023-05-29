
"""
Configurations specifying the scopes and oauth related path information
Database table schemas corresponding to each table

"""
import os
CONFIGURATIONS = {

    "SCOPES": ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify'],
    "CLIENT_SECRET_FILE_PATH": os.environ.get('GMAIL_CLIENT_SECRET_PATH'),
    "TOKEN_FILE_PATH": os.environ.get('GMAIL_TOKEN_PATH')

}

DATABASE = {
    "TABLE_SCHEMA": {
        "Mail": [
            'threadId TEXT PRIMARY KEY',
            'labels TEXT',
            'from_email TEXT',
            'to_email TEXT',
            # 'CC TEXT',
            # 'BCC TEXT',
            'action_date TEXT',
            'subject TEXT',
            'messageBody TEXT',
            'attachment TEXT'

        ],
        "Attachments": [
            'id INTEGER PRIMARY KEY',
            'msg_id TEXT',
            'filename TEXT',
            'filedata BLOB',
            'FOREIGN KEY (msg_id) REFERENCES Main(threadId)'
        ]
    }
}
