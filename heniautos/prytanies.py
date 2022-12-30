# Copyright (C) 2022 Sean Redmond

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from collections import namedtuple
from enum import IntEnum
import juliandate as jd
import heniautos
from itertools import product

class Prytanies(IntEnum):
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5
    VI = 6
    VII = 7
    VIII = 8
    IX = 9
    X = 10
    XI = 11
    XII = 12
    XIII = 13


class Prytany(IntEnum):
    """Constants representing choices of conciilar calendars."""
    AUTO = 0
    QUASI_SOLAR = 1
    ALIGNED_10 = 2
    ALIGNED_12 = 3
    ALIGNED_13 = 4


PrytanyDay = namedtuple("PrytanyDay", ("jdn", "prytany_index", "prytany", "day", "doy"))


# Maybe remove
def __add_years(t, y):
    """Return a new Time object with y years added to Time t."""
    return jd.from_julian(*[sum(x) for x in zip(jd.to_julian(t), (y, 0, 0, 0, 0, 0))])


def _max_or_fewer(n, mx):
    """Return n if n is less than mx, otherwise mx."""
    return n if n < mx else mx


def prytany_label(p):
    return (
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
        "XI",
        "XII",
        "XIII",
    )[int(p) - 1]


def _pryt_len(days, count=4):
    """Recursively generate prytany lengths.

    Generator for conciliar years that have count number of prytanies
    of days length, with the remaining being days - 1. E.g. Four
    36-day pryanties followed by 35-day prytanies.
    """
    if count:
        yield days
        yield from _pryt_len(days, count - 1)

    if count == 0:
        yield from _pryt_len(days - 1, count - 1)

    yield from _pryt_len(days, count)


def __pryt_len_festival(cal):
    """Recursivly generate prytanies that match the festival calendar."""
    if len(cal) == 0:
        return

    yield cal[0][1] - cal[0][0]
    yield from __pryt_len_festival(cal[1:])


def _pryt_gen(start, end, length, num=10, count=1):
    """Recursively generate dicts representing prytanies."""
    if count == num:
        # If this is the 10th prytany, return the EOY date as the end
        # date of the prytany, which may be one day more or one day
        # less than the expected length. Then stop
        yield {
            "prytany": count,
            "constant": list(Prytanies)[count - 1],
            "start": int(start),
            "end": int(end),
        }
        return

    # p_end = tt_round(start, next(length))
    p_end = heniautos.to_jdn(start) + next(length)

    yield {
        "prytany": count,
        "constant": list(Prytanies)[count - 1],
        "start": int(start),
        "end": int(p_end),
    }
    yield from _pryt_gen(p_end, end, length, num, count + 1)


def _pryt_auto(year):
    """Determine prytany type base on year."""
    if year < -507:
        raise heniautos.HeniautosError(
            "There were no prytanies before the foundation "
            "of democracy in Athens in 508 BCE"
        )

    if year >= -507 and year <= -409:
        return Prytany.QUASI_SOLAR

    if year >= -306 and year <= -223:
        return Prytany.ALIGNED_12

    if year >= -222 and year <= -200:
        return Prytany.ALIGNED_13

    if year >= -199 and year <= -100:
        return Prytany.ALIGNED_12

    return Prytany.ALIGNED_10


def _pryt_auto_start(year, start):
    """Determine start dates for quasi-solar prytanies. Based on Meritt
    (1961)

    """
    if start == Prytany.AUTO:
        if year < -423:
            # return tt_round(__h["ts"].ut1(year, 7, 4, 12, 0, 0))
            return jd.from_julian(year, 7, 4, 12, 0, 0)

        if year < -419:
            # return tt_round(__h["ts"].ut1(year, 7, 7, 12, 0, 0))
            return jd.from_julian(year, 7, 7, 12, 0, 0)

        if year < -418:
            # return tt_round(__h["ts"].ut1(year, 7, 8, 12, 0, 0))
            return jd.from_julian(year, 7, 8, 12, 0, 0)

        # return tt_round(__h["ts"].ut1(year, 7, 9, 12, 0, 0))
        return jd.from_julian(year, 7, 9, 12, 0, 0)

    # return tt_round(__h["ts"].ut1(year, 7, start, 12, 0, 0))
    return jd.from_julian(year, 7, start, 12, 0, 0)


