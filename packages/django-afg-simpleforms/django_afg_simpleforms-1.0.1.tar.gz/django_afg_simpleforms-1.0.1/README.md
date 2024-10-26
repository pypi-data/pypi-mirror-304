---КОМАНДЫ---

Включение venv (виртуального окружения): source .venv/bin/activate
*не факт, что понадобится

Создание проекта: django-admin startproject <название>
Создание приложения: django-admin startapp <название>
Запуск сервера: python manage.py runserver
Запуск сервера на опр хосте: python manage.py runserver localhost:<host>
Миграция: python manage.py makemigrations
          python manage.py migrate
Создание суперпользователя: python manage.py createsuperuser
Сбор статичных файлов (после указания STATIC_ROOT в настройках): python manage.py collectstatic

Движение по файловому менеджеру:
cd <куда нужно перейти в текущем каталоге>
cd ../


1. Поля текста
CharField

max_length: Максимальная длина строки.
blank: Разрешить пустые значения (по умолчанию False).
null: Разрешить значение None (по умолчанию False).
TextField

blank: Разрешить пустые значения.
null: Разрешить значение None.
2. Поля чисел
IntegerField

blank
null
PositiveIntegerField

blank
null
NegativeIntegerField

blank
null
FloatField

blank
null
DecimalField

max_digits: Общее количество цифр.
decimal_places: Количество знаков после запятой.
blank
null
3. Поля даты и времени
DateField

auto_now: Автоматически устанавливает дату при обновлении объекта.
auto_now_add: Автоматически устанавливает дату при создании объекта.
blank
null
TimeField

auto_now
auto_now_add
blank
null
DateTimeField

auto_now
auto_now_add
blank
null
DurationField

blank
null
4. Поля для работы с логическими данными
BooleanField

default: Значение по умолчанию (True или False).
blank
NullBooleanField (устаревший в новых версиях)

blank
5. Поля для идентификаторов
AutoField

primary_key: Установить поле как первичный ключ (по умолчанию True).
UUIDField

default: Значение по умолчанию (uuid.uuid4).
editable: Задает, можно ли редактировать это поле в админке.
6. Поля для работы со связями между моделями
ForeignKey

to: Связанная модель.
on_delete: Поведение при удалении связанного объекта.
related_name: Имя обратной связи.
blank
null
OneToOneField

Все параметры ForeignKey плюс:
parent_link: Если True, создает ссылку на родительскую модель.
ManyToManyField

to: Связанная модель.
through: Указать промежуточную модель.
related_name
blank
7. Поля для файлов и изображений
FileField

upload_to: Папка для загрузки.
max_length
blank
null
ImageField

Все параметры FileField плюс:
Проверка на изображение.
8. Поля для выбора значений
SlugField

max_length
unique: Уникальность.
blank
EmailField

max_length
blank
URLField

max_length
blank
9. Специальные поля
JSONField

blank
null
ArrayField (только для PostgreSQL)

base_field: Базовый тип поля для массива.
size: Ограничение по размеру массива.
HStoreField (только для PostgreSQL)

blank
null


