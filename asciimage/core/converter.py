import os
import tkinter as tk
from tkinter import filedialog

import numpy as np
from PIL import Image

from InvalidPathException import InvalidPathException

# Constants
ASCII_CHARS = ["@", "#", "+", "*", ".", " "]
THRESHOLDS = [50, 100, 150, 200, 230]


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
    for threshold, char in zip(THRESHOLDS, ASCII_CHARS):
        if pixel_light_value < threshold:
            return char
    return ASCII_CHARS[-1]


def ask_to_save(ascii_result):
    save = input("Do you want to save the ASCII image? (y/n)[default: n] : ")

    if save.lower() == "y":
        save_path = select_save_file()

        if not save_path:
            raise InvalidPathException("No save path selected")

        with open(save_path, "w") as file:
            file.write(ascii_result)
            
        print("ASCII image saved")

    else:
        print("ASCII image not saved")


def select_save_file():
    initialdir = os.path.join(os.path.dirname(__file__), '..', '..', 'texts')
    save_path = filedialog.asksaveasfilename(
        title="Save the ASCII Image",
        filetypes=[("Text Files", "*.txt")],
        initialdir=initialdir
    )
    return save_path


def display_ascii_image(ascii_array):
    ascii_result = "\n".join("".join(row) for row in ascii_array)
    print(ascii_result)
    ask_to_save(ascii_result)


def convert_image(image_path):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    image_array = np.array(image)
    ascii_array = np.zeros((height, width), dtype=str)

    for i in range(height):
        for j in range(width):
            r, g, b, a = image_array[i, j]
            if a < 128:
                ascii_array[i, j] = " "
            else:
                pixel_light_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                ascii_array[i, j] = pixel_to_ascii(pixel_light_value)

    return ascii_array


if __name__ == "__main__":
    try:
        selected_image = select_image()
        converted_image = convert_image(selected_image)
        display_ascii_image(converted_image)
    except InvalidPathException as e:
        print(e.message)
        exit()
