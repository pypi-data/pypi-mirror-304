# Receipt_Generator

Finance_Report — Python-пакет для автоматической генерации чеков из заказов.

## Установка

Установите библиотеку с помощью команды:

```bash
pip install receipt_generator
```

## Пример использования 

```bash
generate-receipt --input-file order.json --output-file repory.txt
```

## Пример исходных данных

```bash
{
  "customer_name": "Анна Петрова",
  "items": [
    {
      "name": "Телевизор",
      "quantity": 1,
      "price": 45000
    },
    {
      "name": "Смартфон",
      "quantity": 2,
      "price": 35000
    },
    {
      "name": "Наушники",
      "quantity": 3,
      "price": 3000
    },
    {
      "name": "Чехол для смартфона",
      "quantity": 5,
      "price": 500
    },
    {
      "name": "Ноутбук",
      "quantity": 1,
      "price": 80000
    },
    {
      "name": "Клавиатура",
      "quantity": 2,
      "price": 2500
    },
    {
      "name": "Мышь",
      "quantity": 3,
      "price": 1500
    },
    {
      "name": "Монитор",
      "quantity": 2,
      "price": 20000
    },
    {
      "name": "Принтер",
      "quantity": 1,
      "price": 15000
    },
    {
      "name": "Коврик для мыши",
      "quantity": 5,
      "price": 200
    },
    {
      "name": "Игровая консоль",
      "quantity": 1,
      "price": 40000
    },
    {
      "name": "Геймпад",
      "quantity": 2,
      "price": 4500
    },
    {
      "name": "Умные часы",
      "quantity": 2,
      "price": 12000
    },
    {
      "name": "Планшет",
      "quantity": 3,
      "price": 25000
    },
    {
      "name": "Фитнес-браслет",
      "quantity": 4,
      "price": 5000
    },
    {
      "name": "Внешний аккумулятор",
      "quantity": 5,
      "price": 1500
    },
    {
      "name": "Флешка",
      "quantity": 10,
      "price": 600
    },
    {
      "name": "Веб-камера",
      "quantity": 1,
      "price": 5000
    },
    {
      "name": "Зарядное устройство",
      "quantity": 3,
      "price": 1200
    },
    {
      "name": "Микрофон",
      "quantity": 2,
      "price": 7000
    },
    {
      "name": "Внешний жесткий диск",
      "quantity": 2,
      "price": 8000
    },
    {
      "name": "Колонки",
      "quantity": 3,
      "price": 3000
    },
    {
      "name": "Переходник HDMI",
      "quantity": 4,
      "price": 700
    },
    {
      "name": "Настольная лампа",
      "quantity": 1,
      "price": 2500
    },
    {
      "name": "Проектор",
      "quantity": 1,
      "price": 35000
    }
  ]
}
```