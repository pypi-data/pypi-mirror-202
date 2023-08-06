import time
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta


class Timer:
    def __init__(self, tz='UTC'):
        self.tz = tz
        self.start = self.now()
        self._last = self.start

    def now(self):
        return datetime.now(pytz.timezone(self.tz))

    def exec_from_start(self):
        self._last = self.now()
        return self.diff_in_seconds(self._last, self.start)

    def exec_from_last(self):
        now = self.now()
        duration = self.diff_in_seconds(now, self._last)
        self._last = now
        return duration

    def restart(self, mode, offset=0, log=True):
        _next = self.calc_next(mode, offset)
        _now = self.now()
        exec_time = self.diff_in_seconds(_now, self.start)
        sleep_time = self.diff_in_seconds(_now, _next) + 1
        if log:
            print(f'\t{_now.strftime("%Y-%m-%d %H:%M:%S")}, '
                  f'executed {exec_time / 3600:.2f}h: '
                  f'restart in {sleep_time / 3600:.2f}h'
                  , flush=True)
        time.sleep(sleep_time)
        self.start = self.now()
        self._last = self.start
        return self

    def calc_next(self, mode, offset=0):
        if mode not in (modes := ['month', 'week', 'day', 'hour', 'minute']):
            raise ValueError(f'Mode must be in {", ".join(modes)}.')
        return eval(f'self._calc_next_{mode}({offset})')

    def _calc_next_month(self, offset=0):
        # Offset=0: 1st day of the month
        if not 0 <= offset <= 28:
            raise ValueError('Offset must be in range [0, 28].')
        next_start = (self.start + relativedelta(months=1)) \
            .replace(microsecond=0, second=0, minute=0, hour=0, day=offset+1)
        next_now = ((self.now()) + relativedelta(months=1)) \
            .replace(microsecond=0, second=0, minute=0, hour=0, day=offset+1)
        if next_now > next_start:
            print('Executed more than 1 month.', flush=True)
        return max([next_start, next_now])

    def _calc_next_week(self, offset=0):
        # Offset=0: Monday
        if not 0 <= offset <= 6:
            raise ValueError('Offset must be in range [0, 6].')
        next_start = (self.start + timedelta(days=(d := (7 + offset - self.start.weekday()) % 7) + 7 * (d == 0))) \
            .replace(microsecond=0, second=0, minute=0, hour=0)
        next_now = ((now := self.now()) + timedelta(days=(d := (7 + offset - now.weekday()) % 7) + 7 * (d == 0))) \
            .replace(microsecond=0, second=0, minute=0, hour=0)
        if next_now > next_start:
            print('Executed more than 1 week.', flush=True)
        return max([next_start, next_now])

    def _calc_next_day(self, offset=0):
        if not 0 <= offset <= 23:
            raise ValueError('Offset must be in range [0, 23].')
        next_start = (self.start + timedelta(days=1)).replace(microsecond=0, second=0, minute=0, hour=offset)
        next_now = (self.now() + timedelta(days=1)).replace(microsecond=0, second=0, minute=0, hour=offset)
        if next_now > next_start:
            print('Executed more than 1 day.', flush=True)
        return max([next_start, next_now])

    def _calc_next_hour(self, offset=0):
        if not 0 <= offset <= 59:
            raise ValueError('Offset must be in range [0, 59].')
        next_start = (self.start + timedelta(hours=1)).replace(microsecond=0, second=0, minute=offset)
        next_now = (self.now() + timedelta(hours=1)).replace(microsecond=0, second=0, minute=offset)
        if next_now > next_start:
            print('Executed more than 1 hour.', flush=True)
        return max([next_start, next_now])

    def _calc_next_minute(self, offset=0):
        if not 0 <= offset <= 59:
            raise ValueError('Offset must be in range [0, 59].')
        next_start = (self.start + timedelta(minutes=1)).replace(microsecond=0, second=offset)
        next_now = (self.now() + timedelta(minutes=1)).replace(microsecond=0, second=offset)
        if next_now > next_start:
            print('Executed more than 1 minute.', flush=True)
        return max([next_start, next_now])

    @staticmethod
    def diff_in_seconds(a, b):
        d = a - b
        s = d.days * 3600 * 24 + d.seconds
        return abs(s)
