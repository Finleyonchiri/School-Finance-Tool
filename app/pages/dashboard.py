import reflex as rx
from app.components.layout import layout
from app.states.receipt_state import ReceiptState
from app.components.charts import monthly_income_chart, class_distribution_chart


def dashboard_stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-600 mb-1"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.icon(icon, size=24, class_name=f"text-{color}-600"),
                class_name=f"p-3 bg-{color}-100 rounded-xl",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def recent_receipt_row(receipt, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            receipt.admission_number,
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            receipt.student_name,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            receipt.class_grade,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            f"${receipt.amount:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600",
        ),
        rx.el.td(
            receipt.date.split("T")[0],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def chart_card(title: str, content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-900 mb-4"),
        rx.el.div(content, class_name="h-64 w-full"),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def index() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(
                    "Welcome back to TOYA Finance Manager",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                dashboard_stat_card(
                    "Total Collected",
                    f"${ReceiptState.total_collected:,.2f}",
                    "wallet",
                    "indigo",
                ),
                dashboard_stat_card(
                    "Total Receipts",
                    ReceiptState.receipts_count.to_string(),
                    "receipt",
                    "blue",
                ),
                dashboard_stat_card(
                    "Active Students",
                    ReceiptState.active_students_count.to_string(),
                    "users",
                    "emerald",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
            ),
            rx.el.div(
                chart_card("Monthly Income (12 Months)", monthly_income_chart()),
                chart_card("Collection by Class", class_distribution_chart()),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Recent Receipts", class_name="text-lg font-bold text-gray-900"
                    ),
                    rx.el.button(
                        "View All",
                        class_name="text-sm font-semibold text-indigo-600 hover:text-indigo-700",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Adm No.",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Student",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Class",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Amount",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Date",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                            ),
                            class_name="bg-gray-50/50",
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                ReceiptState.receipts,
                                lambda r, i: recent_receipt_row(r, i),
                            ),
                            class_name="bg-white",
                        ),
                        class_name="min-w-full",
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 overflow-hidden",
            ),
            class_name="w-full",
        )
    )