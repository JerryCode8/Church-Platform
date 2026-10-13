import json
import os
import flet as ft 

#--- COLOR PATTERN DEFINITION --- 
COLOR_BLUE = "#1A237E"       #Deep Blue  
COLOR_PURPLE = "#4A148C"     #Deep Purple
COLOR_GOLD = "#FFC107"       #Vibrant Gold
COLOR_GREEN = "#2ECC71"      #Emerald Green
COLOR_WHITE = "#FFFFFF"      #White
COLOR_DARK_TEXT = "#212121"  #Dark text for readability

# -- JSON STORAGE HELPERS ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "prayers": os.path.join(DATA_DIR, "form_prayer.json"),
    "membership" : os.path.join(DATA_DIR, "membership"),
    "volunteer": os.path.join(DATA_DIR, "form_volunteer.json"),
    "announcements": os.path.join(DATA_DIR, "form_announcements.json"),
}

def load_json(key):
    path = FILES.get(key)
    if not path or not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_json(key, record):
    path = FILES.get(key)
    data = load_json(key)
    data.append(record)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def main(page: ft.Page):
    page.title = "Miracles Church of God International"
    page.bgcolor = COLOR_WHITE
    page.padding = 0

    # -- STATE --
    is_minister = False

    # -- notification helper --
    def notify(msg, bg_color=COLOR_GREEN, text_color=COLOR_WHITE):
        page.snackbar = ft.SnackBar(
            ft.Text(msg, color=text_color, weight=ft.FontWeight.BOLD),
            bgcolor=bg_color
        )
        page.snackbar.open = True
        page.update()

    # -- DIALOGS --
    username_input = ft.TextField(label="Username", width=260, border_color=COLOR_PURPLE)
    password_input = ft.TextField(label="Password", width=260, border_color=COLOR_PURPLE)

    def login(e):
        nonlocal is_minister
        if username_input.value == "minister" and password_input.value == "grace2026":
            is_minister = True
            login_dialog.open = False
            notify("Logged in successfully as Minister!", COLOR_GREEN)
            rebuild_ui()
        else:
            notify("Invalid credentials!", COLOR_PURPLE)

    def perform_logout(e):
        nonlocal is_minister
        is_minister = False
        notify("Logged out", COLOR_PURPLE)
        rebuild_ui()

    login_dialog = ft.AlertDialog(
        ft.Text("Minister Login Portal", color=COLOR_BLUE, weight=ft.FontWeight.BOLD),
        content=ft.Column([username_input, password_input], tight=True),
        actions=[
            ft.TextButton("Cancel",on_click=lambda e: setattr(login_dialog, "open", False) or page.update()),
            ft.Button("Login", bgcolor=COLOR_GREEN, color=COLOR_WHITE, on_click=login),
        ],
    )

    def open_login(e):
        page.dialog = login_dialog
        login_dialog.open = True
        page.update()

    # -- FORM HANDLERS -- 
    def submit_prayer(e):
        if not prayer_name.value or not prayer_req.value:
            notify("Please fill in all the fields.", COLOR_PURPLE)
            return

        save_json("prayer", {"name": prayer_name.value, "request": prayer_req.value})
        prayer_name.value = ""
        prayer_req.value = ""
        notify("Prayer submitted successfully!", COLOR_GREEN)
        rebuild_ui()

    def submit_membership(e):
        if not mem_name.value or not mem_email.value or not mem_phone.value:
            notify("Please fill in all the fields", COLOR_PURPLE)
            return

        save_json("membership", {"name": mem_name.value, "email": mem_email.value, "phone": mem_phone.value})
        mem_name.value = ""
        mem_email.value = ""
        mem_phone.value = ""
        notify("Membership application submitted!", COLOR_GREEN)
        rebuild_ui()

    def submit_volunteer(e):
        if not vol_name.value:
            notify("Please provide your name", COLOR_PURPLE)
            return

        save_json("volunteer", {"name": vol_name.value, "department": vol_dept.value})
        vol_name.value = ""
        notify("Volunteer registration submitted!", COLOR_GREEN)
        rebuild_ui()

    def submit_contact(e):
        if not contact_name.value or not contact_email.value or not contact_message.value:
            notify("Contact us using the details requested", COLOR_PURPLE)
            return

        contact_name.value = ""
        contact_email.value = ""
        contact_message.value = ""
        notify("Message sent directly to the pastrol team!", COLOR_BLUE)

    def submit_announcements(e):
        if not anc_title.value or not anc_content.value:
            notify("Please fill out both title and content", COLOR_PURPLE)
            return

        save_json("announcements", {"title": anc_title.value, "content": anc_content.value})
        anc_title = ""
        anc_content = ""   
        notify("Announcement posted!", COLOR_GREEN)
        rebuild_ui()

    # --- FORM INPUT ---
    prayer_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    prayer_req = ft.TextField(label="Prayer Request", multiline=True, rows=3, border_color=COLOR_BLUE)

    mem_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    mem_email = ft.TextField(label="Email Address", border_color=COLOR_BLUE)
    mem_phone = ft.TextField(label="Phone Number", border_color=COLOR_BLUE)

    vol_name = ft.TextField(label="Full Name", border_color=COLOR_BLUE)
    vol_dept = ft.Dropdown(
        label="Department Choice",
        border_color=COLOR_BLUE,
        options=[
            ft.dropdown.Option("Pastrol Team"),
            ft.dropdown.Option("Ushering"),
            ft.dropdown.Option("Media & Tech"),
            ft.dropdown.Option("Worship Ministry"),
            ft.dropdown.Option("Children's Ministry")
        ],
        value="Ushering"
    )