import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageTk

from babel.dates import format_date
import requests
import pytz
import tzlocal

import ctypes
import locale
import sys
import os
import platform
import webbrowser
import threading
import datetime
import json

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
    'Wersja',
    'Błąd',
    'Nie udało się sprawdzić dostępności aktualizacji.',
    'Aktualizacja',
    'Masz najnowszą wersję.',
    'Dostępna jest aktualizacja.',
    'Bieżąca wersja',
    'Najnowsza wersja',
    'wydana',
    'Czy chcesz ją pobrać?',
    'Pełny ekran',
    'Okno',
    'Zawsze na wierzchu',
    'Przezroczystość',
    'Góra',
    'Dół',
    'Lewo',
    'Prawo',
    'Lewy górny róg',
    'Prawy górny róg',
    'Lewy dolny róg',
    'Prawy dolny róg',
    'Środek',
    'Kierunek przyciągania',
    'Widok',
    'Kolor tła okna',
    'Przezroczyste tło okna',
    'Kolor tytułu',
    'Kolor etykiet dat',
    'Kolor dat',
    'Kolor nagłówka "Pozostało:"',
    'Kolor etykiet jednostek czasu',
    'Kolor tekstu odliczania',
    'Kolor tła odliczania',
    'Wybierz kolor'
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
    'Version',
    'Can\'t check for updates.',
    'Update',
    'Your version is up to date.'
    'An update is available.',
    'Current version',
    'Latest version',
    'released',
    'Do you want to download it?',
    'Full screen',
    'Window',
    'Always on top',
    'Transparency'
    'Top',
    'Bottom',
    'Left',
    'Right',
    'Top left',
    'Top right',
    'Bottom left',
    'Bottom right',
    'Center',
    'Snap direction',
    'View',
    'Window background color',
    'Transparent window background',
    'Title color',
    'Date labels colors',
    'Dates colors',
    'Header "Left:" color',
    'Time unit labels color',
    'Countdown text color',
    'Countdown background color',
    'Chose color'
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


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)

    return tuple(rgb)


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


def check_for_updates(information=True):
    fp = os.path.join(os.environ.get('APPDATA'),
                      GITHUB_REPO_OWNER, GITHUB_REPO_NAME,
                      'cache_newest_version.json')

    if os.path.isfile(fp):
        with open(fp) as file:
            newest_version = json.load(file)
        headers = {'If-None-Match': newest_version['etag']}
    else:
        headers = {}

    try:
        r = requests.get(
            f'https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases/latest',
            headers=headers)
    except Exception:
        if information:
            messagebox.showerror(get_text(24), get_text(25))
    else:
        if r.status_code == 200:
            rj = r.json()

            newest_version = {
                'version': rj['name'],
                'description': rj['body'],
                'published_at': rj['published_at'],
                'etag': r.headers.get('etag')
            }

            with open(fp, 'w') as file:
                json.dump(newest_version, file, indent=4)
        elif r.status_code == 304:
            with open(fp) as file:
                newest_version = json.load(file)
        else:
            newest_version = None

        if newest_version is None:
            if information:
                messagebox.showerror(get_text(24), get_text(25))
        elif VERSION == newest_version['version']:
            if information:
                messagebox.showinfo(get_text(26), get_text(27))
        else:
            release_date_dt = datetime.datetime.fromisoformat(
                newest_version['published_at'])
            release_date = format_date(
                release_date_dt,
                format='full',
                locale=language) + ' ' + release_date_dt.strftime('%H:%M:%S')
            update_info = f'''{get_text(28)}
{get_text(29)}: {VERSION}
{get_text(30)}: {newest_version['version']} ({get_text(31)} {release_date})
{get_text(32)}'''
            response = messagebox.askyesno(get_text(26), update_info)

            if response:
                webbrowser.open(
                    f'https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases/latest',
                    new=2)


def full_screen():
    window.attributes('-fullscreen', full_screen_var.get())


def always_on_top():
    window.attributes('-topmost', always_on_top_var.get())


