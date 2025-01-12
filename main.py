import pygetwindow as gw
import mss
import cv2
import numpy as np
import win32gui
import win32con
import pyautogui
import keyboard
import threading
from time import sleep, time
import matplotlib.pyplot as plt

PROGRAM_NAME = "Fusion 3.64 - SegaCD - Penn & Teller's Smoke and Mirrors"
DEFAULT_POINT = (160, 370)

keys_to_map = [
    "up",  # to up
    "down", # to down
    "left", # to left
    "right", # to right
    "a", # to a
    "b", # to b
    "c", # to c
    "enter", # to start
    "x", # to x
    "y", # to y
    "z", # to z
    "ctrl", # to mode
]

def get_screenshot(bbox):
    with mss.mss() as sct:
        screenshot = sct.grab(bbox)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        return img

def get_closest_point(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_yellow = np.array([20, 120, 150])
    upper_yellow = np.array([30, 180, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    countours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contour = max(countours, key=cv2.contourArea)
    # print(yellow_contour)

    # plt.imshow(mask)
    # plt.show()

    start_point = (160,370)

    image_height = img.shape[0]

    min_y_threshold = image_height * 0.5
    bottom_contour_points = [tuple(point[0]) for point in yellow_contour if point[0][1] > min_y_threshold]
    # print(bottom_contour_points)

    min_distance = float("inf")
    closest_point = None

    for contour_point in bottom_contour_points:
        distance = np.sqrt((start_point[0] - contour_point[0])**2 + (start_point[1] - contour_point[1])**2)
        #print(distance)
        if distance < min_distance:
            min_distance = distance
            closest_point = contour_point

    #print(closest_point)
    return closest_point

def get_side_of_closest_point(next_point):
    return "right" if next_point[0] > DEFAULT_POINT[0] else "left"

def stering_wheel_control(side):
    if side == "left":
        pyautogui.press('pause')
        # hold_key('enter', 2)
        return

def hold_key(key, hold_time):
    start_time = time()

    while time() - start_time < hold_time:
        pyautogui.press(key)


def controler_bus():

    
    start = input("Press Enter to start the game or any key to quit: ")
    if start != "":
        return

    print("Starting the game - Press Q to quit")

    windows = gw.getWindowsWithTitle(PROGRAM_NAME)
    if len(windows) > 1:
        print("Multiple windows found")
        return
    
    window = windows[0]
    windows = gw.getWindowsWithTitle(PROGRAM_NAME)
    hwnd = win32gui.FindWindow(None, PROGRAM_NAME)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    pyautogui.press('pause')
    win32gui.SetForegroundWindow(hwnd)
    sleep(0.5)

    bbox = {
        "top": window.top,
        "left": window.left,
        "width": window.width,
        "height": window.height 
    }

    if len(windows) == 0:
        print("Window not found")
        return

    threading.Thread(target=hold_key_a).start()

    for i in range(3):
        print("Starting in ", 3-i)
        sleep(1)

    while True:
        try:
            img = get_screenshot(bbox)
            close_points = get_closest_point(img)
            side = get_side_of_closest_point(close_points)
            print(side)
            if side == "left":
                left_wheel()
            # stering_wheel_control(side)
            sleep(3)

            if keyboard.is_pressed('q'):
                break

        except Exception as e:
            print("Error occured: ", e)

def left_wheel():
    keyboard.press('left')
    sleep(1)
    keyboard.release('left')

def map_controls(): 
    print("Mapping the keys")
    print("Open the emulator and click and Set Config --> Controllers")
    sleep(0.1)
    print("Port 1 --> 6 Btn Pad")
    choice = input("Press Enter to continue or Q to quit: ")

    if choice == 'Q':
        return
    if choice == '':
        print("Mapping automatic")
        print("Press Define")
        for i in range(3):
            print("Starting in ", 3-i)
            sleep(1)
        
        for key in keys_to_map:
            keyboard.press(key)
            sleep(0.3)
            keyboard.release(key)
            print("Key Mapped: ", key)

def manual_control():
    print("Press the key to control emulator")
    print("Press Q to quit")
    while True:
        key = keyboard.read_key()
        print("Key Pressed: ", key)
        if key == 'Q' or key == 'q':
            break
        keyboard.press(key)
        sleep(0.3)
        keyboard.release(key)


def hold_key_a():
    while True:
        keyboard.press('a')
        sleep(0.1)
        keyboard.release('a')
        if keyboard.is_pressed('q'):
            break


if __name__ == "__main__":
    print(" --------- Starting Desert Bus Controller --------- ")
    print()
    #map_controls()
    #manual_control()
    #controler_bus()
    # threading.Thread(target=hold_key_a).start()

    # while True:
    #     left_wheel()

    while True:
        choice = input("""
        1: Automatic Control
        2: Manual Control
        3: Map the keys

        Q: Quit

        Please enter your choice: """)

        if choice == '1':
            controler_bus()
        if choice == '2':
            manual_control()
        if choice == '3':
            map_controls()
        if choice == 'Q' or choice == 'q':
            break

    


#     sleep(2)
#     # print("0")
#     # press_pause_key()
#     # print("1")
#     # press_key_using_win()
#     # print("2")
#     # # press_key_using_win()
#     # press_left_pypunt_key()
#     print("3")aaa
#     # left_wheel()
#     press_up_down_using_keyboard()
# #    main()