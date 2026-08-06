import flet as ft
import time

def main(page: ft.Page):
    # 1. Base engine configurations
    page.title = "Kenooff Logistics"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # 2. Prevent mobile startup race condition 
    time.sleep(0.5)

    # 3. Create Form Elements (Updated to capitalized ft.Colors and ft.Icons)
    header = ft.Text("Kenooff Logistics Form", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
    subheader = ft.Text("Log New Package Entry", size=14, color=ft.Colors.GREY_600)

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

    def run_calculation(e):
        try:
            qty = float(qty_input.value) if qty_input.value else 0
            price = float(price_input.value) if price_input.value else 0
            total = qty * price
            total_badge.value = f"Total Value: ₦{total:,.2f}"
        except Exception:
            total_badge.value = "Total Value: ₦0.00"
        page.update()

    calc_btn = ft.ElevatedButton(
        text="Calculate Total Value",
        icon=ft.Icons.CALCULATE,
        on_click=run_calculation,
        style=ft.ButtonStyle(color=ft.Colors.GREEN_700)
    )

    def handle_submit(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Package Saved Successfully!", color=ft.Colors.WHITE), 
            bgcolor=ft.Colors.GREEN_600
        )
        page.snack_bar.open = True
        page.update()

    submit_btn = ft.ElevatedButton(
        text="Log & Save Package",
        on_click=handle_submit,
        height=50,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_800, color=ft.Colors.WHITE)
    )

    # 4. Wrap everything inside a single master scrollable view box
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
                ft.Row([ft.Expanded(child=submit_btn)])
            ]
        ),
        padding=16,
        expand=True
    )

    page.clean()
    page.add(master_layout)
    page.update()

ft.app(target=main)