def transparency():
    window.attributes('-alpha', 1 - transparency_var.get())


def snap_direction():
    gui_frame.place_forget()

    relx = {
        'n': 0.5,
        's': 0.5,
        'w': 0,
        'e': 1,
        'nw': 0,
        'ne': 1,
        'sw': 0,
        'se': 1,
        'center': 0.5
    }
    rely = {
        'n': 0,
        's': 1,
        'w': 0.5,
        'e': 0.5,
        'nw': 0,
        'ne': 0,
        'sw': 1,
        'se': 1,
        'center': 0.5
    }

    gui_frame.place(relx=relx[snap_direction_var.get()],
                    rely=rely[snap_direction_var.get()],
                    anchor=snap_direction_var.get())


def change_color(element):
    if element == 'background':
        initial_color = background_color_var.get()
    elif element == 'title':
        initial_color = title_color_var.get()
    elif element == 'date_title':
        initial_color = date_title_color_var.get()
    elif element == 'date':
        initial_color = date_color_var.get()
    elif element == 'left_header':
        initial_color = left_header_color_var.get()
    elif element == 'countdown_text':
        initial_color = countdown_text_color_var.get()
    elif element == 'countdown_background':
        initial_color = countdown_background_color_var.get()
    elif element == 'unit_labels':
        initial_color = unit_labels_color_var.get()

    color = colorchooser.askcolor(title=get_text(57),
                                  initialcolor=initial_color)

    if color[1] is not None:
        if element == 'background':
            background_color_var.set(color[1])
            transparent_background_var.set(False)

            window.config(bg=color[1])
            gui_frame.config(bg=color[1])
            title_frame.config(bg=color[1])
            title_label.config(bg=color[1])
            icon_label.config(bg=color[1])
            today_title_label.config(bg=color[1])
            today_label.config(bg=color[1])
            elephant_day_title_label.config(bg=color[1])
            elephant_day_label.config(bg=color[1])
            left_header_label.config(bg=color[1])
            days_label.config(bg=color[1])
            hours_label.config(bg=color[1])
            minutes_label.config(bg=color[1])
            seconds_label.config(bg=color[1])
            milliseconds_label.config(bg=color[1])
        elif element == 'title':
            title_color_var.set(color[1])

            title_label.config(fg=color[1])
        elif element == 'date_title':
            date_title_color_var.set(color[1])

            today_title_label.config(fg=color[1])
            elephant_day_title_label.config(fg=color[1])
        elif element == 'date':
            date_color_var.set(color[1])

            today_label.config(fg=color[1])
            elephant_day_label.config(fg=color[1])
        elif element == 'left_header':
            left_header_color_var.set(color[1])

            left_header_label.config(fg=color[1])
        elif element == 'unit_labels':
            unit_labels_color_var.set(color[1])

            days_label.config(fg=color[1])
            hours_label.config(fg=color[1])
            minutes_label.config(fg=color[1])
            seconds_label.config(fg=color[1])
            milliseconds_label.config(fg=color[1])
        elif element == 'countdown_text':
            countdown_text_color_var.set(color[1])

            days_countdown.config(fg=color[1])
            hours_countdown.config(fg=color[1])
            minutes_countdown.config(fg=color[1])
            seconds_countdown.config(fg=color[1])
            milliseconds_countdown.config(fg=color[1])
        elif element == 'countdown_background':
            countdown_background_color_var.set(color[1])

            days_countdown.config(bg=color[1])
            hours_countdown.config(bg=color[1])
            minutes_countdown.config(bg=color[1])
            seconds_countdown.config(bg=color[1])
            milliseconds_countdown.config(bg=color[1])


