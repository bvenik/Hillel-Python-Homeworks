from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from django.db import transaction
from ninja.errors import HttpError
from ..models import Product, CartItem, Order, OrderItem
from ..schemas import ProductIn, ProductOut, CartItemIn, CartItemOut, OrderOut
from ..auth import bearer_auth

router = Router()


@router.get("/products", response=List[ProductOut], auth=bearer_auth)
def list_products(request):
    """
    Retrieves the list of all available products.
    :param request: standard Django HTTP request object
    :return: list of all products in the database
    """
    return Product.objects.all()


@router.get("/products/{product_id}", response=ProductOut, auth=bearer_auth)
def get_product(request, product_id: int):
    """
    Retrieves a single product's details by its ID.
    :param request: standard Django HTTP request object
    :param product_id: unique integer identifier of the product
    :return: Product instance or raises 404 Not Found
    """
    return get_object_or_404(Product, id=product_id)


@router.post("/products", response={201: ProductOut}, auth=bearer_auth)
def create_product(request, data: ProductIn):
    """
    Creates a new product in the store database.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing product name, description, price, and stock quantity
    :return: tuple of HTTP status code 201 and the created Product instance
    """
    product = Product.objects.create(**data.dict())
    return 201, product


@router.put("/products/{product_id}", response=ProductOut, auth=bearer_auth)
def update_product(request, product_id: int, data: ProductIn):
    """
    Updates an existing product's details.
    :param request: standard Django HTTP request object
    :param product_id: unique integer identifier of the product to update
    :param data: Pydantic schema containing updated product name, description, price, and stock quantity
    :return: updated Product instance
    """
    product = get_object_or_404(Product, id=product_id)
    for attr, value in data.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@router.delete("/products/{product_id}", response={204: None}, auth=bearer_auth)
def delete_product(request, product_id: int):
    """
    Deletes a product from the database.
    :param request: standard Django HTTP request object
    :param product_id: unique integer identifier of the product to delete
    :return: tuple of HTTP status code 204 and None
    """
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return 204, None


@router.get("/cart", response=List[CartItemOut], auth=bearer_auth)
def view_cart(request):
    """
    Retrieves all cart items belonging to the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :return: list of CartItem instances for the user
    """
    return CartItem.objects.filter(user=request.user)


@router.post("/cart", response={200: CartItemOut, 201: CartItemOut}, auth=bearer_auth)
def add_to_cart(request, data: CartItemIn):
    """
    Adds a specified quantity of a product to the user's shopping cart.
    :param request: standard Django HTTP request object containing authenticated user
    :param data: Pydantic schema containing product ID and quantity to add
    :return: tuple of HTTP status code (200 for updated, 201 for created) and the CartItem instance
    """
    product = get_object_or_404(Product, id=data.product_id)
    if product.stock < data.quantity:
        raise HttpError(
            400, f"Insufficient stock. Only {product.stock} available.")

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': data.quantity}
    )
    if not created:
        if product.stock < (cart_item.quantity + data.quantity):
            raise HttpError(
                400, f"Insufficient stock to add more. Total stock: {product.stock}.")
        cart_item.quantity += data.quantity
        cart_item.save()
        return 200, cart_item
    return 201, cart_item


@router.delete("/cart/{item_id}", response={204: None}, auth=bearer_auth)
def remove_from_cart(request, item_id: int):
    """
    Removes an item from the user's shopping cart.
    :param request: standard Django HTTP request object containing authenticated user
    :param item_id: unique integer identifier of the cart item to remove
    :return: tuple of HTTP status code 204 and None
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return 204, None


@router.post("/orders", response={201: OrderOut}, auth=bearer_auth)
def place_order(request):
    """
    Creates an order from the items in the user's shopping cart, deducting stock and clearing the cart.
    :param request: standard Django HTTP request object containing authenticated user
    :return: tuple of HTTP status code 201 and the created Order instance with items
    """
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        raise HttpError(400, "Your cart is empty.")

    with transaction.atomic():
        for item in cart_items:
            if item.product.stock < item.quantity:
                raise HttpError(
                    400, f"Product {item.product.name} is out of stock or insufficient.")

        order = Order.objects.create(user=request.user, status='in_progress')

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

    return 201, Order.objects.prefetch_related('items__product').get(id=order.id)


@router.get("/orders", response=List[OrderOut], auth=bearer_auth)
def list_orders(request):
    """
    Retrieves all orders placed by the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :return: list of Order instances with prefetched items
    """
    return Order.objects.filter(user=request.user).prefetch_related('items__product')


@router.put("/orders/{order_id}/status", response=OrderOut, auth=bearer_auth)
def update_order_status(request, order_id: int, status: str):
    """
    Updates the status of an existing order.
    :param request: standard Django HTTP request object containing authenticated user
    :param order_id: unique integer identifier of the order
    :param status: new status value ('in_progress', 'shipped', 'delivered')
    :return: updated Order instance
    """
    valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if status not in valid_statuses:
        raise HttpError(
            400, f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = status
    order.save()
    return order
