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


def info_row(label: str, value: rx.Component | str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            label,
            class_name="text-xs text-gray-500 uppercase tracking-wider font-medium",
        ),
        rx.el.span(
            value, class_name="text-sm font-semibold text-gray-900 mt-0.5 block"
        ),
        class_name="mb-3",
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
                            rx.el.div(
                                rx.icon(
                                    "graduation-cap",
                                    class_name="h-10 w-10 text-indigo-600",
                                ),
                                rx.el.div(
                                    rx.el.h1(
                                        SettingsState.school_name,
                                        class_name="text-xl font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        SettingsState.school_motto,
                                        class_name="text-xs text-gray-500 font-medium",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    SettingsState.school_address,
                                    class_name="text-xs text-gray-600 text-right",
                                ),
                                rx.el.p(
                                    SettingsState.school_phone,
                                    class_name="text-xs text-gray-600 text-right",
                                ),
                                rx.el.p(
                                    SettingsState.school_email,
                                    class_name="text-xs text-gray-600 text-right",
                                ),
                                class_name="flex flex-col justify-center",
                            ),
                            class_name="flex justify-between items-start border-b border-gray-200 pb-6 mb-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "OFFICIAL RECEIPT",
                                class_name="text-lg font-black text-gray-900 tracking-wider text-center mb-6 uppercase",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Receipt No:",
                                        class_name="text-xs text-gray-500 mr-2",
                                    ),
                                    rx.el.span(
                                        ReceiptState.selected_receipt.reference_id,
                                        class_name="text-sm font-mono font-bold text-gray-900",
                                    ),
                                    class_name="flex items-center bg-gray-50 px-3 py-1.5 rounded-md",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Date:", class_name="text-xs text-gray-500 mr-2"
                                    ),
                                    rx.el.span(
                                        rx.moment(
                                            ReceiptState.selected_receipt.date,
                                            format="MMMM DD, YYYY • HH:mm A",
                                        ),
                                        class_name="text-sm font-bold text-gray-900",
                                    ),
                                    class_name="flex items-center bg-gray-50 px-3 py-1.5 rounded-md",
                                ),
                                class_name="flex justify-between mb-8",
                            ),
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Student Information",
                                    class_name="text-xs font-bold text-indigo-600 uppercase mb-4 border-b border-gray-100 pb-2",
                                ),
                                info_row(
                                    "Student Name",
                                    ReceiptState.selected_receipt.student_name,
                                ),
                                info_row(
                                    "Admission No",
                                    ReceiptState.selected_receipt.admission_number,
                                ),
                                info_row(
                                    "Class / Grade",
                                    ReceiptState.selected_receipt.class_grade,
                                ),
                                class_name="flex flex-col pr-4 border-r border-gray-100",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "Payment Details",
                                    class_name="text-xs font-bold text-indigo-600 uppercase mb-4 border-b border-gray-100 pb-2",
                                ),
                                info_row(
                                    "Payer Name",
                                    ReceiptState.selected_receipt.payer_name,
                                ),
                                info_row(
                                    "Payment Method",
                                    ReceiptState.selected_receipt.payment_method,
                                ),
                                info_row("Received By", "Admin User"),
                                class_name="flex flex-col pl-4",
                            ),
                            class_name="grid grid-cols-2 mb-8",
                        ),
                        rx.cond(
                            ReceiptState.selected_receipt.notes != "",
                            rx.el.div(
                                rx.el.h3(
                                    "Notes",
                                    class_name="text-xs font-bold text-gray-500 uppercase mb-2",
                                ),
                                rx.el.p(
                                    ReceiptState.selected_receipt.notes,
                                    class_name="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg border border-gray-100",
                                ),
                                class_name="mb-8",
                            ),
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "TOTAL AMOUNT",
                                        class_name="text-xs font-bold text-white/80 tracking-wider",
                                    ),
                                    rx.el.h3(
                                        f"${ReceiptState.selected_receipt.amount:,.2f}",
                                        class_name="text-3xl font-bold text-white mt-1",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                rx.el.div(
                                    rx.image(
                                        src=ReceiptState.selected_receipt_qr,
                                        class_name="h-16 w-16 bg-white p-1 rounded-lg",
                                    )
                                ),
                                class_name="flex justify-between items-center bg-gray-900 p-6 rounded-xl shadow-sm mb-4",
                            ),
                            rx.el.p(
                                f"** {ReceiptState.selected_receipt_words} **",
                                class_name="text-xs text-gray-500 text-center italic uppercase tracking-wide font-medium",
                            ),
                            class_name="mb-10",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    class_name="border-t border-gray-300 w-48 h-0 mb-2"
                                ),
                                rx.el.p(
                                    "Authorized Signature",
                                    class_name="text-xs text-gray-500 uppercase font-medium",
                                ),
                                class_name="flex flex-col items-center",
                            ),
                            class_name="flex justify-end mb-8",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Thank you for your business!",
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                "Please retain this receipt for your records.",
                                class_name="text-xs text-gray-500 mt-1",
                            ),
                            class_name="text-center border-t border-gray-100 pt-6",
                        ),
                        class_name="max-w-2xl mx-auto bg-white p-8 md:p-12 shadow-lg border border-gray-200 rounded-xl",
                        id="printable-area",
                    ),
                    class_name="flex justify-center w-full px-4 md:px-0",
                ),
                rx.el.div(
                    rx.el.p("Receipt not found.", class_name="text-gray-500"),
                    class_name="text-center py-20",
                ),
            ),
            class_name="w-full pb-20",
        )
    )