import datetime


class Dispatcher:

    def __init__(self, periods):
        self.dates = periods['dates']
        self.times = periods['times']
        self.period_param = periods['param']
        self.delta = datetime.timedelta(days=1)
        self.start_day = datetime.date.today()
        self.end_day = datetime.date(year=self.start_day.year,
                                     month=self.start_day.month + 4,
                                     day=self.start_day.day)
        self.fly_dates = []

    def make_fly_dates(self):
        while self.end_day > self.start_day:
            for date in self.dates:
                if self.period_param == 0:
                    if date == self.start_day.weekday():
                        self._combine_date()
                elif self.period_param == 1:
                    if date == self.start_day.day:
                        self._combine_date()
            self.start_day += self.delta
        return self.fly_dates

    def _combine_date(self):
        for time in self.times:
            fly_date = datetime.datetime.combine(self.start_day, time)
            self.fly_dates.append(fly_date.strftime('%d-%m-%Y %H:%M'))


if __name__ == '__main__':
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
    disp = Dispatcher(mon_wed_fri).make_fly_dates()
    print(disp)
    disp1 = Dispatcher(tue_thu_sat).make_fly_dates()
    print(disp1)
    disp2 = Dispatcher(every_fifth_day).make_fly_dates()
    print(disp2)
