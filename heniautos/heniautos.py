from enum import IntEnum
from itertools import product, zip_longest
from pathlib import Path
from skyfield import api
from skyfield import almanac
from skyfield.api import GREGORIAN_START


class HeniautosError(Exception):
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
    HEK = 0
    MET = 1
    BOE = 2
    PUA = 3
    MAI = 4
    POS = 5
    GAM = 6
    ANT = 7
    ELA = 8
    MOU = 9
    THA = 10
    SKI = 11
    INT = 12
    UNC = 13


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
               "Puanepsiṓn",
               "Maimaktēriṓn",
               "Poseidēiṓn",
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
                  "Πυανεψιών",
                  "Μαιμακτηριών",
                  "Ποσιδηϊών",
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


__h = {
    "init": False,
    "eph": None,
    "eph_file": "de422.bsp",
    "ts": None,
    "loc": None
}


def init_data(eph=None, lat=37.983972, lon=23.727806, force=False):
    """Initialize data required for calculations.

    Parameters:
        eph (str): Path to ephemeris file
        lat (float): Latitude for calculations (default 37.983972)
        lon (float): Longitude for calculations (default 23.727806)
        force (bool): Force reinitialization

    If an ephemeris file cannot be found in the path and no file is
    specified by the eph parameter, de422.bsp will be downloaded.

    Longitude and latitude are set for Athens by default but can be changed.

    Initialization will only be done once unless the force parameter is True.
    """
    if __h["init"] is True and not force:
        return

    if eph is not None:
        __h["eph_file"] = eph

    __h["eph"] = api.load(__h["eph_file"])
    __h["ts"] = api.load.timescale()
    __h["ts"].julian_calendar_cutoff = GREGORIAN_START
    __h["loc"] = api.wgs84.latlon(lat, lon)
    __h["init"] = True

    return api.load.path_to(__h["eph_file"])


def is_bce(t):
    """Return true if time t represents a BCE date."""
    return t.ut1_calendar()[0] < 1


def bce_as_negative(year):
    """Convert positive year (considered BCE) to negative number.

    BCE years are represented as years less than 1. 1 BCE is 0 so all numbers
    are offset by 1 in the positive direction."""

    return year * -1 + 1


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
    """Return a new Time object with h hours added to Time t."""
    return __h["ts"].ut1(
        *[sum(x) for x in zip(t.ut1_calendar(), (0, 0, 0, h, 0, 0))])


def add_days(t, d):
    """Return a new Time object with d days added to Time t."""
    return add_hours(t, d * 24)


def add_years(t, y):
    """Return a new Time object with y years added to Time t."""
    return __h["ts"].ut1(
        *[sum(x) for x in zip(t.ut1_calendar(), (y, 0, 0, 0, 0, 0))])


def span(first, second):
    """Return the number of days between two dates."""
    return int(second.tt) - int(first.tt)


def _epoch(t):
    """Return a string (BCE/CE) indicating the epoch of date t."""
    if is_bce(t):
        return "BCE"

    return " CE"


def as_gmt(t, full=False):
    """Return a string representation of Time object in GMT."""
    if full:
        return _epoch(t) + t.utc_jpl()[4:25] + " GMT"

    return _epoch(t) + t.utc_jpl()[4:16]


def as_eet(t, full=False):
    """Return a string representation of Time object in EET.

    Easter European Time is the local timezone for Athens. This does
    not adjust for daylight savings.

    """
    if full:
        return _epoch(t) + add_hours(t, 2).utc_jpl()[4:25] + " EET"

    return _epoch(t) + add_hours(t, 2).utc_jpl()[4:16]


def _solar_events(year):
    """Return Time objects for solstices and equinoxes for year y."""
    return tuple(
        zip(*almanac.find_discrete(
            __h["ts"].ut1(year, 1, 31),
            __h["ts"].ut1(year, 12, 31),
            almanac.seasons(__h["eph"]))))


def solar_event(year, e):
    """Return a Time object for the event e in the given year.

    Parameters:
        year (int): The year
        e (Seasons): Constant from Seasons indicating the event

    """
    return [se[0] for se in _solar_events(year) if se[1] == e][0]


def summer_solstice(year):
    """Return Time objects for the summer solstice for the given year."""
    return solar_event(year, Seasons.SUMMER_SOLSTICE)


