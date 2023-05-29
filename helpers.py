from database_connection import DatabaseTables
from config import DATABASE


def create_necessary_tables():
    """
    Helper function to create the tables needed for database storage of gmail messages
    """
    table = DatabaseTables("Mail")
    files_table = DatabaseTables("Attachments")
    table.create_table(DATABASE["TABLE_SCHEMA"]["Mail"])
    files_table.create_table(DATABASE["TABLE_SCHEMA"]["Attachments"])
    return table, files_table


def map_actions(gmail, action, id):
    """
     Helper function for calling the respective functions of the action strings given in rules.json
    :param gmail: GmailMessages Object
    :param action: String representing the action to be taken
    :param id: Message id
    :return: None
    """
    if action == "MOVE_TO_INBOX":
        gmail.move_to_inbox(id)
        return
    if action == "MARK_AS_READ":
        gmail.mark_as_read(id)
        return


