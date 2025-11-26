import reflex as rx
import sqlmodel
import logging
from app.db import Receipt, SchoolInfo, Settings


def initialize_db():
    """Initialize the database tables if they do not exist."""
    try:
        with rx.session() as session:
            engine = session.get_bind()
            sqlmodel.SQLModel.metadata.create_all(engine)
            logging.info("Database tables verified/initialized successfully.")
    except Exception as e:
        logging.exception(f"Database initialization failed: {e}")