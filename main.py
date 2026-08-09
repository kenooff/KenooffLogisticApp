import flet as ft
import sqlite3
import time
import os

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
    # Setup Database
    init_db()

    page.title = "Kenooff Logistics"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    time.sleep(0.5)

    header = ft.Text("Kenooff Logistics Form", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
    subheader = ft.Text("Log New Package Entry", size=14, color=ft.Colors.GREY_600)

    # Input Controls
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

    # Helper function to open snackbars reliably
    def show_alert(message: str, bg_color):
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=bg_color,
            open=True
        )
        page.overlay.append(snack)
        page.update()

    # REAL SUBMIT & SAVE HANDLER
    def handle_submit(e):
        # 1. Validation check
        if not vendor_input.value or not package_input.value:
            show_alert("Please fill in Vendor Name and Package Description!", ft.Colors.RED_600)
            return

        try:
            qty = float(qty_input.value) if qty_input.value else 0.0
            price = float(price_input.value) if price_input.value else 0.0
            del_charge = float(delivery_charge.value) if delivery_charge.value else 0.0
            total_val = qty * price

            # 2. Save into SQLite Database
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

            # 3. Clear inputs after saving
            vendor_input.value = ""
            package_input.value = ""
            qty_input.value = "1"
            price_input.value = "0"
            location_input.value = ""
            rider_input.value = ""
            delivery_charge.value = "0"
            total_badge.value = "Total Value: ₦0.00"

            show_alert("Package Log Saved to Database Successfully!", ft.Colors.GREEN_600)

        except Exception as ex:
            show_alert(f"Error saving entry: {str(ex)}", ft.Colors.RED_600)

    submit_btn = ft.ElevatedButton(
        content=ft.Text("Log & Save Package", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        on_click=handle_submit,
        height=50,
        expand=True,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_800)
    )

    # Main Scroll View
    master_layout = ft.Container(
        content=ft.ListView(
            spacing=14,
            controls=[
                header,
                subheader,
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
        ),
        padding=16,
        expand=True
    )

    page.clean()
    page.add(master_layout)
    page.update()

ft.app(target=main)