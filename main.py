"""
main.py
-------
Telegram control panel for remotely executing
system functions on the host computer.
"""

from datetime import datetime
import os
import time
import threading
import dotenv
from telebot import TeleBot, types
from functions import *

# ==========================================================
# Load Environment Variables
# ==========================================================
dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = TeleBot(API_TOKEN)

# ==========================================================
# Auto-Delete Confirmation Helper
# ==========================================================
def send_confirmation(chat_id, text, delay=5):
    """
    Sends a text message and spawns a background thread 
    to automatically delete it after the specified delay (seconds).
    """
    msg = bot.send_message(chat_id, text, parse_mode="Markdown")
    
    def auto_delete():
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            # Prevents crashes if the message was manually deleted earlier
            pass

    # Run as a daemon thread so it closes cleanly if the script exits
    threading.Thread(target=auto_delete, daemon=True).start()


# ==========================================================
# Startup Notification
# ==========================================================
def send_startup_message():
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%I:%M:%S %p")

    message = (
        "✅ *System Activated*\n\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time: {time_str}"
    )
    bot.send_message(ADMIN_ID, message, parse_mode="Markdown")

# ==========================================================
# /start Command (UI Construction)
# ==========================================================
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()

    # Row 1: System Info & Speed Test
    btn_sys_info = types.InlineKeyboardButton("📊 System Info", callback_data="sys_info")
    btn_speed_test = types.InlineKeyboardButton("🚀 Speed Test", callback_data="speed_test")
    markup.row(btn_sys_info, btn_speed_test)

    # Row 2: Volume Panel
    btn_vol_up = types.InlineKeyboardButton("🔊 Vol Up", callback_data="vol_up")
    btn_vol_down = types.InlineKeyboardButton("🔉 Vol Down", callback_data="vol_down")
    btn_mute = types.InlineKeyboardButton("🔇 Mute", callback_data="vol_mute")
    markup.row(btn_vol_up, btn_vol_down, btn_mute)

    # Row 3: Media Control Panel
    btn_prev = types.InlineKeyboardButton("⏮️ Prev", callback_data="med_prev")
    btn_play = types.InlineKeyboardButton("⏯️ Play/Pause", callback_data="med_play")
    btn_next = types.InlineKeyboardButton("⏭️ Next", callback_data="med_next")
    markup.row(btn_prev, btn_play, btn_next)

    # Row 4: Power Controls
    btn_sleep = types.InlineKeyboardButton("💤 Sleep", callback_data="sleep")
    btn_lock = types.InlineKeyboardButton("🔒 Lock PC", callback_data="lock")
    btn_shutdown = types.InlineKeyboardButton("🔴 Shutdown", callback_data="shutdown")
    markup.row(btn_sleep, btn_lock, btn_shutdown)

    # Row 5: Utilities (Clipboard, Mouse Tracking, Location)
    btn_clip = types.InlineKeyboardButton("📋 Clipboard", callback_data="clipboard")
    btn_mouse = types.InlineKeyboardButton("📍 Mouse Pos", callback_data="mouse_pos")
    btn_loc = types.InlineKeyboardButton("🗺️ Location", callback_data="location")
    markup.row(btn_clip, btn_mouse, btn_loc)

    # Row 6: Recording & Capture
    btn_ss = types.InlineKeyboardButton("📸 Screenshot", callback_data="screenshot")
    btn_sr = types.InlineKeyboardButton("🎥 Screen Rec", callback_data="scrn_rec")
    btn_mic = types.InlineKeyboardButton("🎙️ Record Mic", callback_data="record_mic")
    markup.row(btn_ss, btn_sr, btn_mic)

    # Row 7: Application Controls
    btn_list_apps = types.InlineKeyboardButton("📋 Opened Apps List", callback_data="list_apps")
    btn_open = types.InlineKeyboardButton("📂 Open App", callback_data="open_app")
    btn_close = types.InlineKeyboardButton("❌ Close App", callback_data="close_app")
    markup.row(btn_list_apps)
    markup.row(btn_open, btn_close)

    # Row 8: Prank Controls
    btn_notify = types.InlineKeyboardButton("🔔 Notification", callback_data="notify")
    btn_beep = types.InlineKeyboardButton("📢 Beep", callback_data="beep_sound")
    markup.row(btn_notify, btn_beep)

    bot.send_message(
        message.chat.id,
        "🎮 *Trinetra Control Panel Enhanced*\n\nChoose an action below:",
        parse_mode="Markdown",
        reply_markup=markup,
    )

