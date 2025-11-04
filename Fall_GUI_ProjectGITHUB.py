"""
Fall themed GUI with animated GIF background, weather, and Spotify controls
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from datetime import datetime
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from zoneinfo import ZoneInfo
import requests
import subprocess
import threading
from typing import Dict, Tuple

PACIFIC = ZoneInfo("America/Los_Angeles")

# ---- font registration ----
FONT_PATH = "/Users/tatsatupadhyay/Downloads/dogica/TTF/dogica.ttf"
LabelBase.register(name="FallClock", fn_regular=FONT_PATH)

# Weather icons mapping
WEATHER_ICONS = {
    "sunny": "/Users/tatsatupadhyay/Downloads/sun.png",
    "rainy": "/Users/tatsatupadhyay/Downloads/drop.png",
    "cloudy": "/Users/tatsatupadhyay/Downloads/cloudy.png",
    "snowy": "/Users/tatsatupadhyay/Downloads/snowflake.png",
    "windy": "/Users/tatsatupadhyay/Downloads/wind.png",
    "thunder": "/Users/tatsatupadhyay/Downloads/lightning-bolt.png"
}

# ---------- Thread-safe AppleScript runner ----------
def run_apple_script(script: str, callback=None):
    """Run AppleScript in a background thread and return result via callback"""
    def worker():
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()
        except Exception as e:
            output = f"Error: {e}"

        if callback:
            # push result back to UI thread
            Clock.schedule_once(lambda dt: callback(output), 0)

    threading.Thread(target=worker, daemon=True).start()


# ---------- Weather ----------
class WeatherService:
    def __init__(self):
        self.OPENWEATHER_API_KEY = "NOT PUTTING API KEY HERE SINCE THIS IS PUBLIC NOW! BUT WORKS FINE"

    def get_location(self) -> Dict:
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5)
            data = response.json()
            if response.status_code == 200 and data.get('status') == 'success':
                return {
                    "city": data['city'],
                    "latitude": data['lat'],
                    "longitude": data['lon']
                }
        except Exception:
            pass

        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            data = response.json()
            if response.status_code == 200:
                return {
                    "city": data['city'],
                    "latitude": float(data['latitude']),
                    "longitude": float(data['longitude'])
                }
        except Exception:
            pass

        return {
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194
        }

    def get_weather(self, lat: float, lon: float) -> Tuple[str, float]:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.OPENWEATHER_API_KEY}&units=imperial"
            response = requests.get(url, timeout=5)
            data = response.json()

            condition = data['weather'][0]['main'].lower()
            temp = round(data['main']['temp'])

            if condition == 'clear':
                icon = WEATHER_ICONS['sunny']
            elif condition in ['rain', 'drizzle']:
                icon = WEATHER_ICONS['rainy']
            elif condition == 'clouds':
                icon = WEATHER_ICONS['cloudy']
            elif condition == 'snow':
                icon = WEATHER_ICONS['snowy']
            elif condition == 'thunderstorm':
                icon = WEATHER_ICONS['thunder']
            else:
                icon = WEATHER_ICONS['sunny']

            return icon, temp
        except Exception:
            return WEATHER_ICONS['sunny'], 72


# ---------- Location & Weather Widget ----------
class LocationWidget(FloatLayout):
    def __init__(self, weather_service, **kwargs):
        super().__init__(**kwargs)
        self.weather_service = weather_service
        self.size_hint = (None, None)
        self.size = (200, 100)
        self.pos_hint = {'center_x': 0.3, 'center_y': 0.65}

        location = self.weather_service.get_location()
        weather_icon_path, temperature = self.weather_service.get_weather(
            location['latitude'], location['longitude']
        )

        self.weather_icon = Image(
            source=weather_icon_path,
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_x': 0.9, 'center_y': 0.5}
        )
        self.add_widget(self.weather_icon)

        self.temp_label = Label(
            text=f"{temperature}°F",
            font_size=45,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            pos_hint={'center_x': 0.2, 'center_y': 0.5},
            font_name="FallClock"
        )
        self.add_widget(self.temp_label)

    def update_weather(self):
        location = self.weather_service.get_location()
        weather_icon_path, temperature = self.weather_service.get_weather(
            location['latitude'], location['longitude']
        )
        self.weather_icon.source = weather_icon_path
        self.temp_label.text = f"{temperature}°F"


# ---------- Background ----------
class AnimatedBackground(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim_delay = 1 / 30  # smooth 30 fps for 120-frame GIF (~4 sec loop)
        self.allow_stretch = True
        self.keep_ratio = False
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}


# ---------- Spotify Media Controls ----------
class MediaControlWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 100)
        self.pos_hint = {'center_x': 0.3, 'center_y': 0.4}

        self.play_pause_btn = Label(
            text="[PLAY]",
            font_size=30,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(50, 50),
            bold=True,
            font_name="FallClock",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.play_pause_btn.bind(on_touch_down=self.toggle_play_pause)
        self.add_widget(self.play_pause_btn)

        self.prev_btn = Label(
            text="<<",
            font_size=30,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(50, 50),
            bold=True,
            font_name="FallClock",
            pos_hint={'center_x': 0.10, 'center_y': 0.5}
        )
        self.prev_btn.bind(on_touch_down=self.previous_track)
        self.add_widget(self.prev_btn)

        self.next_btn = Label(
            text=">>",
            font_size=30,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(50, 50),
            bold=True,
            font_name="FallClock",
            pos_hint={'center_x': 0.90, 'center_y': 0.5}
        )
        self.next_btn.bind(on_touch_down=self.next_track)
        self.add_widget(self.next_btn)

        self.track_info = Label(
            text="",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            font_name="FallClock"
        )
        self.add_widget(self.track_info)

        # Update track info every 5 seconds instead of 1
        Clock.schedule_interval(self.update_track_info, 5)

    def toggle_play_pause(self, instance, touch):
        if instance.collide_point(*touch.pos):
            script = '''
            tell application "Spotify"
                if player state is playing then
                    pause
                else
                    play
                end if
            end tell
            '''
            run_apple_script(script, self.update_play_pause_state)

    def previous_track(self, instance, touch):
        if instance.collide_point(*touch.pos):
            script = 'tell application "Spotify" to previous track'
            run_apple_script(script)

    def next_track(self, instance, touch):
        if instance.collide_point(*touch.pos):
            script = 'tell application "Spotify" to next track'
            run_apple_script(script)

    def update_track_info(self, dt):
        script = '''
        tell application "Spotify"
            if player state is playing then
                return (get artist of current track) & " - " & (get name of current track)
            else
                return "Paused"
            end if
        end tell
        '''
        run_apple_script(script, self.set_track_info)

    def set_track_info(self, track_info):
        self.track_info.text = track_info
        self.update_play_pause_state()

    def update_play_pause_state(self, _=None):
        script = 'tell application "Spotify" to return player state'
        run_apple_script(script, self.set_play_pause_button)

    def set_play_pause_button(self, state):
        self.play_pause_btn.text = "[PAUSED]" if state == "playing" else "[PLAY]"


# ---------- Main App ----------
class FallApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (800, 450)
        self.weather_service = WeatherService()

    def build(self):
        layout = FloatLayout()

        background = AnimatedBackground(
            source='/Users/tatsatupadhyay/Downloads/Fallbg.gif'
        )
        layout.add_widget(background)

        with layout.canvas.before:
            Color(0.8, 0.4, 0.2, 0.2)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)
        Window.bind(size=self._update_rect)

        self.location_widget = LocationWidget(self.weather_service)
        layout.add_widget(self.location_widget)

        self.clock_label = Label(
            text=datetime.now(PACIFIC).strftime('%I:%M %p').lstrip("0").lower(),
            font_size=55,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            pos_hint={'center_x': 0.3, 'center_y': 0.5},
            font_name="FallClock"
        )
        layout.add_widget(self.clock_label)

        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_interval(lambda dt: self.location_widget.update_weather(), 1800)

        self.media_control_widget = MediaControlWidget()
        layout.add_widget(self.media_control_widget)

        return layout

    def update_clock(self, dt):
        now = datetime.now(PACIFIC)
        self.clock_label.text = now.strftime('%I:%M%p').lstrip("0").lower()

    def _update_rect(self, instance, value):
        if hasattr(self, 'rect'):
            self.rect.size = instance.size


if __name__ == '__main__':
    FallApp().run()
