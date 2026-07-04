import flet as ft

def main(page: ft.Page):
    page.title = "Kenooff Logistics"
    page.padding = 16

    # 1. Main Form Titles
    header = ft.Text("Kenooff Logistics Form", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800)
    subheader = ft.Text("Log New Package Entry", size=14, color=ft.colors.GREY_600)

    # 2. Form Input Fields
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

    # 3. Calculation Display Banner
    total_badge = ft.Text("Total Value: ₦0.00", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700)

    # 4. Calculation Logic
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
        icon=ft.icons.CALCULATE,
        on_click=run_calculation,
        style=ft.ButtonStyle(color=ft.colors.GREEN_700)
    )

    # 5. Save/Submit Action
    def handle_submit(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Package Saved Successfully!", color=ft.colors.WHITE), 
            bgcolor=ft.colors.GREEN_600
        )
        page.snack_bar.open = True
        page.update()

    submit_btn = ft.ElevatedButton(
        text="Log & Save Package",
        on_click=handle_submit,
        height=50,
        style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_800, color=ft.colors.WHITE)
    )

    # 6. Mobile Layout Context
    app_layout = ft.ListView(
        expand=True,
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
    )

    page.add(app_layout)

ft.app(target=main)