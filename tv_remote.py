from pywebostv.connection import WebOSClient
from pywebostv.controls import MediaControl, InputControl, SystemControl
import json
import os

class TVRemote:
    def __init__(self):
        self.client = None
        self.tv_ip = None
        self.store_file = 'tv_pairing.json'
        self.store = self._load_store()
    
    def _load_store(self):
        """Load pairing information"""
        if os.path.exists(self.store_file):
            with open(self.store_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_store(self):
        """Save pairing information"""
        with open(self.store_file, 'w') as f:
            json.dump(self.store, f)
    
    def connect(self, ip=None):
        """Connect to TV"""
        if ip:
            self.tv_ip = ip
        
        if not self.tv_ip:
            from find_devices import discover_tvs
            tvs = discover_tvs()
            if tvs:
                self.tv_ip = str(tvs[0])
            else:
                raise Exception("❌ TV not found! Make sure the TV is on and on the same network.")
        
        print(f"🔌 Connecting to {self.tv_ip}...")
        self.client = WebOSClient(self.tv_ip)
        
        for status in self.client.register(self.store):
            if status == WebOSClient.PROMPTED:
                print("📺 Click 'YES' on the TV screen!")
            elif status == WebOSClient.REGISTERED:
                print("✅ Connection successful!")
                self._save_store()
        
        return self.client
    
    def get_controls(self):
        """Get all controls"""
        if not self.client:
            self.connect()
        
        return {
            'media': MediaControl(self.client),
            'input': InputControl(self.client),
            'system': SystemControl(self.client)
        }
    
    def volume_up(self):
        controls = self.get_controls()
        controls['media'].volume_up()
        print("🔊 Volume increased")
    
    def volume_down(self):
        controls = self.get_controls()
        controls['media'].volume_down()
        print("🔉 Volume decreased")
    
    def mute(self):
        controls = self.get_controls()
        controls['media'].mute(True)
        print("🔇 Muted")
    
    def set_volume(self, level):
        controls = self.get_controls()
        controls['media'].set_volume(level)
        print(f"🔊 Volume level: {level}")
    
    def arrow_up(self):
        controls = self.get_controls()
        controls['input'].up()
        print("⬆️ Up")
    
    def arrow_down(self):
        controls = self.get_controls()
        controls['input'].down()
        print("⬇️ Down")
    
    def arrow_left(self):
        controls = self.get_controls()
        controls['input'].left()
        print("⬅️ Left")
    
    def arrow_right(self):
        controls = self.get_controls()
        controls['input'].right()
        print("➡️ Right")
    
    def ok(self):
        controls = self.get_controls()
        controls['input'].ok()
        print("✅ OK")
    
    def back(self):
        controls = self.get_controls()
        controls['input'].back()
        print("⬅️ Back")
    
    def home(self):
        controls = self.get_controls()
        controls['input'].home()
        print("🏠 Home")
    
    def play(self):
        controls = self.get_controls()
        controls['media'].play()
        print("▶️ Play")
    
    def pause(self):
        controls = self.get_controls()
        controls['media'].pause()
        print("⏸️ Pause")
    
    def channel_up(self):
        controls = self.get_controls()
        controls['media'].channel_up()
        print("📺 Channel +")
    
    def channel_down(self):
        controls = self.get_controls()
        controls['media'].channel_down()
        print("📺 Channel -")
    
    def launch_app(self, app_id):
        if not self.client:
            self.connect()
        
        apps = {
            'netflix': 'netflix',
            'youtube': 'youtube.leanback.v4',
            'disney': 'com.disney.disneyplus-prod',
            'prime': 'amazon',
            'spotify': 'spotify-beehive'
        }
        
        app_name = apps.get(app_id.lower(), app_id)
        self.client.launch_app(app_name)
        print(f"📱 Launching {app_id.upper()}...")
    
    def notify(self, message):
        controls = self.get_controls()
        controls['system'].notify(message)
        print(f"💬 Notification sent: {message}")