def transparent_background():
    if transparent_background_var.get():
        color = '#fefefe'

        while True:
            if color in [title_color_var.get(),
                         date_title_color_var.get(),
                         date_color_var.get(), left_header_color_var.get(),
                         countdown_text_color_var.get(),
                         countdown_background_color_var.get(),
                         unit_labels_color_var.get()]:
                rgb = hex_to_rgb(color[1:])
                color = rgb_to_hex(rgb[0] - 1, rgb[1] - 1, rgb[2] - 1)
            else:
                break

        window.config(bg=color)
        gui_frame.config(bg=color)
        title_frame.config(bg=color)
        title_label.config(bg=color)
        icon_label.config(bg=color)
        today_title_label.config(bg=color)
        today_label.config(bg=color)
        elephant_day_title_label.config(bg=color)
        elephant_day_label.config(bg=color)
        left_header_label.config(bg=color)
        days_label.config(bg=color)
        hours_label.config(bg=color)
        minutes_label.config(bg=color)
        seconds_label.config(bg=color)
        milliseconds_label.config(bg=color)

        window.wm_attributes('-transparentcolor', color)
    else:
        color = background_color_var.get()

        window.config(bg=color)
        gui_frame.config(bg=color)
        title_frame.config(bg=color)
        title_label.config(bg=color)
        icon_label.config(bg=color)
        today_title_label.config(bg=color)
        today_label.config(bg=color)
        elephant_day_title_label.config(bg=color)
        elephant_day_label.config(bg=color)
        left_header_label.config(bg=color)
        days_label.config(bg=color)
        hours_label.config(bg=color)
        minutes_label.config(bg=color)
        seconds_label.config(bg=color)
        milliseconds_label.config(bg=color)

        window.wm_attributes('-transparentcolor', None)


