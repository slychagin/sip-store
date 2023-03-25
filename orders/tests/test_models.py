from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from category.models import Category
from orders.models import (
    Order,
    OrderItem,
    NewPostTerminals,
    Customers,
    save_customer,
    Subscribers,
    OrderMessage,
    ThanksPage
)
from store.models import Product


class OrderModelTest(TestCase):
    """Tests Order model"""

    @classmethod
    def setUpTestData(cls):
        """Create Order object"""
        cls.order = Order.objects.create(
            order_number='2000', customer_name='Сергій', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100
        )

    def test_order_entry(self):
        """Test Order model data insertion/types/field attributes"""
        data = self.order
        self.assertTrue(isinstance(data, Order))

    def test_order_model_name(self):
        """Tests Order object name"""
        data = self.order
        self.assertEqual(str(data), f'№ 2000 від {date.today().strftime("%d.%m.%Y")}')

    def test_phone_number_validation(self):
        """Check phone format by RegexValidator"""
        order = Order.objects.create(
            order_number='2000', customer_name='Сергій', phone='099-777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100
        )

        self.assertRaises(ValidationError, order.full_clean)

    def test_order_fields_max_length(self):
        """Test Order fields max length"""
        data = self.order

        order_number_max_length = data._meta.get_field('order_number').max_length
        customer_name_max_length = data._meta.get_field('customer_name').max_length
        email_max_length = data._meta.get_field('email').max_length
        city_max_length = data._meta.get_field('city').max_length
        street_max_length = data._meta.get_field('street').max_length
        house_max_length = data._meta.get_field('house').max_length
        room_max_length = data._meta.get_field('room').max_length
        new_post_city_max_length = data._meta.get_field('new_post_city').max_length
        new_post_office_max_length = data._meta.get_field('new_post_office').max_length
        delivery_method_max_length = data._meta.get_field('delivery_method').max_length
        payment_method_max_length = data._meta.get_field('payment_method').max_length
        order_note_max_length = data._meta.get_field('order_note').max_length
        ip_max_length = data._meta.get_field('ip').max_length

        self.assertEqual(order_number_max_length, 20)
        self.assertEqual(customer_name_max_length, 100)
        self.assertEqual(email_max_length, 100)
        self.assertEqual(city_max_length, 50)
        self.assertEqual(street_max_length, 50)
        self.assertEqual(house_max_length, 10)
        self.assertEqual(room_max_length, 10)
        self.assertEqual(new_post_city_max_length, 100)
        self.assertEqual(new_post_office_max_length, 200)
        self.assertEqual(delivery_method_max_length, 50)
        self.assertEqual(payment_method_max_length, 50)
        self.assertEqual(order_note_max_length, 255)
        self.assertEqual(ip_max_length, 20)

    def test_order_labels(self):
        """Test Order verbose names"""
        data = self.order

        order_number = data._meta.get_field('order_number').verbose_name
        customer_name = data._meta.get_field('customer_name').verbose_name
        phone = data._meta.get_field('phone').verbose_name
        email = data._meta.get_field('email').verbose_name
        city = data._meta.get_field('city').verbose_name
        street = data._meta.get_field('street').verbose_name
        house = data._meta.get_field('house').verbose_name
        room = data._meta.get_field('room').verbose_name
        new_post_city = data._meta.get_field('new_post_city').verbose_name
        new_post_office = data._meta.get_field('new_post_office').verbose_name
        delivery_date = data._meta.get_field('delivery_date').verbose_name
        delivery_time = data._meta.get_field('delivery_time').verbose_name
        delivery_method = data._meta.get_field('delivery_method').verbose_name
        payment_method = data._meta.get_field('payment_method').verbose_name
        order_note = data._meta.get_field('order_note').verbose_name
        order_total = data._meta.get_field('order_total').verbose_name
        discount = data._meta.get_field('discount').verbose_name
        ip = data._meta.get_field('ip').verbose_name
        is_ordered = data._meta.get_field('is_ordered').verbose_name
        created = data._meta.get_field('created').verbose_name
        updated = data._meta.get_field('updated').verbose_name

        self.assertEqual(order_number, 'номер замовлення')
        self.assertEqual(customer_name, 'ПІБ')
        self.assertEqual(phone, 'телефон')
        self.assertEqual(email, 'E-mail')
        self.assertEqual(city, 'місто')
        self.assertEqual(street, 'вулиця')
        self.assertEqual(house, 'будинок')
        self.assertEqual(room, 'квартира')
        self.assertEqual(new_post_city, 'Місто Нової Пошти')
        self.assertEqual(new_post_office, 'Відділення Нової Пошти')
        self.assertEqual(delivery_date, 'бажана дата доставки')
        self.assertEqual(delivery_time, 'час доставки')
        self.assertEqual(delivery_method, 'спосіб доставки')
        self.assertEqual(payment_method, 'спосіб оплати')
        self.assertEqual(order_note, 'примітка до замовлення')
        self.assertEqual(order_total, 'усього зі знижкою')
        self.assertEqual(discount, 'знижка')
        self.assertEqual(ip, 'IP адреса')
        self.assertEqual(is_ordered, 'замовлено')
        self.assertEqual(created, 'дата замовлення')
        self.assertEqual(updated, 'дата коригування')


