from enum import IntEnum
from itertools import product, zip_longest
from skyfield import api
from skyfield import almanac
from skyfield.api import GREGORIAN_START


# from  .patterndata import *


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
    NEXT_DAY = 0
    SECOND_DAY = 1


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
    if __h["init"] is True and not force:
        return

    if eph is not None:
        __h["eph_file"] = eph

    __h["eph"] = api.load(__h["eph_file"])
    __h["ts"] = api.load.timescale()
    __h["ts"].julian_calendar_cutoff = GREGORIAN_START
    __h["loc"] = api.wgs84.latlon(37.983972, 23.727806)
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
    """Return the Time object for the summer solstice for the given year."""
    return solar_event(year, Seasons.SUMMER_SOLSTICE)


def _all_moon_phases(year):
    return tuple(zip(*almanac.find_discrete(
        __h["ts"].ut1(year, 1, 1),
        __h["ts"].ut1(year, 12, 31, 23, 59, 59),
        almanac.moon_phases(__h["eph"]))))


def moon_phases(year, p):
    """Return a list of Time objects for all lunar phases e in the given year.

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
    if rule == Visible.NEXT_DAY:
        return [add_days(n, 1) for n in new_moons(year)]

    if rule == Visible.SECOND_DAY:
        return [add_days(n, 2) for n in new_moons(year)]


def _make_hour(t, h=9):
    return __h["ts"].ut1(*(t.ut1_calendar()[0:3] + (h, 0, 0)))


def _on_after(t1, t2):
    return t1.tt > t2.tt


def _before(t1, t2):
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
    months = calendar_months(year, rule)

    return tuple([{"month": m[0][0],
                   "constant": m[0][1],
                   "start": m[1][0],
                   "end": m[1][1]}
                  for m in zip(_intercalate(len(months), intercalate,
                                            abbrev, greek), months)])


def _doy_gen(n=1):
    yield n
    yield from _doy_gen(n + 1)


def _month_days(start, finish, doy):
    return tuple([{"day":  d + 1,
                   "date": add_days(start, d),
                   "doy":  next(doy)}
                  for d in range(0, int(finish.tt) - int(start.tt))])


def festival_calendar(year, intercalate=Months.POS, abbrev=False, greek=False,
                      rule=Visible.SECOND_DAY):
    """Return a tuple representing Athenian festival calendar.

    Parameters:
        year (int): The year for the calendar
        intercalate (int): index of month to intercalate if necessary
    (starting with 1 default 6 = Poseidēiṓn)
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
    if count:
        yield days
        yield from _pryt_len(days, count - 1)

    if count == 0:
        yield from _pryt_len(days - 1, count - 1)

    yield from _pryt_len(days, count)


def _pryt_len_festival(cal):
    if len(cal) == 0:
        return

    yield span(*cal[0])
    yield from _pryt_len_festival(cal[1:])


def _pryt_gen(start, end, length, num=10, count=1):

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
    if year < -507:
        raise HeniautosError("There were no prytanies before the foundation of"
                             "democracy in Athens in 508 BCE")

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
    doy = _doy_gen()

    return tuple([{"prytany": p["prytany"],
                   "days": _month_days(p["start"], p["end"], doy)}
                  for p
                  in prytanies(year, pryt_type=pryt_type,
                               pryt_start=pryt_start, rule=rule,
                               rule_of_aristotle=rule_of_aristotle)])


PrytanyOrd = IntEnum("PrytanyOrd", "VARIABLE STRICT")


# class TribeCount(IntEnum):
#     TEN = 10
#     TWELVE = 12


# YearType = IntEnum("YearType", "O I")

    
# def _prytany_sum(lengths, counts):
#     return sum([lengths[x] * counts[x] for x in [0, 1]])


# def _pry_valid(full_count, pry, strict):
#     if strict == PrytanyOrd.STRICT:
#         full_min = 4 if pry > 4 else pry
#         return full_count == full_min