def _all_moon_phases(year):
    """Return Time objects for all moon phases in year y."""
    return tuple(zip(*almanac.find_discrete(
        __h["ts"].ut1(year, 1, 1),
        __h["ts"].ut1(year, 12, 31, 23, 59, 59),
        almanac.moon_phases(__h["eph"]))))


def moon_phases(year, p):
    """Return a list of Time objects for each indicated lunar phase in the
    given year.

    Parameters:
        year (int): The year
        e (Phases): Constant from Phases indicating the lunar phase

    """
    return [mp[0] for mp in _all_moon_phases(year) if mp[1] == p]


def new_moons(year):
    """Return a list of Time objects for all new moons e in the given year."""
    return moon_phases(year, Phases.NEW)


def visible_new_moons(year, rule=Visible.SECOND_DAY):
    """Return a list of Time objects for all visible new moons according
       to selected rule.

    Parameters:
        year (int): The year
        rule (Visible): Constant from Visible indicating the desired rule

    new_moons() returns the time of new moons according to an
    astronomical calculation, not when the waxing crescent of the new
    moon was first visible to human eyes. The time of first visibility
    is what is needed for calendar calculations but it is complicated
    so two simplified rules are provided:

        SECOND_DAY (the default): The moon is visible the second day
    after the astronomical new moon.
        NEXT DAY: The moon is visible the first day after the
    astronomical new moon.

    """
    if rule == Visible.CONJUNCTION:
        return new_moons(year)

    if rule == Visible.NEXT_DAY:
        return [add_days(n, 1) for n in new_moons(year)]

    if rule == Visible.SECOND_DAY:
        return [add_days(n, 2) for n in new_moons(year)]


def _make_hour(t, h=9):
    """Return Time object for date t set to hour h (default 9)."""
    return __h["ts"].ut1(*(t.ut1_calendar()[0:3] + (h, 0, 0)))


def _on_after(t1, t2):
    """Is time t1 on or after time t2?"""
    return t1.tt > t2.tt


def _before(t1, t2):
    """Is time t1 before t2?"""
    return not _on_after(t1, t2)


def calendar_months(year, rule=Visible.SECOND_DAY):
    """Return a tuple representing start and end dates of Athenian festival
    calendar months.

    Parameters:
        year (int): The year for the calendar
        rule (Visible): Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)

    Return a tuple with start and end times for each month, in order
    of Athenian festival calendar months calculated according to the
    give new moon visibility rule. The length of the tuple will be 12
    for regular years or 13 for intercalary years. Each member of the
    tuple is a tuple with two members: (a) the start of the given
    month and (b) the start of the next month. The extent of the month
    is therefore inclusive of (a) and exclusive of b (a <= month < b).

    The returned Time objects have hours, minutes, and seconds, but
    these are just artifacts of the calendar calculates and are not
    meaningful. Only the Julian year, month, and day are relevant.

    """
    sol1 = summer_solstice(year)
    sol2 = summer_solstice(year + 1)

    moons = [_make_hour(v) for v in visible_new_moons(year, rule) +
             visible_new_moons(year + 1, rule)]

    return tuple([(m) for m in zip(moons, moons[1:])
                  if _on_after(m[0], sol1) and _before(m[0], sol2)])


def _insert_interc(names, i, suffix):
    """Insert intercalated month name i with suffix suffix into list of
    month names names."""
    return names[:i+1] + ((names[i][0] + suffix, Months.INT),) + names[i+1:]


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


def _intercalate(m, i, abbrev, greek):
    """Insert an intercalated month into a list of month names."""

    if m == 12:
        return tuple(zip(_month_names(abbrev, greek), Months))

    return _insert_interc(_intercalate(12, i, abbrev, greek), i,
                          _suffix(abbrev, greek))


def _month_names(abbrev, greek):
    """Return list of English, abbreviated, or Greek month names."""
    if greek:
        return MONTH_NAMES_GK

    if abbrev:
        return MONTH_ABBREVS

    return MONTH_NAMES