class OrderItemModelTest(TestCase):
    """Tests OrderItem model"""

    @classmethod
    def setUpTestData(cls):
        """Create OrderItem object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')
        product = Product.objects.create(
            product_name='chicken', slug='chicken', price=100,
            product_image='good chicken', category=category
        )
        order = Order.objects.create(
            order_number='2000', customer_name='Сергій', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100
        )
        cls.order_item = OrderItem.objects.create(
            order=order, product=product, price=product.price, user_email=order.email
        )

    def test_order_item_entry(self):
        """Test OrderItem model data insertion/types/field attributes"""
        data = self.order_item
        self.assertTrue(isinstance(data, OrderItem))

    def test_order_item_model_name(self):
        """Tests OrderItem object name"""
        data = self.order_item
        self.assertEqual(str(data), 'chicken')

    def test_order_item_fields_max_length(self):
        """Test OrderItem fields max length"""
        data = self.order_item
        user_email_max_length = data._meta.get_field('user_email').max_length

        self.assertEqual(user_email_max_length, 100)

    def test_order_item_labels(self):
        """Test OrderItem verbose names"""
        data = self.order_item

        order = data._meta.get_field('order').verbose_name
        product = data._meta.get_field('product').verbose_name
        price = data._meta.get_field('price').verbose_name
        quantity = data._meta.get_field('quantity').verbose_name
        is_ordered = data._meta.get_field('is_ordered').verbose_name
        user_email = data._meta.get_field('user_email').verbose_name
        created = data._meta.get_field('created').verbose_name
        updated = data._meta.get_field('updated').verbose_name

        self.assertEqual(order, 'замовлення')
        self.assertEqual(product, 'товар')
        self.assertEqual(price, 'ціна товару')
        self.assertEqual(quantity, 'кількість')
        self.assertEqual(is_ordered, 'замовлено')
        self.assertEqual(user_email, 'E-mail')
        self.assertEqual(created, 'дата створення')
        self.assertEqual(updated, 'дата оновлення')


class NewPostTerminalsModelTest(TestCase):
    """Tests NewPostTerminals model"""

    @classmethod
    def setUpTestData(cls):
        """Create NewPostTerminals object"""
        cls.new_post_terminal = NewPostTerminals.objects.create(
            city='Черкаси', terminal='Відділення №1'
        )

    def test_new_post_terminal_entry(self):
        """Test NewPostTerminals model data insertion/types/field attributes"""
        data = self.new_post_terminal
        self.assertTrue(isinstance(data, NewPostTerminals))

    def test_new_post_terminal_model_name(self):
        """Tests NewPostTerminals object name"""
        data = self.new_post_terminal
        self.assertEqual(str(data), 'Черкаси, Відділення №1')

    def test_new_post_terminal_fields_max_length(self):
        """Test NewPostTerminals fields max length"""
        data = self.new_post_terminal
        city_max_length = data._meta.get_field('city').max_length
        terminal_max_length = data._meta.get_field('terminal').max_length

        self.assertEqual(city_max_length, 100)
        self.assertEqual(terminal_max_length, 255)


class CustomersModelTest(TestCase):
    """Tests Customers model"""

    @classmethod
    def setUpTestData(cls):
        """Create Customers object"""
        cls.customer = Customers.objects.create(
            customer_name='Serhio', phone='+38(099)777-77-77', email='email@gmail.com'
        )

    def test_customers_entry(self):
        """Test Customers model data insertion/types/field attributes"""
        data = self.customer
        self.assertTrue(isinstance(data, Customers))

    def test_customers_model_name(self):
        """Tests Customers object name"""
        data = self.customer
        self.assertEqual(str(data), 'Serhio')

    def test_phone_number_validation(self):
        """Check phone format by RegexValidator"""
        customer = Customers.objects.create(
            customer_name='Serhio', phone='099-777-77-77', email='email@gmail.com'
        )

        self.assertRaises(ValidationError, customer.full_clean)

    def test_customers_fields_max_length(self):
        """Test Customers fields max length"""
        data = self.customer

        customer_name_max_length = data._meta.get_field('customer_name').max_length
        phone_max_length = data._meta.get_field('phone').max_length
        email_max_length = data._meta.get_field('email').max_length

        self.assertEqual(customer_name_max_length, 100)
        self.assertEqual(phone_max_length, 16)
        self.assertEqual(email_max_length, 100)

    def test_customers_labels(self):
        """Test Customers verbose names"""
        data = self.customer

        customer_name = data._meta.get_field('customer_name').verbose_name
        phone = data._meta.get_field('phone').verbose_name
        email = data._meta.get_field('email').verbose_name
        note = data._meta.get_field('note').verbose_name

        self.assertEqual(customer_name, 'ПІБ')
        self.assertEqual(phone, 'телефон')
        self.assertEqual(email, 'E-mail')
        self.assertEqual(note, 'примітка')


class SaveCustomerTest(TestCase):
    """Tests save customer function in Customer model"""

    def setUp(self):
        """Create two different orders and one customer that ordered one of them"""
        self.order_1 = Order.objects.create(
            order_number='2000', customer_name='Сергій', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100
        )
        self.order_2 = Order.objects.create(
            order_number='3000', customer_name='Serhio', phone='+38(066)555-55-55',
            email='serhio@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100
        )
        self.customer = Customers.objects.create(
            customer_name='Сергій', phone='+38(099)777-77-77', email='email@gmail.com'
        )

    def test_save_customer(self):
        """Test save customer function"""
        save_customer(self.order_1)
        save_customer(self.order_2)
        customers_in_db = len(Customers.objects.all())

        self.assertEqual(customers_in_db, 2)


class SubscribersTest(TestCase):
    """Tests Subscribers model"""

    def setUp(self):
        """Create Subscribers object"""
        self.subscribers = Subscribers.objects.create(
            email='email@gmail.com'
        )

    def test_subscribers_entry(self):
        """Test Subscribers model data insertion/types/field attributes"""
        data = self.subscribers
        self.assertTrue(isinstance(data, Subscribers))

    def test_subscribers_model_name(self):
        """Tests Subscribers object name"""
        data = self.subscribers
        self.assertEqual(str(data), 'email@gmail.com')

    def test_subscribers_fields_max_length(self):
        """Test Subscribers fields max length"""
        data = self.subscribers
        email_max_length = data._meta.get_field('email').max_length
        self.assertEqual(email_max_length, 100)

    def test_subscribers_labels(self):
        """Test Subscribers verbose names"""
        data = self.subscribers
        email = data._meta.get_field('email').verbose_name
        self.assertEqual(email, 'E-mail')


class OrderMessageTest(TestCase):
    """Tests OrderMessage model"""

    def setUp(self):
        """Create OrderMessage object"""
        self.order_message = OrderMessage.objects.create()

    def test_subscribers_entry(self):
        """Test OrderMessage model data insertion/types/field attributes"""
        data = self.order_message
        self.assertTrue(isinstance(data, OrderMessage))

    def test_subscribers_model_name(self):
        """Tests OrderMessage object name"""
        data = self.order_message
        self.assertEqual(str(data), 'Повідомлення покупцям на email після замовлення')

    def test_subscribers_labels(self):
        """Test OrderMessage verbose names"""
        data = self.order_message
        text_1 = data._meta.get_field('text_1').verbose_name
        text_2 = data._meta.get_field('text_2').verbose_name

        self.assertEqual(text_1, 'текст до деталей замовлення')
        self.assertEqual(text_2, 'текст після деталей замовлення')


class ThanksPageTest(TestCase):
    """Tests ThanksPage model"""

    def setUp(self):
        """Create ThanksPage object"""
        self.thanks_page = ThanksPage.objects.create()

    def test_thanks_page_entry(self):
        """Test ThanksPage model data insertion/types/field attributes"""
        data = self.thanks_page
        self.assertTrue(isinstance(data, ThanksPage))

    def test_thanks_page_model_name(self):
        """Tests ThanksPage object name"""
        data = self.thanks_page
        self.assertEqual(str(data), 'Сторінка подяки')

    def test_thanks_page_labels(self):
        """Test ThanksPage verbose names"""
        data = self.thanks_page
        text = data._meta.get_field('text').verbose_name
        self.assertEqual(text, 'текст до сторінки подяки')
