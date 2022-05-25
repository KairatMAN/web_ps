# импортируем библиотеки для создания парсера
import requests
from bs4 import BeautifulSoup
import json
import lxml

URL = 'https://www.wildberries.ru/'
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/81.0.4044.113 Safari/537.36'
}


# Делаем запрос на страницу и сохраняем ответ в файл
def get_html(URL, HEADERS):
    response = requests.get(URL, headers=HEADERS)

    with open('response_dates/parser_wildberries.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text


# Присваиваем сохраненный файл на диске переменной
def get_content():
    with open('response_dates/parser_wildberries.html', 'r', encoding='utf-8') as f:
        content = f.read()

    return content


# Создаем объект класса BeautifulSoup, находим все ссылки на каталог и записываем их в файл
def get_data(content):
    dates = {}
    soup = BeautifulSoup(content, 'lxml')
    items = soup.find_all('div', class_='menu-burger__main j-menu-burger-main')[0]
    for item in items.find_all('li'):
        href = item.find('a').get('href')
        text = item.find('a').text
        dates[text] = href

    with open('links_menu-burger/wildberries.json', 'w', encoding='utf-8') as f:
        json.dump(dates, f, ensure_ascii=False, indent=4)


# Получает ссылку выбранного каталога
def get_links():
    global resp
    with open('links_menu-burger/wildberries.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Выберите одну из следующих каталогов:")
    keys = list(data.keys())
    print(keys)
    category = input('\nВведите название каталога:')
    result = data[category.title()]

    try:
        resp = requests.get(result, headers=HEADERS)

        with open(f'response_dates/{category.title()}.html', 'w', encoding='utf-8') as f:
            f.write(resp.text)

    except Exception as e:
        print(f'Ошибка: {e}')

    with open(f'response_dates/{category.title()}.html', 'r', encoding='utf-8') as f:
        content = f.read()

    return print(content)


def main():
    # get_html(URL, HEADERS)
    get_data(get_content())
    get_links()


if __name__ == '__main__':
    main()
