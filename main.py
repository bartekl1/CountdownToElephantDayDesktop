import tkinter as tk
from tkinter import colorchooser
from datetime import datetime

def intro():
    print(f'Odliczanie do Dnia Słonia')
    intro_elephant = '       ╔\n╔█████■╝\n╝█████\n ╚╚ ╚╚'
    print(intro_elephant)
    print(f'\n')

def update_left_time():
    global window, left_days_label, left_hours_label, left_minutes_label, left_seconds_label, left_microseconds_label

    now = datetime.now()

    if not (now.month == 8 and now.day == 12):
        if now.month < 8 or (now.month == 8 and now.day < 12):
            year_of_international_elephant_day = now.year
        else:
            year_of_international_elephant_day = now.year + 1

        international_elephant_day_date = datetime(year_of_international_elephant_day, 8, 12, 0, 0, 0)

        left = international_elephant_day_date - now
        left_days = left.days
        left_seconds_temp = left.seconds
        left_seconds = left_seconds_temp % 60
        left_minutes_temp = int(left_seconds_temp / 60)
        left_minutes = left_minutes_temp % 60
        left_hours = int(left_minutes_temp / 60)
        left_microseconds = left.microseconds

        # print(left)
        # print(left_days)
        # print(left_hours)
        # print(left_minutes)
        # print(left_seconds)
        # print(left_microseconds)

        left_days_label.config(text=left_days)
        left_hours_label.config(text=left_hours)
        left_minutes_label.config(text=left_minutes)
        left_seconds_label.config(text=left_seconds)
        left_microseconds_label.config(text=left_microseconds)
    else:
        left_days_label.config(text=0)
        left_hours_label.config(text=0)
        left_minutes_label.config(text=0)
        left_seconds_label.config(text=0)
        left_microseconds_label.config(text=0)

    window.after(10, update_left_time)

def update_fullscreen():
    global window, fullscreen

    window.attributes('-fullscreen', fullscreen.get())

def update_alpha(alpha):
    global window

    window.attributes('-alpha', alpha)

def update_background():
    global window, title_label, left_label, left_days_text_label, left_hours_text_label, left_minutes_text_label, left_seconds_text_label, left_microseconds_text_label

    rgb_color, hex_color = colorchooser.askcolor(parent=window, initialcolor=(255, 255, 255))
    window.configure(bg=hex_color)
    title_label.config(bg=hex_color)
    left_label.config(bg=hex_color)
    left_days_text_label.config(bg=hex_color)
    left_hours_text_label.config(bg=hex_color)
    left_minutes_text_label.config(bg=hex_color)
    left_seconds_text_label.config(bg=hex_color)
    left_microseconds_text_label.config(bg=hex_color)


