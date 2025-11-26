import reflex as rx
from app.components.layout import layout
from app.states.receipt_state import ReceiptState
from app.states.settings_state import SettingsState


def print_style() -> rx.Component:
    return rx.el.style("""
        @media print {
            body * {
                visibility: hidden;
            }
            #printable-area, #printable-area * {
                visibility: visible;
            }
            #printable-area {
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                margin: 0;
                padding: 20px;
                box-shadow: none;
                border: none;
            }
            nav, aside, header, .no-print {
                display: none !important;
            }
        }
        """)


def receipt_field(label: str, value: str, is_amount: bool = False) -> rx.Component:
    return rx.el.div(
        rx.el.span(f"{label}:", class_name="text-gray-500 font-medium mr-2"),
        rx.el.span(
            value,
            class_name=rx.cond(is_amount, "text-gray-900 font-bold", "text-gray-900"),
        ),
        class_name="flex justify-between py-2 border-b border-dashed border-gray-200 text-sm",
    )


def view_receipt_page() -> rx.Component:
    return layout(
        rx.el.div(
            print_style(),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                        "Back to List",
                        class_name="flex items-center text-gray-600 hover:text-gray-900 transition-colors",
                    ),
                    href="/receipts",
                    class_name="no-print",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("printer", class_name="h-5 w-5 mr-2"),
                        "Print Receipt",
                        on_click=rx.call_script("window.print()"),
                        class_name="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm",
                    ),
                    class_name="no-print",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.cond(
                ReceiptState.selected_receipt,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "graduation-cap", class_name="h-12 w-12 text-indigo-600"
                            ),
                            rx.el.div(
                                rx.el.h1(
                                    SettingsState.school_name,
                                    class_name="text-xl font-bold text-gray-900 text-center",
                                ),
                                rx.el.p(
                                    "Excellence in Education",
                                    class_name="text-xs text-gray-500 text-center mt-1",
                                ),
                                class_name="flex flex-col items-center mt-2",
                            ),
                            class_name="flex flex-col items-center mb-6 pb-6 border-b-2 border-gray-100",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "PAYMENT RECEIPT",
                                class_name="text-lg font-bold text-gray-900 mb-4 text-center tracking-wide",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "Date:", class_name="text-xs text-gray-500"
                                    ),
                                    rx.el.p(
                                        ReceiptState.selected_receipt.date.split("T")[
                                            0
                                        ],
                                        class_name="text-sm font-semibold text-gray-900",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Receipt No:",
                                        class_name="text-xs text-gray-500 text-right",
                                    ),
                                    rx.el.p(
                                        ReceiptState.selected_receipt.reference_id,
                                        class_name="text-sm font-semibold text-gray-900 text-right",
                                    ),
                                ),
                                class_name="flex justify-between mb-6",
                            ),
                            rx.el.div(
                                receipt_field(
                                    "Student Name",
                                    ReceiptState.selected_receipt.student_name,
                                ),
                                receipt_field(
                                    "Admission No",
                                    ReceiptState.selected_receipt.admission_number,
                                ),
                                receipt_field(
                                    "Class / Grade",
                                    ReceiptState.selected_receipt.class_grade,
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                receipt_field(
                                    "Received From",
                                    ReceiptState.selected_receipt.payer_name,
                                ),
                                receipt_field(
                                    "Payment Method",
                                    ReceiptState.selected_receipt.payment_method,
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "AMOUNT PAID",
                                        class_name="text-sm font-bold text-gray-500",
                                    ),
                                    rx.el.h3(
                                        f"${ReceiptState.selected_receipt.amount:,.2f}",
                                        class_name="text-3xl font-bold text-gray-900 mt-1",
                                    ),
                                    class_name="text-center py-4 bg-gray-50 rounded-lg mb-4",
                                ),
                                rx.el.p(
                                    f"Amount in words: {ReceiptState.selected_receipt_words}",
                                    class_name="text-xs text-gray-500 text-center italic",
                                ),
                                class_name="mb-8",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.image(
                                        src=ReceiptState.selected_receipt_qr,
                                        class_name="h-24 w-24 mx-auto",
                                    ),
                                    class_name="mb-4",
                                ),
                                rx.el.p(
                                    "Thank you for your payment!",
                                    class_name="text-sm font-semibold text-gray-900 text-center",
                                ),
                                rx.el.p(
                                    "This receipt is computer generated.",
                                    class_name="text-xs text-gray-400 text-center mt-1",
                                ),
                                class_name="border-t-2 border-gray-100 pt-6 flex flex-col items-center",
                            ),
                        ),
                        class_name="max-w-md mx-auto bg-white p-8 shadow-sm border border-gray-200 rounded-xl",
                        id="printable-area",
                    ),
                    class_name="flex justify-center w-full",
                ),
                rx.el.div(
                    rx.el.p("Receipt not found.", class_name="text-gray-500"),
                    class_name="text-center py-20",
                ),
            ),
            class_name="w-full pb-20",
        )
    )