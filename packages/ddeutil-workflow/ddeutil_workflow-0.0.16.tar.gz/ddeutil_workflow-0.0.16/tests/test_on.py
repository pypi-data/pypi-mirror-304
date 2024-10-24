from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ddeutil.workflow.on import On, YearOn


def test_on():
    schedule = On.from_loader(
        name="every_5_minute_bkk",
        externals={},
    )
    assert "Asia/Bangkok" == schedule.tz
    assert "*/5 * * * *" == str(schedule.cronjob)

    start_date: datetime = datetime(2024, 1, 1, 12)
    start_date_bkk: datetime = start_date.astimezone(ZoneInfo(schedule.tz))
    cron_runner = schedule.generate(start=start_date)
    assert cron_runner.date.tzinfo == ZoneInfo(schedule.tz)

    assert cron_runner.date == start_date_bkk
    assert cron_runner.next == start_date_bkk
    assert cron_runner.next == start_date_bkk + timedelta(minutes=5)
    assert cron_runner.next == start_date_bkk + timedelta(minutes=10)
    assert cron_runner.next == start_date_bkk + timedelta(minutes=15)

    cron_runner.reset()

    assert cron_runner.date == start_date_bkk
    assert cron_runner.prev == start_date_bkk - timedelta(minutes=5)


def test_on_value():
    schedule = On.from_loader(
        name="every_day_noon",
        externals={},
    )
    assert "Etc/UTC" == schedule.tz
    assert "12 0 1 * 1" == str(schedule.cronjob)


def test_on_aws():
    schedule = YearOn.from_loader(
        name="aws_every_5_minute_bkk",
        externals={},
    )
    assert "Asia/Bangkok" == schedule.tz


def test_on_every_minute():
    schedule = On.from_loader(
        name="every_minute_bkk",
        externals={},
    )
    current: datetime = datetime(2024, 8, 1, 12, 5, 45)
    adjust: datetime = current.replace(second=0, microsecond=0).astimezone(
        tz=ZoneInfo(schedule.tz)
    )
    gen = schedule.generate(adjust)
    print(f"{gen.next:%Y-%m-%d %H:%M:%S}")


def test_on_serialize():
    schedule = On.from_loader(
        name="every_minute_bkk",
        externals={},
    )
    print(schedule.model_dump())