def _pryt_solar_end(start):
    return heniautos.to_jdn(__add_years(start, 1))


def prytanies(
    year,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    rule=heniautos.Visible.NEXT_DAY,
    rule_of_aristotle=False,
    data=heniautos.load_data(),
):
    """Return tuple of prytanies. See prytany_calendar for parameters."""
    auto_type = _pryt_auto(year) if pryt_type == Prytany.AUTO else pryt_type

    if auto_type == Prytany.QUASI_SOLAR:
        start = _pryt_auto_start(year, pryt_start)
        end = _pryt_solar_end(start)
        p_len = _pryt_len(37, 5)
        pryt = _pryt_gen(start, end, p_len)
        return tuple([p for p in pryt])

    # Get the calendar for the requested year
    cal = heniautos.calendar_months(year, rule=rule, data=data)
    # y_len = sum([__span(*m) for m in calendar_months(year, rule=rule, data=data)])
    # y_len = sum([m[1] - m[0] for m in heniautos.calendar_months(year, rule=rule, data=data)])
    y_len = sum([m[1] - m[0] for m in cal])

    if auto_type == Prytany.ALIGNED_10:
        # Generate prytanies
        return tuple(
            [
                p
                for p in _pryt_gen(
                    cal[0][0], cal[-1][1], _pryt_len(39 if y_len > 355 else 36)
                )
            ]
        )

    if auto_type == Prytany.ALIGNED_12:
        # Generate prytanies
        # Normal: 30 * 6 + 29 * 6 (if rule of Aristotle is forced)
        # Intercalated: 32 * 12
        if y_len > 355 or rule_of_aristotle:
            return tuple(
                [
                    p
                    for p in _pryt_gen(
                        cal[0][0],
                        cal[-1][1],
                        _pryt_len(*((33, 0) if y_len > 355 else (30, 6))),
                        12,
                    )
                ]
            )

        # Normal year prytanies follow festival months unless rule of
        # Aristotle is forced
        return tuple(
            [p for p in _pryt_gen(cal[0][0], cal[-1][1], __pryt_len_festival(cal), 12)]
        )

    if auto_type == Prytany.ALIGNED_13:
        # Generate prytanies
        # Intercalated prytanies follow festival months unless rule of
        # Aristotle is forced
        if y_len > 355 and not rule_of_aristotle:
            return tuple(
                [
                    p
                    for p in _pryt_gen(
                        cal[0][0], cal[-1][1], __pryt_len_festival(cal), 13
                    )
                ]
            )

        # Normal: 28 * 3 + 27 * 10
        # Intercalated: 32 * 12
        return tuple(
            [
                p
                for p in _pryt_gen(
                    cal[0][0],
                    cal[-1][1],
                    _pryt_len(*((30, 7) if y_len > 355 else (28, 3))),
                    13,
                )
            ]
        )

    raise HeniautosError("Not Handled")


def _make_prytany(prytany, prytany_index, doy):
    return [
        PrytanyDay(
            prytany["start"] + d - 1, prytany_index, prytany["constant"], d, next(doy)
        )
        for d in range(1, prytany["end"] - prytany["start"] + 1, 1)
    ]


def _doy_gen(n=1):
    """Recursivly return natural numbers starting with n."""
    yield n
    yield from _doy_gen(n + 1)


def prytany_calendar(
    year,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    rule=heniautos.Visible.NEXT_DAY,
    rule_of_aristotle=False,
    data=heniautos.load_data(),
):
    """Return a tuple representing Athenian conciliar calendar.

        Parameters:
        year (int) -- The year for the calendar
        pryt_type (Prytany) -- Constant representign the type of prytanies
    (default Prytany,AUTO)
        pryt_start -- start day (in June) for quasi-solar prytanies. If
    Prytany.AUTO it will be calculated.
        rule (heniautos.Visible) -- Constant from heniautos.Visible indicating the desired rule
    (default heniautos.Visible.SECOND_DAY)
        data -- Astronomical data for calculations. By default this is
        returned from load_data()

        See calendar_months for documentation of visibility rules.

        Each member of the returned tuple is a dict containing:
            "prytany": the number of the prytany
            "constant": Prytanies constant for the prytany
            "days": a tuple with one member for day of the month.

        Each member of the "days" tuple is a dict containing:
             "day": the day of the month
             "date": the Julian date of the day
             "doy": the day of the year the day represents.
    """

    doy = _doy_gen()

    return tuple(
        [
            a
            for b in [
                _make_prytany(p, i, doy)
                for i, p in enumerate(
                    prytanies(
                        year,
                        pryt_type=pryt_type,
                        pryt_start=pryt_start,
                        rule=rule,
                        rule_of_aristotle=rule_of_aristotle,
                        data=data,
                    ),
                    1,
                )
            ]
            for a in b
        ]
    )


#     # return tuple([{"prytany": p["prytany"],
#     #                "constant": p["constant"],
#     #                "days": _month_days(p["start"], p["end"], doy)}
#     #               for p
#     #               in prytanies(year, pryt_type=pryt_type,
#     #                            pryt_start=pryt_start, rule=rule,
#     #                            rule_of_aristotle=rule_of_aristotle,
#     #                            data=data)])


def by_prytanies(p):
    """Return prytany calendar grouped into a tuple of tuples by prytany."""
    return heniautos.calendar_groups(p, lambda x: x.prytany)


def prytany_to_julian(year, prytany, day, rule=heniautos.Visible.NEXT_DAY, data=heniautos.load_data()):
    """Return the Julian Day Number for a prytany date.

    Parameters:
    year (int) -- The year
    prytany (Prytanies) -- Constant from Prytanies indicating the desired prytany
    day (int) -- The day
    rule (heniautos.Visible) -- Constant from heniautos.Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from heniautos.load_data()
    """
    try:
        return [
            p
            for p in prytany_calendar(year, rule=rule, data=data)
            if p.prytany == prytany and p.day == day
        ][0]
    except IndexError:
        raise heniautos.HeniautionNoDayInYearError(
            f"There is no day matching prytany {prytany}, day {day} in the year {year}"
        )


def _pryt_long_count(n, pryt_type, intercalated):
    """Return the number of long prytanies allowed for prytany type."""
    if pryt_type == Prytany.QUASI_SOLAR:
        return _max_or_fewer(n - 1, 5)

    if pryt_type == Prytany.ALIGNED_10:
        return _max_or_fewer(n - 1, 4)

    if pryt_type == Prytany.ALIGNED_12:
        return _max_or_fewer(n - 1, 7)

    if pryt_type == Prytany.ALIGNED_13 and not intercalated:
        return _max_or_fewer(n - 1, 3)

    if pryt_type == Prytany.ALIGNED_13 and intercalated:
        return _max_or_fewer(n - 1, 7)

    raise HeniautosError("Unhandled")


def _pryt_short_count(n, pryt_type, intercalated):
    """Return the number of short prytanies allowed for prytany type."""
    if pryt_type == Prytany.QUASI_SOLAR:
        return _max_or_fewer(n - 1, 5)

    if pryt_type == Prytany.ALIGNED_10:
        return _max_or_fewer(n - 1, 6)

    if pryt_type == Prytany.ALIGNED_12:
        return _max_or_fewer(n - 1, 5)

    if pryt_type == Prytany.ALIGNED_13 and not intercalated:
        return _max_or_fewer(n - 1, 10)

    if pryt_type == Prytany.ALIGNED_13 and intercalated:
        return _max_or_fewer(n - 1, 6)

    raise HeniautosError("Unhandled")


