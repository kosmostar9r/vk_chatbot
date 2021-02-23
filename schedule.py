import datetime
import json

import dispatcher


def make_schedule():
    mon_wed_fri = {
        'dates': [0, 2, 4],
        'times': [datetime.time(hour=10, minute=00), datetime.time(hour=18, minute=00)],
        'param': 0
    }
    tue_thu_sat = {
        'dates': [1, 3, 5],
        'times': [datetime.time(hour=9, minute=00), datetime.time(hour=17, minute=00)],
        'param': 0
    }
    thu_sun = {
        'dates': [3, 6],
        'times': [datetime.time(hour=22, minute=40), datetime.time(hour=14, minute=00)],
        'param': 0
    }
    every_third_day = {
        'dates': [x for x in range(0, 31, 3)],
        'times': [datetime.time(hour=16, minute=25), ],
        'param': 1
    }
    every_fifth_day = {
        'dates': [x for x in range(0, 31, 5)],
        'times': [datetime.time(hour=8, minute=45), ],
        'param': 1
    }
    every_tenth_day = {
        'dates': [x for x in range(0, 31, 10)],
        'times': [datetime.time(hour=10, minute=00), ],
        'param': 1
    }
    flies_schedule = {'mon_wed_fri': dispatcher.Dispatcher(mon_wed_fri).make_fly_dates(),
                      'tue_thu_sat': dispatcher.Dispatcher(tue_thu_sat).make_fly_dates(),
                      'thu_sun': dispatcher.Dispatcher(thu_sun).make_fly_dates(),
                      'every_third_day': dispatcher.Dispatcher(every_third_day).make_fly_dates(),
                      'every_fifth_day': dispatcher.Dispatcher(every_fifth_day).make_fly_dates(),
                      'every_tenth_day': dispatcher.Dispatcher(every_tenth_day).make_fly_dates()}

    departures = {
        'Москва': {
            'Лондон': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
            'Берлин': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
            'Париж': flies_schedule['thu_sun'],  # чт вс 22:40 14:00
            'Мадрид': flies_schedule['every_fifth_day'],
            # 5 10 15 20 25 30 числа каждого месяца в 8:45
            'Мюнхен': flies_schedule['every_tenth_day'],  # 10 20 30 числа каждого месяца в 8:00
            'Рим': flies_schedule['every_third_day'],  # каждые 3 дня в 16:25
        },
        'Лондон': {
            'Москва': flies_schedule['thu_sun'],  # чт вс 14:00 22:40
            'Берлин': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
            'Париж': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
            'Мадрид': flies_schedule['every_third_day'],  # каждые 3 дня
            'Мюнхен': flies_schedule['every_fifth_day'],
            # 5 10 15 20 25 30 числа каждого месяца в 8:45
        },
        'Берлин': {
            'Лондон': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
            'Москва': flies_schedule['thu_sun'],  # чт вс 14:00 22:40
            'Париж': flies_schedule['every_tenth_day'],  # 10 20 30 числа каждого месяца в 8:00
            'Мюнхен': flies_schedule['every_third_day'],  # каждые 3 дня
            'Рим': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
        },
        'Париж': {
            'Лондон': flies_schedule['thu_sun'],  # чт вс 14:00 22:40
            'Берлин': flies_schedule['every_tenth_day'],  # 10 20 30 числа каждого месяца в 8:00
            'Москва': flies_schedule['every_third_day'],  # каждые 3 дня
            'Мадрид': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
            'Мюнхен': flies_schedule['every_fifth_day'],
            # 5 10 15 20 25 30 числа каждого месяца в 8:45
            'Рим': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
        },
        'Мадрид': {
            'Лондон': flies_schedule['every_third_day'],  # каждые 3 дня
            'Берлин': flies_schedule['thu_sun'],  # чт вс 14:00 22:40
            'Париж': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
            'Москва': flies_schedule['every_tenth_day'],  # 10 20 30 числа каждого месяца в 8:00
            'Мюнхен': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
        },
        'Мюнхен': {
            'Лондон': flies_schedule['every_tenth_day'],  # 10 20 30 числа каждого месяца в 8:00
            'Берлин': flies_schedule['every_fifth_day'],
            # 5 10 15 20 25 30 числа каждого месяца в 8:45
            'Париж': flies_schedule['thu_sun'],  # чт вс 14:00 22:40
            'Мадрид': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
            'Москва': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
            'Рим': flies_schedule['every_third_day'],  # каждые 3 дня
        },
        'Рим': {
            'Берлин': flies_schedule['thu_sun'],  # чт вс 22:40 14:00
            'Париж': flies_schedule['every_fifth_day'],
            # 5 10 15 20 25 30 числа каждого месяца в 8:45
            'Мадрид': flies_schedule['tue_thu_sat'],  # вт чт сб 9:00 17:00
            'Мюнхен': flies_schedule['mon_wed_fri'],  # пн ср пт 10:00 18:00
            'Москва': flies_schedule['every_third_day'],  # каждые 3 дня
        },
    }

    with open('schedule.json', 'w', encoding='UTF8') as file:
        json.dump(departures, file, indent=4)
