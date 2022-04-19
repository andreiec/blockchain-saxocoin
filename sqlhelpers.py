from app import mysql, session
from blockchain import Blockchain, Block


class InvalidTransactionException(Exception):
    pass


class InsufficientFundsException(Exception):
    pass


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

    # Delete all
    def deleteall(self):
        cur = mysql.connection.cursor()
        cur.execute(f"TRUNCATE TABLE {self.table}")
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
        cur.execute(f"INSERT INTO `saxocoin`.`{self.table}` ({self.columns}) VALUES({data[:len(data) - 1]})")
        mysql.connection.commit()
        cur.close()


# Function to convert to sql raw command
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()


# Function to get balance of a specific user
def get_balance(username):
    balance = 0.00
    blockchain = get_blockchain()

    # Iterate each block and check every transaction
    for block in blockchain.chain:
        data = block.data.split(">")

        if username == data[0]:
            balance -= float(data[2])
        elif username == data[1]:
            balance += float(data[2])

    return balance


# Function to send currency to another user
def send_coin(sender, recipient, amount):
    try:
        amount = float(amount)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction.")

    if amount > get_balance(sender) and sender != 'admin':
        raise InsufficientFundsException("Insufficient Funds.")

    if sender == recipient or amount <= 0.00:
        raise InvalidTransactionException("Invalid Transaction.")

    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = f'{sender}>{recipient}>{amount}'
    blockchain.mine(Block(number=number, data=data))
    sync_blockchain(blockchain)


# Function to get blockchain
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain", 'number', 'hash', 'previous', 'data', 'nonce')

    for b in blockchain_sql.getall():
        blockchain.add(Block(number=int(b.get('number')), previous=b.get('previous'), data=b.get('data'), nonce=b.get('nonce')))

    return blockchain


# Function to sync blockchain to mysql
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", 'number', 'hash', 'previous', 'data', 'nonce')
    blockchain_sql.deleteall()

    for b in blockchain.chain:
        blockchain_sql.insert(str(b.number), b.hash(), b.previous_hash, b.data, b.nonce)