def main():
    global window, fullscreen
    global title_label, left_label, left_days_text_label, left_hours_text_label, left_minutes_text_label, left_seconds_text_label, left_microseconds_text_label
    global left_days_label, left_hours_label, left_minutes_label, left_seconds_label, left_microseconds_label

    window = tk.Tk()

    window.title(f'Odliczanie do Dnia Słonia')
    window.iconbitmap('img/Słoń.ico')

    window.minsize(600, 550)
    window.geometry('600x550')

    window.config(bg='light green')

    fullscreen = tk.BooleanVar()

    menu = tk.Menu(window)

    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label='Wyjście', command=window.destroy)
    menu.add_cascade(label='Plik', menu=file_menu)

    window_menu = tk.Menu(menu, tearoff=0)
    window_menu.add_checkbutton(label="Pełny ekran", variable=fullscreen, command=update_fullscreen)

    alpha_menu = tk.Menu(window_menu)
    alpha_menu.add_radiobutton(label='100%', command=lambda: update_alpha(1))
    alpha_menu.add_radiobutton(label='90%', command=lambda: update_alpha(0.9))
    alpha_menu.add_radiobutton(label='80%', command=lambda: update_alpha(0.8))
    alpha_menu.add_radiobutton(label='70%', command=lambda: update_alpha(0.7))
    alpha_menu.add_radiobutton(label='60%', command=lambda: update_alpha(0.6))
    alpha_menu.add_radiobutton(label='50%', command=lambda: update_alpha(0.5))
    alpha_menu.add_radiobutton(label='40%', command=lambda: update_alpha(0.4))
    alpha_menu.add_radiobutton(label='30%', command=lambda: update_alpha(0.3))
    alpha_menu.add_radiobutton(label='20%', command=lambda: update_alpha(0.2))
    alpha_menu.add_radiobutton(label='10%', command=lambda: update_alpha(0.1))
    alpha_menu.add_radiobutton(label='0%', command=lambda: update_alpha(0))
    window_menu.add_cascade(label='Przezroczystość', menu=alpha_menu)

    window_menu.add_command(label='Kolor tła', command=update_background)

    menu.add_cascade(label='Okno', menu=window_menu)

    window.config(menu=menu)


    title_label = tk.Label(window,
                           text='Odliczanie do Dnia Słonia',
                           fg='blue',
                           bg='light green',
                           font=('Segoe Ui', 18, 'bold'))
    title_label.pack()

    left_label = tk.Label(window,
                           text='Pozostało:',
                           fg='blue',
                           bg='light green',
                           font=('Segoe Ui', 14))
    left_label.pack()

    # Days

    left_days_label = tk.Label(window,
                              text='0',
                              fg='dark blue',
                              bg='green',
                              font=('Segoe Ui', 30, 'bold'),
                              width=7,
                              height=1,
                              relief='solid',
                              borderwidth=4)
    left_days_label.pack()

    left_days_text_label = tk.Label(window,
                          text='dni',
                          fg='blue',
                          bg='light green',
                          font=('Segoe Ui', 12))
    left_days_text_label.pack()

    # Hours

    left_hours_label = tk.Label(window,
                               text='0',
                               fg='dark blue',
                               bg='green',
                               font=('Segoe Ui', 30, 'bold'),
                               width=7,
                               height=1,
                               relief='solid',
                               borderwidth=4)
    left_hours_label.pack()

    left_hours_text_label = tk.Label(window,
                                    text='godzin',
                                    fg='blue',
                                    bg='light green',
                                    font=('Segoe Ui', 12))
    left_hours_text_label.pack()

    # Minutes

    left_minutes_label = tk.Label(window,
                               text='0',
                               fg='dark blue',
                               bg='green',
                               font=('Segoe Ui', 30, 'bold'),
                               width=7,
                               height=1,
                               relief='solid',
                               borderwidth=4)
    left_minutes_label.pack()

    left_minutes_text_label = tk.Label(window,
                                    text='minut',
                                    fg='blue',
                                    bg='light green',
                                    font=('Segoe Ui', 12))
    left_minutes_text_label.pack()

    # Seconds

    left_seconds_label = tk.Label(window,
                               text='0',
                               fg='dark blue',
                               bg='green',
                               font=('Segoe Ui', 30, 'bold'),
                               width=7,
                               height=1,
                               relief='solid',
                               borderwidth=4)
    left_seconds_label.pack()

    left_seconds_text_label = tk.Label(window,
                                    text='sekund',
                                    fg='blue',
                                    bg='light green',
                                    font=('Segoe Ui', 12))
    left_seconds_text_label.pack()

    # Microseconds

    left_microseconds_label = tk.Label(window,
                               text='0',
                               fg='dark blue',
                               bg='green',
                               font=('Segoe Ui', 30, 'bold'),
                               width=7,
                               height=1,
                               relief='solid',
                               borderwidth=4)
    left_microseconds_label.pack()

    left_microseconds_text_label = tk.Label(window,
                                    text='mikrosekund',
                                    fg='blue',
                                    bg='light green',
                                    font=('Segoe Ui', 12))
    left_microseconds_text_label.pack()

    window.after(10, update_left_time)

    window.mainloop()


if __name__ == '__main__':
    intro()

    main()