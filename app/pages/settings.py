import reflex as rx
from app.components.layout import layout
from app.states.settings_state import SettingsState
from app.states.receipt_state import ReceiptState


def settings_section(title: str, content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            title,
            class_name="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-100",
        ),
        content,
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-6",
    )


def settings_input(
    label: str, value_prop, on_change_prop, type_="text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            on_change=on_change_prop,
            type=type_,
            class_name="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-indigo-500 focus:border-indigo-500",
            default_value=value_prop,
        ),
        class_name="mb-4",
    )


def pin_modal() -> rx.Component:
    return rx.cond(
        SettingsState.show_pin_modal,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 z-50",
                on_click=SettingsState.cancel_pin,
            ),
            rx.el.div(
                rx.el.h3(
                    "Enter Admin PIN", class_name="text-lg font-bold text-center mb-4"
                ),
                rx.el.input(
                    type="password",
                    on_change=SettingsState.set_pin_input,
                    placeholder="****",
                    class_name="w-full text-center text-2xl tracking-widest p-2 border rounded-lg mb-4",
                    max_length=4,
                    auto_focus=True,
                    default_value=SettingsState.input_pin,
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=SettingsState.cancel_pin,
                        class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                    ),
                    rx.el.button(
                        "Verify",
                        on_click=SettingsState.verify_pin,
                        class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700",
                    ),
                    class_name="flex justify-between",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl shadow-xl z-50 w-80",
            ),
        ),
    )


def settings_page() -> rx.Component:
    return layout(
        rx.el.div(
            pin_modal(),
            rx.el.div(
                rx.el.h1("Settings", class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(
                    "Manage school configuration and data",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            settings_section(
                "School Information",
                rx.el.div(
                    settings_input(
                        "School Name",
                        SettingsState.school_name,
                        lambda v: SettingsState.update_school_info("school_name", v),
                    ),
                    settings_input(
                        "Address",
                        SettingsState.school_address,
                        lambda v: SettingsState.update_school_info("school_address", v),
                    ),
                    settings_input(
                        "Phone",
                        SettingsState.school_phone,
                        lambda v: SettingsState.update_school_info("school_phone", v),
                    ),
                    settings_input(
                        "Email",
                        SettingsState.school_email,
                        lambda v: SettingsState.update_school_info("school_email", v),
                    ),
                    settings_input(
                        "Motto",
                        SettingsState.school_motto,
                        lambda v: SettingsState.update_school_info("school_motto", v),
                    ),
                    settings_input(
                        "Currency Symbol",
                        SettingsState.currency_symbol,
                        lambda v: SettingsState.update_school_info(
                            "currency_symbol", v
                        ),
                    ),
                    rx.el.button(
                        "Save Changes",
                        on_click=SettingsState.save_settings,
                        class_name="mt-2 px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors",
                    ),
                ),
            ),
            settings_section(
                "Data Management",
                rx.el.div(
                    rx.el.p(
                        "Backup your data regularly to prevent loss.",
                        class_name="text-sm text-gray-600 mb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("download", class_name="h-5 w-5 mr-2"),
                            "Backup Data (JSON)",
                            on_click=ReceiptState.export_backup,
                            class_name="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-gray-700 font-medium",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Restore feature coming soon",
                                class_name="text-xs text-gray-400 italic mt-2",
                            ),
                            class_name="flex flex-col items-center",
                        ),
                        class_name="flex gap-4 items-start",
                    ),
                ),
            ),
            settings_section(
                "Security",
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Cashier Mode", class_name="font-medium text-gray-900"
                            ),
                            rx.el.p(
                                "Restrict access to settings and deletions",
                                class_name="text-sm text-gray-500",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.button(
                            "Configure PIN",
                            on_click=SettingsState.prompt_pin,
                            class_name="text-sm font-medium text-indigo-600 hover:text-indigo-700",
                        ),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            rx.cond(
                                SettingsState.is_authenticated,
                                "Status: Authenticated (Admin)",
                                "Status: Restricted (Cashier)",
                            ),
                            class_name=rx.cond(
                                SettingsState.is_authenticated,
                                "text-sm font-bold text-green-600",
                                "text-sm font-bold text-orange-600",
                            ),
                        )
                    ),
                ),
            ),
            class_name="w-full max-w-4xl mx-auto pb-20",
        )
    )