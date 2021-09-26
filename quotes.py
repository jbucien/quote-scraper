import requests
from bs4 import BeautifulSoup
from csv import DictWriter


def quotes_list():
    URL = 'https://quotes.toscrape.com/'
    page_num = 1
    quotes_list = []
    next_page = True

    while next_page:
        page_response = requests.get(
            f'{URL}page/{page_num}/')
        page_soup = BeautifulSoup(
            page_response.content, 'html.parser')
        quotes = page_soup.find_all(class_='quote')
        for quote in quotes:
            bio = quote.find('a')['href']
            bio_response = requests.get(
                f"{URL}{bio}")
            bio_soup = BeautifulSoup(
                bio_response.text, 'html.parser')
            dob = bio_soup.find(class_='author-born-date').get_text()
            pob = bio_soup.find(class_='author-born-location').get_text()
            pob = pob.split('in', 1)[1]

            quote_dict = {
                'Quote': quote.find(class_='text').get_text(),
                'Author': quote.find(class_='author').get_text(),
                'DOB': dob,
                'POB': pob
            }
            quotes_list.append(quote_dict)

        nav = page_soup.find(class_='next')
        if nav:
            page_num += 1
        else:
            next_page = False
    return list(quotes_list)


def create_csv(quotes):
    with open('famous_quotes.csv', 'w') as file:
        headers = ['Quote', 'Author', 'DOB', 'POB']
        headers = ['Quote', 'Author', 'DOB', 'POB']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow({
                'Quote': quote['Quote'],
                'Author': quote['Author'],
                'DOB': quote['DOB'],
                'POB': quote['POB']
            })


def main():
    quotes = quotes_list()
    create_csv(quotes)
    print('CSV created.')


if __name__ == "__main__":
    main()

main()
