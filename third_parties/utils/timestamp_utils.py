from datetime import datetime, tzinfo, timedelta


class Zone(tzinfo):
    def __init__(self, offset, isdst, name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
        return self.name


class TimestampUtils:
    minimum_timestamp = 1451581200  # 2016-01-01

    @staticmethod
    def timestamp_now():
        return datetime.now().timestamp()

    @staticmethod
    def gmt7_now():
        GMT = Zone(7, False, 'GMT7')
        return datetime.now(GMT)
