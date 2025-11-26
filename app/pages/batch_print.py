import reflex as rx
from app.states.receipt_state import ReceiptState
from app.pages.view_receipt import print_style


def batch_print_item(receipt) -> rx.Component:
    from app.states.settings_state import SettingsState

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    SettingsState.school_name,
                    class_name="text-lg font-bold text-center",
                ),
                rx.el.p(
                    "RECEIPT",
                    class_name="text-sm font-bold text-center mb-4 border-b pb-2",
                ),
                class_name="mb-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Date:", class_name="font-semibold mr-2"),
                    rx.el.span(receipt.date.split("T")[0]),
                    class_name="text-xs",
                ),
                rx.el.div(
                    rx.el.span("Ref:", class_name="font-semibold mr-2"),
                    rx.el.span(receipt.reference_id),
                    class_name="text-xs",
                ),
                class_name="flex justify-between mb-2",
            ),
            rx.el.div(
                rx.el.p(f"Student: {receipt.student_name}", class_name="text-sm"),
                rx.el.p(f"Class: {receipt.class_grade}", class_name="text-sm"),
                rx.el.p(
                    f"Amount: ${receipt.amount:,.2f}",
                    class_name="text-sm font-bold mt-1",
                ),
                class_name="mb-4",
            ),
            class_name="border border-gray-300 p-4 rounded mb-8 break-inside-avoid page-break-inside-avoid",
        ),
        class_name="w-full",
    )


def batch_print_page() -> rx.Component:
    return rx.el.div(
        print_style(),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    "< Back",
                    on_click=rx.redirect("/receipts"),
                    class_name="mr-4 text-gray-600 hover:text-gray-900",
                ),
                rx.el.button(
                    "Print All",
                    on_click=rx.call_script("window.print()"),
                    class_name="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 shadow-sm",
                ),
                class_name="no-print p-4 flex items-center bg-gray-50 border-b",
            ),
            rx.el.div(
                rx.foreach(
                    ReceiptState.all_receipts,
                    lambda r: rx.cond(
                        ReceiptState.selected_receipt_ids.contains(r.reference_id),
                        batch_print_item(r),
                        rx.fragment(),
                    ),
                ),
                class_name="p-8 max-w-2xl mx-auto",
                id="printable-area",
            ),
        ),
    )