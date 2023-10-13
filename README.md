Прошлый `README.md` был перемещен в `/task/README.md`

# Задание 1

Решение:

1. Был написан [view](robots/views.py), принимающий по url `/robots/api` POST и GET (для отладки) запросы
2. Благодаря функции `Model.full_clean()` сделана валидация и чистка данных
    * В случае не прохождения валидации данных, отправителю выдается JSON с сообщением об ошибке
    * В случае успешной валидации данных, отправителю выдается JSON с информацией о записи данных в базу данных
3. Были написаны автотесты, тестирующие написанный функционал

# Задание 2

Требования:

* Установить библиотеку `openpyxl`. С помощью неё формируется `.xlsx` файл

Решение:

1. Было создано отдельное приложение reports. Оно будет отвечать за формирование отчетов
2. С помощью скрипта [fill_data.py](reports/tools/fill_data.py) база данных была заполнена данными
3. [excel.py](reports/tools/excel.py) - модуль занимается преобразованием данных и формированием .xlsx отчета
4. Отчет сохраняется во временном файле и отправляется посредством [HTTP запроса](reports/views.py)
5. Чтобы директору заполучить отчет, ему нужно просто открыть url `/reports`, скачивание начнется автоматически

# Задание 3

Решение:

1. Для отправки писем использована встроенная библиотека `django.core.mail`.
   Ее легко использовать и тестировать в Django приложении. Функцию по отправке сообщений поместил во `orders/views.py`
2. Момент появления нового робота (оно же появление записи в базе данных Robot) прослушиваются с помощью сигналов.
   Был написан простой получатель в `orders/models/` (именно здесь он сразу активировался, при импорте модели Order)
3. При создании нового робота, получатель ищет последний заказ такого робота (клиент которого ждет дольше всех)
4. Если такой существует, ему отправляется письмо-извещение по форме
5. По окончании, объекты заказа и робота удаляются из баз данных (робота больше нет в наличии, а заказ уже выполнен)
6. Написаны [тесты](orders/tests.py) этой функциональности

## Данные для администрирования

Admin:

- Username: admin
- Email: admin@example.com
- Password: pass123word

## TODO:

Дальнейшие улучшения

1. (Рефакторинг): Удалить поле serial из модели.

    + Это сэкономило бы место в базе данных
    + Код стал бы чище. Не нужно было постоянно записывать это поле как `f"{model}-{version}"`
      Чем можно было бы заменить? Свойством `@property`

   ```python
   class Robot(models.Model):
       ...
   
       @property
       def serial(self):
           return f"{self.model}-{self.version}"
   ```

2. (Тесты) Тесты для второго задания
3. (Функциональность за рамки заданий) Функциональность добавления нового заказа.
   Если добавляется новый заказ, то должна проверятся база данных роботов "А можно ли выполнить его сейчас?"
   и выполнять, если можно.