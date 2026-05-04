import xml.etree.ElementTree as ET


def available_products(product_file: str) -> None:
    """
    Читає XML-файл і виводить назви продуктів та їхню кількість.

    :param product_file: Шлях до XML-файлу з продуктами.
    :return: None
    """
    tree = ET.parse(product_file)
    root = tree.getroot()
    for product in root.findall('product'):
        name = product.find('name').text
        quantity = product.find('quantity').text
        print(f"{name} - {quantity}")


def update_product_quantity(product_file: str, product_name: str, new_product_quantity: int) -> None:
    """
    Змінює кількість товару в XML-файлі та виводить звіт про зміни.

    :param product_file: Шлях до XML-файлу.
    :param product_name: Назва продукту, який треба оновити.
    :param new_product_quantity: Нова кількість одиниць товару.
    :return: None
    """
    tree = ET.parse(product_file)
    root = tree.getroot()
    flag = False
    old_product_quantity = ''

    for product in root.findall('product'):
        if product.find('name').text == product_name:
            old_product_quantity = product.find('quantity').text
            product.find('quantity').text = str(new_product_quantity)
            flag = True
            break

    if flag:
        tree.write(product_file, encoding='utf-8', xml_declaration=True)
        print(f'Кількість продукта "{product_name}" змінено з {old_product_quantity} на {new_product_quantity}')
    else:
        print(f'Помилка! Продукт "{product_name}" не існує в XML-файлі!')

available_products('products.xml')
update_product_quantity('products.xml', 'Молоко', 526)
update_product_quantity('products.xml', 'Яблука', 2)