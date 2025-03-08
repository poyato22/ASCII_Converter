from PIL import Image, ImageDraw, ImageFont
from tkinter import scrolledtext
import tkinter.font as tkFont
import tkinter as tk
import numpy as np
import cv2

# ASCII characters
ASCII_CHARS =  ascii_chars = [
    ' ', '.', '`', '¨', ',', '˚', ':', "'", '-', ';', '*', '"', '•', '_', '\\', '/', '~', 'i', '¬', '^', 'º', '!', '¡', 
    'r', 'l', 'ª', '|', '<', '>', '(', ')', '+', '«', 'j', '1', 't', '=', 'v', 'f', '}', '{', '?', ']', '7', '∞', '[', 
    'x', 'n', 'u', 'y', 'z', '†', 's', 'k', 'o', '∂', 'h', '4', 'π', '™', '3', '2', 'e', 'a', '¢', 'q', 'd', 'p', 'b', 
    '5', '0', 'w', 'å', 'ß', '6', '9', 'm', '8', '#', 'g', '$', '%', '&', '@',
    'ʳ', 'ʲ', 'ᴥ', 'ʰ', 'ȷ', 'ᴎ', '﹋', 'ⁱ', '₁', '˙', '̀', '⁰', '⁺', 'ᵢ', 'ᵈ', '₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉', '╲', '✿', '✪', '✯', '✷', '✵']


def measure_darkness(char=" "):
    image_size = (100, 100)
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    
    image = Image.new('RGB', image_size, background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/Library/Fonts/Monaco.ttf", 80)

    text_position = (10, 10)
    draw.text(text_position, char, font=font, fill=text_color)

    image = image.convert('L')
    image_np = np.array(image)
    _, binary_image = cv2.threshold(image_np, 128, 255, cv2.THRESH_BINARY_INV)
    dark_pixel_count = np.sum(binary_image == 255)

    return dark_pixel_count

def sort():
    sorted_dict = {}
    for char in ASCII_CHARS:
        dark_pixels = measure_darkness(char)
        sorted_dict[char] = int(dark_pixels)

    sorted_items = sorted(sorted_dict.items(), key=lambda item: item[1])
    sorted_dict = dict(sorted_items)
    return sorted_dict

def convert(frame, new_width=100):
    alpha = 1.0  # Simple contrast control (>1 increases contrast)
    beta = -30    # Simple brightness control (0 means no change)

    high_contrast_image = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    gray_frame = cv2.cvtColor(high_contrast_image, cv2.COLOR_BGR2GRAY)
    height, width = gray_frame.shape
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_frame = cv2.resize(gray_frame, (new_width, new_height))

    pixels = np.array(resized_frame)
    ascii_chars = list(sort())

    ascii_image = ""
    for y in range(new_height):
        for x in range(new_width):
            pixel_intensity = pixels[y, x]
            ascii_index = int((pixel_intensity / 255) * (len(ascii_chars) - 1))
            ascii_index = max(0, min(ascii_index, len(ascii_chars) - 1))  
            ascii_image += ascii_chars[ascii_index]
        ascii_image += "\n"
    
    return ascii_image, new_width, new_height

def display(window, text_area, cap, width):
    ret, frame = cap.read()

    if ret:
        frame = cv2.flip(frame, 1)

        ascii_image, new_width, new_height = convert(frame, width)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, ascii_image)

    window.after(100, display, window, text_area, cap, width)


def loop(phase):
    window = tk.Tk()
    window.title("Camera ASCII Art")

    if phase == 1:
        custom_font = tkFont.Font(family="Monaco", size=12)
        width = 1141
        height = 874
        char_width = 160

    elif phase == 1:
        custom_font = tkFont.Font(family="Monaco", size=7)
        width = 1269
        height = 1017
        char_width = 300

    elif phase == 4:
        custom_font = tkFont.Font(family="Monaco", size=24)
        width = 1463
        height = 1036
        char_width = 100

    elif phase == 3:
        custom_font = tkFont.Font(family="Monaco", size=3)
        width = 1282
        height = 960
        char_width = 700

    else:
        print('error')
        custom_font = tkFont.Font(family="Monaco", size=7)
        width = 1269
        height = 1017
        char_width = 300

    text_area = scrolledtext.ScrolledText(window, wrap=tk.NONE, font=custom_font, width=width, height=height)
    window.geometry(f"{width}x{height}")
    text_area.pack(expand=True, fill='both')
    text_area.update_idletasks()

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Cannot access camera")
        return

    window.after(100, display, window, text_area, cap, char_width)
    window.mainloop()

    cap.release()

#1, 2, 3, 4
loop(1)
