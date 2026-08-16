import flet as ft
import json
import urllib.request
import urllib.parse
import time

# ==================== SUPABASE CONFIG ====================
SUPABASE_URL = "https://nkllvhzebktydnqvjuoc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rbGx2aHplYmt0eWRucXZqdW9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYyODQzNDMsImV4cCI6MjEwMTg2MDM0M30.zIPGzDv5krWPUaIJzTP2BnKhSxU5LjJ0DraR46zFFLI"  # Keep your real eyJ... key here!

# Direct HTTP Helper for Supabase REST API
def supabase_request(endpoint: str, method: str = "GET", data: dict = None):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    with urllib.request.urlopen(req) as response:
        res_data = response.read().decode("utf-8")
        return json.loads(res_data) if res_data else []

def main(page: ft.Page):
    page.title = "Kenooff Logistics"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    time.sleep(0.3)

    def show_alert(message: str, bg_color):
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=bg_color,
            open=True
        )
        page.overlay.append(snack)
        page.update()

    # ==================== FORM CONTROLS ====================
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

    submit_btn_content = ft.Row(
        [ft.Text("Log & Save Package", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    submit_btn = ft.ElevatedButton(
        content=submit_btn_content,
        height=50,
        expand=True,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_800)
    )

    def handle_submit(e):
        if not vendor_input.value or not package_input.value:
            show_alert("Please fill in Vendor Name and Package Description!", ft.Colors.RED_600)
            return

        submit_btn.disabled = True
        submit_btn_content.controls = [
            ft.ProgressRing(width=20, height=20, stroke_width=2, color=ft.Colors.WHITE),
            ft.Text(" Saving to Cloud...", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
        ]
        page.update()

        try:
            qty = float(qty_input.value) if qty_input.value else 0.0
            price = float(price_input.value) if price_input.value else 0.0
            del_charge = float(delivery_charge.value) if delivery_charge.value else 0.0
            total_val = qty * price

            data = {
                "vendor": vendor_input.value,
                "package_desc": package_input.value,
                "quantity": qty,
                "unit_price": price,
                "total_value": total_val,
                "location": location_input.value,
                "rider": rider_input.value,
                "delivery_charge": del_charge,
                "payment_method": payment_method.value,
                "status": initial_status.value
            }

            supabase_request("packages", method="POST", data=data)

            vendor_input.value = ""
            package_input.value = ""
            qty_input.value = "1"
            price_input.value = "0"
            location_input.value = ""
            rider_input.value = ""
            delivery_charge.value = "0"
            total_badge.value = "Total Value: ₦0.00"

            show_alert("Package Saved Online Successfully!", ft.Colors.GREEN_600)

        except Exception as ex:
            show_alert(f"Error saving to Cloud: {str(ex)}", ft.Colors.RED_600)

        finally:
            submit_btn.disabled = False
            submit_btn_content.controls = [
                ft.Text("Log & Save Package", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ]
            page.update()

    submit_btn.on_click = handle_submit

    form_view = ft.ListView(
        spacing=14,
        controls=[
            ft.Text("Kenooff Logistics Form", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
            ft.Text("Log New Package Entry (Cloud Connected)", size=14, color=ft.Colors.GREY_600),
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

    # ==================== DATA HISTORY & UPDATE ====================
    history_list = ft.ListView(spacing=10, expand=True)

    def delete_record(record_id):
        try:
            supabase_request(f"packages?id=eq.{record_id}", method="DELETE")
            show_alert("Record deleted from Cloud!", ft.Colors.GREY_700)
            load_database_records()
        except Exception as ex:
            show_alert(f"Failed to delete: {str(ex)}", ft.Colors.RED_600)

    def update_status(record_id, new_status):
        try:
            supabase_request(f"packages?id=eq.{record_id}", method="PATCH", data={"status": str(new_status)})
            show_alert(f"Status updated to '{new_status}'!", ft.Colors.GREEN_700)
            load_database_records()
        except Exception as ex:
            show_alert(f"Failed to update status: {str(ex)}", ft.Colors.RED_600)

    def make_status_handler(target_id):
        return lambda e: update_status(target_id, e.control.value)

    def make_delete_handler(target_id):
        return lambda e: delete_record(target_id)

    def load_database_records():
        history_list.controls.clear()
        try:
            rows = supabase_request("packages?select=*&order=id.desc", method="GET")

            if not rows:
                history_list.controls.append(
                    ft.Container(
                        content=ft.Text("No saved packages found in online database.", italic=True, color=ft.Colors.GREY_500),
                        alignment=ft.Alignment.CENTER,
                        padding=20
                    )
                )
            else:
                for row in rows:
                    current_id = row.get("id")
                    vendor = row.get("vendor", "")
                    desc = row.get("package_desc", "")
                    total = row.get("total_value", 0.0) or 0.0
                    loc = row.get("location", "")
                    rider = row.get("rider", "")
                    status = str(row.get("status", "Pending"))

                    status_color = ft.Colors.ORANGE_700
                    if status == "Delivered":
                        status_color = ft.Colors.GREEN_700
                    elif status == "In Transit":
                        status_color = ft.Colors.BLUE_700

                    # Fixed Dropdown syntax
                    status_dropdown = ft.Dropdown(
                        value=status,
                        width=140,
                        height=40,
                        text_size=12,
                        border_radius=6,
                        options=[
                            ft.dropdown.Option("Pending"),
                            ft.dropdown.Option("In Transit"),
                            ft.dropdown.Option("Delivered"),
                        ]
                    )
                    status_dropdown.on_change = make_status_handler(current_id)

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
                                    ft.Row([
                                        status_dropdown,
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINED, 
                                            icon_color=ft.Colors.RED_400,
                                            on_click=make_delete_handler(current_id)
                                        )
                                    ])
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ])
                        )
                    )
                    history_list.controls.append(card)
        except Exception as ex:
            history_list.controls.append(
                ft.Container(
                    content=ft.Text(f"Error connecting to Cloud Database: {str(ex)}", color=ft.Colors.RED_500),
                    padding=20
                )
            )
        page.update()

    body = ft.Container(content=form_view, padding=12, expand=True)

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
