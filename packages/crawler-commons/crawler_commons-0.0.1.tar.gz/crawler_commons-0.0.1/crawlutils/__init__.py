from datetime import datetime


class Interval:
    def __init__(self, level: int, fr: str, to: str, secs: int):
        self.level = level
        self.time_from = None if len(fr) < 1 else datetime.strptime(fr, "%H:%M").time()
        self.time_to = None if len(to) < 1 else datetime.strptime(to, "%H:%M").time()
        self.secs = secs

    def __str__(self):
        return f"level : {self.level}, from : {self.time_from}, to : {self.time_to}, secs : {self.time_to}"


class CrawlingInterval:
    """
    설정에 따라 crawling interval 을 설정한다
    """
    def __init__(self, intervals):
        self.intervals = list(map(lambda x: Interval(x.get("level"), x.get("from"), x.get("to"), x.get("secs")), intervals))

    def choose_sleep_time(self, dt):
        t = dt.time()
        default_secs = 10
        for interval in self.intervals:
            if interval.time_from is None:
                default_secs = interval.secs
            else:
                if interval.time_from <= t < interval.time_to:
                    return interval.secs

        return default_secs


if __name__ == "__main__":
    c = CrawlingInterval()
    assert(0.4 == c.choose_sleep_time(datetime(1970, 1, 1, 10, 10)))
    assert(1 == c.choose_sleep_time(datetime(1970, 1, 1, 16, 10)))
    assert(1 == c.choose_sleep_time(datetime(1970, 1, 1, 8, 59)))
    assert(0.4 == c.choose_sleep_time(datetime(1970, 1, 1, 15, 59)))
    assert(0.4 == c.choose_sleep_time(datetime(1970, 1, 1, 9, 0)))