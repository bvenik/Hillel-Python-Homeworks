def create_product(name: str, price: float, quantity: int) -> tuple:
    """
    Створює товар та повертає функцію для керування його ціною через замикання.
    """
    product_data = {
        "name": name,
        "price": price,
        "quantity": quantity
    }

    def edit_price(new_price: float) -> None:
        """
        Змінює ціну товару та виводить оновлену інформацію.
        """
        if new_price > 0:
            product_data["price"] = new_price
            print(f"Ціну товару '{product_data['name']}' змінено: {product_data['price']}")
        else:
            print("Помилка: Ціна має бути більшою за нуль!")

    def show_info() -> None:
        """
        Виводить поточну інформацію про товар.
        """
        print(f"Товар: {product_data['name']} | Ціна: {product_data['price']} | Кількість: {product_data['quantity']}")

    return edit_price, show_info


edit_apple_price, info_apple = create_product("Apple", 25.5, 100)
edit_phone_price, info_phone = create_product("Smartphone", 15000, 5)

info_apple()
edit_apple_price(28.0)
info_apple()
print("\n")
info_phone()
edit_phone_price(14500.99)
info_phone()
print("\n")
edit_phone_price(-100)
