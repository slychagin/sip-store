import threading

import requests

from orders.forms import OrderForm
from telebot.models import TelegramSettings


def get_telegram_settings():
    """Return method and query from telegram settings"""
    try:
        # Get Telegram Bot settings from the database
        tg_settings = TelegramSettings.objects.filter(available=True)[0]
        api = str(tg_settings.tg_api)
        token = str(tg_settings.tg_token)
        chat_id = str(tg_settings.tg_chat)
        method = '/sendMessage'

        # Create query for Telegram
        query = api + token + method

        return {'chat_id': chat_id, 'query': query}
    except IndexError:
        pass


def send_to_telegram_order_message(basket, order):
    """Create thread for sending message to telegram with new order"""
    telegram_settings = get_telegram_settings()

    # Get communication method
    readable_comm_methods = ''
    comm_methods = OrderForm().fields['communication_method'].choices
    for i in comm_methods:
        if i[0] in order.communication_method:
            readable_comm_methods += f'{i[1]}  '

    # Get delivery method
    delivery_method = dict(OrderForm().fields['delivery_method'].choices)[order.delivery_method]

    # Get payment method
    pay_method = dict(OrderForm().fields['payment_method'].choices)[order.payment_method]

    # Get delivery date
    delivery_date = '-'
    if order.delivery_date:
        delivery_date = order.delivery_date.strftime('%d.%m.%Y')

    # Get delivery time
    delivery_time = '-'
    if order.delivery_time:
        delivery_time = order.delivery_time.strftime('%H:%M')

    # Get order details
    details = ''
    for item in basket:
        details += f"{item['product']}  x  {item['qty']}\n"

    if order.delivery_method == 'COURIER_CHERKASY' or order.delivery_method == 'COURIER_ZOLOTONOSHA':
        message = f"НОВЕ ЗАМОВЛЕННЯ!" \
                  f"\n______________________________" \
                  f"\nПІБ:  {order.customer_name}" \
                  f"\nТелефон:  {order.phone}" \
                  f"\nEmail:  {order.email}" \
                  f"\n______________________________" \
                  f"\nСпосіб доставки:  {delivery_method}" \
                  f"\n------------------------------" \
                  f"\nМісто:  {order.city}" \
                  f"\nВулиця:  {order.street}" \
                  f"\nБудинок:  {order.house}" \
                  f"\nКвартира:  {order.room}" \
                  f"\n______________________________" \
                  f"\nДата доставки:  {delivery_date}" \
                  f"\nЧас доставки:  {delivery_time}" \
                  f"\n______________________________" \
                  f"\nСпосіб оплати:  {pay_method}" \
                  f"\nБажаний спосіб зв'язку:  {readable_comm_methods}" \
                  f"\nКоментар:  {order.order_note}" \
                  f"\n______________________________" \
                  f"\nДеталі замовлення:" \
                  f"\n№ {order.order_number} від {order.created.date().strftime('%d.%m.%Y')}" \
                  f"\n______________________________" \
                  f"\n{details}" \
                  f"______________________________" \
                  f"\nСума:  {basket.get_total_price()} ₴" \
                  f"\nЗнижка:  {order.discount} ₴" \
                  f"\nУсього:  {order.order_total} ₴"
    else:
        message = f"НОВЕ ЗАМОВЛЕННЯ!" \
                  f"\n______________________________" \
                  f"\nПІБ:  {order.customer_name}" \
                  f"\nТелефон:  {order.phone}" \
                  f"\nEmail:  {order.email}" \
                  f"\n______________________________" \
                  f"\nСпосіб доставки:  {delivery_method}" \
                  f"\n------------------------------" \
                  f"\nМісто Нової Пошти:  {order.new_post_city}" \
                  f"\n------------------------------" \
                  f"\nВідділення Нової Пошти:  {order.new_post_office}" \
                  f"\n______________________________" \
                  f"\nДата доставки:  {delivery_date}" \
                  f"\nЧас доставки:  {delivery_time}" \
                  f"\n______________________________" \
                  f"\nСпосіб оплати:  {pay_method}" \
                  f"\nБажаний спосіб зв'язку:  {readable_comm_methods}" \
                  f"\nКоментар:  {order.order_note}" \
                  f"\n______________________________" \
                  f"\nДеталі замовлення:" \
                  f"\n№ {order.order_number} від {order.created.date().strftime('%d.%m.%Y')}" \
                  f"\n______________________________" \
                  f"\n{details}" \
                  f"______________________________" \
                  f"\nСума:  {basket.get_total_price()} ₴" \
                  f"\nЗнижка:  {order.discount} ₴" \
                  f"\nУсього:  {order.order_total} ₴"

    thread = threading.Thread(
        target=telegram_sender,
        args=(telegram_settings['query'], telegram_settings['chat_id'], message)
    )
    thread.start()


def send_to_telegram_moderate_new_comment_message():
    """Create thread for sending message to telegram for moderate a new comment"""
    telegram_settings = get_telegram_settings()
    message = "На сайті новий коментар до посту чекає на модерацію!"

    thread = threading.Thread(
        target=telegram_sender,
        args=(telegram_settings['query'], telegram_settings['chat_id'], message)
    )
    thread.start()


def send_to_telegram_moderate_updated_comment_message():
    """Create thread for sending message to telegram for moderate an updated comment"""
    telegram_settings = get_telegram_settings()
    message = "На сайті було оновлено коментар до посту. Чекає на модерацію!"

    thread = threading.Thread(
        target=telegram_sender,
        args=(telegram_settings['query'], telegram_settings['chat_id'], message)
    )
    thread.start()


def send_to_telegram_moderate_new_review_message():
    """Create thread for sending message to telegram with new comment"""
    telegram_settings = get_telegram_settings()
    message = "На сайті новий відгук до товару чекає на модерацію!"

    thread = threading.Thread(
        target=telegram_sender,
        args=(telegram_settings['query'], telegram_settings['chat_id'], message)
    )
    thread.start()


def send_to_telegram_moderate_updated_review_message():
    """Create thread for sending message to telegram with new comment"""
    telegram_settings = get_telegram_settings()
    message = "На сайті було оновлено відгук до товару. Чекає на модерацію!"

    thread = threading.Thread(
        target=telegram_sender,
        args=(telegram_settings['query'], telegram_settings['chat_id'], message)
    )
    thread.start()


def telegram_sender(query, chat_id, message):
    """Send a message with order details to the admin telegram chat"""
    try:
        requests.post(query, data={'chat_id': chat_id, 'text': message})
    except (Exception,):
        pass
