import reflex as rx


def floating_action_button() -> rx.Component:
    return rx.el.a(
        rx.icon("plus", class_name="text-white h-6 w-6"),
        href="/receipts/new",
        class_name="fixed bottom-6 right-6 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full p-4 shadow-lg transition-transform hover:scale-105 md:hidden z-40 flex items-center justify-center",
        aria_label="Create New Receipt",
    )