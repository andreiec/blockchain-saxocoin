from hashlib import sha256


def updatehash(*args):
    hashed_text = ""
    hashing = sha256()

    for arg in args:
        hashed_text += str(arg)

    hashing.update(hashed_text.encode('utf-8'))
    return hashing.hexdigest()


class Block:
    def __init__(self, data=None, number=0, previous='0'*64, nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous
        self.nonce = nonce

    def hash(self):
        return updatehash(self.previous_hash, self.number, self.data, self.nonce)

    def __str__(self):
        return str(f"Block number: {self.number}\nHash: {self.hash()}\nPrevious hash: {self.previous_hash}\nData: {self.data}\nNonce: {self.nonce}")


class Blockchain:
    difficulty = 4

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

    def checkvalid(self):
        chainlen = len(self.chain)
        difficultychar = "0" * self.difficulty

        for i in range(1, chainlen):
            _prev = self.chain[i].previous_hash
            _cur = self.chain[i - 1].hash()

            if _prev != _cur or _cur[:self.difficulty] != difficultychar:
                return False

        return True


def main():
    pass


if __name__ == "__main__":
    main()