def _pryt_doy_ranges(pry, day, pryt_type, lng, intercalation):
    """Return possible DOYs with preceding prytanies."""
    if pryt_type == Prytany.ALIGNED_12 and intercalation:
        return [
            {
                "date": (pry, day),
                "doy": sum(r) + day,
                "preceding": r,
                "intercalation": intercalation,
            }
            for r in ((32,) * (pry - 1),)
        ]

    max_long = _pryt_long_count(pry, pryt_type, intercalation)
    max_short = _pryt_short_count(pry, pryt_type, intercalation)
    min_long = int(pry - 1) - max_short
    min_short = int(pry - 1) - max_long

    pairs = [
        p
        for p in product(range(min_long, max_long + 1), range(min_short, max_short + 1))
        if sum(p) == pry - 1
    ]

    ranges = [(lng,) * p[0] + (lng - 1,) * p[1] for p in pairs]

    return [
        {
            "date": (pry, day),
            "doy": sum(r) + day,
            "preceding": r,
            "intercalation": intercalation,
        }
        for r in ranges
    ]


def prytany_doy(pry, day, pryt_type=Prytany.AUTO, year=None):
    """Return possible DOYs for a given prytany and day.

    Calculates every possible DOY for a prytany and day with all the
    possible combinations of long and short prytanies preceding it.

    Parameters:
        pry (Prytanies): Prytanies constant for the month
        day (int): Day of the prytany
        pryt_type: Prytany constant for the type of prytany
        year: year, needed of pryt_type is Prytany.AUTO

    Returns a tuple of dicts, one for each DOY, and each consisting of:
        date: Prytany and day supplied
        doy: The DOY
        preceding: tuple of ints that are the lengths of the prytanies
                   preceding the given date, which goes in the DOY calculation
        intercalation: True if the DOY is for an intercalated year. N.B.: this
                       is different from festival_doy() because it True
                       for and intercalary DOY whether or not the intercalation
                       occurs before the given prytany or not.

    """
    if pryt_type == Prytany.AUTO:
        if year is None:
            raise heniautos.HeniautosError("Year required if pryt_type is Prytany.AUTO")
        return prytany_doy(pry, day, _pryt_auto(year))

    if pryt_type == Prytany.QUASI_SOLAR:
        return tuple(
            sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 37, None), key=lambda p: p["doy"]
            )
        )

    if pryt_type == Prytany.ALIGNED_10:
        if day > 36:
            # Must be intercalary
            return tuple(
                sorted(
                    _pryt_doy_ranges(pry, day, pryt_type, 39, True),
                    key=lambda p: p["doy"],
                )
            )

        return tuple(
            sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 36, False)
                + _pryt_doy_ranges(pry, day, pryt_type, 39, True),
                key=lambda p: p["doy"],
            )
        )

    if pryt_type == Prytany.ALIGNED_12:
        if day > 30:
            return tuple(
                sorted(
                    _pryt_doy_ranges(pry, day, pryt_type, 32, True),
                    key=lambda p: p["doy"],
                )
            )

        return tuple(
            sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 30, False)
                + _pryt_doy_ranges(pry, day, pryt_type, 32, True),
                key=lambda p: p["doy"],
            )
        )

    if pryt_type == Prytany.ALIGNED_13:
        if day > 28:
            return tuple(
                sorted(
                    _pryt_doy_ranges(pry, day, pryt_type, 30, True),
                    key=lambda p: p["doy"],
                )
            )

        return tuple(
            sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 28, False)
                + _pryt_doy_ranges(pry, day, pryt_type, 30, True),
                key=lambda p: p["doy"],
            )
        )

    raise HeniautosError("Unhandled")



