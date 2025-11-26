import reflex as rx
from datetime import datetime, timedelta
from app.states.receipt_state import ReceiptState
from app.utils.export import generate_csv
import logging


class ReportsState(rx.State):
    """Manages reports data and filtering."""

    start_date: str = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date: str = datetime.now().strftime("%Y-%m-%d")
    selected_class: str = ""

    @rx.var
    async def filtered_receipts(self) -> list[dict]:
        receipt_state = await self.get_state(ReceiptState)
        receipts = receipt_state.all_receipts
        filtered = []
        for r in receipts:
            r_date = r.date.split("T")[0]
            if r_date < self.start_date or r_date > self.end_date:
                continue
            if self.selected_class and r.class_grade != self.selected_class:
                continue
            filtered.append(r)
        return filtered

    @rx.var
    async def total_collected_period(self) -> float:
        receipts = await self.filtered_receipts
        return sum((r.amount for r in receipts))

    @rx.var
    async def total_transactions_period(self) -> int:
        receipts = await self.filtered_receipts
        return len(receipts)

    @rx.var
    async def income_over_time(self) -> list[dict]:
        """Daily income for the selected period."""
        receipts = await self.filtered_receipts
        stats = {}
        curr = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        while curr <= end:
            stats[curr.strftime("%Y-%m-%d")] = 0.0
            curr += timedelta(days=1)
        for r in receipts:
            d = r.date.split("T")[0]
            if d in stats:
                stats[d] += r.amount
        return [{"date": k, "amount": v} for k, v in stats.items()]

    @rx.event
    def set_start_date(self, date: str):
        self.start_date = date

    @rx.event
    def set_end_date(self, date: str):
        self.end_date = date

    @rx.event
    def set_selected_class(self, class_name: str):
        self.selected_class = class_name

    @rx.event
    async def download_csv(self):
        receipts = await self.filtered_receipts
        csv_string = generate_csv(receipts)
        return rx.download(
            data=csv_string, filename=f"report_{self.start_date}_{self.end_date}.csv"
        )