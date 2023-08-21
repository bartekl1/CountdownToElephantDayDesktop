from datetime import datetime


def intro():
    print(f'Odliczanie do Dnia Słonia')
    intro_elephant = '       ╔\n╔█████■╝\n╝█████\n ╚╚ ╚╚'
    print(intro_elephant)
    print(f'\n')


def main():
    while True:
        try:
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

                print(f'Pozostało {left_days} dni,',
                      f'{left_hours} godzin,',
                      f'{left_minutes} minut,',
                      f'{left_seconds} sekund,',
                      f'{left_microseconds} mikrosekund.',
                      f'                      ',
                      end='\r')
            else:
                print(f'Dziś jest międzynarodowy dzień słonie',
                      f'                           ',
                      end='\r')
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    intro()

    main()