#     return True


# def _prytany_doy_10(pry, day, strict: PrytanyOrd=PrytanyOrd.STRICT):
#     plen = dict(zip(YearType, [[36, 35], [39, 38]]))

#     return [{"doy": _prytany_sum(b[0], plen[b[1]]) + day,
#              "intercalation": b[1] == YearType.I,
#              "preceding": b[0]}
#             for b in product([[p, pry - p]
#                               for p in range(0, pry + 1)
#                               if _pry_valid(p, pry, strict)], YearType)]


#     # return [[_prytany_sum(b[0], plen[b[1]]) + day, b[1], b[0]]
#     #         for b in product([[p, pry - p]
#     #                           for p in range(0, pry + 1)
#     #                           if _pry_valid(p, pry, strict)], YearType)]



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
    """ Dispatch correct DOY calculation depending on whether there months 
    are all one length or different lengths.
    """
    return _cal_doy_single(pry_orig, pry, day, interc, lengths[0]) \
        if len(lengths) == 1 \
        else _cal_doy_len(pry_orig, pry, day, interc, lengths)


def _cal_length_sort(cal):
    """ Sort a list of DOY dicts ont the "doy" value. """
    return sorted(cal, key=lambda d: d["doy"])


def _within_max_diff(l, max_d):
    if max_d and len(l["lengths"]) > 1:
        return abs(l["lengths"][0][1] - l["lengths"][1][1]) <= max_d
    
    return True


def _cal_lengths(pry_orig, pry, day, lengths, max_diff):
    """ Return a flattened list of DOYs of all lengths in lengths. """
    return _cal_length_sort(
        [c for c in [a for b in
         [_cal_lengths_calc(pry_orig, pry, day, i, l)
          for i, l in lengths]
                     for a in b] if _within_max_diff(c, max_diff)])


def festival_doy(month, day, max_diff=4):
    return tuple(
        _cal_length_sort(
            _cal_lengths(month, month + 1, day, ((False, (30, 29)),),
                         max_diff) + 
            _cal_lengths(month, month + 2, day, ((True, (30, 29)),),
                         max_diff)))


def prytany_doy(pry, day, year=None, pryt_type=Prytany.AUTO, max_diff=0):
    pryt_auto = _pryt_auto(year) \
        if year is not None and pryt_type == Prytany.AUTO else pryt_type

    if pryt_auto == Prytany.QUASI_SOLAR:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (37, 36)),), max_diff)))
    
    if pryt_auto == Prytany.ALIGNED_10:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (36, 35)), (True, (39, 38))), max_diff)))
    
    if pryt_auto == Prytany.ALIGNED_12:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (30, 29)), (True, (32,))), max_diff)))

    if pryt_auto == Prytany.ALIGNED_13:
        return tuple(
            _cal_length_sort(
                _cal_lengths(pry, pry, day,
                             ((False, (28, 27)), (True, (30, 29))), max_diff)))
    
    raise HeniautosError("No Prytany type identified. Did you forget to "
                         "supply a year?")


def _fest_eq(months, max_diff=4):
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
                       
    

def equations(months, prytanies, max_fest_diff=4, max_pryt_diff=0, year=None,
              pryt_type=Prytany.AUTO):
    pryt_eqs = _pryt_eq(prytanies, max_pryt_diff, year, pryt_type)
    fest_eqs = _fest_eq(months, max_fest_diff)
    #matches = sorted(set([x["doy"] for x in fest_eqs + pryt_eqs]))

    matches = sorted(
        set([p["doy"] for p in pryt_eqs]) & set([f["doy"] for f in fest_eqs]))

    return tuple([{
        "doy": doy,
        "equations": {"festival": [f for f in fest_eqs if f["doy"] == doy],
                      "conciliar": [p for p in pryt_eqs if p["doy"] == doy]}}
                  for doy in matches])
