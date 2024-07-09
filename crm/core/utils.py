import requests
from bs4 import BeautifulSoup
import asyncio

from core.models import Course


def get_course():
    try:
        url = 'https://ligovka.ru/detailed/usd'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        td = soup.find_all(class_='money_price')
        crs = Course(course=td[1].text)
        crs.save()
    except Exception as error:
        print(error)
    return Course.objects.last()

