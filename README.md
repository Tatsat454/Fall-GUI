

---

# 🍂 Fall Themed GUI

### A cozy autumn-inspired desktop dashboard with live weather, animated background, and Spotify media controls

![Fall Theme Preview](assets/preview.gif)

> *"Designed for peaceful focus, inspired by falling leaves and lo-fi playlists."*

---

## 🌟 Features

### 🕒 **Dynamic Clock**

* Displays current time in a retro-pixel style font (`dogica`)
* Auto-updates every second
* Uses **Pacific Time (America/Los_Angeles)** by default

### 🌦️ **Live Weather**

* Detects your **current city** using IP geolocation
* Fetches live data from **OpenWeatherMap API**
* Displays temperature with a matching icon (☀️ 🌧️ ☁️ ❄️ ⚡)
* Refreshes every **30 minutes**

### 🎧 **Spotify Controls (macOS)**

* Full playback integration via **AppleScript**
* Supports:

  * ▶️ Play / Pause
  * ⏭️ Next Track
  * ⏮️ Previous Track
* Shows artist + song name
* Updates every **5 seconds**

### 🍁 **Animated Fall Background**

* Smooth 120-FPS looping fall GIF
* Warm transparent overlay for ambience
* Resizes fluidly to fit your window

---

## 🧰 Tech Stack

| Component     | Description                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| **Language**  | Python 3                                                                                                    |
| **Framework** | [Kivy](https://kivy.org/)                                                                                   |
| **APIs**      | [OpenWeatherMap](https://openweathermap.org/api), [ip-api](http://ip-api.com), [ipapi.co](https://ipapi.co) |
| **Platform**  | macOS (Spotify control via AppleScript)                                                                     |
| **UI Assets** | Custom fall icons, dogica font, animated GIF background                                                     |

---

## ⚙️ Setup

### 1️⃣ Install Dependencies

```bash
pip install kivy requests
```

### 2️⃣ Add Your API Key

Open `WeatherService` in the code and replace:

```python
self.OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
```

### 3️⃣ Adjust File Paths

Update these for your local system:

* Font path (`dogica.ttf`)
* GIF background
* Weather icons (sun, rain, cloud, etc.)

### 4️⃣ Run the App

```bash
python fall_gui.py
```

> ✅ Works best on **macOS**. Spotify controls depend on AppleScript.

---

## 🧠 Architecture Overview

```
FallApp (Main Kivy App)
│
├── AnimatedBackground     # Renders looping fall GIF
├── LocationWidget         # Fetches and displays city + temperature
├── WeatherService         # Handles API calls and weather logic
├── MediaControlWidget     # Spotify controls + song info
└── Clock Label            # Real-time time display
```

---

## 🪄 Customization Ideas

* 🌙 Add **Day/Night mode** based on local time
* 📈 Show **5-day weather forecast**
* 🔊 Add **volume / playlist controls**
* 🌡️ Display **air quality or humidity**
* 💻 Cross-platform: swap AppleScript with [Spotipy](https://spotipy.readthedocs.io/)

---

## 🖼️ Example Layout (Default)

```
 --------------------------------------------------
|        🍁 Animated Fall Background (GIF)         |
|  --------------------------------------------   |
|  🌦️  Weather: 72°F ☀️      🕒 12:34 pm           |
|                                                  |
|  🎵  <<   [PLAY]   >>    "Artist - Track"         |
 --------------------------------------------------
```

---

## 🧑‍🎨 Credits

**Font:** [Dogica Pixel Font](https://www.dafont.com/dogica.font)
**Weather Icons:** Custom flat PNG set
**Background:** https://www.reddit.com/r/PixelArt/comments/fovvoo/view_over_japanese_valley_in_autumn_animated/ 

---

## 🧡 Author

**Tatsat Upadhyay**
Student · Writer · Builder of cozy code.
📖 [TheNextFramework.blog](https://thenextframework.blog) | 🐦 [@tatsatupadhyay](https://x.com/tatsatupadhyay)

---
