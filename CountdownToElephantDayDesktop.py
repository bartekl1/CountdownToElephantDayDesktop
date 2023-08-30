import tkinter as tk
from tkinter import messagebox
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
import pytz
import tzlocal
import datetime
from babel.dates import format_date

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
    'milisekund',
    'Zakończ',
    'Plik',
    'Informacje',
    'Repozytorium GitHub',
    'Sprawdź aktualizacje',
    'Pomoc',
    'Autor',
    'Wersja'
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
    'milliseconds',
    'Exit',
    'File',
    'Information',
    'GitHub repository',
    'Check updates',
    'Help',
    'Author',
    'Version'
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


def countdown():
    now = datetime.datetime.now(tz)

    if now.month == 8 and now.day == 12:
        elephant_day = datetime.datetime(now.year, 8, 12)

        days_countdown.config(text=0)
        hours_countdown.config(text=0)
        minutes_countdown.config(text=0)
        seconds_countdown.config(text=0)
        milliseconds_countdown.config(text=0)

        days_label.config(text=get_text(4))
        hours_label.config(text=get_text(6))
        minutes_label.config(text=get_text(9))
        seconds_label.config(text=get_text(12))
    else:
        if now.month < 8 or (now.month == 8 and now.day < 12):
            elephant_day = datetime.datetime(now.year, 8, 12)
        else:
            elephant_day = datetime.datetime(now.year + 1, 8, 12)

        elephant_day = tz.localize(elephant_day)

        delta = elephant_day - now

        left_days = delta.days
        left_hours = delta.seconds // (60 ** 2)
        left_minutes = delta.seconds % (60 ** 2) // 60
        left_seconds = delta.seconds % (60 ** 2) % 60
        left_milliseconds = delta.microseconds // 1000

        days_countdown.config(text=left_days)
        hours_countdown.config(text=left_hours)
        minutes_countdown.config(text=left_minutes)
        seconds_countdown.config(text=left_seconds)
        milliseconds_countdown.config(text=left_milliseconds)

        if left_days == 1:
            days_label.config(text=get_text(5))
        else:
            days_label.config(text=get_text(4))

        if left_hours == 1:
            hours_label.config(text=get_text(8))
        elif (len(str(left_hours)) > 1 and
                str(left_hours)[-1] in ['2', '3', '4'] and
                str(left_hours)[-2] != '1') or \
            (len(str(left_hours)) == 1 and
             str(left_hours) in ['2', '3', '4']):
            hours_label.config(text=get_text(7))
        else:
            hours_label.config(text=get_text(6))

        if left_minutes == 1:
            minutes_label.config(text=get_text(11))
        elif (len(str(left_minutes)) > 1 and
                str(left_minutes)[-1] in ['2', '3', '4'] and
                str(left_minutes)[-2] != '1') or \
            (len(str(left_minutes)) == 1 and
             str(left_minutes) in ['2', '3', '4']):
            minutes_label.config(text=get_text(10))
        else:
            minutes_label.config(text=get_text(9))

        if left_seconds == 1:
            seconds_label.config(text=get_text(14))
        elif (len(str(left_seconds)) > 1 and
                str(left_seconds)[-1] in ['2', '3', '4'] and
                str(left_seconds)[-2] != '1') or \
            (len(str(left_seconds)) == 1 and
             str(left_seconds) in ['2', '3', '4']):
            seconds_label.config(text=get_text(13))
        else:
            seconds_label.config(text=get_text(12))

    now_date = format_date(
        now,
        format='full',
        locale=language) + ' ' + now.strftime('%H:%M:%S')
    elephant_day_date = format_date(
        elephant_day,
        format='full',
        locale=language)

    today_label.config(text=now_date)
    elephant_day_label.config(text=elephant_day_date)

    window.after(50, countdown)

def info():
    information = f'''Countdown To Elephant Day Desktop
{get_text(22)}: @{GITHUB_REPO_OWNER}
{get_text(23)}: {VERSION}'''
    messagebox.showinfo(title=get_text(18), message=information)

def github_repo():
    webbrowser.open(
        f'https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}',
        new=2)


def main():
    global language, window, gui_frame, title_frame, title_label, icon_label, \
        today_title_label, today_label, elephant_day_title_label, \
        elephant_day_label, left_header_label, days_countdown, days_label, \
        hours_countdown, hours_label, minutes_countdown, minutes_label, \
        seconds_countdown, seconds_label, milliseconds_countdown, \
        milliseconds_label, tz

    windll = ctypes.windll.kernel32
    language = locale.windows_locale[windll.GetUserDefaultUILanguage()]

    tz_name = tzlocal.get_localzone_name()
    tz = pytz.timezone(tz_name)

    window = tk.Tk()

    window.minsize(448, 630)

    window.title(get_text(0))
    window.iconbitmap(resource_path('img/elephant.ico'))

    window.config(bg=get_setting('background_color'))

    menu = tk.Menu(window)
    window.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label=get_text(16), command=window.destroy)
    menu.add_cascade(label=get_text(17), menu=file_menu)

    help_menu = tk.Menu(menu, tearoff=0)
    help_menu.add_command(label=get_text(18), command=info)
    help_menu.add_command(label=get_text(19), command=github_repo)
    help_menu.add_separator()
    help_menu.add_command(label=get_text(20), command=None)
    menu.add_cascade(label=get_text(21), menu=help_menu)

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

    window.after(50, countdown)

    window.mainloop()


if __name__ == '__main__':
    main()
