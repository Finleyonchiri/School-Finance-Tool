import reflex as rx
from app.states.receipt_state import ReceiptState


def monthly_income_chart() -> rx.Component:
    return rx.recharts.line_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-25"
        ),
        rx.recharts.graphing_tooltip(
            separator="",
            content_style={
                "backgroundColor": "white",
                "borderRadius": "8px",
                "border": "1px solid #e5e7eb",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                "padding": "8px 12px",
            },
            item_style={"color": "#374151", "fontSize": "14px", "fontWeight": "500"},
        ),
        rx.recharts.line(
            data_key="amount",
            stroke="#4f46e5",
            stroke_width=2,
            type_="monotone",
            dot=True,
        ),
        rx.recharts.x_axis(
            data_key="month",
            tick_line=False,
            axis_line=False,
            tick_size=10,
            interval="preserveStartEnd",
            custom_attrs={"fontSize": "12px"},
        ),
        rx.recharts.y_axis(
            tick_line=False,
            axis_line=False,
            tick_size=10,
            custom_attrs={"fontSize": "12px"},
        ),
        data=ReceiptState.monthly_stats,
        width="100%",
        height=300,
        margin={"left": -20, "right": 10, "top": 10, "bottom": 0},
    )


def class_distribution_chart() -> rx.Component:
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-25"
        ),
        rx.recharts.graphing_tooltip(
            cursor=False,
            separator="",
            content_style={
                "backgroundColor": "white",
                "borderRadius": "8px",
                "border": "1px solid #e5e7eb",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                "padding": "8px 12px",
            },
            item_style={"color": "#374151", "fontSize": "14px", "fontWeight": "500"},
        ),
        rx.recharts.bar(
            data_key="amount", fill="#0ea5e9", radius=[4, 4, 0, 0], bar_size=40
        ),
        rx.recharts.x_axis(
            data_key="name",
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
        data=ReceiptState.class_stats,
        width="100%",
        height=300,
        margin={"left": -20, "right": 10, "top": 10, "bottom": 0},
    )