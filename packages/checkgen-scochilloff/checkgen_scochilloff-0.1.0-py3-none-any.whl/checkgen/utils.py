import json


def load_order(filename: str) -> dict[str]:
    with open(filename, encoding="utf-8") as file:
        order = json.load(file)
    return order


def write_check(order: dict[str], filename: str) -> None:
    check = get_check(order)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(check)


def get_check(order: dict[str]) -> str:
    template = """Клиент: {}
    
Товары:
{}

Итого: {} руб."""
    customer_name = order["customer_name"]
    item_strs = []
    total = 0
    for item in order["items"]:
        name = item["name"]
        quantity = item["quantity"]
        price = item["price"]
        item_str = f"{name} x{quantity} {price} руб./шт."
        item_strs.append(item_str)
        total += price * quantity
    items_str = "\n".join(item_strs)
    return template.format(customer_name, items_str, total)