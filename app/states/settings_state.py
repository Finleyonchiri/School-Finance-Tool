import reflex as rx
from typing import Any


class SettingsState(rx.State):
    """Manages application settings and UI state."""

    sidebar_open: bool = True
    current_theme: str = "light"
    school_name: str = "TOYA International Academy"
    school_address: str = "123 Education Lane, Knowledge City"
    school_phone: str = "+1 234 567 890"
    school_email: str = "admin@toya.edu"
    school_motto: str = "Excellence in Education"
    school_logo: str = "/placeholder.svg"
    currency_symbol: str = "$"
    is_cashier_mode: bool = False
    cashier_pin: str = "1234"
    input_pin: str = ""
    is_authenticated: bool = False
    show_pin_modal: bool = False

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def toggle_theme(self):
        """Toggle between light and dark mode."""
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"

    @rx.event
    def update_school_info(self, field: str, value: str):
        setattr(self, field, value)

    @rx.event
    def save_settings(self):
        return rx.toast.success("Settings saved successfully!")

    @rx.event
    def verify_pin(self):
        if self.input_pin == self.cashier_pin:
            self.is_authenticated = True
            self.show_pin_modal = False
            self.input_pin = ""
            return rx.toast.success("Access granted")
        else:
            return rx.toast.error("Invalid PIN")

    @rx.event
    def prompt_pin(self):
        self.show_pin_modal = True

    @rx.event
    def set_pin_input(self, value: str):
        self.input_pin = value

    @rx.event
    def cancel_pin(self):
        self.show_pin_modal = False
        self.input_pin = ""

    @rx.event
    def get_settings_dict(self) -> dict[str, Any]:
        return {
            "school_name": self.school_name,
            "school_address": self.school_address,
            "school_phone": self.school_phone,
            "currency_symbol": self.currency_symbol,
        }