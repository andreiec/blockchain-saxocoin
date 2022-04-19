from app import mysql, session


def isnewtable(name):
    cur = mysql.connection.cursor()

    try:
        result = cur.execute(f"SELECT * from {name}")
        cur.close()
    except:
        return True
    else:
        return False


# Base class for table
class Table:
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = f"{','.join(args)}"
        self.columnList = args

    # Base class for table
    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute(f"SELECT * FROM {self.table}")
        data = cur.fetchall()
        return data

    # Base class for table
    def getone(self, search, value):
        data = {}
        cur = mysql.connection.cursor()
        result = cur.execute(f"SELECT * FROM {self.table} WHERE {search} = \"{value}\"")

        if result > 0:
            data = cur.fetchone()

        cur.close()
        return data

    # Delete function for table
    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE from {self.table} where {search} = \"{value}\"")
        mysql.connection.commit()
        cur.close()

    # Drop function for table
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute(f"DROP TABLE {self.table}")
        cur.close()

    # Insert function for table
    def insert(self, *args):
        data = ""
        for arg in args:
            data += f'\"{arg}\",'

        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO `saxocoin`.`{self.table}` ({self.columns}) VALUES({data[:len(data)-1]})")
        mysql.connection.commit()
        cur.close()


# Function to convert to sql raw command
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()
