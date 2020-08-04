from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=128,
        verbose_name='Имя категории'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товаров"""
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование товара'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='products'
    )
    sku = models.CharField(
        max_length=64,
        verbose_name='Артикул'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )

    def __str__(self):
        return self.name

    @property
    def get_total_price(self):
        return self.price * self.quantity

# class Warehouse(models.Model):
#     """Модель остатков товаров на складе"""
#     product = models.OneToOneField(
#         Product,
#         verbose_name='Товар',
#         on_delete=models.CASCADE,
#         primary_key=True
#     )
#     quantity = models.PositiveIntegerField(
#         verbose_name='Количество'
#     )


class Supplier(models.Model):
    """Модель поставщиков"""
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование поставшика'
    )
    address = models.CharField(
        max_length=128,
        verbose_name='Адрес'
    )
    bank_details = models.CharField(
        max_length=128,
        verbose_name='Реквизиты'
    )
    contact_person = models.CharField(
        max_length=128,
        verbose_name='Контактное лицо'
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты'
    )
    product_category = models.ManyToManyField(
        Category,
        verbose_name='Категории поставляемых товаров'
    )

    def __str__(self):
        return self.name


class Delivery(models.Model):
    """Модель поставки товаров"""

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('draft', 'Draft'),
    )
    supplier = models.ForeignKey(
        Supplier,
        related_name='deliveries',
        on_delete=models.CASCADE,
        verbose_name='Поставщик'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )
    items = models.ManyToManyField(Product, through='DeliveryItem')


class DeliveryItem(models.Model):
    """Модель товаров в поставке"""
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        verbose_name='Поставка'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )


class Buyer(models.Model):
    """Модель покупателя"""
    full_name = models.CharField(
        max_length=128,
        verbose_name='ФИО'
    )
    contact_person = models.CharField(
        max_length=128,
        verbose_name='Контактное лицо'
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты'
    )

    def __str__(self):
        return self.full_name


class Order(models.Model):
    """Модель заказа"""

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('draft', 'Draft'),
    )
    buyer = models.ForeignKey(
        Buyer,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания заказа',
        auto_now_add=True
    )
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )
    url_for_qr_code = models.CharField(
        max_length=128,
        verbose_name='QR код',
        blank=True
    )


class OrderItem(models.Model):
    """Модель товаров в заказе"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )
