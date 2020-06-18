from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import urllib.parse
import datetime

from django.core.management import BaseCommand

from avito_parser_app.models import Product

# Create your views here.
ItemBlock = namedtuple('Block', ['title', 'price', 'currency', 'date', 'url'])


class Block(ItemBlock):

    def __str__(self):
        return f'{self.title} -- {self.price} {self.currency} -- {self.date} {self.url}'


class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Accept-Language': 'ru'
        }

    def get_avito_page(self, page: int = None):
        parameters = {
            'radius': 0,
            'user': 1,
        }
        if page and page > 1:
            parameters['p'] = page

        url = 'https://www.avito.ru/rossiya/avtomobili/ford/mustang-ASgBAgICAkTgtg2cmCjitg3Aqyg'
        response = self.session.get(url, params=parameters)
        return response.text

    @staticmethod
    def parse_date(item: str):
        params_data_tooltip = item.get('data-tooltip').split(' ')
        month_dict = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сенрября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12,
        }

        def parse_date_three_obj(params_data_tooltip: list):
            day, month_parse, time = params_data_tooltip
            day = int(day)
            month = month_dict.get(month_parse)
            if not month:
                print('Не распознал месяц')
                return

            today = datetime.datetime.today()
            time = datetime.datetime.strptime(time, '%H:%M')
            return datetime.datetime(day=day, month=month, year=today.year, hour=time.hour, minute=time.minute)

        if len(params_data_tooltip) == 3:
            return parse_date_three_obj(params_data_tooltip)
        else:
            try:
                params_data_tooltip = item.get_text().strip().split(' ')
                return parse_date_three_obj(params_data_tooltip)
            except:
                print('Не смог распознать дату', item)
                return

    def parse_block(self, item):
        url_block = item.select_one('a.snippet-link')
        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        title = url_block.get_text().strip()

        price_block = item.select_one('span.snippet-price ').get_text().strip().split(' ')
        currency = price_block.pop(-1)
        price_block.pop(-1)
        price = ''
        for i in price_block:
            if i == price_block[-1]:
                price += str(i)
            else:
                price += str(i) + ' '
        price = int(price.replace(' ', ''))
        date = None
        date = self.parse_date(item.select_one('div.snippet-date-row div'))

        try:
            product = Product.objects.get(url=url)
            product.title = title
            product.price = price
            product.currency = currency
            product.save()
        except Product.DoesNotExist:
            product = Product(
                url=url,
                title=title,
                price=price,
                currency=currency,
                published_date=date,
            ).save()

        print(f'Product {product}')

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=date,
        )

    def get_max_page_number(self):
        text = self.get_avito_page()
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('a.pagination-page')
        last_button = container[-1]
        href = last_button.get('href')
        if not href:
            return 1
        parse_href = urllib.parse.urlparse(href)
        get_query_page = urllib.parse.parse_qs(parse_href.query)
        return int(get_query_page['p'][0])

    def get_blocks(self, page: int = None):
        text = self.get_avito_page(page=page)
        soup = BeautifulSoup(text, 'lxml')

        data_container = soup.select(
            'div.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
        for item in data_container:
            block = self.parse_block(item=item)

    def parse_all_pages_product(self):
        limit = self.get_max_page_number()
        print(f'Всего страниц по заданной ссылке {limit}')
        for i in range(1, limit + 1):
            self.get_blocks(page=i)


class Command(BaseCommand):
    help = 'Парсинг Avito'

    def handle(self, *args, **options):
        parser = AvitoParser()
        parser.parse_all_pages_product()

