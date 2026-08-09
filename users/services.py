import os

import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("API_KEY")


def create_stripe_product(name):
    """Создаем продукт в страйпе"""
    return stripe.Product.create(name=name)


def create_stripe_price(product, amount):
    """Создаем цену в страйпе"""
    return stripe.Price.create(currency="rub", unit_amount=amount * 100, product=product.id)


def create_stripe_session(price):
    """Создаем сессию в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
