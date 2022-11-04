import hashlib
import pickle
import random
import os
from concurrent.futures import ThreadPoolExecutor

'''
Password constraints: - 8 chars
                      - Alphanumeric only
                      - Lowercase
'''
char_set = 'abcdefghijklmnopqrstuvwxyz0123456789'
filename = 'rainbow.txt'
password_len = 8

class RainbowTable:
    
    class Dimensions:
        rows = 0
        cols = 0

    empty = True
    table = {}
    random_strings = []
    dimensions = Dimensions()
    serialized = None

    def reduction(self, hash, column):

        def hexToDec(hex, offset=0):
            dec = int(hex, base=16)
            return dec + offset

        def decToBase(dec, base=36):
            ans = ''

            while len(ans) < password_len:
                ans += char_set[dec % base]
                dec //= base

            return ans

        return decToBase(hexToDec(hash, column))

    def __randomStringGenerator(self, len=8):
        return ''.join(random.choice(char_set) for i in range(len))

    def __serialize(self):
        self.serialized = pickle.dumps(self.table)

    def __deserialize(self):
        self.table = pickle.loads(self.serialized)

    
    def initialize(self, rows, cols):
        if cols % 2 > 0:
            return None

        self.dimensions.rows = rows
        self.dimensions.cols = cols
        
        self.table['Dim'] = (rows, cols)

        [self.random_strings.append(self.__randomStringGenerator()) for _ in range(rows)]
        
    def compute(self):

        for r in range(self.dimensions.rows):
            col = 1
            start = self.random_strings[r]
            end = start

            while col < self.dimensions.cols:
                hash = hashlib.sha256(end.encode()).hexdigest()
                end = self.reduction(hash, col+1)
                col += 2

            self.table[end] = start

        self.empty = False


    def save(self, output=filename):
        if self.empty is True:
            return None

        self.__serialize()
        with open(output, 'wb') as file:
            file.write(self.serialized)

    def load(self, input=filename):
        with open(input, 'rb') as file:
            self.serialized = file.read()

        self.empty = False
        self.__deserialize()
        (self.dimensions.rows, self.dimensions.cols) = self.table['Dim']
        

def create_table(r, c):
    rainbow_table = RainbowTable()
    if os.path.exists(filename) is True:
        rainbow_table.load()
        if rainbow_table.dimensions.rows != r or rainbow_table.dimensions.cols != c:
            os.remove(filename)
            return create_table(r, c)
    else:
        rainbow_table.initialize(r, c)
        rainbow_table.compute()
        rainbow_table.save()

    return rainbow_table

def run(hash, rainbow):
    col = rainbow.dimensions.cols
    while col > 0:
        
        start = hash
        for i in range(col, rainbow.dimensions.cols+1, 2):
            reduced = rainbow.reduction(start, i)
            start = hashlib.sha256(reduced.encode()).hexdigest()
            
        if reduced in rainbow.table:
            c = 1
            curr = rainbow.table[reduced]

            while c < rainbow.dimensions.cols:
                dig = hashlib.sha256(curr.encode()).hexdigest()

                if dig == hash:
                    print(dig + '->' + curr)
                    return

                curr = rainbow.reduction(hash, c+1)
                c += 2
            
            return None
         
        col -= 2

def main():
    
    rainbow_table = create_table(r=int(1e7), c=int(1e3))

    print('Rainbow table created successfully!')

    with open('dump_hashes.txt', 'r') as file:
        digest = file.read().splitlines()

    executors = ThreadPoolExecutor(len(digest))
    for hash in digest:
        executors.submit(run(hash, rainbow_table))

if __name__ == '__main__':
    main()