def festival_months(year, intercalate=Months.POS, abbrev=False, greek=False,
                    rule=Visible.SECOND_DAY):
    """Return a tuple representing Athenian festival calendar months.

    Parameters:
        year (int): The year for the calendar
        intercalate (Months): Constant indicating the month to intercalate if
        necessary
        abbrev (bool): Return month names as abbreviations (default False)
        greek (bool): Return month names in Greek (default False)
        rule (Visible): Constant from Visible indicating the desired rule
        (default Visible.SECOND_DAY)

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
    months = calendar_months(year, rule)

    return tuple([{"month": m[0][0],
                   "constant": m[0][1],
                   "start": m[1][0],
                   "end": m[1][1]}
                  for m in zip(_intercalate(len(months), intercalate,
                                            abbrev, greek), months)])


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
                  for d in range(0, int(finish.tt) - int(start.tt))])


def festival_calendar(year, intercalate=Months.POS, abbrev=False, greek=False,
                      rule=Visible.SECOND_DAY):
    """Return a tuple representing Athenian festival calendar.

    Parameters:
        year (int): The year for the calendar
        intercalate (Months): Month constant for month to intercalate if
necessary (default Months.POS)
        abbrev (bool): Return month names as abbreviations (default False)
        greek (bool): Return month names in Greek (default False)
        rule (Visible): Constant from Visible indicating the desired rule
(default Visible.SECOND_DAY)

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
         "date": the Julian date of the day
         "doy": the day of the year the day represents.
    """
    doy = _doy_gen()

    return tuple([{"month": m["month"],
                   "constant": m["constant"],
                   "days": _month_days(m["start"], m["end"], doy)}
                  for m
                  in festival_months(year, intercalate, abbrev, greek, rule)])


def find_date(year, month, day, intercalate=Months.POS, abbrev=False,
              greek=False, rule=Visible.SECOND_DAY):
    """Find the Athenian date corresponding to a Julian date

    Parameters:
        year (int): The Julian year, negative for BCE
        month (int): The Julian month
        day (int): The Julian day
        intercalate (Months): Month constant for month to intercalate if
necessary (default Months.POS)
        abbrev (bool): Return month names as abbreviations (default False)
        greek (bool): Return month names in Greek (default False)
        rule (Visible): Constant from Visible indicating the desired rule
(default Visible.SECOND_DAY)
    """
    try:
        return [a for b
                in [[{**{"month": f["month"], "constant": f["constant"]}, **d}
                     for d in f["days"] if d["day"] == day]
                    for f in festival_calendar(year, intercalate=intercalate,
                                               abbrev=abbrev, greek=greek,
                                               rule=rule)
                    if f["constant"] == month] for a in b][0]
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
        yield {"prytany": count, "start": start, "end": end}
        return

    p_end = add_days(start, next(length))

    yield {"prytany": count, "start": start, "end": p_end}
    yield from _pryt_gen(p_end, end, length, num, count + 1)


def _pryt_auto(year):
    """Determine prytany type base on year."""
    if year < -507:
        raise HeniautosError("There were no prytanies before the foundation "
                             "of democracy in Athens in 508 BCE")

    if year >= -507 and year <= -409:
        return Prytany.QUASI_SOLAR

    if year >= -306 and year <= -221:
        return Prytany.ALIGNED_12

    if year >= -220 and year <= -200:
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
            return __h["ts"].ut1(year, 7, 4, 12, 0, 0)

        if year < -419:
            return __h["ts"].ut1(year, 7, 7, 12, 0, 0)

        if year < -418:
            return __h["ts"].ut1(year, 7, 8, 12, 0, 0)

        return __h["ts"].ut1(year, 7, 9, 12, 0, 0)

    return __h["ts"].ut1(year, 7, start, 12, 0, 0)


def _pryt_solar_end(start):
    return add_years(start, 1)


def prytanies(year, pryt_type=Prytany.AUTO, pryt_start=Prytany.AUTO,
              rule=Visible.SECOND_DAY, rule_of_aristotle=False):
    """Return tuple of prytanies. See prytany_celendar for parameters."""
    auto_type = _pryt_auto(year) if pryt_type == Prytany.AUTO else pryt_type

    if auto_type == Prytany.QUASI_SOLAR:
        start = _pryt_auto_start(year, pryt_start)
        end = _pryt_solar_end(start)
        p_len = _pryt_len(37, 5)
        pryt = _pryt_gen(start, end, p_len)
        return tuple([p for p in pryt])

    # Get the calendar for the requested year
    cal = calendar_months(year, rule)
    y_len = sum([span(*m) for m in calendar_months(year, rule)])
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


def prytany_calendar(year, pryt_type=Prytany.AUTO, pryt_start=Prytany.AUTO,
                     rule=Visible.SECOND_DAY, rule_of_aristotle=False):
    """Return a tuple representing Athenian conciliar calendar.

    Parameters:
        year (int): The year for the calendar
        pryt_type (Prytany): Constant representign the type of prytanies
