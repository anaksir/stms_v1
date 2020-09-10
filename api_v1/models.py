from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager,)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # if not username:
        #     raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_buyer = models.BooleanField('buyer status', default=False)
    is_supplier = models.BooleanField('supplier status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=128,
        verbose_name='Имя категории',
        unique=True
    )

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Модель поставщиков"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='supplier_profile',
        primary_key=True
    )
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

    product_category = models.ManyToManyField(
        Category,
        verbose_name='Категории поставляемых товаров',
        blank=True
    )

    def __str__(self):
        return self.name


class Buyer(models.Model):
    """Модель покупателя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='buyer_profile',
        primary_key=True
    )
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

    def __str__(self):
        return self.full_name


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
    def total_price(self):
        """
        Считает полную стоимость товаров одного вида на складе
        для отображения в админке
        """
        return self.price * self.quantity


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
    # items = models.ManyToManyField(Product, through='DeliveryItem')

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

    @property
    def get_item_price(self):
        return self.product.price * self.quantity


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
