import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import requests
import locale
import sys
import os
import platform
import subprocess
import webbrowser
import threading

VERSION = '2.0'

GITHUB_REPO_OWNER = 'bartekl1'
GITHUB_REPO_NAME = 'CountdownToElephantDayDesktop'

POLISH_TEXT = [
    'Odliczanie do Dnia Słonia',
    'Dzisiaj:',
    'Dzień Słonia:',
    'Pozostało:',
    'dni',
    'dzień',
    'godzin',
    'godziny',
    'godzina',
    'minut',
    'minuty',
    'minuta',
    'sekund',
    'sekundy',
    'sekunda',
    'milisekund'
]

ENGLISH_TEXT = [
    'Countdown to Elephant Day',
    'Today:',
    'Elephant Day:'
    'Left:',
    'days',
    'day',
    'hours',
    'hours',
    'hour',
    'minutes',
    'minutes',
    'minute',
    'seconds',
    'seconds',
    'second',
    'milliseconds'
]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_text(text_number):
    if language == 'pl_PL':
        return POLISH_TEXT[text_number]
    else:
        return ENGLISH_TEXT[text_number]


def get_setting(name):
    return {
        'background_color': '#9acd32',
        'title_color': '#0000ff',
        'date_title_color': '#0000ff',
        'date_color': '#0000ff',
        'left_header_color': '#0000ff',
        'countdown_text_color': '#000072',
        'countdown_background_color': '#007a00',
        'countdown_border_width': 5,
        'countdown_border_style': 'solid',
        'unit_labels_color': '#0000ff'
    }[name]


def main():
    global language, window

    windll = ctypes.windll.kernel32
    language = locale.windows_locale[windll.GetUserDefaultUILanguage()]

    window = tk.Tk()

    window.minsize(448, 630)

    window.title(get_text(0))
    window.iconbitmap(resource_path('img/elephant.ico'))

    window.config(bg=get_setting('background_color'))

    gui_frame = tk.Frame(window, background=get_setting('background_color'))
    gui_frame.pack()

    title_frame = tk.Frame(
        gui_frame, background=get_setting('background_color'))
    title_frame.pack()

    title_label = tk.Label(
        title_frame,
        text=get_text(0),
        background=get_setting('background_color'),
        foreground=get_setting('title_color'),
        font=('Segoe UI', 26)
    )
    title_label.pack(side='left')

    icon_img = ImageTk.PhotoImage(Image.open(
        resource_path('img/elephant.png')).resize((40, 40)))
    icon_label = tk.Label(
        title_frame,
        image=icon_img,
        background=get_setting('background_color')
    )
    icon_label.pack(side='left')

    today_title_label = tk.Label(
        gui_frame,
        text=get_text(1),
        background=get_setting('background_color'),
        foreground=get_setting('date_title_color'),
        font=('Segoe UI', 12, 'bold')
    )
    today_title_label.pack()

    today_label = tk.Label(
        gui_frame,
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    today_label.pack()

    elephant_day_title_label = tk.Label(
        gui_frame,
        text=get_text(2),
        background=get_setting('background_color'),
        foreground=get_setting('date_title_color'),
        font=('Segoe UI', 12, 'bold')
    )
    elephant_day_title_label.pack()

    elephant_day_label = tk.Label(
        gui_frame,
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    elephant_day_label.pack()

    left_header_label = tk.Label(
        gui_frame,
        text=get_text(3),
        background=get_setting('background_color'),
        foreground=get_setting('left_header_color'),
        font=('Segoe UI', 18)
    )
    left_header_label.pack()

    days_countdown = tk.Label(
        gui_frame,
        background=get_setting('countdown_background_color'),
        foreground=get_setting('countdown_text_color'),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=get_setting('countdown_border_width'),
        relief=get_setting('countdown_border_style')
    )
    days_countdown.pack()

    days_label = tk.Label(
        gui_frame,
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    days_label.pack()

    hours_countdown = tk.Label(
        gui_frame,
        background=get_setting('countdown_background_color'),
        foreground=get_setting('countdown_text_color'),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=get_setting('countdown_border_width'),
        relief=get_setting('countdown_border_style')
    )
    hours_countdown.pack()

    hours_label = tk.Label(
        gui_frame,
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    hours_label.pack()

    minutes_countdown = tk.Label(
        gui_frame,
        background=get_setting('countdown_background_color'),
        foreground=get_setting('countdown_text_color'),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=get_setting('countdown_border_width'),
        relief=get_setting('countdown_border_style')
    )
    minutes_countdown.pack()

    minutes_label = tk.Label(
        gui_frame,
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    minutes_label.pack()

    seconds_countdown = tk.Label(
        gui_frame,
        background=get_setting('countdown_background_color'),
        foreground=get_setting('countdown_text_color'),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=get_setting('countdown_border_width'),
        relief=get_setting('countdown_border_style')
    )
    seconds_countdown.pack()

    seconds_label = tk.Label(
        gui_frame,
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    seconds_label.pack()

    milliseconds_countdown = tk.Label(
        gui_frame,
        background=get_setting('countdown_background_color'),
        foreground=get_setting('countdown_text_color'),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=get_setting('countdown_border_width'),
        relief=get_setting('countdown_border_style')
    )
    milliseconds_countdown.pack()

    milliseconds_label = tk.Label(
        gui_frame,
        text=get_text(15),
        background=get_setting('background_color'),
        foreground=get_setting('date_color'),
        font=('Segoe UI', 12)
    )
    milliseconds_label.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
