import requests
from bs4 import BeautifulSoup
import sqlite3

def create_table():
    conn = sqlite3.connect('rolls.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rolls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ingredients TEXT,
        weight TEXT,
        image_url TEXT,
        category TEXT,
        price TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print("Таблица 'rolls' создана!")
def parse_rolls_from_url(url, category):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        roll_items = soup.find_all('div', class_='product-item')

        conn = sqlite3.connect('rolls.db')
        cursor = conn.cursor()

        for roll_item in roll_items:
            name_tag = roll_item.find('h3', class_='title')
            name = name_tag.text.strip() if name_tag else 'Без названия'

            ingredients_tag = roll_item.find('p', class_='desc')
            ingredients = ingredients_tag.text.strip() if ingredients_tag else 'Не указан'

            weight_tag = roll_item.find('span', class_='s_h3')
            weight = weight_tag.text.strip() if weight_tag else 'Не указан'

            image_tag = roll_item.find('img', class_='lazyImg')
            image_url = image_tag['data-original'] if image_tag else 'Не указано'

            cost_line = roll_item.find('div', class_='cost-line')
            price_tag = cost_line.find('p', class_='cost') if cost_line else None
            price = price_tag.text.strip() if price_tag else 'Не указана'

            cursor.execute('''
            INSERT INTO rolls (name, ingredients, weight, image_url, category, price)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, ingredients, weight, image_url, category, price))

        conn.commit()
        conn.close()
        print(f"Данные для категории '{category}' успешно записаны в базу данных!")

create_table()

parse_rolls_from_url("https://momohit.ru/firmennie-rolli", "Фирменные")
parse_rolls_from_url("https://momohit.ru/tempura-rolli", "Темпура")
parse_rolls_from_url("https://momohit.ru/zapechennie-rolli", "Запеченные")
