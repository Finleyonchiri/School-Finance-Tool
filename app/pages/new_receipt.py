import reflex as rx
from app.components.layout import layout
from app.states.receipt_state import ReceiptState


def form_field(
    label: str, input_component: rx.Component, required: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            rx.cond(required, rx.el.span(" *", class_name="text-red-500"), ""),
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        input_component,
        class_name="col-span-1",
    )


def new_receipt_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("New Receipt", class_name="text-2xl font-bold text-gray-900"),
                rx.el.p("Record a new fee payment", class_name="text-gray-500 mt-1"),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Student Details",
                        class_name="text-lg font-semibold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        form_field(
                            "Admission Number",
                            rx.el.input(
                                placeholder="e.g. ADM001",
                                on_change=ReceiptState.set_new_admission_number,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                default_value=ReceiptState.new_admission_number,
                            ),
                            required=True,
                        ),
                        form_field(
                            "Student Name",
                            rx.el.input(
                                placeholder="Full Name",
                                on_change=ReceiptState.set_new_student_name,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                default_value=ReceiptState.new_student_name,
                            ),
                            required=True,
                        ),
                        form_field(
                            "Class/Grade",
                            rx.el.select(
                                rx.el.option("Select Class", value=""),
                                rx.el.option("Grade 8", value="Grade 8"),
                                rx.el.option("Grade 9", value="Grade 9"),
                                rx.el.option("Grade 10", value="Grade 10"),
                                rx.el.option("Grade 11", value="Grade 11"),
                                rx.el.option("Grade 12", value="Grade 12"),
                                value=ReceiptState.new_class_grade,
                                on_change=ReceiptState.set_new_class_grade,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500 bg-white",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6",
                    ),
                    rx.el.h2(
                        "Payment Details",
                        class_name="text-lg font-semibold text-gray-900 mb-4 pt-4 border-t border-gray-100",
                    ),
                    rx.el.div(
                        form_field(
                            "Amount Paid",
                            rx.el.input(
                                type="number",
                                placeholder="0.00",
                                on_change=ReceiptState.set_new_amount,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                default_value=ReceiptState.new_amount,
                            ),
                            required=True,
                        ),
                        form_field(
                            "Payment Method",
                            rx.el.select(
                                rx.el.option("Cash", value="Cash"),
                                rx.el.option("Bank Transfer", value="Bank Transfer"),
                                rx.el.option("Mobile Money", value="Mobile Money"),
                                rx.el.option("Check", value="Check"),
                                value=ReceiptState.new_payment_method,
                                on_change=ReceiptState.set_new_payment_method,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500 bg-white",
                            ),
                            required=True,
                        ),
                        form_field(
                            "Transaction/Reference ID",
                            rx.el.div(
                                rx.el.input(
                                    placeholder="Auto-generated or enter ID",
                                    on_change=ReceiptState.set_new_reference_id,
                                    class_name="w-full rounded-l-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                    default_value=ReceiptState.new_reference_id,
                                ),
                                rx.el.button(
                                    "Generate",
                                    type="button",
                                    on_click=ReceiptState.generate_reference,
                                    class_name="px-4 py-2 bg-gray-100 border border-l-0 border-gray-300 rounded-r-lg text-gray-600 hover:bg-gray-200 text-sm font-medium",
                                ),
                                class_name="flex",
                            ),
                        ),
                        form_field(
                            "Date",
                            rx.el.input(
                                type="date",
                                on_change=ReceiptState.set_new_date,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                default_value=ReceiptState.new_date,
                            ),
                            required=True,
                        ),
                        form_field(
                            "Payer Name",
                            rx.el.input(
                                placeholder="Parent/Guardian Name",
                                on_change=ReceiptState.set_new_payer_name,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                default_value=ReceiptState.new_payer_name,
                            ),
                        ),
                        form_field(
                            "Notes",
                            rx.el.textarea(
                                placeholder="Optional notes...",
                                on_change=ReceiptState.set_new_notes,
                                rows=1,
                                class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
                                default_value=ReceiptState.new_notes,
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                ),
                rx.el.div(
                    rx.el.button(
                        "Clear Form",
                        type="button",
                        on_click=ReceiptState.clear_form,
                        class_name="px-6 py-3 border border-gray-300 rounded-xl text-gray-700 font-medium hover:bg-gray-50 transition-colors",
                    ),
                    rx.el.button(
                        "Save Receipt",
                        type="button",
                        on_click=ReceiptState.save_receipt,
                        class_name="px-6 py-3 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 shadow-sm hover:shadow transition-all",
                    ),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                class_name="max-w-5xl mx-auto",
            ),
        )
    )