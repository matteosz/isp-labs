import hashlib
from concurrent.futures import ThreadPoolExecutor

digests = { '2e41f7133fd134335f566736c03cc02621a03a4d21954c3bec6a1f2807e87b8a',
            '7987d2f5f930524a31e0716314c2710c89ae849b4e51a563be67c82344bcc8da',
            '076f8c265a856303ac6ae57539140e88a3cbce2a2197b872ba6894132ccf92fb',
            'b1ea522fd21e8fe242136488428b8604b83acea430d6fcd36159973f48b1102e',
            '3992b888e772681224099302a5eeb6f8cf27530f7510f0cce1f26e79fdf8ea21',
            '326e90c0d2e7073d578976d120a4071f83ce6b7bc89c16ecb215d99b3d51a29b',
            '269398301262810bdf542150a2c1b81ffe0e1282856058a0e26bda91512cfdc4',
            '4fbee71939b9a46db36a3b0feb3d04668692fa020d30909c12b6e00c2d902c31',
            '55c5a78379afce32da9d633ffe6a7a58fa06f9bbe66ba82af61838be400d624e', 
            '5106610b8ac6bc9da787a89bf577e888bce9c07e09e6caaf780d2288c3ec1f0c' }

dictionary = {}

def generate_variations(base):

    def generate(word, id):

        if id == len(word):
            hash1, hash2 = hashlib.sha256(word.encode()).hexdigest(), hashlib.sha256(word.title().encode()).hexdigest()
            
            if hash1 in digests:
                print(hash1 + '->' + word)

            if hash1 != hash2 and hash2 in digests:
                print(hash2 + '->' + word.title())

            return

        if word[id] == 'e':
            word_new = list(word)
            word_new[id] = '3'
            generate(''.join(word_new), id+1)
        
        elif word[id] == 'o':
            word_new = list(word)
            word_new[id] = '0'
            generate(''.join(word_new), id+1)

        elif word[id] == 'i':
            word_new = list(word)
            word_new[id] = '1'
            generate(''.join(word_new), id+1)

        generate(word, id+1)

    generate(base, 0)

def main():
    with open('rockyou.txt', 'r', encoding='latin-1') as file:
        passwords = file.read().splitlines()

    executors = ThreadPoolExecutor(len(passwords))
    for p in passwords:
        executors.submit(generate_variations(p))

if __name__ == '__main__':
    main()
