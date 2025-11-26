import reflex as rx


def delete_confirmation_modal(
    is_open: bool,
    on_confirm: rx.event.EventType,
    on_cancel: rx.event.EventType,
    title: str = "Confirm Delete",
    message: str = "Are you sure you want to delete this item? This action cannot be undone.",
) -> rx.Component:
    return rx.cond(
        is_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 z-50 transition-opacity",
                on_click=on_cancel,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "flag_triangle_right", class_name="text-red-600 h-6 w-6"
                        ),
                        class_name="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            title,
                            class_name="text-base font-semibold leading-6 text-gray-900",
                        ),
                        rx.el.div(
                            rx.el.p(message, class_name="text-sm text-gray-500"),
                            class_name="mt-2",
                        ),
                        class_name="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left",
                    ),
                    class_name="sm:flex sm:items-start",
                ),
                rx.el.div(
                    rx.el.button(
                        "Delete",
                        on_click=on_confirm,
                        class_name="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto",
                    ),
                    rx.el.button(
                        "Cancel",
                        on_click=on_cancel,
                        class_name="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto",
                    ),
                    class_name="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse",
                ),
                class_name="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6 z-50",
            ),
            class_name="fixed inset-0 z-50 flex items-end justify-center p-4 text-center sm:items-center sm:p-0",
        ),
    )