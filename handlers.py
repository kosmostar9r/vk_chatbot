import datetime
import json
import re

from generate_ticket import generate_ticket
from schedule import make_schedule

re_cities = {
    re.compile(r'[Мм]оск[во]\w+'): 'Москва',
    re.compile(r'[Лл]ондон\w*'): 'Лондон',
    re.compile(r'[Бб]ерлин\w*'): 'Берлин',
    re.compile(r'[Пп]ариж\w*'): 'Париж',
    re.compile(r'[Мм]адрид\w*'): 'Мадрид',
    re.compile(r'[Мм]юнхен\w*'): 'Мюнхен',
    re.compile(r'[Рр]им\w*'): 'Рим'
}
re_date = re.compile(r'([1-9]|[0-2]\d|30|31)-([1-9]|0[1-9]|1[0-2])-(2021)')
re_email = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
re_phone_number = re.compile(r'89\d{9}|[+]79\d{9}')
choices = ['1', '2', '3', '4', '5']
try:
    with open('schedule.json', 'r') as file:
        schedule = json.load(file)
except FileNotFoundError as err:
    make_schedule()
    print(err)


def dispatcher(dep_city, arr_city, date):
    fly_dates = schedule[dep_city][arr_city]
    nearest_dates = []
    date = date.split('-')
    try:
        fly_date = datetime.datetime(year=int(date[2]), month=int(date[1]), day=int(date[0]))
        for day in fly_dates:
            day = day.split(' ')
            date_day = day[0]
            time_day = day[1]
            time_day = time_day.split(':')
            date_day = date_day.split('-')
            day = datetime.datetime(year=int(date_day[2]),
                                    month=int(date_day[1]),
                                    day=int(date_day[0]),
                                    hour=int(time_day[0]),
                                    minute=int(time_day[1]))
            if fly_date <= day and len(nearest_dates) < 5:
                nearest_dates.append(day.strftime('%d-%m-%Y %H:%M'))
                if len(nearest_dates) == 5:
                    break
        return nearest_dates
    except ValueError:
        return False


def handle_departure(text, context):
    cities = []
    for key, value in re_cities.items():
        cities.append(value)
    context['cities'] = '\n-'.join(cities)
    for pattern in re_cities:
        match = re.search(pattern, text)
        if match:
            context['departure'] = re_cities[pattern]
            return True
    else:
        return False


def handle_arrival(text, context):
    for pattern in re_cities:
        match = re.search(pattern, text)
        if match:
            context['arrival'] = re_cities[pattern]
            try:
                schedule[context['departure']][context['arrival']]
            except KeyError:
                return False
            return True
    else:
        return False


def handle_date(text, context):
    match = re.search(re_date, text)
    if match:
        context['date'] = match[0]
        flies = []
        dispatcher_run = dispatcher(context['departure'], context['arrival'], context['date'])
        if dispatcher_run:
            for num, day in enumerate(dispatcher_run):
                flies.append(f'{num + 1}. {day}')
            context['flies'] = '\n'.join(flies)
            return True
        else:
            return False
    else:
        return False


def handle_choice(text, context):
    for num in choices:
        match = re.match(num, text)
        if match:
            users_choice = dispatcher(context['departure'], context['arrival'], context['date'])[int(text) - 1]
            context['chosen_date'] = users_choice
            return True
    else:
        return False


def handle_places(text, context):
    for num in choices:
        match = re.match(num, text)
        if match:
            context['places'] = match[0]
            return True
    else:
        return False


def handle_commentary(text, context):
    context['comment'] = text
    return True


def handle_confirm(text, context):
    if text.lower() == 'да':
        context['confirmed'] = True
        return True
    else:
        context['confirmed'] = False
        return False


def handle_email(text, context):
    match = re.search(re_email, text)
    if match:
        context['email'] = match[0]
        return True
    else:
        return False


def handle_phone_number(text, context):
    match = re.search(re_phone_number, text)
    if match:
        context['number'] = match[0]
        return True
    else:
        return False


def handle_generate_ticket(text, context):
    return generate_ticket(departure=context['departure'],
                           arrival=context['arrival'],
                           date=context['chosen_date'],
                           email=context['email'])
