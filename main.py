import Quartz
import pyautogui
import time
import os
import sys
from pynput.keyboard import Listener, Key

# Optimization settings for pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

os.system('title telegram: Blum Cliker App')

# Window input and messages
window_input = "\nВведите название окна (1 - TelegramDesktop | 2 - iMe): "
window_not_found = "[❌] | Окно - {} не найдено!"
window_found = "[✅] | Окно найдено - {}\nНажмите 'q' для паузы."
pause_message = "Пауза \nНажмите снова 'q' что бы продолжить"
continue_message = 'Продолжение работы.'

# Function to get windows with a specific title
def get_windows_with_title(window_title: str):
    window_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    matching_windows = [window for window in window_list if window.get('kCGWindowName', '') == window_title]
    return matching_windows

# Click function using pyautogui for speed
def click(x, y):
    pyautogui.moveTo(x, y)  # Move to the specified position
    pyautogui.click()  # Click at the current position

# Get window name from user
window_name = input(window_input).strip()
window_name = "Telegram" if window_name == '1' else "iMe" if window_name == '2' else window_name

# Find the window
check = get_windows_with_title(window_name)
if not check:
    print(window_not_found.format(window_name))
    sys.exit()
else:
    print(window_found.format(window_name))

telegram_window = check[0]
paused = False

# Keyboard listener for pause/resume functionality
def on_press(key):
    global paused
    if key == Key.alt:
        paused = not paused
        print(pause_message if paused else continue_message)
        time.sleep(0.2)

# Start keyboard listener
listener = Listener(on_press=on_press)
listener.start()

while True:
    if paused:
        continue

    # Get the window rectangle
    window_rect = (
        int(telegram_window['kCGWindowBounds']['X']),
        int(telegram_window['kCGWindowBounds']['Y']),
        int(telegram_window['kCGWindowBounds']['Width']),
        int(telegram_window['kCGWindowBounds']['Height'])
    )

    # Capture the screenshot of the specified window region
    scrn = pyautogui.screenshot(region=window_rect)

    width, height = scrn.size

    # Iterate through pixels with a step to speed up processing
    for x in range(0, width, 10):  # Reduce step size for finer control
        for y in range(0, height, 10):
            r, g, b = scrn.getpixel((x, y))[:3]  # Get RGB values
            if ((b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255))) or (
                    x == 40 and y in range(int(0.81 * height), int(0.88 * height)) and r == 255 and g == 255 and b == 255):
                click(window_rect[0] + x + 4, window_rect[1] + y)
                time.sleep(0.001)  # Optional: small delay to avoid too rapid clicks
                break  # Exit the loop after clicking to avoid multiple clicks on the same element
