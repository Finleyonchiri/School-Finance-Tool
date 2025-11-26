import reflex as rx
from typing import Optional
from app.db import Receipt
from sqlmodel import select, col, or_, desc, func
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
    total_collected_val: float = 0.0
    receipts_count_val: int = 0
    active_students_count_val: int = 0
    monthly_stats_data: list[dict[str, str | float]] = []
    class_stats_data: list[dict[str, str | float]] = []

    @rx.var
    def total_collected(self) -> float:
        return self.total_collected_val

    @rx.var
    def receipts_count(self) -> int:
        return self.receipts_count_val

    @rx.var
    def outstanding_amount(self) -> float:
        return self.total_collected_val * 0.45

    @rx.var
    def active_students_count(self) -> int:
        return self.active_students_count_val

    @rx.var
    def total_pages(self) -> int:
        return max(1, math.ceil(self.total_count / self.page_size))

    @rx.var
    def current_receipts(self) -> list[Receipt]:
        return self.receipts

    @rx.var
    def monthly_stats(self) -> list[dict[str, str | float]]:
        return self.monthly_stats_data

    @rx.var
    def class_stats(self) -> list[dict[str, str | float]]:
        return self.class_stats_data

    def _seed_database(self):
        """Seed database with sample data if empty."""
        with rx.session() as session:
            if session.exec(select(Receipt)).first():
                return
            logging.info("Seeding database with sample receipts...")
            classes = ["GRADE 1", "GRADE 2", "GRADE 3", "PP1", "PP2"]
            methods = ["Cash", "Bank Transfer", "Mobile Money"]
            names = [
                "John Doe",
                "Jane Smith",
                "Alice Jones",
                "Bob Brown",
                "Charlie Davis",
            ]
            for i in range(15):
                date_offset = random.randint(0, 60)
                r_date = (datetime.now() - timedelta(days=date_offset)).isoformat()
                receipt = Receipt(
                    student_name=random.choice(names),
                    admission_number=f"ADM{1000 + i}",
                    class_grade=random.choice(classes),
                    payer_name="Parent",
                    amount=float(random.randint(100, 5000)),
                    payment_method=random.choice(methods),
                    reference_id=f"REF{random.randint(100000, 999999)}",
                    date=r_date,
                    created_at=datetime.now().isoformat(),
                    notes="Sample receipt",
                )
                session.add(receipt)
            session.commit()

    @rx.event
    def load_stats(self):
        """Load global stats from DB."""
        try:
            with rx.session() as session:
                total = session.exec(select(func.sum(Receipt.amount))).one_or_none()
                self.total_collected_val = float(total) if total else 0.0
                self.receipts_count_val = (
                    session.exec(select(func.count(Receipt.id))).one() or 0
                )
                self.active_students_count_val = len(
                    session.exec(select(Receipt.admission_number).distinct()).all()
                )
                all_recs = session.exec(select(Receipt)).all()
                self.all_receipts = all_recs
                stats = {}
                today = datetime.now()
                for i in range(11, -1, -1):
                    d = today - timedelta(days=i * 30)
                    key = d.strftime("%b %Y")
                    stats[key] = 0.0
                for r in all_recs:
                    try:
                        d = datetime.fromisoformat(r.date)
                        key = d.strftime("%b %Y")
                        if key in stats:
                            stats[key] += r.amount
                    except Exception as e:
                        logging.exception(f"Error parsing receipt date: {e}")
                        continue
                self.monthly_stats_data = [
                    {"month": m, "amount": amt} for m, amt in stats.items()
                ]
                c_stats = {}
                for r in all_recs:
                    if r.class_grade in c_stats:
                        c_stats[r.class_grade] += r.amount
                    else:
                        c_stats[r.class_grade] = r.amount
                c_result = [{"name": k, "amount": v} for k, v in c_stats.items()]
                c_result.sort(key=lambda x: x["name"])
                self.class_stats_data = c_result
        except Exception as e:
            logging.exception(f"Error loading stats: {e}")
            self.total_collected_val = 0.0
            self.receipts_count_val = 0
            self.active_students_count_val = 0
            self.all_receipts = []
            self.monthly_stats_data = []
            self.class_stats_data = []

    @rx.event
    def load_receipts(self):
        """Fetch receipts from database with filters applied."""
        try:
            query = select(Receipt).order_by(desc(Receipt.date))
            if self.search_query:
                sq = f"%{self.search_query.lower()}%"
                query = query.where(
                    or_(
                        col(Receipt.student_name).contains(self.search_query),
                        col(Receipt.admission_number).contains(self.search_query),
                        col(Receipt.reference_id).contains(self.search_query),
                    )
                )
            if self.filter_class:
                query = query.where(Receipt.class_grade == self.filter_class)
            if self.filter_date_start:
                query = query.where(Receipt.date >= self.filter_date_start)
            if self.filter_date_end:
                query = query.where(Receipt.date <= self.filter_date_end)
            with rx.session() as session:
                self.total_count = len(session.exec(query).all())
                start = (self.page - 1) * self.page_size
                query = query.offset(start).limit(self.page_size)
                self.receipts = session.exec(query).all()
        except Exception as e:
            logging.exception(f"Error loading receipts: {e}")
            self.receipts = []
            self.total_count = 0

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
        from app.db_init import initialize_db

        try:
            initialize_db()
            self._seed_database()
            self.load_stats()
            self.load_receipts()
        except Exception as e:
            logging.exception(f"Error in ReceiptState on_mount: {e}")

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
        with rx.session() as session:
            all_data = session.exec(select(Receipt)).all()
            json_data = generate_json_backup(all_data, settings_dict)
            return rx.download(data=json_data, filename="toya_backup.json")

    @rx.var
    def selected_receipt(self) -> Optional[Receipt]:
        """Get receipt by view_receipt_id."""
        if not self.view_receipt_id:
            return None
        for r in self.receipts:
            if r.reference_id == self.view_receipt_id:
                return r
        with rx.session() as session:
            return session.exec(
                select(Receipt).where(Receipt.reference_id == self.view_receipt_id)
            ).first()

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
        try:
            with rx.session() as session:
                existing = session.exec(
                    select(Receipt).where(Receipt.reference_id == self.new_reference_id)
                ).first()
                if existing:
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
                session.add(new_receipt)
                session.commit()
            self.load_receipts()
            self.load_stats()
            self.clear_form()
            return rx.toast.success("Receipt saved successfully!")
        except Exception as e:
            logging.exception(f"Error saving receipt: {e}")
            return rx.toast.error("Database error occurred while saving receipt.")

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
            try:
                with rx.session() as session:
                    receipt = session.exec(
                        select(Receipt).where(
                            Receipt.reference_id == self.receipt_to_delete_id
                        )
                    ).first()
                    if receipt:
                        session.delete(receipt)
                        session.commit()
                self.load_receipts()
                self.load_stats()
                self.is_delete_modal_open = False
                self.receipt_to_delete_id = ""
                return rx.toast.success("Receipt deleted.")
            except Exception as e:
                logging.exception(f"Error deleting receipt: {e}")
                return rx.toast.error("Failed to delete receipt.")

    @rx.event
    def load_view_receipt(self, ref_id: str):
        """Load specific receipt for view page based on URL param."""
        if ref_id:
            self.view_receipt_id = ref_id