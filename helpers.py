from database_connection import DatabaseTables
from config import DATABASE

LABEL_IDS = {
    "MOVE_TO_INBOX": "INBOX",
    "MOVE_TO_SPAM": "SPAM",
    "MOVE_TO_TRASH": "TRASH",
    "MOVE_TO_PROMOTIONS": "CATEGORY_PROMOTIONS",
    "MOVE_TO_FORUMS": "CATEGORY_FORUMS",
    "MOVE_TO_SOCIAL": "CATEGORY_SOCIAL",
    "MOVE_TO_UPDATES": "CATEGORY_UPDATES",

}


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
    if "MOVE_TO" in action:
        if action in LABEL_IDS:
            gmail.move_message(id, LABEL_IDS[action])
        else:
            print("The action specified is not found")
        return
    if action == "MARK_AS_READ":
        gmail.mark_as_given(id, ["UNREAD"])
        return
    if action == "MARK_AS_UNREAD":
        gmail.mark_as_given(id, None, ["UNREAD"])
        return
    if action == "MARK_AS_IMPORTANT":
        gmail.mark_as_given(id, None, ["IMPORTANT"])
        return
