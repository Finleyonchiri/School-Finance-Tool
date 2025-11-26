import reflex as rx
from app.states.settings_state import SettingsState


def sidebar_item(text: str, icon_name: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon_name,
                size=20,
                class_name="text-gray-500 group-hover:text-indigo-600 transition-colors",
            ),
            rx.el.span(
                text, class_name="font-medium text-gray-700 group-hover:text-gray-900"
            ),
            class_name="flex items-center gap-3",
        ),
        href=href,
        class_name="flex items-center px-4 py-3 rounded-xl hover:bg-indigo-50 transition-all duration-200 group w-full",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("graduation-cap", size=32, class_name="text-indigo-600"),
                    class_name="bg-indigo-100 p-2 rounded-xl",
                ),
                rx.el.div(
                    rx.el.h1(
                        "TOYA",
                        class_name="text-xl font-bold text-gray-900 leading-none",
                    ),
                    rx.el.p(
                        "Finance Manager",
                        class_name="text-xs text-gray-500 font-medium",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3 px-4 py-6 border-b border-gray-100",
            ),
            rx.el.nav(
                sidebar_item("Dashboard", "layout-dashboard", "/"),
                sidebar_item("Receipts", "receipt", "/receipts"),
                sidebar_item("New Receipt", "circle_plus", "/receipts/new"),
                sidebar_item("Reports", "bar-chart-3", "/reports"),
                sidebar_item("Students", "users", "#"),
                class_name="flex flex-col gap-1 p-4 flex-1",
            ),
            rx.el.div(
                sidebar_item("Settings", "settings", "/settings"),
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=SettingsState.school_logo,
                            class_name="w-10 h-10 rounded-full bg-gray-200",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Admin User",
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.p("Bursar", class_name="text-xs text-gray-500"),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="p-4 border-t border-gray-100",
                ),
                class_name="flex flex-col gap-1",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.cond(
            SettingsState.sidebar_open,
            "w-64 bg-white border-r border-gray-200 h-screen fixed left-0 top-0 transition-all duration-300 z-30 hidden md:block",
            "w-0 overflow-hidden h-screen fixed left-0 top-0 transition-all duration-300 z-30 md:block",
        ),
    )


def mobile_sidebar() -> rx.Component:
    """Sidebar for mobile devices."""
    return rx.el.div(
        rx.el.div(
            class_name="fixed inset-0 bg-black/50 z-40",
            on_click=SettingsState.toggle_sidebar,
            display=rx.cond(SettingsState.sidebar_open, "block", "none"),
        ),
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "graduation-cap", size=32, class_name="text-indigo-600"
                        ),
                        class_name="bg-indigo-100 p-2 rounded-xl",
                    ),
                    rx.el.h1("TOYA", class_name="text-xl font-bold text-gray-900"),
                    class_name="flex items-center gap-3 px-4 py-6 border-b border-gray-100",
                ),
                rx.el.nav(
                    sidebar_item("Dashboard", "layout-dashboard", "/"),
                    sidebar_item("Receipts", "receipt", "/receipts"),
                    sidebar_item("New Receipt", "circle_plus", "/receipts/new"),
                    sidebar_item("Reports", "bar-chart-3", "/reports"),
                    sidebar_item("Students", "users", "#"),
                    class_name="flex flex-col gap-1 p-4 flex-1",
                ),
                rx.el.div(
                    sidebar_item("Settings", "settings", "/settings"),
                    class_name="flex flex-col gap-1 pb-4",
                ),
                class_name="flex flex-col h-full bg-white",
            ),
            class_name=rx.cond(
                SettingsState.sidebar_open,
                "fixed inset-y-0 left-0 w-64 bg-white z-50 transition-transform duration-300 ease-in-out transform translate-x-0 md:hidden",
                "fixed inset-y-0 left-0 w-64 bg-white z-50 transition-transform duration-300 ease-in-out transform -translate-x-full md:hidden",
            ),
        ),
        class_name="md:hidden",
    )