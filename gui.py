import flet as ft
import threading
from tv_remote import TVRemote

class TVRemoteApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.remote = TVRemote()
        self.is_connected = False
        self.volume_value = 50
        
        self.page.title = "LG WebOS TV Remote Control"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.page.window.width = 600
        self.page.window.height = 700
        self.page.scroll = ft.ScrollMode.AUTO
        
        self.init_ui()
        self.auto_connect()
    
    def init_ui(self):
        self.status_text = ft.Text(
            "Status: Disconnected",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="red"
        )
        
        self.connect_btn = ft.ElevatedButton(
            "📶 Connect to TV",
            bgcolor="#4CAF50",
            color="white",
            on_click=self.connect_tv,
            width=200
        )
        
        status_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    self.status_text,
                    self.connect_btn
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        volume_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Volume Control", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("🔉 -", on_click=lambda _: self.remote.volume_down(), width=80),
                        ft.ElevatedButton("🔇 Mute", on_click=lambda _: self.remote.mute(), width=100),
                        ft.ElevatedButton("🔊 +", on_click=lambda _: self.remote.volume_up(), width=80),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Slider(
                        min=0,
                        max=100,
                        value=50,
                        divisions=100,
                        label="{value}%",
                        on_change=self.on_volume_changed,
                        width=400
                    )
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        nav_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Navigation", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Container(width=80),
                        ft.ElevatedButton("⬆️", on_click=lambda _: self.remote.arrow_up(), width=60, height=60),
                        ft.Container(width=80)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        ft.ElevatedButton("⬅️", on_click=lambda _: self.remote.arrow_left(), width=60, height=60),
                        ft.ElevatedButton("OK", on_click=lambda _: self.remote.ok(), width=80, height=80),
                        ft.ElevatedButton("➡️", on_click=lambda _: self.remote.arrow_right(), width=60, height=60),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        ft.Container(width=80),
                        ft.ElevatedButton("⬇️", on_click=lambda _: self.remote.arrow_down(), width=60, height=60),
                        ft.Container(width=80)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        ft.ElevatedButton("⬅️ Back", on_click=lambda _: self.remote.back(), width=150),
                        ft.ElevatedButton("🏠 Home", on_click=lambda _: self.remote.home(), width=150),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        media_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Media Control", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("▶️ Play", on_click=lambda _: self.remote.play(), width=150),
                        ft.ElevatedButton("⏸️ Pause", on_click=lambda _: self.remote.pause(), width=150),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        channel_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Channel Control", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("📺 Ch -", on_click=lambda _: self.remote.channel_down(), width=150),
                        ft.ElevatedButton("📺 Ch +", on_click=lambda _: self.remote.channel_up(), width=150),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        apps = [
            ("Netflix", "netflix", "#C62828"),
            ("YouTube", "youtube", "#D32F2F"),
            ("Disney+", "disney", "#1976D2"),
            ("Prime", "prime", "#2196F3"),
            ("Spotify", "spotify", "#4CAF50")
        ]
        
        app_buttons = []
        for name, app_id, color in apps:
            app_buttons.append(
                ft.ElevatedButton(
                    name,
                    on_click=lambda e, a=app_id: self.remote.launch_app(a),
                    bgcolor=color,
                    color="white",
                    width=110
                )
            )
        
        apps_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Launch Apps", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(app_buttons, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        self.notify_input = ft.TextField(
            label="Notification Message",
            hint_text="Enter your message...",
            width=400,
            on_submit=self.send_notification
        )
        
        notify_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Send Notification", size=18, weight=ft.FontWeight.BOLD),
                    self.notify_input,
                    ft.ElevatedButton(
                        "💬 Send Notification",
                        on_click=self.send_notification,
                        width=200
                    )
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        )
        
        scrollable_content = ft.Column(
            controls=[
                status_card,
                volume_card,
                nav_card,
                media_card,
                channel_card,
                apps_card,
                notify_card
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
        
        self.page.add(scrollable_content)
        
        self.update_buttons_state(False)
    
    def update_buttons_state(self, enabled):
        controls = []
        for control in self.page.controls:
            controls.extend(self._get_all_controls(control))
        
        for control in controls:
            if isinstance(control, (ft.ElevatedButton, ft.Slider, ft.TextField)):
                control.disabled = not enabled
    
    def _get_all_controls(self, control):
        controls = [control]
        if hasattr(control, 'content'):
            if isinstance(control.content, (ft.Column, ft.Row)):
                for item in control.content.controls:
                    controls.extend(self._get_all_controls(item))
            elif isinstance(control.content, ft.Container):
                if hasattr(control.content, 'content'):
                    controls.extend(self._get_all_controls(control.content))
        elif hasattr(control, 'controls'):
            for item in control.controls:
                controls.extend(self._get_all_controls(item))
        return controls
    
    def auto_connect(self):
        self.connect_tv(None)
    
    def connect_tv(self, e):
        self.connect_btn.disabled = True
        self.status_text.value = "Status: Connecting..."
        self.status_text.color = "orange"
        self.page.update()
        
        def connect_thread():
            try:
                self.remote.connect()
                self.is_connected = True
                self.on_connected(True, f"Connected to {self.remote.tv_ip}")
            except Exception as ex:
                self.is_connected = False
                self.on_connected(False, str(ex))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connected(self, success, message):
        self.connect_btn.disabled = False
        if success:
            self.status_text.value = f"Status: ✅ Connected ({self.remote.tv_ip})"
            self.status_text.color = "green"
            self.update_buttons_state(True)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ Connection successful!"),
                bgcolor="#4CAF50"
            )
            self.page.snack_bar.open = True
        else:
            self.status_text.value = "Status: ❌ Connection Failed"
            self.status_text.color = "red"
            self.update_buttons_state(False)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ {message}"),
                bgcolor="#D32F2F"
            )
            self.page.snack_bar.open = True
        
        self.page.update()
    
    def on_volume_changed(self, e):
        if self.is_connected:
            try:
                value = int(e.control.value)
                self.remote.set_volume(value)
            except:
                pass
    
    def send_notification(self, e):
        message = self.notify_input.value.strip()
        if message:
            try:
                self.remote.notify(message)
                self.notify_input.value = ""
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"💬 Notification sent: {message}"),
                    bgcolor="#2196F3"
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Error: {ex}"),
                    bgcolor="#D32F2F"
                )
                self.page.snack_bar.open = True
                self.page.update()

def main(page: ft.Page):
    app = TVRemoteApp(page)

ft.app(target=main)
