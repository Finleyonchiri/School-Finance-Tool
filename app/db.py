import reflex as rx
from datetime import datetime


class Receipt(rx.Base):
    student_name: str
    admission_number: str
    class_grade: str
    payer_name: str
    amount: float
    payment_method: str
    reference_id: str
    date: str
    notes: str = ""
    created_at: str = ""


class SchoolInfo(rx.Base):
    name: str
    address: str
    phone: str
    email: str
    logo_path: str = ""
    motto: str = ""
    currency_symbol: str = "$"


class Settings(rx.Base):
    key: str
    value: str