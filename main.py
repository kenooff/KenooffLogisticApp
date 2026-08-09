import flet as ft
import sqlite3
import time

# 1. Initialize Local SQLite Database
def init_db():
    conn = sqlite3.connect("logistics.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            package_desc TEXT,
            quantity REAL,
            unit_price REAL,
            total_value REAL,
            location TEXT,
            rider TEXT,
            delivery_charge REAL,
            payment_method TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def main(page: ft.Page):
    init_db()

    page.title = "Kenooff Logistics"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    time.sleep(0.3)

    # Toast/Snackbar Alert Helper
    def show_alert(message: str, bg_color):
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=bg_color,
            open=True
        )
        page.overlay.append(snack)
        page.update()

    # ==================== FORM INPUT CONTROLS ====================
    vendor_input = ft.TextField(label="Vendor Name", border_radius=8)
    package_input = ft.TextField(label="Package Description", border_radius=8)
    qty_input = ft.TextField(label="Quantity", value="1", keyboard_type=ft.KeyboardType.NUMBER, border_radius=8)
    price_input = ft.TextField(label="Unit Price (₦)", value="0", keyboard_type=ft.KeyboardType.NUMBER, border_radius=8)
    
    location_input = ft.TextField(label="Delivery Location", border_radius=8)
    rider_input = ft.TextField(label="Assigned Rider", border_radius=8)
    delivery_charge = ft.TextField(label="Delivery Charges (₦)", value="0", keyboard_type=ft.KeyboardType.NUMBER, border_radius=8)
    
    payment_method = ft.Dropdown(
        label="Payment Method",
        options=[ft.dropdown.Option("Cash"), ft.dropdown.Option("Bank Transfer"), ft.dropdown.Option("POS")],
        value="Cash",
        border_radius=8
    )
    
    initial_status = ft.Dropdown(
        label="Initial Status",
        options=[ft.dropdown.Option("Pending"), ft.dropdown.Option("In Transit"), ft.dropdown.Option("Delivered")],
        value="Pending",
        border_radius=8
    )

    total_badge = ft.Text("Total Value: ₦0.00", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)

    def run_calculation(e=None):
        try:
            qty = float(qty_input.value) if qty_input.value else 0
            price = float(price_input.value) if price_input.value else 0
            total = qty * price
            total_badge.value = f"Total Value: ₦{total:,.2f}"
            page.update()
            return total
        except Exception:
            total_badge.value = "Total Value: ₦0.00"
            page.update()
            return 0.0

    calc_btn = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.CALCULATE), ft.Text("Calculate Total Value")],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        on_click=run_calculation,
        style=ft.ButtonStyle(color=ft.Colors.GREEN_700)
    )

    def handle_submit(e):
        if not vendor_input.value or not package_input.value:
            show_alert("Please fill in Vendor Name and Package Description!", ft.Colors.RED_600)
            return

        try:
            qty = float(qty_input.value) if qty_input.value else 0.0
            price = float(price_input.value) if price_input.value else 0.0
            del_charge = float(delivery_charge.value) if delivery_charge.value else 0.0
            total_val = qty * price

            conn = sqlite3.connect("logistics.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO packages (
                    vendor, package_desc, quantity, unit_price, total_value, 
                    location, rider, delivery_charge, payment_method, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vendor_input.value,
                package_input.value,
                qty,
                price,
                total_val,
                location_input.value,
                rider_input.value,
                del_charge,
                payment_method.value,
                initial_status.value
            ))
            conn.commit()
            conn.close()

            # Clear inputs
            vendor_input.value = ""
            package_input.value = ""
            qty_input.value = "1"
            price_input.value = "0"
            location_input.value = ""
            rider_input.value = ""
            delivery_charge.value = "0"
            total_badge.value = "Total Value: ₦0.00"

            show_alert("Package Log Saved to Database Successfully!", ft.Colors.GREEN_600)
            load_database_records()  # Refresh history view

        except Exception as ex:
            show_alert(f"Error saving entry: {str(ex)}", ft.Colors.RED_600)

    submit_btn = ft.ElevatedButton(
        content=ft.Text("Log & Save Package", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        on_click=handle_submit,
        height=50,
        expand=True,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_800)
    )

    # Form Layout View
    form_view = ft.ListView(
        spacing=14,
        controls=[
            ft.Text("Kenooff Logistics Form", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Text("Log New Package Entry", size=14, color=ft.Colors.GREY_600),
            ft.Divider(height=10),
            vendor_input,
            package_input,
            qty_input,
            price_input,
            ft.Container(height=5),
            total_badge,
            calc_btn,                  
            ft.Divider(height=10),
            location_input,
            rider_input,
            delivery_charge,
            payment_method,
            initial_status,
            ft.Container(height=10),
            ft.Row([submit_btn])
        ]
    )

    # ==================== DATA HISTORY VIEW ====================
    history_list = ft.ListView(spacing=10, expand=True)

    def delete_record(record_id):
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM packages WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        show_alert("Record deleted!", ft.Colors.GREY_700)
        load_database_records()

    def load_database_records():
        history_list.controls.clear()
        conn = sqlite3.connect("logistics.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, vendor, package_desc, total_value, location, rider, status, created_at FROM packages ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            history_list.controls.append(
                ft.Container(
                    content=ft.Text("No saved packages found in database.", italic=True, color=ft.Colors.GREY_500),
                    alignment=ft.Alignment.CENTER,
                    padding=20
                )
            )
        else:
            for row in rows:
                pkg_id, vendor, desc, total, loc, rider, status, created = row
                
                status_color = ft.Colors.ORANGE_700
                if status == "Delivered":
                    status_color = ft.Colors.GREEN_700
                elif status == "In Transit":
                    status_color = ft.Colors.BLUE_700

                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"{vendor}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Container(
                                    content=ft.Text(f" {status} ", color=ft.Colors.WHITE, size=12),
                                    bgcolor=status_color,
                                    border_radius=4,
                                    padding=4
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Item: {desc}", size=14),
                            ft.Text(f"Location: {loc or 'N/A'} | Rider: {rider or 'N/A'}", size=12, color=ft.Colors.GREY_700),
                            ft.Row([
                                ft.Text(f"₦{total:,.2f}", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINED, 
                                    icon_color=ft.Colors.RED_400,
                                    on_click=lambda e, r_id=pkg_id: delete_record(r_id)
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ])
                    )
                )
                history_list.controls.append(card)
        page.update()

    load_database_records()

    # Screen View Container
    body = ft.Container(content=form_view, padding=12, expand=True)

    # Bottom Navigation Handler
    def on_nav_change(e):
        idx = int(e.control.selected_index)
        if idx == 0:
            body.content = form_view
        else:
            load_database_records()
            body.content = history_list
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.ADD_BOX, label="New Log"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="View History"),
        ],
        on_change=on_nav_change
    )

    page.clean()
    page.add(body)
    page.update()

ft.app(target=main)