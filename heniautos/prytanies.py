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
# import heniautos
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

def load_data():
    from heniautos import load_data
    return load_data()

def __optionally_load_data(data):
    """Return result of function call if param is a function, or the param."""
    if callable(data):
        return data()

    return data


# Maybe remove
def __add_years(t, y):
    """Return a new Time object with y years added to Time t."""
    return jd.from_julian(*[sum(x) for x in zip(jd.to_julian(t), (y, 0, 0, 0, 0, 0))])


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
    import heniautos
    
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


def prytany_type(year):
    """Determine prytany type base on year."""
    from heniautos import HeniautosError

    if year < -507:
        raise HeniautosError(
            "There were no prytanies before the foundation "
            "of democracy in Athens in 508 BCE"
        )

    if year >= -507 and year <= -375:
        return Prytany.QUASI_SOLAR

    if year >= -306 and year <= -223:
        return Prytany.ALIGNED_12

    if year >= -222 and year <= -200:
        return Prytany.ALIGNED_13

    if year >= -199 and year <= -100:
        return Prytany.ALIGNED_12

    return Prytany.ALIGNED_10


def _pryt_auto_start(
    year,
    pryt_start=Prytany.AUTO,
    v_off=1,
    s_off=0,
    data=(),
):
    """Determine start dates for quasi-solar prytanies. Based on Meritt
    (1961)

    """

    from heniautos import festival_to_jdn

    if pryt_start != Prytany.AUTO:
        offset = year - jd.to_julian(pryt_start)[0]
        return pryt_start + (offset * 366)

    start_jdn = festival_to_jdn(-406, 1, 1, v_off=v_off, s_off=s_off, data=data)
    offset = year - jd.to_julian(start_jdn)[0]

    return start_jdn + (offset * 366)


def _pryt_solar_end(start):
    return heniautos.to_jdn(__add_years(start, 1))


def __prytanies(
    year,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    v_off=1,
    s_off=0,
    rule_of_aristotle=False,
    data=load_data,
):
    """Return tuple of prytanies. See prytany_calendar for parameters."""

    from heniautos import calendar_months
    
    auto_type = prytany_type(year) if pryt_type == Prytany.AUTO else pryt_type

    if auto_type == Prytany.QUASI_SOLAR:
        start = _pryt_auto_start(year, pryt_start, v_off=v_off, s_off=s_off, data=data)
        end = start + 366  # _pryt_solar_end(start)
        p_len = _pryt_len(37, 6)
        pryt = _pryt_gen(start, end, p_len)
        return tuple([p for p in pryt])

    # Get the calendar for the requested year
    cal = calendar_months(year, v_off=v_off, s_off=s_off, data=data)
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


def __make_prytany(prytany, pryt_year, prytany_index, doy, year_length, year):
    from heniautos import PrytanyDay
    return [
        PrytanyDay(
            prytany["start"] + d - 1,
            prytany_index,
            prytany["constant"],
            prytany["end"] - prytany["start"],
            d,
            next(doy),
            pryt_year,
            year_length,
            year
        )
        for d in range(1, prytany["end"] - prytany["start"] + 1, 1)
    ]


def prytany_calendar(
    year,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    v_off=1,
    s_off=0,
    rule_of_aristotle=False,
    data=load_data
):
    """Return a tuple representing Athenian conciliar calendar.

    Parameters:
    year (int) -- The year for the calendar
    pryt_type (Prytany) -- Constant representign the type of prytanies
    (default Prytany,AUTO)
    pryt_start -- start day (JDN) for quasi-solar prytanies. If
    Prytany.AUTO it will be calculated as the first day of 407 BCE (which was also Prytany 1.1 that year) If an integer (a JDN), 366-day prytanies will be calculated relative to this day.
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

    from heniautos import doy_gen, arkhon_year, festival_to_jdn
    doy = doy_gen()
    cal_year = arkhon_year(year)


    astro_data = __optionally_load_data(data)
    

    pryt_year = __prytanies(
        year,
        pryt_type=pryt_type,
        pryt_start=pryt_start,
        v_off=v_off,
        s_off=s_off,
        rule_of_aristotle=rule_of_aristotle,
        data=astro_data,
    )
    year_len = pryt_year[-1]["end"] - pryt_year[0]["start"]

    return tuple(
        [
            a
            for b in [
                __make_prytany(p, cal_year, i, doy, year_len, year)
                for i, p in enumerate(pryt_year, 1)
            ]
            for a in b
        ]
    )


def by_prytanies(p):
    """Return prytany calendar grouped into a tuple of tuples by prytany."""
    from heniautos import calendar_groups
    return calendar_groups(p, lambda x: x.prytany)


def prytany_to_julian(
    year, prytany, day, v_off=1, s_off=0, data=load_data
):
    """Return the Julian Day Number for a prytany date.

    Parameters:
    year (int) -- The year
    prytany (Prytanies) -- Constant from Prytanies indicating the desired prytany
    day (int) -- The day
    rule (heniautos.Visible) -- Constant from heniautos.Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from heniautos.load_data()
    """
    from heniautos import HeniautosNoDayInYearError
    try:
        return [
            p
            for p in prytany_calendar(year, v_off=v_off, s_off=s_off, data=data)
            if p.prytany == prytany and p.day == day
        ][0]
    except IndexError:
        raise HeniautosNoDayInYearError(
            f"There is no day matching prytany {prytany}, day {day} in the year {year}"
        )


def jdn_to_prytany_day(
    jdn,
    year=None,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    v_off=1,
    s_off=0,
    rule_of_aristotle=False,
    data=load_data,
):

    # If the year hint is not supplied, extract it from the jdn and recurse
    if not isinstance(year, int):
        return jdn_to_prytany_day(
            jdn,
            jd.to_julian(jdn)[0],
            pryt_type=pryt_type,
            pryt_start=pryt_start,
            v_off=v_off,
            s_off=s_off,
            rule_of_aristotle=rule_of_aristotle,
            data=data,
        )

    return [
        d
        for d in [
            a
            for b in [
                prytany_calendar(
                    y,
                    pryt_type=pryt_type,
                    pryt_start=pryt_start,
                    v_off=v_off,
                    s_off=s_off,
                    rule_of_aristotle=rule_of_aristotle,
                    data=data,
                )
                for y in range(year - 1, year + 2)
            ]
            for a in b
        ]
        if d.jdn == jdn
    ][0]


def julian_to_prytany_day(
    year,
    month,
    day,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    v_off=1,
    s_off=0,
    rule_of_aristotle=False,
    data=load_data,
):
    from heniautos import to_jdn
    return jdn_to_prytany_day(
        to_jdn(jd.from_julian(year, month, day)),
        year,
        pryt_type=pryt_type,
        pryt_start=pryt_start,
        v_off=v_off,
        s_off=s_off,
        rule_of_aristotle=rule_of_aristotle,
        data=data,
    )


def gregorian_to_prytany_day(
    year,
    month,
    day,
    pryt_type=Prytany.AUTO,
    pryt_start=Prytany.AUTO,
    v_off=1,
    s_off=0,
    rule_of_aristotle=False,
    data=load_data,
):
    from heniautos import to_jdn
    return jdn_to_prytany_day(
        to_jdn(jd.from_gregorian(year, month, day)),
        year,
        pryt_type=pryt_type,
        pryt_start=pryt_start,
        v_off=v_off,
        s_off=s_off,
        rule_of_aristotle=rule_of_aristotle,
        data=data,
    )
