
from database_connection import DatabaseTables
from helpers import map_actions
from processing_messages import GmailMessages
import argparse
import json


def execute_rule(rule_no):
    """
    Execute the rule mentioned by taking the actions specified in json rules file
    :param rule_no:Rule number specified in json rules file
    :return:
    """
    msg_table = DatabaseTables("Mail")
    gmail = GmailMessages()
    with open('rules.json', 'r') as file:
        json_data = json.load(file)
    rule=json_data["RULES"][rule_no]
    conditions=rule['CONDITIONS']
    actions=rule["ACTIONS"]
    message_ids=msg_table.query_based_record_retrieval(conditions)

    for id in message_ids:
        for action in actions:
            map_actions(gmail,action,id)



def local_storage(count):
    """
    Stores the specified number of gmail messages in local database file
    :param count:Specifies the number of gmail messages that must be stored in the local database
    :return:
    """
    gmail = GmailMessages()
    gmail.store_messages_in_db(count)


def func():
    """
    Dummy function
    :return:
    """
    d=DatabaseTables("Mail")
    d.retrieve_all_rows()

def main():
    parser = argparse.ArgumentParser(description='Description of your program.')

    # Add command-line arguments
    parser.add_argument('-r', '--rule', help='Execute specific rules')
    parser.add_argument('-s', '--store_message',help='Build local DB')
    parser.add_argument('-a', '--all',action='store_true',help='Get local DB')

    # Parse the command-line arguments
    args = parser.parse_args()
    if args.rule:
        execute_rule(args.rule)

    if args.store_message:
        local_storage(args.store_message)

    if args.all:
        func()






if __name__ == '__main__':
    main()
