from os.path import exists

from numpy import busdaycalendar, busday_offset
from pendulum import UTC, DateTime, Time, parse
from pendulum.tz.timezone import FixedTimezone, Timezone

from airflow.plugins_manager import AirflowPlugin
from airflow.timetables.base import (
    DagRunInfo,
    DataInterval,
    Timetable,
    TimeRestriction,
)
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.utils.types import DagRunType

ANBIMA_HOLIDAYS = "anbima_holidays.csv"
B3_PREGAO_HOLIDAYS = "b3pregao_holidays.csv"


def _fetch_anbima_holidays():
    try:
        from pandas import read_excel

        _holidays = read_excel(
            "https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls",
            skipfooter=9,
            names=["Data", "unused", "Descrição"],
            usecols=["Data", "Descrição"],
        )
        _holidays = _holidays.where(_holidays["Data"] > "2021-12-31").dropna()
        _holidays.to_csv(ANBIMA_HOLIDAYS, sep=";", index=False, encoding="utf-8")
    except Exception:
        raise RuntimeError("Missing Anbima holidays csv file")


class CustomCronHolidaysTimetable(CronDataIntervalTimetable):
    def __init__(
        self,
        cron: str,
        timezone: str | Timezone | FixedTimezone,
        calfile: str,
        skip_header: bool = True,
        sep: str = ";",
    ) -> None:
        with open(calfile, "r", encoding="utf-8") as fp:
            if skip_header:
                _ = fp.readline()  # header
            self._holidays = set(
                t[0] for t in [line.split(sep) for line in fp.readlines()]
            )
        super().__init__(cron=cron, timezone=timezone)

    def _get_next(self, current: DateTime) -> DateTime:
        next_date = super()._get_next(current)
        while next_date.to_date_string() in self._holidays:
            next_date = super()._get_next(next_date.end_of("day"))
        return next_date

    def _get_prev(self, current: DateTime) -> DateTime:
        prev_date = super()._get_prev(current)
        while prev_date.to_date_string() in self._holidays:
            prev_date = super()._get_prev(prev_date.start_of("day"))
        return prev_date


class CustomHolidaysTimetable(Timetable):
    def __init__(
        self,
        schedule_at: Time,
        calfile: str,
        skip_header: bool = True,
        sep: str = ";",
        descr: str = "",
    ):
        self._calfile = calfile
        self._schedule_at = schedule_at
        self.description = descr
        with open(calfile, "r", encoding="utf-8") as fp:
            if skip_header:
                _ = fp.readline()  # header
            self._holidays = [
                t[0] for t in [line.split(sep) for line in fp.readlines()]
            ]

    def _get_calendar(self):
        return busdaycalendar(holidays=self._holidays)

    def serialize(self):
        return {"schedule_at": self._schedule_at.isoformat()}

    @classmethod
    def deserialize(cls, value):
        return cls(Time.fromisoformat(value["schedule_at"]))

    def _roll_date(self, dte: DateTime, offset: int = 0, method="forward") -> DateTime:
        assert isinstance(dte, DateTime), f"invalid type: {type(dte)} {dte}"
        _dt = dte.to_date_string()
        bcal = self._get_calendar()
        return DateTime.combine(
            parse(busday_offset(_dt, offset, roll=method, busdaycal=bcal).astype(str)),
            self._schedule_at,
        ).replace(tzinfo=UTC)

    def infer_manual_data_interval(self, run_after: DateTime) -> DataInterval:
        sd = self._roll_date(run_after, 0, method="backward")
        ed = self._roll_date(sd, 1)
        return DataInterval(start=sd, end=ed)

    def next_dagrun_info(
        self,
        *,
        last_automated_data_interval: DataInterval | None,
        restriction: TimeRestriction,
    ) -> DagRunInfo:
        # This is the first ever run on the regular schedule.
        if last_automated_data_interval is None:
            # No start date, don´t schedule
            if restriction.earliest is None:
                return None
            # If the DAG has catchup=False, today is the earliest to consider.
            if restriction.catchup is False:
                next_start = max(
                    restriction.earliest,
                    self._roll_date(DateTime.now(), -1, method="backward"),
                )
            else:
                next_start = self._roll_date(restriction.earliest, 0)
            next_end = self._roll_date(next_start, 1)
        else:
            # There was a previous run on the regular schedule.
            next_start = last_automated_data_interval.end
            next_end = self._roll_date(next_start, 1)

        # Over the DAG's scheduled end; don't schedule.
        if restriction.latest is not None and next_start > restriction.latest:
            return None

        return DagRunInfo.interval(start=next_start, end=next_end)

    def generate_run_id(
        self,
        *,
        run_type: DagRunType,
        logical_date: DateTime,
        data_interval: DataInterval,
        **extra,
    ) -> str:
        if run_type == DagRunType.SCHEDULED and data_interval:
            return data_interval.end.format("YYYY-MM-DDTHH:mm:ssZ")
        return super().generate_run_id(
            run_type=run_type,
            logical_date=logical_date,
            data_interval=data_interval,
            **extra,
        )


class AnbimaWorkdayTimetable(CustomHolidaysTimetable):
    def __init__(self, schedule_at=Time(0, 0, 0)):
        descr = f"After each Anbima business day, at {schedule_at.isoformat()}"
        if not exists(ANBIMA_HOLIDAYS):
            _fetch_anbima_holidays()
        super().__init__(schedule_at=schedule_at, calfile=ANBIMA_HOLIDAYS, descr=descr)

    @property
    def summary(self) -> str:
        return "Anbima Workday"


class B3PregaoTimetable(CustomHolidaysTimetable):
    def __init__(self, schedule_at=Time(0, 0, 0)):
        descr = f"After each B3 Pregao, at {schedule_at.isoformat()}"
        if not exists(B3_PREGAO_HOLIDAYS):
            raise RuntimeError("Missing B3 pregao holidays csv file")
        super().__init__(
            schedule_at=schedule_at, calfile=B3_PREGAO_HOLIDAYS, descr=descr
        )

    @property
    def summary(self) -> str:
        return "B3 Pregão"


class AnbimaCronTimetable(CustomCronHolidaysTimetable):
    def __init__(self, cron: str, timezone: str | Timezone | FixedTimezone = "UTC"):
        if not exists(ANBIMA_HOLIDAYS):
            _fetch_anbima_holidays()
        super().__init__(cron=cron, timezone=timezone, calfile=ANBIMA_HOLIDAYS)

    @property
    def summary(self) -> str:
        return "Anbima Workday"


class B3CronTimetable(CustomCronHolidaysTimetable):
    def __init__(self, cron: str, timezone: str | Timezone | FixedTimezone = "UTC"):
        if not exists(B3_PREGAO_HOLIDAYS):
            raise RuntimeError("Missing B3 pregao holidays csv file")
        super().__init__(cron=cron, timezone=timezone, calfile=B3_PREGAO_HOLIDAYS)

    @property
    def summary(self) -> str:
        return "B3 Pregão"


class SpartaTimetablePlugin(AirflowPlugin):
    name = "sparta_timetable_plugin"
    timetables = [
        AnbimaWorkdayTimetable,
        AnbimaCronTimetable,
        B3PregaoTimetable,
        B3CronTimetable,
    ]