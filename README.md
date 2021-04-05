# stms_v1
Небольшой тестовый бэк для системы складского учета на DRF
Есть такое:

1. Поставщики.
У каждого ункциипоставщика есть личная карточка, которая содержит:
-Информацию о Юридическом лице (реквизиты, адрес).
-Контактные данные (контактное лицо, телефон, e-mail).
-Категории привозимых товаров и последние поставки.

Все данные о поставщиках вносятся вручную, приходтовара регистрируется вручную.

2. Покупатели. У каждого покупателя естьличная карточка, которая содержит:
-ФИО.-Контактные данные (контактное лицо, телефон, e-mail).
-Сведения о заказах.

Все данные о поставщиках вносятся вручную, заявкана заказ товара регистрируется вручную.

3. Список товаров.
Карточка товара состоит из:
-Категорий товаров(подкатегорий).
-Стоимость всех товаров в категории.
-Количества подкатегорий (наименований в категории).
-Наименований товаров.
-Стоимость единицы товара.
-Количество товара на складе.
-Артикул товара.

4. Поставка.
Хранит наши заявки на поставку товаров на склад.
-Статус.
-Дата.

5. Отгрузка
Хранит заявки на отгрузку товара от покупателя.
Модуль поставки состоит из общего списка  заявок скраткой информацией, а также карточекна отгрузки в которые можно перейти.
Список заявок можно фильтровать и проводить по нему поиск.
Карточка состоит из:
-Номер заявки,
-Наименования покупателя,
-Количество позиций,
-Сумма,
-Статус,
-Дата,
