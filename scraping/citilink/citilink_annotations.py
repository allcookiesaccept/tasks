import requests
from bs4 import BeautifulSoup

def get_annotation(url: str):

    get_param = '?view_type=list'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'}

    req = requests.get(f'{url}{get_param}', headers=headers, timeout=10)

    print(f'{url} is opened')

    soup = BeautifulSoup(req.text, 'lxml')

    counter = soup.find_all('div', class_='ProductCardHorizontal__image-block')

    h1 = soup.find('h1').text.replace('\n', '').lstrip().rstrip()

    breadcrumbs = soup.find('div', class_='js--Breadcrumbs')

    if len(counter) > 0 and len(breadcrumbs) > 0:
        clean_breadcrumbs = breadcrumbs.text.replace('\n', ' ').replace('                                      ',
                                                                        '').lstrip().rstrip()
        product_info = soup.find_all('div', class_='ProductCardHorizontal__description-block')
        param_block = product_info[0].find_all('li', class_='ProductCardHorizontal__properties_item')
        param_info = ''
        for item in param_block:
            item = item.text.replace('\t', ' ').replace('                 ', '')
            item = item.replace('                               ', ' ')
            item = item.lstrip().rstrip().replace('\n', ': ').replace(':            :               ', ': ')
            param_info += f'{item} ->\t'

        return f'{h1};{clean_breadcrumbs};{param_info}'
    else:
        return f'{h1}'

def main():

    with open('citilink.txt', 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()
        file.close()

    with open('result_citilink.txt', 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(f'{url};{get_annotation(url)}\n')
        file.close()



if __name__ == '__main__':

    main()