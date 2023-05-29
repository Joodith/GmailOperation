import datetime
import sqlite3


class Connection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_connection(self):
        # Creates a database if not exists or access the database from local
        self.connection = sqlite3.connect('gmail_store.db')
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class DbTablesException(Exception):
    pass


class DatabaseTables:
    def __init__(self, table_name):
        self.conn = Connection()
        self.table_name = table_name

    def check_table_exists(self):
        # Check if the current instance with the given table name exists.If not raises Exception
        self.conn.open_connection()
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.conn.cursor.execute(query, (self.table_name,))
        result = self.conn.cursor.fetchone()
        if not result:
            self.conn.connection.commit()
            self.conn.close_connection()
            raise DbTablesException("Table does not exist!")

        self.conn.connection.commit()
        self.conn.close_connection()
        return

    def create_table(self, columns):
        """
        :param columns: Table schema as mentioned in config file
        :return: None
        """
        self.conn.open_connection()
        create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({', '.join(columns)})"
        print(create_table_query)
        self.conn.cursor.execute(create_table_query)
        self.conn.connection.commit()
        self.conn.close_connection()

    def insert_rows(self, columns, data_to_be_inserted):
        """
        Inserts list of rows into the table        :param columns: fields specified as a list        :param data_to_be_inserted: of message rows to be inserted
        :return:
        """
        try:
            self.check_table_exists()
            self.conn.open_connection()
            insert_data_query = f"INSERT INTO {self.table_name} ({','.join(columns)}) VALUES ({','.join(['?'] * len(columns))})"
            self.conn.cursor.executemany(insert_data_query, data_to_be_inserted)
            self.conn.connection.commit()
            self.conn.close_connection()
        except DbTablesException as e:
            print("Exception : ", str(e))

    def get_sqlite_condition(self, field, cond, target):
        """
        Returns query strings to be used in select query based on
        inputs provided in a specific format.Needs the field name,condition specifier and the target value
        """
        if cond == "EQ":
            return f"{str(field)} = {target}"
        if cond == "LT":
            return f"{str(field)} < {target}"
        if cond == "LTE":
            return f"{str(field)} <= {target}"
        if cond == "GT":
            return f"{str(field)} > {target}"
        if cond == "GTE":
            return f"{str(field)} >= {target}"

        if cond == "CONTAINS":
            return f"{str(field)} LIKE '%{target}%'"
        if cond == "NOT CONTAINS":
            return f"{str(field)} NOT LIKE '%{target}%'"

    def retrieve_all_rows(self):
        try:
            self.check_table_exists()
            self.conn.open_connection()
            retrieve_data_query = f"SELECT * FROM {self.table_name}"
            self.conn.cursor.execute(retrieve_data_query)
            rows = self.conn.cursor.fetchall()
            for row in rows:
                print(row)
            self.conn.connection.commit()
            self.conn.close_connection()
        except DbTablesException as e:
            print("Exception : ", str(e))

    def query_based_record_retrieval(self, conditions, predicate="ALL"):
        """
        Given a list of conditions and the corresponding predicate,returns a list of message ids by querying the database
        :param conditions: list of conditions specified for each rule in rules json file
        :param predicate:ALL or ANY specified in rules json file
        :return: List of message ids
        """

        q = list()
        for c in conditions:
            field, cond, target = c[0], c[1], c[2]
            if field == "action_date":
                current_date = datetime.date.today()
                t = target.split("|")
                exact_target = int(t[0])
                if t[1] == "D":
                    exact_target = current_date - datetime.timedelta(days=int(t[0]))
                elif t[1] == "H":
                    exact_target = current_date - datetime.timedelta(hours=int(t[0]))
                target = f"date('{exact_target}')"
            q.append(self.get_sqlite_condition(field, cond, target))
        where_query_string = ""
        if predicate == "ALL":
            where_query_string = " AND ".join(q)
        elif predicate == "ANY":
            where_query_string = " OR ".join(q)
        row_query = f"SELECT * FROM {self.table_name} WHERE {where_query_string}"
        print(row_query)
        self.conn.open_connection()
        self.conn.cursor.execute(row_query)
        rows = self.conn.cursor.fetchall()
        msg_ids = list()
        for row in rows:
            msg_ids.append(row[0])
        print(msg_ids)
        return msg_ids
