import os
import tkinter as tk
from tkinter import filedialog

import numpy as np
from PIL import Image

from InvalidPathException import InvalidPathException


# Functions
def select_image():
    root = tk.Tk()
    root.withdraw()

    initialdir = os.path.join(os.path.dirname(__file__), '..', '..', 'images')
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")],
        initialdir=initialdir
    )

    if not image_path:
        raise InvalidPathException("No image selected")

    return image_path


def pixel_to_ascii(pixel_light_value):
    if pixel_light_value >= 230:
        return " "
    elif pixel_light_value >= 200:
        return "."
    elif pixel_light_value >= 150:
        return "*"
    elif pixel_light_value >= 100:
        return "+"
    elif pixel_light_value >= 50:
        return "#"
    else:
        return "@"


def ask_to_save(ascii_result):
    save = input("Do you want to save the ASCII image? (y/n)[default: n] : ")
    try:
        if save.lower() == "y":
            initialdir = os.path.join(os.path.dirname(__file__), '..', '..', 'texts')
            save_path = filedialog.asksaveasfilename(
                title="Save the ASCII Image",
                filetypes=[("Text Files", "*.txt")],
                initialdir=initialdir
            )

            if not save_path:
                raise InvalidPathException("No save path selected")

            with open(save_path, "w") as file:
                file.write(ascii_result)

            print("ASCII image saved")
        else:
            print("ASCII image not saved")
    except InvalidPathException as e:
        print(e.message)
        exit()


def show_ascii_image(ascii_array):
    ascii_result = ""
    for row in ascii_array:
        ascii_result = ascii_result + "".join(row) + "\n"
    ascii_result = ascii_result[:-1]  # Remove the last newline character

    print(ascii_result)
    ask_to_save(ascii_result)


def convert_image(image_path):
    image = Image.open(image_path).convert("RGBA")  # Open in RGBA mode to access alpha channel

    width, height = image.size

    image_array = np.array(image)
    ascii_array = np.zeros((height, width), dtype=str)

    for i in range(height):
        for j in range(width):
            r, g, b, a = image_array[i, j]
            if a < 128:  # If alpha value is less than 128, then it is transparent.
                ascii_array[i, j] = " "
            else:
                # Convert to grayscale using the luminosity method
                pixel_light_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                ascii_array[i, j] = pixel_to_ascii(pixel_light_value)

    return ascii_array


# Main

if __name__ == "__main__":
    try:
        selected_image = select_image()
    except InvalidPathException as e:
        print(e.message)
        exit()

    converted_image = convert_image(selected_image)

    show_ascii_image(converted_image)