(default Prytany,AUTO)
        pryt_start: start day (in June) for quasi-solar prytanies. If
Prytany.AUTO it will be calculated.
        rule (Visible): Constant from Visible indicating the desired rule
(default Visible.SECOND_DAY)

    See calendar_months for documentation of visibility rules.

    Each member of the returned tuple is a dict containing:
        "prytany": the number of the prytany
        "days": a tuple with one member for day of the month.

    Each member of the "days" tuple is a dict containing:
         "day": the day of the month
         "date": the Julian date of the day
         "doy": the day of the year the day represents.
    """

    doy = _doy_gen()

    return tuple([{"prytany": p["prytany"],
                   "days": _month_days(p["start"], p["end"], doy)}
                  for p
                  in prytanies(year, pryt_type=pryt_type,
                               pryt_start=pryt_start, rule=rule,
                               rule_of_aristotle=rule_of_aristotle)])


def _months_sum(s):
    """ Return the sum of pairs of ints multiplied by each other.

    That is given numbers of months and their lengths, calculate their sum.

    For example:
    ((30, 1), (29, 2)) =
    (30 * 1) + (29 * 2) =
    30 + 58
    = 88
    """
    return sum([(x[0] * x[1]) for x in s])


def _cal_doy_single(pry_orig, pry, day, interc, length):
    """ Return a dict with DOY calculated from pairs of months and lengths
    where there is only one length.

    That is, calculate potential DOYs if all the months are 32 days.
    """
    return tuple([{"date": (pry_orig, day),
                   "doy": p * length + day,
                   "lengths": ((length, p),),
                   "intercalated": interc}
                  for p in [pry - 1]])


def _cal_doy_len(pry_orig, pry, day, interc, lengths):
    """ Return a dict with DOY calculated from pairs of months and lengths

    That is, calculate potential DOYs give a number of months of length L1 and
    a number of months of L2.
    """
    return tuple([{"date": (pry_orig, day),
                   "doy": _months_sum(c) + day,
                   "lengths": c,
                   "intercalated": interc}
                  for c in [tuple(zip(lengths, [p, pry-p-1]))
                            for p in range(pry)]])


def _cal_lengths_calc(pry_orig, pry, day, interc, lengths):
    """ Dispatch correct DOY calculation depending on whether the months
    are all one length or different lengths.
    """
    return _cal_doy_single(pry_orig, pry, day, interc, lengths[0]) \
        if len(lengths) == 1 \
        else _cal_doy_len(pry_orig, pry, day, interc, lengths)


def _cal_length_sort(cal):
    """ Sort a list of DOY dicts ont the "doy" value. """
    return sorted(cal, key=lambda d: d["doy"])


def _within_max_diff(ln, max_d):
    """Is the difference in count of follow and hollow less than max_d? """
    if max_d and len(ln["lengths"]) > 1:
        return abs(ln["lengths"][0][1] - ln["lengths"][1][1]) <= max_d

    return True


def _calc_min_count(cal_count, full, hollow, test_min, test):
    """Do the count of full and hollow meet minimums?"""
    return (test_min - test) <= (cal_count - full - hollow)


def _meets_min_count(c, cal_count, min_full, min_hollow):
    """Do the count of full and hollow meet minimums?"""
    # Intercalary, 12 tribes, all are 32-days so ignore min count
    if len(c["lengths"]) == 1 and c["lengths"][0][0] == 32:
        return True

    return _calc_min_count(
        cal_count, c["lengths"][0][1], c["lengths"][1][1],
        min_full, c["lengths"][0][1]) and \
        _calc_min_count(
            cal_count, c["lengths"][0][1], c["lengths"][1][1],
            min_hollow, c["lengths"][1][1])


def _cal_lengths(pry_orig, pry, day, lengths, max_diff, cal_c, min_f, min_h):
    """ Return a flattened list of DOYs of all lengths in lengths. """
    return _cal_length_sort(
        [c for c in
         [a for b in
          [_cal_lengths_calc(pry_orig, pry, day, i, l) for i, l in lengths]
          for a in b]
         if _meets_min_count(c, cal_c, min_f, min_h)
         and _within_max_diff(c, max_diff)])


def festival_doy(month, day, max_diff=0):
    """Return the possible values of DOY for a Greek month and day."""
    return tuple(
        _cal_length_sort(
            _cal_lengths(month, month + 1, day, ((False, (30, 29)),),
                         max_diff, 12, 5, 5) +
            _cal_lengths(month, month + 2, day, ((True, (30, 29)),),
                         max_diff, 13, 6, 5)))


def prytany_doy(pry, day, year=None, pryt_type=Prytany.AUTO, max_diff=0):
    """Return the possible values of DOY for a prytany and day."""
    pryt_auto = _pryt_auto(year) \
        if year is not None and pryt_type == Prytany.AUTO else pryt_type

    if pryt_auto == Prytany.QUASI_SOLAR:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (37, 36)),), max_diff, 10, 5, 5)))

    if pryt_auto == Prytany.ALIGNED_10:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (36, 35)), (True, (39, 38))),
                             max_diff, 10, 4, 6)))

    if pryt_auto == Prytany.ALIGNED_12:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (30, 29)), (True, (32,))),
                             max_diff, 12, 5, 5)))

    if pryt_auto == Prytany.ALIGNED_13:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (28, 27)), (True, (30, 29))),
                             max_diff, 13, 3, 7)))

    raise HeniautosError("No Prytany type identified. Did you forget to "
                         "supply a year?")


def _fest_eq(months, max_diff=0):
    try:
        return festival_doy(months[0], months[1], max_diff)
    except TypeError as e:
        # We got a tuple of tuples
        if "to tuple" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        # We got a tuple of tuples, but the len is only 1
        pass

    return tuple(
        [a for b in [_fest_eq(m, max_diff) for m in months] for a in b])


def _pryt_eq(prytanies, max_diff=0, year=None, pryt_type=Prytany.AUTO):
    try:
        return prytany_doy(prytanies[0], prytanies[1], year=year,
                           max_diff=max_diff, pryt_type=pryt_type)
    except TypeError as e:
        if "'tuple' object" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        pass

    return tuple(
        [a for b in [_pryt_eq(p, max_diff=max_diff, year=year,
                              pryt_type=pryt_type) for p in prytanies]
         for a in b])


def equations(months, prytanies, max_fest_diff=0, max_pryt_diff=0, year=None,
              pryt_type=Prytany.AUTO):
    """Return possible solutions for a calendar equation

    Parameters:
        month (tuple): A tuple consisting of a Month constant and a day, or a
tuple of such tuples
        prytanies: A tuple consisting of a Prytany constant and a day, or a
tuple of such tuples
        year (int): Year, used to calculate prytany type is Prytany.AUTO
        pryt_type (Prytany): Type of prytany calendar to use
(default Prytany.AUTO)

    """
    pryt_eqs = _pryt_eq(prytanies, max_pryt_diff, year, pryt_type)
    fest_eqs = _fest_eq(months, max_fest_diff)

    matches = sorted(
        set([p["doy"] for p in pryt_eqs]) & set([f["doy"] for f in fest_eqs]))

    return tuple([{
        "doy": doy,
        "equations": {"festival": [f for f in fest_eqs if f["doy"] == doy],
                      "conciliar": [p for p in pryt_eqs if p["doy"] == doy]}}
                  for doy in matches])


def dinsmoor_month_name(m, intercalated, abbrev, greek):
    """Accomodate uncertain months in Dinsmoor data"""
    if m == Months.UNC:
        if abbrev:
            return "Unc"
        return "Uncertain"

    return (_month_names(abbrev, greek)[m] + _suffix(abbrev, greek)) \
        if intercalated else _month_names(abbrev, greek)[m]


def dinsmoor_months(year, abbrev=False, greek=False):
    """Return festival calendar according to Dinsmoor (1931)."""
    if "dinsmoor" not in __h:
        __h["dinsmoor"] = _load_dinsmoor()

    try:
        return [{"month": dinsmoor_month_name(m["constant"], m["intercalated"],
                                              abbrev, greek),
                 "constant": Months.INT if m["intercalated"]
                 else m["constant"],
                 "start": date(m["year"], m["month"], m["day"]),
                 "end": add_days(date(m["year"], m["month"], m["day"]),
                                 m["length"])}
                for m in __h["dinsmoor"][year]]
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