def main():
    global language, window, gui_frame, title_frame, title_label, icon_label, \
        today_title_label, today_label, elephant_day_title_label, \
        elephant_day_label, left_header_label, days_countdown, days_label, \
        hours_countdown, hours_label, minutes_countdown, minutes_label, \
        seconds_countdown, seconds_label, milliseconds_countdown, \
        milliseconds_label, tz, full_screen_var, always_on_top_var, \
        transparency_var, snap_direction_var, background_color_var, \
        title_color_var, date_title_color_var, date_color_var, \
        left_header_color_var, countdown_text_color_var, \
        countdown_background_color_var, countdown_border_width_var, \
        countdown_border_style_var, unit_labels_color_var, \
        transparent_background_var

    system = platform.system()

    if system != 'Windows':
        support_info = '''This system is not supported.
This program works only on Windows.
Linux support is planned.'''
        messagebox.showerror('Error', support_info)

        return

    windll = ctypes.windll.kernel32
    language = locale.windows_locale[windll.GetUserDefaultUILanguage()]

    tz_name = tzlocal.get_localzone_name()
    tz = pytz.timezone(tz_name)

    window = tk.Tk()

    window.minsize(448, 630)

    window.title(get_text(0))
    window.iconbitmap(resource_path('img/elephant.ico'))

    full_screen_var = tk.BooleanVar(window, False)
    always_on_top_var = tk.BooleanVar(window, False)
    transparency_var = tk.DoubleVar(window, 0)
    snap_direction_var = tk.StringVar(window, 'n')

    background_color_var = tk.StringVar(window, '#9acd32')
    title_color_var = tk.StringVar(window, '#0000ff')
    date_title_color_var = tk.StringVar(window, '#0000ff')
    date_color_var = tk.StringVar(window, '#0000ff')
    left_header_color_var = tk.StringVar(window, '#0000ff')
    countdown_text_color_var = tk.StringVar(window, '#000072')
    countdown_background_color_var = tk.StringVar(window,  '#007a00')
    countdown_border_width_var = tk.IntVar(window, 5)
    countdown_border_style_var = tk.StringVar(window, 'solid')
    unit_labels_color_var = tk.StringVar(window, '#0000ff')

    transparent_background_var = tk.BooleanVar(window, False)

    window.config(bg=background_color_var.get())

    menu = tk.Menu(window)
    window.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label=get_text(16), command=window.destroy)
    menu.add_cascade(label=get_text(17), menu=file_menu)

    view_menu = tk.Menu(menu, tearoff=0)
    view_menu.add_command(label=get_text(48),
                          command=lambda: change_color('background'))
    view_menu.add_checkbutton(label=get_text(49),
                              variable=transparent_background_var,
                              command=transparent_background)
    view_menu.add_separator()
    view_menu.add_command(label=get_text(50),
                          command=lambda: change_color('title'))
    view_menu.add_command(label=get_text(51),
                          command=lambda: change_color('date_title'))
    view_menu.add_command(label=get_text(52),
                          command=lambda: change_color('date'))
    view_menu.add_command(label=get_text(53),
                          command=lambda: change_color('left_header'))
    view_menu.add_command(label=get_text(54),
                          command=lambda: change_color('unit_labels'))
    view_menu.add_separator()
    view_menu.add_command(label=get_text(55),
                          command=lambda: change_color('countdown_text'))
    view_menu.add_command(label=get_text(56),
                          command=lambda: change_color('countdown_background'))
    menu.add_cascade(label=get_text(47), menu=view_menu)

    window_menu = tk.Menu(menu, tearoff=0)
    window_menu.add_checkbutton(label=get_text(33),
                                variable=full_screen_var, command=full_screen)
    window_menu.add_checkbutton(label=get_text(35),
                                variable=always_on_top_var,
                                command=always_on_top)

    transparency_menu = tk.Menu(window_menu, tearoff=0)
    transparency_menu.add_radiobutton(label='0%',
                                      var=transparency_var,
                                      value=0,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='10%',
                                      var=transparency_var,
                                      value=0.1,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='20%',
                                      var=transparency_var,
                                      value=0.2,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='30%',
                                      var=transparency_var,
                                      value=0.3,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='40%',
                                      var=transparency_var,
                                      value=0.4,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='50%',
                                      var=transparency_var,
                                      value=0.5,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='60%',
                                      var=transparency_var,
                                      value=0.6,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='70%',
                                      var=transparency_var,
                                      value=0.7,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='80%',
                                      var=transparency_var,
                                      value=0.8,
                                      command=transparency)
    transparency_menu.add_radiobutton(label='90%',
                                      var=transparency_var,
                                      value=0.9,
                                      command=transparency)
    window_menu.add_cascade(label=get_text(36), menu=transparency_menu)

    snap_direction_menu = tk.Menu(window_menu, tearoff=0)
    snap_direction_menu.add_radiobutton(label=get_text(37),
                                        var=snap_direction_var,
                                        value='n',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(38),
                                        var=snap_direction_var,
                                        value='s',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(39),
                                        var=snap_direction_var,
                                        value='w',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(40),
                                        var=snap_direction_var,
                                        value='e',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(41),
                                        var=snap_direction_var,
                                        value='nw',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(42),
                                        var=snap_direction_var,
                                        value='ne',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(43),
                                        var=snap_direction_var,
                                        value='sw',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(44),
                                        var=snap_direction_var,
                                        value='se',
                                        command=snap_direction)
    snap_direction_menu.add_radiobutton(label=get_text(45),
                                        var=snap_direction_var,
                                        value='center',
                                        command=snap_direction)
    window_menu.add_cascade(label=get_text(46), menu=snap_direction_menu)

    menu.add_cascade(label=get_text(34), menu=window_menu)

    help_menu = tk.Menu(menu, tearoff=0)
    help_menu.add_command(label=get_text(18), command=info)
    help_menu.add_command(label=get_text(19), command=github_repo)
    help_menu.add_separator()
    help_menu.add_command(label=get_text(20), command=check_for_updates)
    menu.add_cascade(label=get_text(21), menu=help_menu)

    gui_frame = tk.Frame(window, background=background_color_var.get())
    gui_frame.place(relx=0.5, rely=0, anchor='n')

    title_frame = tk.Frame(
        gui_frame, background=background_color_var.get())
    title_frame.pack()

    title_label = tk.Label(
        title_frame,
        text=get_text(0),
        background=background_color_var.get(),
        foreground=title_color_var.get(),
        font=('Segoe UI', 26)
    )
    title_label.pack(side='left')

    icon_img = ImageTk.PhotoImage(Image.open(
        resource_path('img/elephant.png')).resize((40, 40)))
    icon_label = tk.Label(
        title_frame,
        image=icon_img,
        background=background_color_var.get()
    )
    icon_label.pack(side='left')

    today_title_label = tk.Label(
        gui_frame,
        text=get_text(1),
        background=background_color_var.get(),
        foreground=date_title_color_var.get(),
        font=('Segoe UI', 12, 'bold')
    )
    today_title_label.pack()

    today_label = tk.Label(
        gui_frame,
        background=background_color_var.get(),
        foreground=date_color_var.get(),
        font=('Segoe UI', 12)
    )
    today_label.pack()

    elephant_day_title_label = tk.Label(
        gui_frame,
        text=get_text(2),
        background=background_color_var.get(),
        foreground=date_title_color_var.get(),
        font=('Segoe UI', 12, 'bold')
    )
    elephant_day_title_label.pack()

    elephant_day_label = tk.Label(
        gui_frame,
        background=background_color_var.get(),
        foreground=date_color_var.get(),
        font=('Segoe UI', 12)
    )
    elephant_day_label.pack()

    left_header_label = tk.Label(
        gui_frame,
        text=get_text(3),
        background=background_color_var.get(),
        foreground=left_header_color_var.get(),
        font=('Segoe UI', 18)
    )
    left_header_label.pack()

    days_countdown = tk.Label(
        gui_frame,
        background=countdown_background_color_var.get(),
        foreground=countdown_text_color_var.get(),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=countdown_border_width_var.get(),
        relief=countdown_border_style_var.get()
    )
    days_countdown.pack()

    days_label = tk.Label(
        gui_frame,
        background=background_color_var.get(),
        foreground=unit_labels_color_var.get(),
        font=('Segoe UI', 12)
    )
    days_label.pack()

    hours_countdown = tk.Label(
        gui_frame,
        background=countdown_background_color_var.get(),
        foreground=countdown_text_color_var.get(),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=countdown_border_width_var.get(),
        relief=countdown_border_style_var.get()
    )
    hours_countdown.pack()

    hours_label = tk.Label(
        gui_frame,
        background=background_color_var.get(),
        foreground=unit_labels_color_var.get(),
        font=('Segoe UI', 12)
    )
    hours_label.pack()

    minutes_countdown = tk.Label(
        gui_frame,
        background=countdown_background_color_var.get(),
        foreground=countdown_text_color_var.get(),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=countdown_border_width_var.get(),
        relief=countdown_border_style_var.get()
    )
    minutes_countdown.pack()

    minutes_label = tk.Label(
        gui_frame,
        background=background_color_var.get(),
        foreground=unit_labels_color_var.get(),
        font=('Segoe UI', 12)
    )
    minutes_label.pack()

    seconds_countdown = tk.Label(
        gui_frame,
        background=countdown_background_color_var.get(),
        foreground=countdown_text_color_var.get(),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=countdown_border_width_var.get(),
        relief=countdown_border_style_var.get()
    )
    seconds_countdown.pack()

    seconds_label = tk.Label(
        gui_frame,
        background=background_color_var.get(),
        foreground=unit_labels_color_var.get(),
        font=('Segoe UI', 12)
    )
    seconds_label.pack()

    milliseconds_countdown = tk.Label(
        gui_frame,
        background=countdown_background_color_var.get(),
        foreground=countdown_text_color_var.get(),
        font=('Segoe UI', 26, 'bold'),
        width=7,
        borderwidth=countdown_border_width_var.get(),
        relief=countdown_border_style_var.get()
    )
    milliseconds_countdown.pack()

    milliseconds_label = tk.Label(
        gui_frame,
        text=get_text(15),
        background=background_color_var.get(),
        foreground=unit_labels_color_var.get(),
        font=('Segoe UI', 12)
    )
    milliseconds_label.pack()

    window.after(0, countdown)

    t = threading.Thread(target=lambda: check_for_updates(information=False))
    t.start()

    window.mainloop()


if __name__ == '__main__':
    main()
