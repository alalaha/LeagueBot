import pyautogui
import pydirectinput
import time
import os
import sys
import winsound
import ctypes
import random

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

from pynput.mouse import Button, Controller
Mouse = Controller

from pynput.keyboard import Key, Controller
Keyboard = Controller

dir_path = os.path.dirname(os.path.realpath(__file__))
sep = os.sep
screenshots_folder = dir_path + sep + "screenshots" + sep
screen_dim = pyautogui.size()

lower_half_screen = (0, int(screen_dim[1]/2), screen_dim[0], int(screen_dim[1]/2))
centre_screen = (int(screen_dim[0]/3), int(screen_dim[1]/3), int(screen_dim[0]/3), int(screen_dim[1]/3))

camera_positions = {1: (1707, 925),
    2: (1714, 948),
    3: (1780, 991),
    4: (1800, 1038),
    }

camps = {
    "b_gromp": [1, (334, 503)],
    "b_blue": [1, (1466, 802)],
    "b_wolves": [2, (1183, 886)],
    "b_chickens": [3, (683, 95)],
    "b_red": [3, (1322, 806)],
    "b_krugs": [4, (963, 89)],
    }

"""sensor function determining the mouse position
    @param duration: How long the sensor function ought to print out the
    position of my mouse for.
"""
def mouseposition(duration):
    t = 0
    for i in range(duration*5 + 1):
        print( "["+ str((t//0.1)/10) + "] location is: ", end="")
        print(pyautogui.position())
        time.sleep(1/5)
        t += 0.2

""" sensor function determining the mouse position as a set of ratios
    @param duration: how long the sensor funtion ought to print out for
"""
def mouseposition_ratio(duration):
    t = 0
    for i in range(duration*5 + 1):
        print( "["+ str((t//0.1)/10) + "] location is: ", end="")
        x, y = pyautogui.position()
        print((x/screen_dim[0], y/screen_dim[1]))
        time.sleep(1/5)
        t += 0.2

"""clicks the image if it's there, does nothing  if it's not
    @param location: the address+name of the image we're looking for
    @param con: the pyautogui's confidence variable
    @return Tuple representing the (x, y) value of the image on screen

"""
def click_image(location, con=0.9):
    spot = pyautogui.locateCenterOnScreen(location, confidence=con)
    if spot:
        # time.sleep(0.05)
        pyautogui.moveTo(spot)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
    return spot

"""Waits until the specified image appears on screen, throws exception
    if image not found within specified duration (or time up)
    @param image: The address+name of the image we're looking for
    @param wait_duration: the amount of time we are checking for
    @param con: pyautogui's confidence variable
    @param reg: region of which we are looking for the image
    @exception raised if the image is not found.
"""
def wait_until_appears(image, wait_duration=10, con=1, reg=None):
    char_ind = -1
    image_name = ""
    while image[char_ind] != sep:
        image_name = image[char_ind] + image_name
        char_ind -= 1

    if reg == None:
        reg = (0, 0) + pyautogui.size()

    been_found = False
    for i in range(wait_duration*2):
        print("###### Looking for [" + image_name + "] ######")
        if pyautogui.locateOnScreen(image, confidence=con, region=reg):
            been_found = True
            break;
        time.sleep(0.5)

    if not been_found:
        raise Exception("Image not found")

"""Waits until the one of the images in the image_lst appears, does
    not throw any exceptions
    @param image_lst: A list of images (their addresses) that we are looking for
    @param wait_duration: the amount of time we are checking for
    @param con: pyautogui's confidence variable
    @param reg: region of which we are looking for the image
    @return Boolean representing whether it found an image
"""
def wait_until_one_appears(image_lst, wait_duration=10, con=1, reg= None):
    if reg == None:
        reg = (0, 0) + pyautogui.size()

    been_found = False
    for i in range(wait_duration*2):
        for image in image_lst:
            char_ind = -1
            image_name = ""
            while image[char_ind] != sep:
                image_name = image[char_ind] + image_name
                char_ind -= 1
            print(">>>>>> Looking for [" + image_name + "] <<<<<<")
            location = pyautogui.locateOnScreen(image, confidence=con, region=reg)
            if location:
                been_found = True
                break;
        if been_found:
            break;
        time.sleep(0.5)
    return been_found

"""Function checking whether and image appeared on screen within indicated duration
    @param image: the full address+name of the image we are looking for
    @param check_duration: The amount of time we should be checking for this image in seconds
    @param con: pyautogui's confidence variable
    @param reg: the region of which we should search for the image
    @return Boolean representing whether the image appeared on-screen in that duration
"""
def check_if_appears(image, check_duration=10, con=1, reg=None):
    if reg == None:
        reg = (0, 0) + pyautogui.size()

    been_found = False
    for i in range(check_duration):
        print("######checking for {}######".format(image))
        if pyautogui.locateOnScreen(image, confidence=con, region=reg):
            been_found = True
            break;
        time.sleep(0.5)
    return been_found

"""A function returning a position object (which is represented as a list of 2 items [x, y])
    @param x_ratio: a ratio betwee 0-1 that represents the x position of the mouse on the screen
    @param y_ratio: a ratio betwee 0-1 that represents the y position of the mouse on the screen
    @return a tuple with the [x, y] of the intended mouse position
"""
def position(x_ratio, y_ratio):
    return (x_ratio*screen_dim, y_ratio*screen_dim)


def tab_into_league(tabbed_in = True):
    icon_location = pyautogui.locateCenterOnScreen(screenshots_folder + "taskbar" + sep + "Capture.jpg", confidence=0.9)
    if icon_location and tabbed_in:
        # print("FOUND IT")
        pyautogui.click(icon_location)
        return True
    else:
        # print("Couldn't find it")
        return False

def left_click():
    mouse_controller = Mouse()
    mouse_controller.press(Button.left)
    mouse_controller.release(Button.left)
    time.sleep(0.1)

def right_click():
    mouse_controller = Mouse()
    mouse_controller.press(Button.right)
    mouse_controller.release(Button.right)
    time.sleep(0.1)

def do_camp(camp_name):
    pyautogui.moveTo(camera_positions[camps[camp_name][0]])
    left_click()
    pyautogui.moveTo(camps[camp_name][1])
    right_click()

def alt_tab(perform=True):
    if perform:
        pyautogui.keyDown('alt')
        pyautogui.keyDown('tab')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('tab')
        pyautogui.mouseUp()
