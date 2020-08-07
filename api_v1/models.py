from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=128,
        verbose_name='Имя категории',
        unique=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товаров"""
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование товара',
        unique=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='products'
    )
    sku = models.CharField(
        max_length=64,
        verbose_name='Артикул',
        unique=True
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


class Supplier(models.Model):
    """Модель поставщиков"""
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование поставшика',
        unique=True
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

    def __str__(self):
        return f'{self.created_at.date()} by {self.supplier}'

    @property
    def total_values(self):
        values = self.items.annotate(item_value=F('quantity') * F('product__price')).aggregate(total=Sum('item_value'))
        return values['total']


class DeliveryItem(models.Model):
    """Модель товаров в поставке"""
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Поставка'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
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
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )
