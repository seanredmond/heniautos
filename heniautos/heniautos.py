# heniautos. Ancient Athenian calendar generator
# Copyright (C) 2021 Sean Redmond

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
from datetime import datetime
from enum import IntEnum
from itertools import groupby, product, zip_longest
import juliandate as jd
from pathlib import Path
from heniautos.__version__ import __version__


class HeniautosError(Exception):
    pass


class HeniautosNoMatchError(Exception):
    pass


class HeniautosNoDataError(HeniautosError):
    pass


class HeniautionNoDayInYearError(HeniautosError):
    pass


class Seasons(IntEnum):
    """Constants representing the solar year seasons."""
    SPRING_EQUINOX = 0
    SUMMER_SOLSTICE = 1
    AUTUMN_EQUINOX = 2
    WINTER_SOLSTICE = 3


class Phases(IntEnum):
    NEW = 0
    FIRST_Q = 1
    FULL = 2
    LAST_Q = 3


class Visible(IntEnum):
    CONJUNCTION = 0
    NEXT_DAY = 1
    SECOND_DAY = 2
    DINSMOOR = 3


class Months(IntEnum):
    HEK = 1
    MET = 2
    BOE = 3
    PUA = 4
    MAI = 5
    POS = 6
    GAM = 7
    ANT = 8
    ELA = 9
    MOU = 10
    THA = 11
    SKI = 12
    INT = 13
    UNC = 14


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


MONTH_NAMES = ("Hekatombaiṓn",
               "Metageitniṓn",
               "Boēdromiṓn",
               "Puanopsiṓn",
               "Maimaktēriṓn",
               "Posideiṓn",
               "Gamēliṓn",
               "Anthestēriṓn",
               "Elaphēboliṓn",
               "Mounuchiṓn",
               "Thargēliṓn",
               "Skirophoriṓn")

MONTH_ABBREVS = ("Hek", "Met", "Boe", "Pua", "Mai", "Pos", "Gam", "Ant",
                 "Ela", "Mou", "Tha", "Ski")

MONTH_NAMES_GK = ("Ἑκατομβαιών",
                  "Μεταγειτνιών",
                  "Βοηδρομιών",
                  "Πυανοψιών",
                  "Μαιμακτηριών",
                  "Ποσιδειών",
                  "Γαμηλιών",
                  "Ἀνθεστηριών",
                  "Ἑλαφηβολιών",
                  "Μουνυχιών",
                  "Θαργηλιών",
                  "Σκιροφοριών")


class Prytany(IntEnum):
    AUTO = 0
    QUASI_SOLAR = 1
    ALIGNED_10 = 2
    ALIGNED_12 = 3
    ALIGNED_13 = 4


FestivalDay = namedtuple(
    "FestivalDay", ("jdn", "month_name", "month_index", "month", "day", "doy")
    )

PrytanyDay = namedtuple(
    "PrytanyDay", ("jdn", "prytany_index", "prytany", "day", "doy")
    )



def _load_data_file(fn):
    """Load astronomical data from file fn

    File should be tab-delimited lines containing a julian date (float) and an event/phase id (int):

    Event ids for solar events are: 0 = Spring Equinox, 1 = Summer Solstice,
    2 = Autumn Equinox, 3 = Winter Solstice

    Lunar phase ids are:  0 = New Moon, 1 = First Quarter, 2 = Full Moon, 4 = Last Quarter
"""
    with open(fn) as data:
        return tuple([tuple([i[0](i[1]) for i in zip((float, int), l.strip().split("\t"))]) for l in data])


def load_data(solstices=Path(__file__).parent / "solstices.tsv",
              new_moons=Path(__file__).parent / "new_moons.tsv"):
    """Load solstice/equinox and moon phase data from files."""
    return {"solstices": _load_data_file(solstices),
            "new_moons": _load_data_file(new_moons)}


def is_bce(t):
    """Return true if time t represents a BCE date."""
    # return t.ut1_calendar()[0] < 1
    return jd.to_julian(t)[0] < 1


def bce_as_negative(year):
    """Convert positive year (considered BCE) to negative number.

    BCE years are represented as years less than 1. 1 BCE is 0 so all numbers
    are offset by 1 in the positive direction."""

    return year * -1 + 1

# bce as_negative works in reverse, but this alias makes things cleaner
negative_as_bce = bce_as_negative


def to_jdn(t):
    """Converts a Julian date to a Julian Day Number."""
    return int(t + 0.5)


def date(y, m, d, h=9):
    """Return a ut1 date from calendar date.

    Parameters:
        y (int): The year, negative for BCE
        m (int): The month
        d (int): The day
        h (int): The hour (default 9)
    """
    return __h["ts"].ut1(y, m, d, h, 0, 0)


def add_hours(t, h):
    """Return a new JDN object with h hours added."""
    return jd.from_julian(*[sum(x) for x in zip(jd.to_julian(t), (0, 0, 0, h, 0, 0, 0))])


def add_days(t, d):
    """Return a new Time object with d days added to Time t."""
    return t + d


def add_years(t, y):
    """Return a new Time object with y years added to Time t."""
    return jd.from_julian(
        *[sum(x) for x in zip(jd.to_julian(t), (y, 0, 0, 0, 0, 0))])


def span(first, second):
    """Return the number of days between two dates."""
    # return int(second.tt) - int(first.tt)
    return to_jdn(second) - to_jdn(first)


def _epoch(t):
    """Return a string (BCE/CE) indicating the epoch of date t."""
    if is_bce(t):
        return "BCE"

    return " CE"


def _gmt_fmt_bce(j, full):
    """Convert negative (BCE) year for formating."""
    return _gmt_fmt((bce_as_negative(j[0]),) + j[1:], full, "BCE")


def _gmt_fmt(j, full, epoch=" CE"):
    """Return a short or full string representation of a JDN."""
    if full:
        return _gmt_fmt_full(j, epoch)

    return datetime(*j).strftime(f"{epoch} %Y-%b-%d")


def _gmt_fmt_full(j, epoch):
    """Return a full string representation of a JDN."""
    return datetime(*j).strftime(f"{epoch} %Y-%b-%d %H:%M:%S GMT")


def as_gmt(t, full=False):
    """Return a string representation of Julian date object in GMT.

    Parameters:
    t -- A Julian date (float or int)
    full -- Boolean. Return a full date if True, short date if False

    The full date representation of 1685074.3287423, for example is
    'BCE 0100-Jun-25 19:53:23 GMT', the short BCE 'BCE 0100-Jun-25'.

    """
    if is_bce(t):
        return _gmt_fmt_bce(jd.to_julian(t), full)

    if t >= 2299161: # Start of Gregorian Calendar
        return _gmt_fmt(jd.to_gregorian(t), full)
    
    
    return _gmt_fmt(jd.to_julian(t), full)


def as_eet(t, full=False):
    """Return a string representation of Time object in EET.

    Parameters:
    t -- A Julian date (float or int)
    full -- Boolean. Return a full date if True, short date if False

    Eastern European Time is the local timezone for Athens. This does
    not adjust for daylight savings and there may be some loss of
    precision due to floating point computations.

    The full date representation of 1685074.3287423, for example is
    'BCE 0100-Jun-25 21:53:23 EET', the short BCE 'BCE 0100-Jun-25'.

    """
    if full:
        return as_gmt(add_hours(t, 2), full)[0:25] + "EET"

    return as_gmt(add_hours(t, 2))


def solar_event(year, e, data=load_data()):
    """Return a Julian date (float) for the event e in the given year.

    Parameters:
    year (int) -- The year
    e (Seasons) -- Constant from Seasons indicating the event
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    """
    try:
        d1 = jd.from_julian(year, 1, 1)
        d2 = jd.from_julian(year, 12, 31, 23, 59, 59)
        return [s[0] for s in data["solstices"] if s[1] == e and s[0] >= d1 and s[0] <= d2][0]
    except IndexError:
        if year < 1:
            raise HeniautosNoDataError(f"No data for the year {bce_as_negative(year)} BCE")

        raise HeniautosNoDataError(f"No data for the year {year} CE")
        
        


def summer_solstice(year, data=load_data()):
    """Return Time objects for the summer solstice for the given year.

    Parameters:
    year -- The year for which the solstice is requested
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

"""
    return solar_event(year, Seasons.SUMMER_SOLSTICE, data=data)


# MAYBE REMOVE
def _all_moon_phases(year, data):
    d1 = jd.from_julian(year, 1, 1)
    d2 = jd.from_julian(year, 12, 31, 23, 59, 59)
    return [m for m in data["new_moons"] if m[0] >= d1 and m[0] <= d2] or None
    

# MAYBE REMOVE
def moon_phases(year, p=Phases.NEW, data=load_data()):
    """Return a list of Time objects for each indicated lunar phase in the
    given year.

    Parameters:
    year -- The year for which the phases are requested
    p (Phases) -- Constant from Phases indicating the lunar phase
    data -- Astronomical data for calculations. By default this is
    returned from load_data() (which only includes data from new moons)
    """
    try:
        phases = [mp[0] for mp in _all_moon_phases(year, data=data) if mp[1] == p]
        if phases:
            return phases

        raise HeniautosNoDataError("No data for requested lunar phase in requested year")
    except TypeError:
        if year < 1:
            raise HeniautosNoDataError(f"No data for the year {bce_as_negative(year)} BCE")

        raise HeniautosNoDataError(f"No data for the year {year} CE")


def new_moons(year, data=load_data()):
    """Return a list of Julian dates for all new moons e in the given year.

    Parameters:
    year -- The year for which the new moons are requested
    data -- Astronomical data for calculations. By default this is
    returned from load_data()
    """
    return moon_phases(year, Phases.NEW, data=data)


def visible_new_moons(year, rule=Visible.NEXT_DAY, data=load_data()):
    """Return a list of Julian dates for all visible new moons according
       to selected rule.

    Parameters:
    year (int) -- The year
    rule (Visible) -- Constant from Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    new_moons() returns the time of new moons according to an
    astronomical calculation, not when the waxing crescent of the new
    moon was first visible to human eyes. The time of first visibility
    is what is needed for calendar calculations but it is complicated
    so three simplified rules are provided:

    CONJUNCTION: The new moon is visible on the same day as the
    astronomical new moon (conjunction).

    NEXT_DAY: The moon is visible the first day after the
    astronomical new moon.

    SECOND_DAY (the default): The moon is visible the second day
    after the astronomical new moon.

    """
    if rule == Visible.CONJUNCTION:
        return [to_jdn(n) for n in new_moons(year, data=data)]

    if rule == Visible.NEXT_DAY:
        return [to_jdn(n) + 1 for n in new_moons(year, data=data)]

    if rule == Visible.SECOND_DAY:
        return [to_jdn(n) + 2 for n in new_moons(year, data=data)]


def _make_hour(t, h=9):
    """Return Time object for date t set to hour h (default 9)."""
    return __h["ts"].ut1(*(t.ut1_calendar()[0:3] + (h, 0, 0)))


def _on_after(t1, t2):
    """Is time t1 on or after time t2?"""
    return t1 > t2


def _before(t1, t2):
    """Is time t1 before t2?"""
    return not _on_after(t1, t2)


def _bounding_before(moons, sol1, sol2):
    """Return the first and last new moons for year if the beginning precedes sol1"""
    return ([m for m in moons if m < sol1][-1],
            [m for m in moons if m <= sol2][-2])
    

def _bounding_after(moons, sol1, sol2):
    """Return the first and last new moons for year if the beginning follows sol1"""
    return([m for m in moons if m > sol1][0],
           [m for m in moons if m <= sol2][-1])    
    

def _bounding_moons(moons, sol1, sol2, before_event):
    """Get the JDNs of the first and last new moons of a year depending on two solar events

    Paramters:
    moons: A tuple of JDNs extending before and after the expected bounds
    sol1: The solar event marking the beginning of the year
    sol2: The solar event marking the end of the year
    before_event: True if new moons should preceded the solar event, false if they should follow

    A Greek festival year either begins with the first new moon
    following a solar event (e.g. the Athenian year began at the first
    full moon following the summer solstice) or with the first new
    moon preceding a solar event (e.g. the Spartan year probably began
    at the first new moon preceding the autumn equinox.

    Return a tuple containing the JDNs of the first and last new moons
    of a year running from one solar event (sol1) to the next (sol2),
    depending on whether the beginning of the year precedes or follows
    the event as specified by the before_event parameter.
    """

    if before_event:
        return _bounding_before(moons, sol1, sol2)

    return _bounding_after(moons, sol1, sol2)



def calendar_months(year, event=Seasons.SUMMER_SOLSTICE, rule=Visible.NEXT_DAY,
                    before_event=False, data=load_data()):

    """Return a tuple representing start and end dates of Athenian festival
    calendar months.

    Parameters:
    year (int) -- The year for the calendar
    event (Seasons) -- The soloar event that marks the beginning of the year (default Seasons.SUMMER_SOLSTICE)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    before_event: True if new moons should preceded the solar event, false if they should follow
    data -- Astronomical data for calculations. By default this is
    returned from load_data()


    Return a tuple with start and end times, as Julian Day Numbers for
    each month, in order of Athenian festival calendar months
    calculated according to the give new moon visibility rule. The
    length of the tuple will be 12 for regular years or 13 for
    intercalary years. Each member of the tuple is a tuple with two
    members: (a) the start of the given month and (b) the start of the
    next month. The extent of the month is therefore inclusive of (a)
    and exclusive of b (a <= month < b).

    """
    sol1 = to_jdn(solar_event(year, event, data=data))
    sol2 = to_jdn(solar_event(year + 1, event, data=data))

    moons = [to_jdn(v) for v in visible_new_moons(year, rule, data=data) +
             visible_new_moons(year + 1, rule, data=data) +
             visible_new_moons(year + 2, rule, data=data)]

    first, last = _bounding_moons(moons, sol1, sol2, before_event)

    return tuple([m for m in zip(moons, moons[1:])
                  if m[0] >= first and m[0] <= last])


def _insert_interc(names, i, suffix):
    """Insert intercalated month name i with suffix suffix into list of
    month names names."""
    return names[:i] + ((names[i-1][0] + suffix, Months.INT),) + names[i:]


def _suffix(abbrev=False, greek=False):
    """Return suffix (if required) indicating an intercalated month.

    Parameters:
        abbrev (bool): Return abbreviated version
        greek (bool): Return Greek version (overrides abbrev)
    """
    if greek:
        return " ὕστερος"

    if abbrev:
        return "₂"

    return " hústeros"


def _maybe_intercalate(m, i, abbrev, greek):
    """Return a list of month names, with an intercalation if necessary

    Parameters:
        m (int): The number of months required
        i (Month): The month to intercalate (if required)
        abbrev (bool): Return names as abbreviations
        greek (bool): Return names in Greek

    """
    if m == 12:
        return tuple(zip(_month_names(abbrev, greek), Months))

    return _insert_interc(_maybe_intercalate(12, i, abbrev, greek), i,
                          _suffix(abbrev, greek))


def _month_names(abbrev, greek):
    """Return list of English, abbreviated, or Greek month names."""
    if greek:
        return MONTH_NAMES_GK

    if abbrev:
        return MONTH_ABBREVS

    return MONTH_NAMES


def month_label(m, abbrev=False, greek=False):
    if m == Months.INT:
        if abbrev:
            return "Int"
        return "Intercalated"

    return _month_names(abbrev, greek)[int(m)-1]


def prytany_label(p):
    return ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
            "XI", "XII", "XIII")[int(p)-1]


def generic_festival_months(year, event=Seasons.SUMMER_SOLSTICE,
                            before_event=False,
                            rule=Visible.NEXT_DAY,
                            data=load_data()):

    return tuple([{"month_index": m[0], "start": m[1][0], "end": m[1][1]}
                  for m in enumerate(calendar_months(year, event=event,
                                                     before_event=before_event,
                                                     rule=rule, data=data), 1)])


def festival_months(year, intercalate=Months.POS, abbrev=False, greek=False,
                    event=Seasons.SUMMER_SOLSTICE,
                    rule=Visible.NEXT_DAY,
                    data=load_data()):
    """Return a tuple representing Athenian festival calendar months.

    Parameters:
    year (int) -- The year for the calendar
    intercalate (Months) -- Constant indicating the month to intercalate if
    necessary
    abbrev (bool) -- Return month names as abbreviations (default False)
    greek (bool) -- Return month names in Greek (default False)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()


    See calendar_months for documentation of visibility rules.

    Returns a tuple with one member for each month. Each tuple contains:
        - The name of the calendar month (str)
        - A constant indicating the calendar (Months). This is Month.INT if the
          month is the intercalated month
        - A tuple of start and end dates of the month. See calendar_month
          for details on the start and end times.

    If intercalation is necessary, the intercalated month will be
    calculated according the the intercalate parameter.

    greek=True will override abbrev=True

    """
    if rule == Visible.DINSMOOR:
        return dinsmoor_months(year, abbrev, greek)
    months = calendar_months(year, event=event, rule=rule, data=data)

    return tuple([{"month": m[0][0],
                   "constant": m[0][1],
                   "start": m[1][0],
                   "end": m[1][1]}
                  for m in zip(
                          _maybe_intercalate(
                              len(months), intercalate, abbrev, greek),
                          months)])


def _doy_gen(n=1):
    """Recursivly return natural numbers starting with n."""
    yield n
    yield from _doy_gen(n + 1)


def _month_days(start, finish, doy):
    """Return tuple of dicts representing days of a month.

    Parameters:
        start: Start time of the month
        finish: Start time of next month
        doy: generator function to get the next day of the year
    """
    return tuple([{"day":  d + 1,
                   "date": add_days(start, d),
                   "doy":  next(doy)}
                  for d in range(0, int(finish) - int(start))])


def _make_month(month, month_index, doy):
    return [FestivalDay(month["start"] + d - 1, month["month"], month_index, month["constant"], d, next(doy)) for d in range(1, month["end"] - month["start"] + 1, 1)]


def generic_festival_calendar(year, rule=Visible.NEXT_DAY,
                              event=Seasons.SUMMER_SOLSTICE, data=load_data()):

    doy = _doy_gen()

    return tuple([a for b in
                  [_make_month(m, i, doy) for i, m in
                   enumerate(festival_months(year, intercalate=intercalate, abbrev=abbrev, greek=greek, rule=rule, event=event, data=data), 1)]
                  for a in b])


def festival_calendar(year, intercalate=Months.POS, abbrev=False, greek=False,
                      rule=Visible.NEXT_DAY, event=Seasons.SUMMER_SOLSTICE,
                      data=load_data()):
    """Return a tuple representing Athenian festival calendar.

    Parameters:
    year (int) -- The year for the calendar
    intercalate (Months) -- Month constant for month to intercalate if
necessary (default Months.POS)
    abbrev (bool) -- Return month names as abbreviations (default False)
    greek (bool) -- Return month names in Greek (default False)
    rule (Visible) -- Constant from Visible indicating the desired rule
(default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()


    See calendar_months for documentation of visibility rules.

    Returns a tuple with one member for each month. Each member is a
    tuple of the month name and tuple of start and end dates of the
    month. See calendar_month for details on the start and end times.

    If intercalation is necessary, the intercalated month will be
    calculated according the the intercalate parameter. This begins
    with 1 = Hekatombaiṓn, with a default of 6 = Poseidēiṓn.

    greek=True will override abbrev=True

    Each member of the tuple is a dict containing:
        "month": the name or abbreviation of the month.
        "constant": The constant of class Months of the month
        "days": a tuple with one member for day of the month.

    Each member of the "days" tuple is a dict containing:
         "day": the day of the month
         "date": the Julian Day Number of the day
         "doy": the day of the year the day represents.
    """
    doy = _doy_gen()

    return tuple([a for b in
                  [_make_month(m, i, doy) for i, m in
                   enumerate(festival_months(year, intercalate=intercalate, abbrev=abbrev, greek=greek, rule=rule, event=event, data=data), 1)]
                  for a in b])


def find_date(year, month, day, intercalate=Months.POS, abbrev=False,
              greek=False, rule=Visible.NEXT_DAY, data=load_data()):
    """Find the Athenian date corresponding to a Julian date

    Parameters:
    year (int) -- The Julian year, negative for BCE
    month (int) -- The Julian month
    day (int) -- The Julian day
    intercalate (Months) -- Month constant for month to intercalate if
necessary (default Months.POS)
    abbrev (bool) -- Return month names as abbreviations (default False)
    greek (bool) -- Return month names in Greek (default False)
    rule (Visible) -- Constant from Visible indicating the desired rule
(default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    """

    try:
        return [d for d in
                festival_calendar(year, intercalate=intercalate,
                                  abbrev=abbrev, greek=greek,
                                  rule=rule, data=data)
                if d.month == month and d.day == day][0]
    except IndexError:
        if month == Months.INT:
            raise HeniautosError(f"No date found or no intercalated month "
                                 f"in year {year}")

        raise HeniautosError(f"No date found for {MONTH_NAMES[month]} "
                             f"{day} {year}")


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


def _pryt_len_festival(cal):
    """Recursivly generate prytanies that match the festival calendar."""
    if len(cal) == 0:
        return

    yield span(*cal[0])
    yield from _pryt_len_festival(cal[1:])


def _pryt_gen(start, end, length, num=10, count=1):
    """Recursively generate dicts representing prytanies."""
    if count == num:
        # If this is the 10th prytany, return the EOY date as the end
        # date of the prytany, which may be one day more or one day
        # less than the expected length. Then stop
        yield {"prytany": count,
               "constant": list(Prytanies)[count-1],
               "start": int(start),
               "end": int(end)}
        return

    # p_end = tt_round(start, next(length))
    p_end = to_jdn(start) + next(length)

    yield {"prytany": count,
           "constant": list(Prytanies)[count-1],
           "start": int(start),
           "end": int(p_end)}
    yield from _pryt_gen(p_end, end, length, num, count + 1)


def _pryt_auto(year):
    """Determine prytany type base on year."""
    if year < -507:
        raise HeniautosError("There were no prytanies before the foundation "
                             "of democracy in Athens in 508 BCE")

    if year >= -507 and year <= -409:
        return Prytany.QUASI_SOLAR

    if year >= -306 and year <= -223:
        return Prytany.ALIGNED_12

    if year >= -222 and year <= -200:
        return Prytany.ALIGNED_13

    if year >= -199 and year <= -100:
        return Prytany.ALIGNED_12

    return Prytany.ALIGNED_10


def phulai_count(year):
    """ Return the number of phulaí in a given year. """
    pryt_t = _pryt_auto(year)

    if pryt_t == Prytany.ALIGNED_12:
        return 12

    if pryt_t == Prytany.ALIGNED_13:
        return 13

    return 10


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
    # return tt_round(add_years(start, 1))
    return to_jdn(add_years(start, 1))


def prytanies(year, pryt_type=Prytany.AUTO, pryt_start=Prytany.AUTO,
              rule=Visible.NEXT_DAY, rule_of_aristotle=False,
              data=load_data()):
    """Return tuple of prytanies. See prytany_calendar for parameters."""
    auto_type = _pryt_auto(year) if pryt_type == Prytany.AUTO else pryt_type

    if auto_type == Prytany.QUASI_SOLAR:
        start = _pryt_auto_start(year, pryt_start)
        end = _pryt_solar_end(start)
        p_len = _pryt_len(37, 5)
        pryt = _pryt_gen(start, end, p_len)
        return tuple([p for p in pryt])

    # Get the calendar for the requested year
    cal = calendar_months(year, rule=rule, data=data)
    y_len = sum([span(*m) for m in calendar_months(year, rule=rule, data=data)])

    if auto_type == Prytany.ALIGNED_10:
        # Generate prytanies
        return tuple([p for p
                      in _pryt_gen(cal[0][0], cal[-1][1],
                                   _pryt_len(39 if y_len > 355 else 36))])

    if auto_type == Prytany.ALIGNED_12:
        # Generate prytanies
        # Normal: 30 * 6 + 29 * 6 (if rule of Aristotle is forced)
        # Intercalated: 32 * 12
        if y_len > 355 or rule_of_aristotle:
            return tuple([p for p
                          in _pryt_gen(
                              cal[0][0], cal[-1][1],
                              _pryt_len(
                                  *((33, 0) if y_len > 355 else (30, 6))),
                              12)])

        # Normal year prytanies follow festival months unless rule of
        # Aristotle is forced
        return tuple([p for p
                      in _pryt_gen(cal[0][0], cal[-1][1],
                                   _pryt_len_festival(cal),
                                   12)])

    if auto_type == Prytany.ALIGNED_13:
        # Generate prytanies
        # Intercalated prytanies follow festival months unless rule of
        # Aristotle is forced
        if y_len > 355 and not rule_of_aristotle:
            return tuple([p for p
                          in _pryt_gen(cal[0][0], cal[-1][1],
                                       _pryt_len_festival(cal),
                                       13)])

        # Normal: 28 * 3 + 27 * 10
        # Intercalated: 32 * 12
        return tuple([p for p
                      in _pryt_gen(
                          cal[0][0], cal[-1][1],
                          _pryt_len(*((30, 7) if y_len > 355 else (28, 3))),
                          13)])

    raise HeniautosError("Not Handled")


def _make_prytany(prytany, prytany_index, doy):
    return [PrytanyDay(prytany["start"] + d - 1, prytany_index, prytany["constant"], d, next(doy)) for d in range(1, prytany["end"] - prytany["start"] + 1, 1)]


def prytany_calendar(year, pryt_type=Prytany.AUTO, pryt_start=Prytany.AUTO,
                     rule=Visible.NEXT_DAY, rule_of_aristotle=False,
                     data=load_data()):
    """Return a tuple representing Athenian conciliar calendar.

    Parameters:
    year (int) -- The year for the calendar
    pryt_type (Prytany) -- Constant representign the type of prytanies
(default Prytany,AUTO)
    pryt_start -- start day (in June) for quasi-solar prytanies. If
Prytany.AUTO it will be calculated.
    rule (Visible) -- Constant from Visible indicating the desired rule
(default Visible.SECOND_DAY)
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

    return tuple([a for b in
                  [_make_prytany(p, i, doy) for i, p in
                   enumerate(prytanies(year, pryt_type=pryt_type,
                                       pryt_start=pryt_start, rule=rule,
                                       rule_of_aristotle=rule_of_aristotle,
                                       data=data), 1)]
                  for a in b])
    

    # return tuple([{"prytany": p["prytany"],
    #                "constant": p["constant"],
    #                "days": _month_days(p["start"], p["end"], doy)}
    #               for p
    #               in prytanies(year, pryt_type=pryt_type,
    #                            pryt_start=pryt_start, rule=rule,
    #                            rule_of_aristotle=rule_of_aristotle,
    #                            data=data)])


def _calendar_groups(c, func):
    """Group calendar by func."""
    return [tuple(g[1]) for g in groupby(c, key=func)]


def by_months(p):
    """ Return festival calendar grouped into a tuple of tuples by months."""
    return tuple(_calendar_groups(p, lambda x: x.month))


def by_prytanies(p):
    """ Return prytany calendar grouped into a tuple of tuples by prytany."""
    return _calendar_groups(p, lambda x: x.prytany)


def doy_to_julian(doy, year, rule=Visible.NEXT_DAY, data=load_data()):
    """Return the Julian Day Number for the Day-of-Year in the given year.

    Parameters:
    doy (int) --  The Doy-of-Year
    year (int) -- The year
    rule (Visible) -- Constant from Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

"""
    try:
        return [d.jdn for d in festival_calendar(year, rule=rule, data=data) if d.doy == doy][0]
    except IndexError:
        raise HeniautionNoDayInYearError(f"There is no DOY {doy} in the year {year}")


def festival_to_julian(year, month, day, rule=Visible.NEXT_DAY, data=load_data()):
    """Return the Julian Day Number for a festival date.

    Parameters:
    year (int) -- The year
    month (Months) -- Constant from Months indicating the desired month
    day (int) -- The day
    rule (Visible) -- Constant from Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

"""
    try:

        return [d.jdn for d in festival_calendar(year, rule=rule, data=data) if d.month == month and d.day == day][0]
    except IndexError:
        raise HeniautionNoDayInYearError(f"There is no day matching month {month}, day {day} in the year {year}")


def prytany_to_julian(year, prytany, day, rule=Visible.NEXT_DAY, data=load_data()):
    """Return the Julian Day Number for a prytany date.

    Parameters:
    year (int) -- The year
    prytany (Prytanies) -- Constant from Prytanies indicating the desired prytany
    day (int) -- The day
    rule (Visible) -- Constant from Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

"""
    try:
        return [p for p in prytany_calendar(year, rule=rule, data=data) if p.prytany == prytany and p.day == day][0]
    except IndexError:
        raise HeniautionNoDayInYearError(f"There is no day matching prytany {prytany}, day {day} in the year {year}")


def _fest_long_count(n, intercalated):
    if not intercalated:
        return _max_or_fewer(n - 1, 7)

    return _max_or_fewer(n, 7)


def _fest_short_count(n, intercalated):
    if not intercalated:
        return _max_or_fewer(n - 1, 5)

    return _max_or_fewer(n, 6)


def _fest_doy_ranges(month, day, intercalation):
    """Return possible DOYs with preceding months."""
    pairs = [p for p
             in [(r, (int(month) + (0 if intercalation else -1)) - r)
                 for r in range(int(month) + (1 if intercalation else 0))]
             if p[0] <= 7 and p[1] <= (6 + (1 if intercalation else 0))]

    ranges = [(30,) * p[0] + (29,) * p[1] for p in pairs]

    return [{"date": (month, day),
             "doy": sum(m) + day,
             "preceding": m,
             "intercalation": intercalation}
            for m in ranges]


def festival_doy(month, day):
    """Return possible DOYs for a given month and day.

    Calculates every possible DOY for a month and day with all the
    possible comibinations of full and hollow months preceding it.

    Parameters:
        month (Months): Months constant for the month
        day (int): Day of the month

    Returns a tuple of dicts, one for each DOY, and each consisting of:
        date: Month and day supplied
        doy: The DOY
        preceding: tuple of ints that are the lengths of the months preceding
                   the given date, which goes in the DOY calculation
        intercalation: True if the DOY requires in intercalation among the
                       months preceding the given date. False otherwise

    """
    if month == Months.HEK:
        return _fest_doy_ranges(month, day, False)

    return tuple(sorted(_fest_doy_ranges(month, day, False) +
                        _fest_doy_ranges(month, day, True),
                        key=lambda m: m["doy"]))


def _max_or_fewer(n, mx):
    """Return n if n is less than mx, otherwise mx."""
    return n if n < mx else mx


def _pryt_long_count(n, pryt_type, intercalated):
    """ Return the number of long prytanies allowed for prytany type."""
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
    """ Return the number of short prytanies allowed for prytany type."""
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
        return [{"date": (pry, day),
                 "doy": sum(r) + day,
                 "preceding": r,
                 "intercalation": intercalation}
                for r in ((32,) * (pry - 1),)]

    max_long = _pryt_long_count(pry, pryt_type, intercalation)
    max_short = _pryt_short_count(pry, pryt_type, intercalation)
    min_long = int(pry - 1) - max_short
    min_short = int(pry - 1) - max_long

    pairs = [p for p in product(range(min_long, max_long + 1),
                                range(min_short, max_short + 1))
             if sum(p) == pry-1]

    ranges = [(lng,) * p[0] + (lng - 1,) * p[1] for p in pairs]

    return [{"date": (pry, day),
             "doy": sum(r) + day,
             "preceding": r,
             "intercalation": intercalation} for r in ranges]


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
            raise HeniautosError("Year required if pryt_type is Prytany.AUTO")
        return prytany_doy(pry, day, _pryt_auto(year))

    if pryt_type == Prytany.QUASI_SOLAR:
        return tuple(sorted(
            _pryt_doy_ranges(pry, day, pryt_type, 37, None),
            key=lambda p: p["doy"]))

    if pryt_type == Prytany.ALIGNED_10:
        if day > 36:
            # Must be intercalary
            return tuple(sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 39, True),
                key=lambda p: p["doy"]))

        return tuple(sorted(
            _pryt_doy_ranges(pry, day, pryt_type, 36, False) +
            _pryt_doy_ranges(pry, day, pryt_type, 39, True),
            key=lambda p: p["doy"]))

    if pryt_type == Prytany.ALIGNED_12:
        if day > 30:
            return tuple(sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 32, True),
                key=lambda p: p["doy"]))

        return tuple(sorted(
            _pryt_doy_ranges(pry, day, pryt_type, 30, False) +
            _pryt_doy_ranges(pry, day, pryt_type, 32, True),
            key=lambda p: p["doy"]))

    if pryt_type == Prytany.ALIGNED_13:
        if day > 28:
            return tuple(sorted(
                _pryt_doy_ranges(pry, day, pryt_type, 30, True),
                key=lambda p: p["doy"]))

        return tuple(sorted(
            _pryt_doy_ranges(pry, day, pryt_type, 28, False) +
            _pryt_doy_ranges(pry, day, pryt_type, 30, True),
            key=lambda p: p["doy"]))

    raise HeniautosError("Unhandled")


def _fest_eq(months):
    try:
        return festival_doy(months[0], months[1])
    except TypeError as e:
        # We got a tuple of tuples
        if "tuple" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        # We got a tuple of tuples, but the len is only 1
        pass

    return tuple(
        [a for b in [_fest_eq(m) for m in months] for a in b])


def _pryt_eq(prytanies, pryt_type=Prytany.AUTO, year=None):
    try:
        return prytany_doy(prytanies[0], prytanies[1], pryt_type=pryt_type,
                           year=year)
    except TypeError as e:
        if "'tuple'" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        pass

    return tuple(
        [a for b in [_pryt_eq(p, pryt_type=pryt_type, year=year)
                     for p in prytanies]
         for a in b])


def equations(months, prytanies, pryt_type=Prytany.AUTO, year=None):
    """Return possible solutions for a calendar equation

    Parameters:
        month (tuple): A tuple consisting of a Month constant and a day, or a
