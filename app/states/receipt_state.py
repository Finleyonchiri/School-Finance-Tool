import reflex as rx
from typing import Optional
from app.db import Receipt
import random
from datetime import datetime, timedelta
import math
import logging


class ReceiptState(rx.State):
    """Manages receipt data, filtering, search, and pagination."""

    receipts: list[Receipt] = []
    all_receipts: list[Receipt] = []
    total_count: int = 0
    search_query: str = ""
    filter_class: str = ""
    filter_date_start: str = ""
    filter_date_end: str = ""
    page: int = 1
    page_size: int = 5

    @rx.var
    def total_collected(self) -> float:
        """Calculate total amount collected from all receipts."""
        return sum((r.amount for r in self.all_receipts))

    @rx.var
    def receipts_count(self) -> int:
        """Total number of receipts."""
        return len(self.all_receipts)

    @rx.var
    def outstanding_amount(self) -> float:
        """Mock calculation for outstanding amount (45% of collected)."""
        return self.total_collected * 0.45

    @rx.var
    def active_students_count(self) -> int:
        """Count unique students."""
        return len(set((r.admission_number for r in self.all_receipts)))

    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages based on filtered count."""
        return max(1, math.ceil(self.total_count / self.page_size))

    @rx.var
    def current_receipts(self) -> list[Receipt]:
        """Return the receipts for the current view."""
        return self.receipts

    @rx.var
    def monthly_stats(self) -> list[dict[str, str | float]]:
        """Calculate monthly income for the last 12 months."""
        stats = {}
        today = datetime.now()
        for i in range(11, -1, -1):
            d = today - timedelta(days=i * 30)
            key = d.strftime("%b %Y")
            stats[key] = 0.0
        for r in self.all_receipts:
            try:
                d = datetime.fromisoformat(r.date)
                key = d.strftime("%b %Y")
                if key in stats:
                    stats[key] += r.amount
            except ValueError as e:
                logging.exception(f"Error parsing date: {e}")
                continue
        return [{"month": m, "amount": amt} for m, amt in stats.items()]

    @rx.var
    def class_stats(self) -> list[dict[str, str | float]]:
        """Calculate total collected per class."""
        stats = {}
        for r in self.all_receipts:
            if r.class_grade in stats:
                stats[r.class_grade] += r.amount
            else:
                stats[r.class_grade] = r.amount
        result = [{"name": k, "amount": v} for k, v in stats.items()]
        result.sort(key=lambda x: x["name"])
        return result

    def _generate_data(self):
        students = [
            ("John Doe", "ADM001", "Grade 10"),
            ("Jane Smith", "ADM002", "Grade 11"),
            ("Michael Brown", "ADM003", "Grade 9"),
            ("Emily Davis", "ADM004", "Grade 12"),
            ("Chris Wilson", "ADM005", "Grade 10"),
            ("Sarah Johnson", "ADM006", "Grade 8"),
            ("David Miller", "ADM007", "Grade 11"),
            ("Jessica Taylor", "ADM008", "Grade 9"),
            ("Robert Key", "ADM009", "Grade 8"),
            ("Linda White", "ADM010", "Grade 12"),
        ]
        payment_methods = ["Cash", "Bank Transfer", "Mobile Money", "Check"]
        new_receipts = []
        for _ in range(80):
            student = random.choice(students)
            amount = random.choice([500.0, 1000.0, 1500.0, 2000.0, 750.0, 3000.0])
            days_ago = random.randint(0, 365)
            date = (datetime.now() - timedelta(days=days_ago)).isoformat()
            receipt = Receipt(
                student_name=student[0],
                admission_number=student[1],
                class_grade=student[2],
                payer_name=f"Parent of {student[0].split()[0]}",
                amount=amount,
                payment_method=random.choice(payment_methods),
                reference_id=f"REF{random.randint(10000, 99999)}",
                date=date,
                notes="Term fee payment",
                created_at=datetime.now().isoformat(),
            )
            new_receipts.append(receipt)
        new_receipts.sort(key=lambda r: r.date, reverse=True)
        self.all_receipts = new_receipts

    @rx.event
    def load_receipts(self):
        """Fetch receipts from mock data with filters applied."""
        if not self.all_receipts:
            self._generate_data()
        filtered = self.all_receipts
        if self.search_query:
            sq = self.search_query.lower()
            filtered = [
                r
                for r in filtered
                if sq in r.student_name.lower()
                or sq in r.admission_number.lower()
                or sq in r.reference_id.lower()
            ]
        if self.filter_class:
            filtered = [r for r in filtered if r.class_grade == self.filter_class]
        if self.filter_date_start:
            filtered = [r for r in filtered if r.date >= self.filter_date_start]
        if self.filter_date_end:
            filtered = [r for r in filtered if r.date <= self.filter_date_end]
        self.total_count = len(filtered)
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        self.receipts = filtered[start:end]

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.page = 1
        self.load_receipts()

    @rx.event
    def set_page(self, page: int):
        self.page = page
        self.load_receipts()

    @rx.event
    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            self.load_receipts()

    @rx.event
    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_receipts()

    @rx.event
    def on_mount(self):
        self.load_receipts()

    new_student_name: str = ""
    new_admission_number: str = ""
    new_class_grade: str = ""
    new_payer_name: str = ""
    new_payer_phone: str = ""
    new_payment_method: str = "Cash"
    new_amount: str = ""
    new_reference_id: str = ""
    new_date: str = datetime.now().isoformat().split("T")[0]
    new_notes: str = ""
    view_receipt_id: str = ""
    is_delete_modal_open: bool = False
    receipt_to_delete_id: str = ""
    selected_receipt_ids: list[str] = []

    @rx.event
    def toggle_selection(self, ref_id: str):
        if ref_id in self.selected_receipt_ids:
            self.selected_receipt_ids.remove(ref_id)
        else:
            self.selected_receipt_ids.append(ref_id)

    @rx.event
    def select_all_current(self):
        for r in self.current_receipts:
            if r.reference_id not in self.selected_receipt_ids:
                self.selected_receipt_ids.append(r.reference_id)

    @rx.event
    def clear_selection(self):
        self.selected_receipt_ids = []

    @rx.event
    async def export_backup(self):
        from app.utils.export import generate_json_backup
        from app.states.settings_state import SettingsState

        settings_state = await self.get_state(SettingsState)
        settings_dict = settings_state.get_settings_dict()
        json_data = generate_json_backup(self.all_receipts, settings_dict)
        return rx.download(data=json_data, filename="toya_backup.json")

    @rx.var
    def selected_receipt(self) -> Optional[Receipt]:
        """Get receipt by view_receipt_id."""
        if not self.view_receipt_id:
            return None
        for r in self.all_receipts:
            if r.reference_id == self.view_receipt_id:
                return r
        return None

    @rx.var
    def selected_receipt_qr(self) -> str:
        """Generate QR code for selected receipt."""
        if not self.selected_receipt:
            return ""
        from app.utils.qr_code import generate_qr_code

        data = f"TOYA-REC:{self.selected_receipt.reference_id}|AMT:{self.selected_receipt.amount}|DATE:{self.selected_receipt.date}"
        return generate_qr_code(data)

    @rx.var
    def selected_receipt_words(self) -> str:
        """Convert amount to words."""
        if not self.selected_receipt:
            return ""
        from app.utils.number_to_words import amount_to_words

        return amount_to_words(self.selected_receipt.amount)

    @rx.event
    def set_new_payment_method(self, method: str):
        self.new_payment_method = method

    @rx.event
    def generate_reference(self):
        import random

        self.new_reference_id = f"REF{random.randint(100000, 999999)}"

    @rx.event
    def save_receipt(self):
        """Validate and save a new receipt."""
        if (
            not self.new_student_name
            or not self.new_admission_number
            or (not self.new_amount)
        ):
            return rx.toast.error("Please fill in all required fields.")
        try:
            amount_float = float(self.new_amount)
            if amount_float <= 0:
                return rx.toast.error("Amount must be greater than 0.")
        except ValueError as e:
            logging.exception(f"Error parsing amount: {e}")
            return rx.toast.error("Invalid amount format.")
        if not self.new_reference_id:
            self.generate_reference()
        if any((r.reference_id == self.new_reference_id for r in self.all_receipts)):
            return rx.toast.error(
                "Reference ID already exists. Please generate a new one."
            )
        new_receipt = Receipt(
            student_name=self.new_student_name,
            admission_number=self.new_admission_number,
            class_grade=self.new_class_grade,
            payer_name=self.new_payer_name,
            amount=amount_float,
            payment_method=self.new_payment_method,
            reference_id=self.new_reference_id,
            date=self.new_date,
            notes=self.new_notes,
            created_at=datetime.now().isoformat(),
        )
        self.all_receipts.insert(0, new_receipt)
        self.load_receipts()
        self.clear_form()
        return rx.toast.success("Receipt saved successfully!")

    @rx.event
    def clear_form(self):
        self.new_student_name = ""
        self.new_admission_number = ""
        self.new_class_grade = ""
        self.new_payer_name = ""
        self.new_payer_phone = ""
        self.new_amount = ""
        self.new_reference_id = ""
        self.new_notes = ""
        self.new_date = datetime.now().isoformat().split("T")[0]

    @rx.event
    def confirm_delete(self, ref_id: str):
        self.receipt_to_delete_id = ref_id
        self.is_delete_modal_open = True

    @rx.event
    def cancel_delete(self):
        self.is_delete_modal_open = False
        self.receipt_to_delete_id = ""

    @rx.event
    def delete_receipt(self):
        if self.receipt_to_delete_id:
            self.all_receipts = [
                r
                for r in self.all_receipts
                if r.reference_id != self.receipt_to_delete_id
            ]
            self.load_receipts()
            self.is_delete_modal_open = False
            self.receipt_to_delete_id = ""
            return rx.toast.success("Receipt deleted.")

    @rx.event
    def load_view_receipt(self, ref_id: str):
        """Load specific receipt for view page based on URL param."""
        if not self.all_receipts:
            self._generate_data()
        if ref_id:
            self.view_receipt_id = ref_id