import reflex as rx
from app.pages.dashboard import index
from app.pages.new_receipt import new_receipt_page
from app.pages.receipts_list import receipts_list_page
from app.pages.view_receipt import view_receipt_page
from app.pages.reports import reports_page
from app.pages.settings import settings_page
from app.pages.batch_print import batch_print_page
from app.states.receipt_state import ReceiptState
from app.states.settings_state import SettingsState

app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="indigo"
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
    ],
    head_components=[
        rx.el.link(rel="manifest", href="/manifest.json"),
        rx.el.meta(name="theme-color", content="#4f46e5"),
        rx.el.meta(name="application-name", content="TOYA"),
        rx.el.meta(name="apple-mobile-web-app-capable", content="yes"),
        rx.el.meta(name="apple-mobile-web-app-status-bar-style", content="default"),
        rx.el.meta(name="apple-mobile-web-app-title", content="TOYA"),
        rx.el.meta(name="format-detection", content="telephone=no"),
        rx.el.meta(name="mobile-web-app-capable", content="yes"),
        rx.script("""
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                    navigator.serviceWorker.register('/sw.js').then(function(registration) {
                        console.log('ServiceWorker registration successful with scope: ', registration.scope);
                    }, function(err) {
                        console.log('ServiceWorker registration failed: ', err);
                    });
                });
            }
            """),
    ],
)
app.add_page(index, route="/", on_load=[ReceiptState.on_mount, SettingsState.on_mount])
app.add_page(new_receipt_page, route="/receipts/new", on_load=SettingsState.on_mount)
app.add_page(
    receipts_list_page,
    route="/receipts",
    on_load=[ReceiptState.on_mount, SettingsState.on_mount],
)
app.add_page(
    view_receipt_page,
    route="/receipts/view/[ref_id]",
    on_load=[ReceiptState.load_view_receipt, SettingsState.on_mount],
)
app.add_page(reports_page, route="/reports", on_load=SettingsState.on_mount)
app.add_page(settings_page, route="/settings", on_load=SettingsState.on_mount)
app.add_page(
    batch_print_page, route="/receipts/batch-print", on_load=SettingsState.on_mount
)