tuple of such tuples
        prytanies: A tuple consisting of a Prytany constant and a day, or a
tuple of such tuples
        year (int): Year, used to calculate prytany type is Prytany.AUTO
        pryt_type (Prytany): Type of prytany calendar to use
(default Prytany.AUTO)

    Returns a tuple of tuples. Each inner tuple is a pair of dicts,
    one for festival and one for conciliar calendar conditions that
    satisfy the equation for a particular DOY. Each of these dicts
    consists of:

        date: The festival or prytany date
        doy: The DOY of the date
        preceding: A tuple of lengths of the preceding months or prytanies
        intercalation: True if intercalation required for this solution

    Intercalation means something slightly different for the festival
    and conciliar calendar solutions. For the conciliar calendar True
    means that the year is intercalary because that affects the
    lengths of all the prytanies. For the festival calendar True means
    that an intercalation must precede the date because that effects
    the number of months, not the lengths. If a pair has intercalation
    = False in the festival solution but intercalation = True in the
    conciliar, it indicated that that solution is valid for an
    intercalary, but only if the intercalation follows the festival
    date.

    """
    pryt_eqs = _pryt_eq(prytanies, pryt_type, year)
    fest_eqs = _fest_eq(months)

    intersection = sorted(set([f["doy"] for f in fest_eqs]) &
                          set([p["doy"] for p in pryt_eqs]))

    return tuple([a for b in
                  [tuple(product([f for f in fest_eqs if f["doy"] == i],
                                 [p for p in pryt_eqs if p["doy"] == i]))
                   for i in intersection] for a in b
                  if not _misaligned_intercalation(a)])


def _misaligned_intercalation(i):
    """ Check if festival is intercalated but conciliar not."""
    if i[0]["intercalation"] is True and i[1]["intercalation"] is False:
        return True

    return False


def _no_deintercalations(i, pre=False):
    """Check festival intercalation sequence.

    Recursively check a sequence of festival month equation
    intercalation requirements. In festival month equation one with no
    intercalation can precede one with intercalation (because it's
    about when the intercalation occurse). Once one of the equations
    requires an intecalation before (True) none that follow can
    require no intercalation (False)

    """
    if not i:
        # If we got to then end of the sequence, it is good
        return True

    if pre is False and i[0] is False:
        # Proceed, no intercalation yet
        return _no_deintercalations(i[1:], False)

    if pre is True and i[0] is True:
        # Proceed, we have intercalation
        return _no_deintercalations(i[1:], True)

    if pre is False and i[0] is True:
        # Proceed, switch from no intercalation to intercalation
        return _no_deintercalations(i[1:], True)

    # The only condition left in pre == True and i[0] == False.
    # The forbidden condition. We have a precedeing intercalation
    # but the current equation requires none
    return False


def _is_contained_in(a, b):
    """Test whether the values in first tuple are contained in second."""
    if not len(a):
        # Successfully exhausted the first tuple. Return remainder
        return b

    try:
        i = b.index(a[0])
        return _is_contained_in(a[1:], b[:i] + b[i+1:])
    except ValueError as e:
        raise HeniautosNoMatchError(f"{a[0]} not found in {b}")


def _each_overlaps(b, a=tuple()):
    """ Test overlapping series of months or prytanies. """
    if not a:
        # First pass
        return _each_overlaps(b[1:], a + (b[0],))

    if not b:
        # Finished succesfully. Results in a
        return a

    # Just use a flattened version of a, results are the same
    # raises HeniautosNoMatchError if unsuccessful
    c = _is_contained_in([x for y in a for x in y], b[0])

    return _each_overlaps(b[1:], (a + (c,)))


def collations(*args, failures=False):
    """Collate multiple equations, looking for those that fit together.

    Take an arbitrary number of calendar equation results (args,
    i.e. results from equations()) and find those that fit together
    according to the following criteria:

        1) required conciliar years are all normal or all intercalary
        2) all equations that require festival year intercalation follow any
           that require no intercalations
        3) Each sequence of month and prytany lengths fits into the following
           sequences.

    Each equation results probably has multiple solutions. This test
    all combinations of solutions. Returns results as a tuple of dicts,
    each consiting of

        partitions: a dict with two members: "festival" and
        "conciliar." Each is a list of month or prytany lengths
        partitioned according to the requirements of the
        equations. For instance, ((30, 29), (30, 29), (30, 30, 29))
        means that the first equation must be preceded by one full and
        one hollow month; after the first equation but before the
        second there must by on full and one hollow month; after the
        second but before the third there must be two full and one
        hollow.

        equations: a list of equations making up this combined
        solution. Each is identical to a result returned from
        equations().

    If the optional "failures" parameter is true, return combinations
    that cannot be fitted together, as a list of combinations

    """
    successes = tuple()
    not_successes = tuple()

    for p in product(*args):
        try:
            # Criterion #1
            if len(set([c[1]["intercalation"] for c in p])) > 1:
                raise HeniautosNoMatchError()

            # Criterion #2
            if not _no_deintercalations([c[0]["intercalation"] for c in p]):
                raise HeniautosNoMatchError()

            # Criterion #3
            fest_partitions = _each_overlaps([c[0]["preceding"] for c in p])
            pryt_partitions = _each_overlaps([c[1]["preceding"] for c in p])
            successes = successes + ({"partitions":
                                      {"festival": fest_partitions,
                                       "conciliar": pryt_partitions},
                                      "equations": p},)

        except HeniautosNoMatchError as e:
            not_successes = not_successes + (p,)

    if failures is True:
        return not_successes

    return successes


def dinsmoor_month_name(m, intercalated, abbrev, greek):

    """Accomodate uncertain months in Dinsmoor data"""
    if m == Months.UNC:
        if abbrev:
            return "Unc"
        return "Uncertain"

    return (_month_names(abbrev, greek)[m-1] + _suffix(abbrev, greek)) \
        if intercalated else _month_names(abbrev, greek)[m-1]


def dinsmoor_months(year, abbrev=False, greek=False):
    """Return festival calendar according to Dinsmoor (1931)."""
    try:
        return [{"month": dinsmoor_month_name(m["constant"], m["intercalated"],
                                              abbrev, greek),
                 "constant": Months.INT if m["intercalated"]
                 else m["constant"],
                 # "start": date(m["year"], m["month"], m["day"]),
                 "start": int(jd.from_julian(m["year"], m["month"], m["day"], 12)),
                 "end": int(jd.from_julian(m["year"], m["month"], m["day"], 12)) + m["length"]}
                for m in _load_dinsmoor()[year]]
    except KeyError:
        raise HeniautosError(f"Year ({year}) outside range of Dinsmoor's "
                             "tables (432-109 BCE)")


def _dinsmoor_line(df, year, prev_month):
    """Parse a line of Dinsmoor data."""
    while True:
        line = df.readline()
        if line == '':
            raise StopIteration()

        if line.startswith("#"):
            continue

        parts = line[0:-1].split()
        if parts[0].isnumeric():
            year = bce_as_negative(int(parts[0]))
            m = 1
        else:
            m = 0

        month = ["Jan.", "Feb.", "March", "April", "May",
                 "June", "July", "Aug.", "Sept.", "Oct.",
                 "Nov.", "Dec."].index(parts[m]) + 1
        day = int(parts[m+1])
        mtype = {"+": 30, "-": 29}[parts[m+2]]
        intercalated = False
        try:
            if parts[m+3].endswith("*"):
                intercalated = True
                gm = parts[m+3][0:-1]
            else:
                gm = parts[m+3]

            gi = ["He", "Me", "Bo", "Py", "Ma", "Po", "Ga", "An", "El",
                  "Mo", "Th", "Sk"].index(gm)
            gmonth = list(Months)[gi]
            intercalated = intercalated or gmonth == prev_month
        except IndexError:
            intercalary = False
            gmonth = Months.UNC
        except KeyError as e:
            print(line)
            raise e

        return {"year": year,
                "month": month,
                "day": day,
                "constant": gmonth,
                "length": mtype,
                "intercalated": intercalated,
                "parts": parts}


def _load_dinsmoor():
    """Load Dinsmoor data."""
    d_years = {}
    with open(Path(__file__).parent / "dinsmoor.txt") as dinsmoor:
        this_year = None
        these_months = []
        last_year = None
        last_month = None
        been_read = 0
        while True:
            try:
                line = _dinsmoor_line(dinsmoor, last_year, last_month)
                if line["constant"] in (Months.HEK, Months.UNC) \
                   and been_read >= 12:
                    d_years = d_years | {these_months[0]["year"]: these_months}
                    these_months = []
                    been_read = 0

                these_months = these_months + [line]
                last_year = line["year"]
                last_month = line["constant"]
                been_read += 1

            except StopIteration:
                break

        return d_years


def version():
    return __version__
