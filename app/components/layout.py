import reflex as rx
from app.components.sidebar import sidebar, mobile_sidebar
from app.states.settings_state import SettingsState


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        mobile_sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.button(
                        rx.icon("menu", class_name="text-gray-600"),
                        on_click=SettingsState.toggle_sidebar,
                        class_name="p-2 rounded-lg hover:bg-gray-100 md:hidden",
                    ),
                    rx.el.div(class_name="hidden md:block w-4"),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon(
                            rx.cond(
                                SettingsState.current_theme == "light", "sun", "moon"
                            ),
                            size=20,
                        ),
                        on_click=rx.toggle_color_mode,
                        class_name="p-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("bell", size=20),
                        class_name="p-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors relative",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="h-16 px-4 md:px-8 border-b border-gray-200 bg-white/80 backdrop-blur-sm flex items-center justify-between sticky top-0 z-20",
            ),
            rx.el.div(content, class_name="p-4 md:p-8 max-w-7xl mx-auto"),
            class_name=rx.cond(
                SettingsState.sidebar_open,
                "flex-1 flex flex-col min-h-screen transition-all duration-300 md:ml-64",
                "flex-1 flex flex-col min-h-screen transition-all duration-300 ml-0",
            ),
        ),
        class_name="flex min-h-screen bg-gray-50 font-['Inter'] text-gray-900",
    )