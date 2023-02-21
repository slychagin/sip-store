import os
import requests
from celery import shared_task
from dotenv import load_dotenv

from orders.models import NewPostTerminals


load_dotenv(override=True)

API_KEY = os.environ.get('NEW_POST_API_KEY')
URL = os.environ.get('NEW_POST_URL')

# TODO: Запустить обновление отделений раз в неделю


@shared_task
def update_terminals():
    """Refresh New Post terminals every monday"""
    params = {
        'apiKey': API_KEY,
        'modelName': 'Address',
        'calledMethod': 'getWarehouses'
    }

    try:
        response = requests.post(url=URL, json=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    data = [(terminal['CityDescription'], terminal['Description']) for terminal in response.json()['data']]

    NewPostTerminals.objects.all().delete()
    for item in data:
        terminal = NewPostTerminals(city=item[0], terminal=item[1])
        terminal.save()
