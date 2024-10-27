# Receipt_Generator

**Receipt_Generator** — Python-пакет для автоматической генерации чеков из заказов. Установка: `pip install receipt_generator`. Использование: `generate-receipt --input-file order_data.json --output-file receipt.txt`. Параметры: `--input-file` — путь к входному JSON-файлу с данными о заказе (обязательный), `--output-file` — путь для сохранения чека (обязательный). Формат JSON: 
```json
{
  "customer_name": "Иван Иванов",
  "items": [
    {"name": "Телефон", "quantity": 1, "price": 20000},
    {"name": "Наушники", "quantity": 2, "price": 1500}
  ]
}
