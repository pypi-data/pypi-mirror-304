# README.md

## Online Store

Этот пакет предоставляет функциональность для управления клиентами и заказами в онлайн-магазине. С помощью классов `UserManager` и `OrderManager` вы можете легко добавлять, обновлять, удалять и находить пользователей и заказы.

### Установка

```bash
pip install online-store-srcelomac
```

### Использование

#### UserManager

Класс `UserManager` позволяет управлять учетными записями клиентов.

```python
from online_store import UserManager

user_manager = UserManager()

# Добавить клиента
user_manager.add_user(user_id='123', user_data={'name': 'Иван', 'age': 30})

# Обновить данные клиента
user_manager.update_user(user_id='123', user_data={'name': 'Иван Петров', 'age': 31})

# Найти клиента
client = user_manager.find_user(user_id='123')

# Удалить клиента
user_manager.remove_user(user_id='123')
```

#### OrderManager

Класс `OrderManager` позволяет управлять заказами.

```python
from online_store import OrderManager

order_manager = OrderManager()

# Создать заказ
order_manager.create_order(order_id='456', order_data={'user': 'Иван', 'item': 'Книга', 'price': 500})

# Обновить заказ
order_manager.update_order(order_id='456', order_data={'status': 'Доставлен'})

# Отменить заказ
order_manager.cancel_order(order_id='456')
```

### Функционал

#### UserManager

- **add_user(user_id, user_data)**: Добавляет нового клиента. Если клиент с данным ID уже существует, выводит сообщение об этом.
- **remove_user(user_id)**: Удаляет клиента. Если клиент не найден, выводит соответствующее сообщение.
- **update_user(user_id, user_data)**: Обновляет данные клиента. Если клиент не найден, выводит сообщение об этом.
- **find_user(user_id)**: Возвращает данные клиента по идентификатору. Если клиент не найден, выводит сообщение об этом.

#### OrderManager

- **create_order(order_id, order_data)**: Создает новый заказ. Если заказ с данным ID уже существует, выводит сообщение об этом.
- **update_order(order_id, order_data)**: Обновляет информацию о заказе. Если заказ не найден, выводит сообщение об этом.
- **cancel_order(order_id)**: Отменяет заказ по идентификатору. Если заказ не найден, выводит сообщение об этом.

### Примечания

- Убедитесь, что данные пользователей и заказов передаются в корректном формате.
- Этот пакет может быть расширен для более сложного функционала и легко масштабируется.

### Лицензия

Этот проект доступен под лицензией MIT. Для подробной информации смотрите файл LICENSE.