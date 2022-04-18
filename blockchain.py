from hashlib import sha256


def updatehash(*args):
    hashed_text = ""
    hashing = sha256()

    for arg in args:
        hashed_text += str(arg)

    hashing.update(hashed_text.encode('utf-8'))
    return hashing.hexdigest()


class Block:
    data = None
    hash = None
    nonce = 0
    previous_hash = "0" * 64

    def __init__(self, data, number=0):
        self.data = data
        self.number = number

    def hash(self):
        return updatehash(self.previous_hash, self.number, self.data, self.nonce)

    def __str__(self):
        return str(f"Block number: {self.number}\nHash: {self.hash()}\nPrevious hash: {self.previous_hash}\nData: {self.data}\nNonce: {self.nonce}")


class Blockchain:
    difficulty = 4

    def __init__(self, chain=[]):
        self.chain = chain

    def add(self, block):
        self.chain.append({'hash': block.hash(), 'previous': block.previous_hash, 'number': block.number, 'data': block.data, 'nonce': block.nonce})


def main():
    block = Block("hello world!", 1)
    print(block, end='\n\n')
    print(block)
    pass


if __name__ == "__main__":
    main()