# ==========================================================
# Button Callback Handler
# ==========================================================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Security Validation Check
    if str(call.from_user.id) != str(ADMIN_ID):
        bot.answer_callback_query(call.id, "🚫 Unauthorized Access!", show_alert=True)
        return

    # Acknowledge Telegram click immediately
    bot.answer_callback_query(call.id)

    # --- Feature Executions ---

    if call.data == "sys_info":
        info_msg = get_system_info()
        bot.send_message(ADMIN_ID, info_msg, parse_mode="Markdown")

    elif call.data == "speed_test":
        send_confirmation(ADMIN_ID, "⏳ Running Speed Test... Please wait up to a minute.")
        speed_msg = run_speed_test()
        bot.send_message(ADMIN_ID, speed_msg, parse_mode="Markdown")

    elif call.data == "vol_up":
        media_control("volup")
        send_confirmation(ADMIN_ID, "🔊 Volume Up command applied successfully.")

    elif call.data == "vol_down":
        media_control("voldown")
        send_confirmation(ADMIN_ID, "🔉 Volume Down command applied successfully.")

    elif call.data == "vol_mute":
        media_control("mute")
        send_confirmation(ADMIN_ID, "🔇 System Volume Mute toggled successfully.")

    elif call.data == "med_prev":
        media_control("prev")
        send_confirmation(ADMIN_ID, "⏮️ Skipped to previous track/video.")

    elif call.data == "med_play":
        media_control("play_pause")
        send_confirmation(ADMIN_ID, "⏯️ Play/Pause command executed.")

    elif call.data == "med_next":
        media_control("next")
        send_confirmation(ADMIN_ID, "⏭️ Skipped to next track/video.")

    elif call.data == "sleep":
        send_confirmation(ADMIN_ID, "💤 Computer switching to sleep mode...")
        sleep_pc()

    elif call.data == "lock":
        lock_pc()
        send_confirmation(ADMIN_ID, "🔒 PC locked successfully.")

    elif call.data == "shutdown":
        send_confirmation(ADMIN_ID, "🔴 Shutdown command scheduled. PC turning off in 5 seconds.")
        shutdown_pc()

    elif call.data == "clipboard":
        clip_text = get_clipboard_text()
        bot.send_message(ADMIN_ID, f"📋 *Current Clipboard Content:*\n\n```{clip_text}```", parse_mode="Markdown")

    elif call.data == "mouse_pos":
        pos_msg = get_mouse_position()
        bot.send_message(ADMIN_ID, pos_msg, parse_mode="Markdown")

    elif call.data == "location":
        loc_msg = get_location_by_ip()
        bot.send_message(ADMIN_ID, loc_msg, parse_mode="Markdown")

    elif call.data == "screenshot":
        screenshot()
        with open("screenshot.png", "rb") as image:
            bot.send_photo(ADMIN_ID, image, caption="📸 Screenshot captured successfully.")

    elif call.data == "scrn_rec":
        send_confirmation(ADMIN_ID, "🎥 Recording screen for 8 seconds...")
        screen_rec()
        with open("screen_rec.mp4", "rb") as video:
            bot.send_video(ADMIN_ID, video, caption="🎥 Screen recording completed successfully.")

    elif call.data == "record_mic":
        send_confirmation(ADMIN_ID, "🎙️ Recording mic audio for 10 seconds...")
        record_microphone()
        with open("mic_rec.wav", "rb") as audio:
            bot.send_audio(ADMIN_ID, audio, caption="🎙️ Microphone audio captured successfully.")

    elif call.data == "open_app":
        random_app_open()
        send_confirmation(ADMIN_ID, "📂 Random utility application opened successfully.")

    elif call.data == "close_app":
        app_close()
        send_confirmation(ADMIN_ID, "❌ Topmost application close command triggered.")

    elif call.data == "notify":
        send_confirmation(ADMIN_ID, "🔔 Sending Prank Notification window...")
        notification()
        send_confirmation(ADMIN_ID, "✅ Prank notification sent successfully.")

    elif call.data == "beep_sound":
        send_confirmation(ADMIN_ID, "📢 Playing 2-second Motherboard Beep...")
        play_sound()
        send_confirmation(ADMIN_ID, "✅ Beep sound played successfully.")

    elif call.data == "list_apps":
        apps = get_open_windows()
        if apps:
            bot.send_message(ADMIN_ID, "📋 *Opened Applications:*\n\n" + "\n".join(apps), parse_mode="Markdown")
        else:
            bot.send_message(ADMIN_ID, "📋 No active window processes found.", parse_mode="Markdown")

# ==========================================================
# Main Entry Point
# ==========================================================
if __name__ == "__main__":
    print("✅ Trinetra Bot Started Successfully...")
    send_startup_message()
    bot.infinity_polling()