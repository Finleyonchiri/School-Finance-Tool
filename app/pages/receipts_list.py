import reflex as rx
from app.components.layout import layout
from app.states.receipt_state import ReceiptState
from app.components.fab import floating_action_button
from app.components.modals import delete_confirmation_modal


def filter_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="Search student, adm no, or ref...",
                on_change=ReceiptState.set_search_query.debounce(300),
                class_name="w-full md:w-80 rounded-xl border-gray-300 border p-2.5 pl-10 focus:ring-indigo-500 focus:border-indigo-500",
                default_value=ReceiptState.search_query,
            ),
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option("All Classes", value=""),
                rx.el.option("Grade 8", value="Grade 8"),
                rx.el.option("Grade 9", value="Grade 9"),
                rx.el.option("Grade 10", value="Grade 10"),
                rx.el.option("Grade 11", value="Grade 11"),
                rx.el.option("Grade 12", value="Grade 12"),
                value=ReceiptState.filter_class,
                on_change=ReceiptState.load_receipts,
                class_name="rounded-xl border-gray-300 border p-2.5 bg-white focus:ring-indigo-500 focus:border-indigo-500",
            ),
            class_name="flex gap-4",
        ),
        class_name="flex flex-col md:flex-row gap-4 justify-between mb-6",
    )


def receipt_row(receipt) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.input(
                type="checkbox",
                checked=ReceiptState.selected_receipt_ids.contains(
                    receipt.reference_id
                ),
                on_change=lambda v: ReceiptState.toggle_selection(receipt.reference_id),
                class_name="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                receipt.date.split("T")[0],
                class_name="text-sm font-medium text-gray-900",
            ),
            rx.el.div(receipt.reference_id, class_name="text-xs text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                receipt.student_name, class_name="text-sm font-medium text-gray-900"
            ),
            rx.el.div(receipt.admission_number, class_name="text-xs text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                receipt.class_grade,
                class_name="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            f"${receipt.amount:,.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-semibold text-indigo-600",
        ),
        rx.el.td(
            receipt.payment_method,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.icon(
                        "eye",
                        class_name="h-5 w-5 text-gray-400 hover:text-indigo-600 transition-colors",
                    ),
                    href=f"/receipts/view/{receipt.reference_id}",
                    class_name="p-1",
                    title="View Receipt",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2",
                        class_name="h-5 w-5 text-gray-400 hover:text-red-600 transition-colors",
                    ),
                    on_click=lambda: ReceiptState.confirm_delete(receipt.reference_id),
                    class_name="p-1",
                    title="Delete Receipt",
                ),
                class_name="flex gap-3 justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            f"Showing page {ReceiptState.page} of {ReceiptState.total_pages}",
            class_name="text-sm text-gray-700",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", class_name="h-5 w-5"),
                on_click=ReceiptState.prev_page,
                disabled=ReceiptState.page <= 1,
                class_name="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
            ),
            rx.el.button(
                rx.icon("chevron-right", class_name="h-5 w-5"),
                on_click=ReceiptState.next_page,
                disabled=ReceiptState.page >= ReceiptState.total_pages,
                class_name="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
            ),
            class_name="flex gap-2",
        ),
        class_name="flex items-center justify-between mt-6 pt-4 border-t border-gray-100",
    )


def receipts_list_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Receipts", class_name="text-2xl font-bold text-gray-900"),
                    rx.el.p(
                        "Manage and track fee payments", class_name="text-gray-500 mt-1"
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.cond(
                        ReceiptState.selected_receipt_ids.length() > 0,
                        rx.el.a(
                            rx.el.button(
                                rx.icon("printer", class_name="h-5 w-5 mr-2"),
                                f"Print Selected ({ReceiptState.selected_receipt_ids.length()})",
                                class_name="inline-flex items-center px-4 py-2 bg-gray-800 text-white rounded-xl font-medium hover:bg-gray-900 shadow-sm hover:shadow transition-all mr-4",
                            ),
                            href="/receipts/batch-print",
                        ),
                    ),
                    rx.el.a(
                        rx.el.button(
                            rx.icon("plus", class_name="h-5 w-5 mr-2"),
                            "New Receipt",
                            class_name="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 shadow-sm hover:shadow transition-all",
                        ),
                        href="/receipts/new",
                        class_name="hidden md:block",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            filter_controls(),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    rx.el.input(
                                        type="checkbox",
                                        on_change=lambda v: ReceiptState.select_all_current(),
                                        class_name="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500",
                                    ),
                                    class_name="px-6 py-3 text-left",
                                ),
                                rx.el.th(
                                    "Date / Ref",
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
                                    "Method",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                            ),
                            class_name="bg-gray-50/50",
                        ),
                        rx.el.tbody(
                            rx.foreach(ReceiptState.current_receipts, receipt_row),
                            class_name="bg-white",
                        ),
                        class_name="min-w-full",
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
            ),
            pagination_controls(),
            floating_action_button(),
            delete_confirmation_modal(
                is_open=ReceiptState.is_delete_modal_open,
                on_confirm=ReceiptState.delete_receipt,
                on_cancel=ReceiptState.cancel_delete,
            ),
            class_name="w-full pb-20",
        )
    )