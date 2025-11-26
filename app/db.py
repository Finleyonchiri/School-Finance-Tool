import reflex as rx
from datetime import datetime
import sqlmodel


class Receipt(sqlmodel.SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    student_name: str
    admission_number: str
    class_grade: str
    payer_name: str
    amount: float
    payment_method: str
    reference_id: str = sqlmodel.Field(unique=True, index=True)
    date: str
    notes: str = ""
    created_at: str = ""


class SchoolInfo(sqlmodel.SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    name: str
    address: str
    phone: str
    email: str
    logo_path: str = ""
    motto: str = ""
    currency_symbol: str = "$"


class Settings(sqlmodel.SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    key: str = sqlmodel.Field(unique=True, index=True)
    value: str