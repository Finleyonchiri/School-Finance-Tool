import reflex as rx
from app.components.layout import layout
from app.states.reports_state import ReportsState


def report_stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-600 mb-1"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.icon(icon, size=24, class_name=f"text-{color}-600"),
                class_name=f"p-3 bg-{color}-100 rounded-xl",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def reports_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Financial Reports", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Analyze fee collection trends and export data",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Start Date",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ReportsState.set_start_date,
                        class_name="w-full rounded-lg border-gray-300 border p-2",
                        default_value=ReportsState.start_date,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "End Date",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ReportsState.set_end_date,
                        class_name="w-full rounded-lg border-gray-300 border p-2",
                        default_value=ReportsState.end_date,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Class Filter",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("All Classes", value=""),
                        rx.el.option("PLAY GROUP", value="PLAY GROUP"),
                        rx.el.option("PP1", value="PP1"),
                        rx.el.option("PP2", value="PP2"),
                        rx.el.option("GRADE 1", value="GRADE 1"),
                        rx.el.option("GRADE 2", value="GRADE 2"),
                        rx.el.option("GRADE 3", value="GRADE 3"),
                        rx.el.option("GRADE 4", value="GRADE 4"),
                        rx.el.option("GRADE 5", value="GRADE 5"),
                        rx.el.option("GRADE 6", value="GRADE 6"),
                        rx.el.option("GRADE 7", value="GRADE 7"),
                        rx.el.option("GRADE 8", value="GRADE 8"),
                        rx.el.option("GRADE 9", value="GRADE 9"),
                        value=ReportsState.selected_class,
                        on_change=ReportsState.set_selected_class,
                        class_name="w-full rounded-lg border-gray-300 border p-2 bg-white",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Actions",
                        class_name="block text-sm font-medium text-gray-700 mb-1 opacity-0",
                    ),
                    rx.el.button(
                        rx.icon("download", class_name="h-4 w-4 mr-2"),
                        "Export CSV",
                        on_click=ReportsState.download_csv,
                        class_name="flex items-center justify-center w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex-1",
                ),
                class_name="grid grid-cols-1 md:grid-cols-4 gap-4 bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8",
            ),
            rx.el.div(
                report_stat_card(
                    "Revenue (Period)",
                    rx.cond(
                        ReportsState.total_collected_period,
                        f"${ReportsState.total_collected_period:,.2f}",
                        "$0.00",
                    ),
                    "dollar-sign",
                    "green",
                ),
                report_stat_card(
                    "Transactions",
                    ReportsState.total_transactions_period.to_string(),
                    "receipt",
                    "blue",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Income Over Time",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.recharts.area_chart(
                        rx.recharts.cartesian_grid(
                            horizontal=True, vertical=False, class_name="opacity-25"
                        ),
                        rx.recharts.graphing_tooltip(),
                        rx.recharts.area(
                            data_key="amount",
                            stroke="#4f46e5",
                            fill="#4f46e5",
                            fill_opacity=0.1,
                        ),
                        rx.recharts.x_axis(
                            data_key="date",
                            tick_line=False,
                            axis_line=False,
                            tick_size=10,
                            custom_attrs={"fontSize": "12px"},
                        ),
                        rx.recharts.y_axis(
                            tick_line=False,
                            axis_line=False,
                            tick_size=10,
                            custom_attrs={"fontSize": "12px"},
                        ),
                        data=ReportsState.income_over_time,
                        width="100%",
                        height=350,
                        margin={"left": -10, "right": 10, "top": 10, "bottom": 0},
                    ),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                ),
                class_name="w-full mb-8",
            ),
            class_name="w-full pb-20",
        )
    )