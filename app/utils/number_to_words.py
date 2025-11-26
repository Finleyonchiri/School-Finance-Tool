from num2words import num2words
import logging


def amount_to_words(amount: float, currency: str = "Dollars") -> str:
    """Convert a numeric amount to words."""
    try:
        text = num2words(amount, to="currency", currency="USD")
        return text.title()
    except Exception as e:
        logging.exception(f"Error converting amount to words: {e}")
        return f"{amount:.2f}"