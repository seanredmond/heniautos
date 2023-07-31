# coding=utf-8

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
#from datetime import datetime
from enum import IntEnum, Enum  # , auto
from itertools import groupby, product  # , zip_longest
import juliandate as jd
from pathlib import Path
from heniautos.__version__ import __version__


class HeniautosError(Exception):
    pass


class HeniautosNoMatchError(HeniautosError):
    pass


class HeniautosNoDataError(HeniautosError):
    pass


class HeniautosNoDayInYearError(HeniautosError):
    pass


class HeniautosDateNotFoundError(HeniautosError):
    pass


class Seasons(IntEnum):
    """Constants representing the solar year seasons."""

    SPRING_EQUINOX = 0
    SUMMER_SOLSTICE = 1
    AUTUMN_EQUINOX = 2
    WINTER_SOLSTICE = 3


class Phases(IntEnum):
    """Constants representing the lunar phases."""

    NEW = 0
    FIRST_Q = 1
    FULL = 2
    LAST_Q = 3


class MonthNameOptions(IntEnum):
    """Options for displaying Greek month names."""

    TRANSLITERATION = 0
    ABBREV = 1
    GREEK = 2


class Cal(Enum):
    """Constants representing available calendars."""

    ARGIVE = object()
    ATHENIAN = object()
    CORINTHIAN = object()
    DELIAN = object()
    DELPHIAN = object()
    SPARTAN = object()

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)


class Visible(IntEnum):
    """Constants representing lunar visibility options."""

    CONJUNCTION = 0
    NEXT_DAY = 1
    SECOND_DAY = 2


class TZOptions(Enum):
    GMT = "GMT"
    ALT = "ALT"


class Months(IntEnum):
    INT = 13
    UNC = 14


class ArgiveMonths(IntEnum):
    AGU = 1
    KAR = 2
    ERI = 3
    HER = 4
    GAM = 5
    TEL = 6
    ARN = 7
    ART = 8
    AGR = 9
    AMU = 10
    PAN = 11
    APE = 12


class AthenianMonths(IntEnum):
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


class DelianMonths(IntEnum):
    LEN = 1
    IER = 2
    GAL = 3
    ART = 4
    THA = 5
    PAN = 6
    HEK = 7
    MET = 8
    BOU = 9
    APA = 10
    ARE = 11
    POS = 12


class DelphianMonths(IntEnum):
    APE = 1
    BOU = 2
    BOA = 3
    HER = 4
    DAD = 5
    POI = 6
    AMA = 7
    BUS = 8
    THE = 9
    END = 10
    HKL = 11
    ILA = 12


class SpartanMonths(IntEnum):
    UN1 = 1
    UN2 = 2
    UN3 = 3
    UN4 = 4
    UN5 = 5
    UN6 = 6
    UN7 = 7
    UN8 = 8
    UN9 = 9
    U10 = 10
    U11 = 11
    U12 = 12


class CorinthianMonths(IntEnum):
    PHO = 1
    KRA = 2
    LAN = 3
    MAK = 4
    DOD = 5
    EUK = 6
    ART = 7
    PSU = 8
    GAM = 9
    AGR = 10
    PAN = 11
    APE = 12


CALENDAR_MAP = {
    Cal.ARGIVE: ArgiveMonths,
    Cal.ATHENIAN: AthenianMonths,
    Cal.CORINTHIAN: CorinthianMonths,
    Cal.DELPHIAN: DelphianMonths,
    Cal.DELIAN: DelianMonths,
    Cal.SPARTAN: SpartanMonths,
}

# Since the values of Enums like AthenianMonths.HEK and
# DelianMonths.LEN are integers (both of these == 1), we need to use
# something more specific as this dict key
MONTH_NAME_MAP = {
    (Cal.ATHENIAN, AthenianMonths.HEK): ("Hekatombaiṓn", "Hek", "Ἑκατομβαιών"),
    (Cal.ATHENIAN, AthenianMonths.MET): ("Metageitniṓn", "Met", "Μεταγειτνιών"),
    (Cal.ATHENIAN, AthenianMonths.BOE): ("Boēdromiṓn", "Boe", "Βοηδρομιών"),
    (Cal.ATHENIAN, AthenianMonths.PUA): ("Puanopsiṓn", "Pua", "Πυανοψιών"),
    (Cal.ATHENIAN, AthenianMonths.MAI): ("Maimaktēriṓn", "Mai", "Μαιμακτηριών"),
    (Cal.ATHENIAN, AthenianMonths.POS): ("Posideiṓn", "Pos", "Ποσιδειών"),
    (Cal.ATHENIAN, AthenianMonths.GAM): ("Gamēliṓn", "Gam", "Γαμηλιών"),
    (Cal.ATHENIAN, AthenianMonths.ANT): ("Anthestēriṓn", "Ant", "Ἀνθεστηριών"),
    (Cal.ATHENIAN, AthenianMonths.ELA): ("Elaphēboliṓn", "Ela", "Ἑλαφηβολιών"),
    (Cal.ATHENIAN, AthenianMonths.MOU): ("Mounukhiṓn", "Mou", "Μουνυχιών"),
    (Cal.ATHENIAN, AthenianMonths.THA): ("Thargēliṓn", "Tha", "Θαργηλιών"),
    (Cal.ATHENIAN, AthenianMonths.SKI): ("Skirophoriṓn", "Ski", "Σκιροφοριών"),
    (Cal.DELIAN, DelianMonths.LEN): ("Lēnaiṓn", "Len", "Ληναιών"),
    (Cal.DELIAN, DelianMonths.IER): ("Hierós", "Hie", "Ἱερός"),
    (Cal.DELIAN, DelianMonths.GAL): ("Galaxiṓn", "Gal", "Γαλαξιών"),
    (Cal.DELIAN, DelianMonths.ART): ("Artemisiṓn", "Art", "Αρτεμισιών"),
    (Cal.DELIAN, DelianMonths.THA): ("Thargēliṓn", "Tha", "Θαργηλιών"),
    (Cal.DELIAN, DelianMonths.PAN): ("Pánēmos", "Pan", "Πάνημος"),
    (Cal.DELIAN, DelianMonths.HEK): ("Hekatombaiṓn", "Hek", "Ἑκατομβαιών"),
    (Cal.DELIAN, DelianMonths.MET): ("Metageitniṓn", "Met", "Μεταγειτνιών"),
    (Cal.DELIAN, DelianMonths.BOU): ("Bouphoniṓn", "Bou", "Βουφονιών"),
    (Cal.DELIAN, DelianMonths.APA): ("Apatouriṓn", "Apa", "Ἀπατουριών"),
    (Cal.DELIAN, DelianMonths.ARE): ("Arēsiṓn", "Are", "Ἀρησιών"),
    (Cal.DELIAN, DelianMonths.POS): ("Posideiṓn", "Pos", "Ποσιδειών"),
    (Cal.SPARTAN, SpartanMonths.UN1): ("Unknown 1", "? 1", "Unknown 1"),
    (Cal.SPARTAN, SpartanMonths.UN2): ("Unknown 2", "? 2", "Unknown 2"),
    (Cal.SPARTAN, SpartanMonths.UN3): ("Unknown 3", "? 3", "Unknown 3"),
    (Cal.SPARTAN, SpartanMonths.UN4): ("Unknown 4", "? 4", "Unknown 4"),
    (Cal.SPARTAN, SpartanMonths.UN5): ("Unknown 5", "? 5", "Unknown 5"),
    (Cal.SPARTAN, SpartanMonths.UN6): ("Unknown 6", "? 6", "Unknown 6"),
    (Cal.SPARTAN, SpartanMonths.UN7): ("Unknown 7", "? 7", "Unknown 7"),
    (Cal.SPARTAN, SpartanMonths.UN8): ("Unknown 8", "? 8", "Unknown 8"),
    (Cal.SPARTAN, SpartanMonths.UN9): ("Unknown 9", "? 9", "Unknown 9"),
    (Cal.SPARTAN, SpartanMonths.U10): ("Unknown 10", "? 10", "Unknown 10"),
    (Cal.SPARTAN, SpartanMonths.U11): ("Unknown 11", "? 11", "Unknown 11"),
    (Cal.SPARTAN, SpartanMonths.U12): ("Unknown 12", "? 12", "Unknown 12"),
    (Cal.CORINTHIAN, CorinthianMonths.PHO): ("Phoinikaîos", "Pho", "Φοινικαῖος"),
    (Cal.CORINTHIAN, CorinthianMonths.KRA): ("Kráneios", "Kra", "Κράνειος"),
    (Cal.CORINTHIAN, CorinthianMonths.LAN): ("Lanotropíos", "Lan", "Λανοτροπίος"),
    (Cal.CORINTHIAN, CorinthianMonths.MAK): ("Makhaneús", "Mak", "Μαχανεύς"),
    (Cal.CORINTHIAN, CorinthianMonths.DOD): ("Dōdekateús", "Dod", "Δωδεκατεύς"),
    (Cal.CORINTHIAN, CorinthianMonths.EUK): ("Εúkleios", "Euk", "Εὔκλειος"),
    (Cal.CORINTHIAN, CorinthianMonths.ART): ("Artemísios", "Art", "Ἀρτεμίσιος"),
    (Cal.CORINTHIAN, CorinthianMonths.PSU): ("Psudreús", "Psu", "Ψυδρεύς"),
    (Cal.CORINTHIAN, CorinthianMonths.GAM): ("Gameílios", "Gam", "Γαμείλιος"),
    (Cal.CORINTHIAN, CorinthianMonths.AGR): ("Agriánios", "Agr", "Αγριάνιος"),
    (Cal.CORINTHIAN, CorinthianMonths.PAN): ("Pánamos", "Pan", "Πάναμος"),
    (Cal.CORINTHIAN, CorinthianMonths.APE): ("Apellaîos", "Ape", "Ἀπελλαῖος"),
    (Cal.DELPHIAN, DelphianMonths.APE): ("Apellaîos", "Ape", "Ἀπελλαῖος"),
    (Cal.DELPHIAN, DelphianMonths.BOU): ("Boukátios", "Bou", "Βουκάτιος"),
    (Cal.DELPHIAN, DelphianMonths.BOA): ("Boathóos", "Boa", "Βοαθόος"),
    (Cal.DELPHIAN, DelphianMonths.HER): ("Heraîos", "Her", "Ἡραῖος"),
    (Cal.DELPHIAN, DelphianMonths.DAD): ("Dadaphórios", "Dad", "Δᾳδαφόριος"),
    (Cal.DELPHIAN, DelphianMonths.POI): ("Poitrópios", "Poi", "Ποιτρόπιος"),
    (Cal.DELPHIAN, DelphianMonths.AMA): ("Amálios", "Ama", "Ἀμάλιος"),
    (Cal.DELPHIAN, DelphianMonths.BUS): ("Búsios", "Bus", "Βύσιος"),
    (Cal.DELPHIAN, DelphianMonths.THE): ("Theoxénios", "The", "Θεοξένιος"),
    (Cal.DELPHIAN, DelphianMonths.END): ("Enduspoitrópios", "End", "Ἐνδυσποιτρόπιος"),
    (Cal.DELPHIAN, DelphianMonths.HKL): ("Herákleios", "Hkl", "Ἡράκλειος"),
    (Cal.DELPHIAN, DelphianMonths.ILA): ("Ilaîos", "Ila", "Ἰλαῖος"),
    (Cal.ARGIVE, ArgiveMonths.AGU): ("Agúeios", "Agu", "Ἀγύειος"),
    (Cal.ARGIVE, ArgiveMonths.KAR): ("Karneîos", "Kar", "Καρνεῖος"),
    (Cal.ARGIVE, ArgiveMonths.ERI): ("Erithaieos", "Eri", "Ἐριθαιεος"),
    (Cal.ARGIVE, ArgiveMonths.HER): ("Hermaîos", "Her", "Ἑρμαῖος"),
    (Cal.ARGIVE, ArgiveMonths.GAM): ("Gámos", "Gam", "Γάμος"),
    (Cal.ARGIVE, ArgiveMonths.TEL): ("Téleos", "Tel", "Τέλεος"),
    (Cal.ARGIVE, ArgiveMonths.ARN): ("Arneîos", "Arn", "Ἀρνεῖος"),
    (Cal.ARGIVE, ArgiveMonths.ART): ("Artamítios", "Art", "Ἀρταμίτιος"),
    (Cal.ARGIVE, ArgiveMonths.AGR): ("Agriánios", "Agr", "Ἀγριάωιος"),
    (Cal.ARGIVE, ArgiveMonths.AMU): ("Amuklaîos", "Amu", "Ἀμυκλαῖος"),
    (Cal.ARGIVE, ArgiveMonths.PAN): ("Pánamos", "Pan", "Πάναμος"),
    (Cal.ARGIVE, ArgiveMonths.APE): ("Apellaîos", "Ape", "Ἀπελλαῖος"),
}


# REMOVE
MONTH_ABBREVS = (
    "Hek",
    "Met",
    "Boe",
    "Pua",
    "Mai",
    "Pos",
    "Gam",
    "Ant",
    "Ela",
    "Mou",
    "Tha",
    "Ski",
)

FestivalDay = namedtuple(
    "FestivalDay",
    (
        "jdn",
        "month_name",
        "month_index",
        "month",
        "month_length",
        "day",
        "doy",
        "year",
        "year_length",
        "astronomical_year",
    ),
)

PrytanyDay = namedtuple(
    "PrytanyDay",
    (
        "jdn",
        "prytany_index",
        "prytany",
        "prytany_length",
        "day",
        "doy",
        "year",
        "year_length",
        "astronomical_year",
    ),
)


def __load_data_file(fn):
    """Load astronomical data from file fn

    File should be tab-delimited lines containing a julian date (float) and an event/phase id (int):

    Event ids for solar events are: 0 = Spring Equinox, 1 = Summer Solstice,
    2 = Autumn Equinox, 3 = Winter Solstice

    Lunar phase ids are:  0 = New Moon, 1 = First Quarter, 2 = Full Moon, 4 = Last Quarter"""
    with open(fn) as data:
        return tuple(
            [
                tuple([i[0](i[1]) for i in zip((float, int), l.strip().split("\t"))])
                for l in data
            ]
        )


def load_data(
    solstices=Path(__file__).parent / "solstices.tsv",
    new_moons=Path(__file__).parent / "new_moons.tsv",
):
    """Load solstice/equinox and moon phase data from files."""
    return {
        "solstices": __load_data_file(solstices),
        "new_moons": __load_data_file(new_moons),
    }


def is_bce(t):
    """Return true if time t represents a BCE date."""
    return jd.to_julian(t)[0] < 1


def bce_as_negative(year):
    """Convert positive year (considered BCE) to negative number.

    BCE years are represented as years less than 1. 1 BCE is 0 so all numbers
    are offset by 1 in the positive direction."""

    return year * -1 + 1


# # bce as_negative works in reverse, but this alias makes things cleaner
negative_as_bce = bce_as_negative


def arkhon_year(year):
    epoch = "BCE" if year < 1 else " CE"
    year1 = negative_as_bce(year) if year < 1 else year
    year2 = year1 - 1 if epoch == "BCE" else year1 + 1
    return f"{epoch} {year1}/{year2}"


def to_jdn(t):
    """Converts a Julian date to a Julian Day Number."""
    return int(t + 0.5)


def __gmt_fmt_bce(j, full, tz=TZOptions.GMT):
    """Convert negative (BCE) year for formating."""
    return __gmt_fmt((bce_as_negative(j[0]),) + j[1:], full, "BCE", tz)


def __jul_month(m):
    return (
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    )[m - 1]


def __gmt_fmt(j, full, epoch=" CE", tz=TZOptions.GMT):
    """Return a short or full string representation of a JDN."""
    if full:
        return __gmt_fmt(j, False, epoch, tz) + f" {j[3]:02d}:{j[4]:02d}:{j[5]:02d} {tz.value}"

    return f"{epoch} {j[0]:04d}-{__jul_month(j[1])}-{j[2]:02d}"


def __alt_offset(jd, tz):
    """Convert a JDN to a value that represents “Athens Local Time”, 23.728056 degrees east of Greenwich."""
    if tz == TZOptions.ALT:
        return jd + (23.728056 / 360)

    return jd


def as_julian(t, full=False, tz=TZOptions.GMT):
    """Return a string representation of Julian date object as a Julian calendar date.

    Parameters:
    t -- A Julian date (float or int)
    full -- Boolean. Return a full date if True, short date if False
    tz -- TZOptions. Convert GMT (default) or "Athens Local Time" (AST)

    The full date representation of 1685074.3287423, for example is
    'BCE 0100-Jun-25 19:53:23 GMT', the short BCE 'BCE 0100-Jun-25'.

    Dates following the start of the gregorian calendar (10/15/1682)
    are returned as Gregorian calendar dates.

    """
    if isinstance(t, FestivalDay) or isinstance(t, PrytanyDay):
        return as_julian(t.jdn, full, tz)

    if is_bce(t):
        return __gmt_fmt_bce(jd.to_julian(__alt_offset(t, tz)), full, tz=tz)

    if t >= 2299161:  # Start of Gregorian Calendar
        return as_gregorian(t, full, tz)

    return __gmt_fmt(jd.to_julian(__alt_offset(t, tz)), full, tz=tz)


def as_gregorian(t, full=False, tz=TZOptions.GMT):
    """Return a string representation of Julian date object as a Gregorian calendar date.

    Parameters:
    t -- A Julian date (float or int)
    full -- Boolean. Return a full date if True, short date if False
    tz -- TZOptions. Convert GMT (default) or "Athens Local Time" (AST)

    The full date representation of 1685074.3287423, for example is
    'BCE 0100-Jun-25 19:53:23 GMT', the short BCE 'BCE 0100-Jun-25'.

    """
    if is_bce(t):
        return __gmt_fmt_bce(jd.to_gregorian(__alt_offset(t, tz)), full, tz=tz)

    return __gmt_fmt(jd.to_gregorian(__alt_offset(t, tz)), full, tz=tz)


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
        return [s[0] for s in data["solstices"] if s[1] == e and d1 <= s[0] <= d2][0]
    except IndexError:
        if year < 1:
            raise HeniautosNoDataError(
                f"No data for the year {bce_as_negative(year)} BCE"
            )

        raise HeniautosNoDataError(f"No data for the year {year} CE")


# # MAYBE REMOVE
def __all_moon_phases(year, data):
    d1 = jd.from_julian(year, 1, 1)
    d2 = jd.from_julian(year, 12, 31, 23, 59, 59)
    return [m for m in data["new_moons"] if d1 <= m[0] <= d2] or None


# # MAYBE REMOVE
def __moon_phases(year, p=Phases.NEW, data=load_data()):
    """Return a list of Julian dates for each indicated lunar phase in the
    given year.

    Parameters:
    year -- The year for which the phases are requested
    p (Phases) -- Constant from Phases indicating the lunar phase
    data -- Astronomical data for calculations. By default this is
    returned from load_data() (which only includes data from new moons)
    """
    try:
        phases = [mp[0] for mp in __all_moon_phases(year, data=data) if mp[1] == p]
        if phases:
            return phases

        raise HeniautosNoDataError(
            "No data for requested lunar phase in requested year"
        )
    except TypeError:
        if year < 1:
            raise HeniautosNoDataError(
                f"No data for the year {bce_as_negative(year)} BCE"
            )

        raise HeniautosNoDataError(f"No data for the year {year} CE")


def new_moons(year, data=load_data()):
    """Return a list of Julian dates for all new moons e in the given year.

    Parameters:
    year -- The year for which the new moons are requested
    data -- Astronomical data for calculations. By default this is
    returned from load_data()
    """
    return __moon_phases(year, Phases.NEW, data=data)


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

    NEXT_DAY (Default): The moon is visible the first day after the
    astronomical new moon.

    SECOND_DAY: The moon is visible the second day
    after the astronomical new moon.

    """
    if rule == Visible.CONJUNCTION:
        return [to_jdn(n) for n in new_moons(year, data=data)]

    if rule == Visible.NEXT_DAY:
        return [to_jdn(n) + 1 for n in new_moons(year, data=data)]

    if rule == Visible.SECOND_DAY:
        return [to_jdn(n) + 2 for n in new_moons(year, data=data)]


def month_name(month, name_as=MonthNameOptions.TRANSLITERATION):
    """Returns the month name corresponding to the given constant"""
    try:
        return [v for m, v in MONTH_NAME_MAP.items() if m[1] is month][0][name_as]
    except IndexError:
        raise HeniautosNoMatchError(f"No month names matching {month}")


def __bounding_before(moons, sol1, sol2):
    """Return the first and last new moons for year if the beginning precedes sol1"""
    return ([m for m in moons if m <= sol1][-1], [m for m in moons if m <= sol2][-2])


def __bounding_after(moons, sol1, sol2):
    """Return the first and last new moons for year if the beginning follows sol1"""
    return ([m for m in moons if m > sol1][0], [m for m in moons if m <= sol2][-1])


def __bounding_moons(moons, sol1, sol2, before_event):
    """Get the JDNs of the first and last new moons of a year depending on two solar events

    Paramters:
    moons: A tuple of JDNs extending before and after the expected bounds
    sol1: The solar event marking the beginning of the year
    sol2: The solar event marking the beginning of the next year
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
        return __bounding_before(moons, sol1, sol2)

    return __bounding_after(moons, sol1, sol2)


def _calendar_months(
    year,
    event=Seasons.SUMMER_SOLSTICE,
    rule=Visible.NEXT_DAY,
    before_event=False,
    data=load_data(),
):

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

    moons = [
        to_jdn(v)
        for v in visible_new_moons(year, rule, data=data)
        + visible_new_moons(year + 1, rule, data=data)
        + visible_new_moons(year + 2, rule, data=data)
    ]

    first, last = __bounding_moons(moons, sol1, sol2, before_event)

    return tuple([m for m in zip(moons, moons[1:]) if first <= m[0] <= last])


def __festival_months(
    year,
    event=Seasons.SUMMER_SOLSTICE,
    before_event=False,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple of dicts, each containing a month index, start JDN for the month and (non-inclusive) end JND

    Parameters:
    year (int) -- The year for the calendar
    event (Seasons) -- The soloar event that marks the beginning of the year (default Seasons.SUMMER_SOLSTICE)
    before_event: True if new moons should preceded the solar event, false if they should follow
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()
    """
    return tuple(
        [
            {"month_index": m[0], "start": m[1][0], "end": m[1][1]}
            for m in enumerate(
                _calendar_months(
                    year, event=event, before_event=before_event, rule=rule, data=data
                ),
                1,
            )
        ]
    )


def _doy_gen(n=1):
    """Recursivly return natural numbers starting with n."""
    yield n
    yield from _doy_gen(n + 1)


def __make_generic_month(month, doy):
    """Generate a tuple of days for a given month

    Params:
    months -- a dict (from festival_months()) with start and end JDNs
    doy -- a generator that returns the next integer (to keep track of days of the year

    This generates a tuple of FestivalDay objects, one for each day of a month bounded by the start JDN (inclusive) and end JDN (exclusive) passed as the month parameter. This is a generic list, with no specific Greek month assigned yet.
    """
    return tuple(
        [
            FestivalDay(
                month["start"] + d - 1,
                None,
                month["month_index"],
                None,
                month["end"] - month["start"],
                d,
                next(doy),
                None,
                None,
                None,
            )
            for d in range(1, month["end"] - month["start"] + 1, 1)
        ]
    )


def __base_festival_calendar(
    year,
    event=Seasons.SUMMER_SOLSTICE,
    before_event=False,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Generate a base calendar for a given year

    Params:
    year (int) -- The year for the calendar
    event (Seasons) -- The soloar event that marks the beginning of the year (default Seasons.SUMMER_SOLSTICE)
    before_event: True if new moons should preceded the solar event, false if they should follow
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Generate a base calendar, a tuple of FestivalDay objects.

    """

    doy = _doy_gen()

    months = __festival_months(
        year, event=event, before_event=before_event, rule=rule, data=data
    )

    return tuple([a for b in [__make_generic_month(m, doy) for m in months] for a in b])


def __intercalary_order(months, intercalate=6):
    """Insert an intercalary month in a list of months

    Params:
    months -- a list of month constants (e.g. AthenianMonths)
    intercalate --  the index at which to insert the intercalary month (Default: 6)
    """
    return months[:intercalate] + (Months.INT,) + months[intercalate:]


def __month_order(calendar, intercalate, intercalary):
    """Get a list of months (possibly intercalated) for a specific calendar

    Params:
    calendar --  A Cal constant
    intercalate (int) -- the month index at which to intercalate if needed
    intercalary (bool) -- True if intercalation is needed

    Returns the list of months constants for a requested calendar, with the intercalary month constant inserted where needed
    """
    if intercalary:
        return __intercalary_order(tuple(CALENDAR_MAP[calendar]), intercalate)

    return tuple(CALENDAR_MAP[calendar])


def __intercalated_names(month):
    """Return a tuple of intercalated versions of the given month"""
    return tuple(["".join(n) for n in zip(month, (" hústeros", "₂", " ὕστερος"))])


def __intercalated_month_name_map(calendar, months):
    """Add the required intercalary month to the month name map if needed"""
    if Months.INT in months:
        return {
            **MONTH_NAME_MAP,
            **{
                (calendar, Months.INT): __intercalated_names(
                    MONTH_NAME_MAP[(calendar, months[months.index(Months.INT) - 1])]
                )
            },
        }

    return MONTH_NAME_MAP


def __make_festival_day(
    cal_day,
    cal_year,
    name_as,
    year,
    year_len=None,
    calendar=None,
    months=None,
    month_length=None,
    month_names=None,
):
    """Add month name and constant to FestivalDay

    Params:
    cal_day: A FestivalDay object
    cal_year: year of calendar (as string, e.g. "BCE 411/410")
    name_as: A MonthNameOptions constant for the month name version
    calendar: A Cal constant for the requested calendar
    months: The list of appropriate month constants
    month_names: The month names lookup dictionary

    The passed in FestivalDay object does not yet contain a month from a specific calendar. If the months param is None, this is returned unchanged. Otherwise, the month constant and requested version (transliterated, abbreviated, Greek as specified by name_as) of the month name are added.

    """
    if months is None:
        return cal_day

    return FestivalDay(
        cal_day.jdn,
        month_names[(calendar, months[cal_day.month_index - 1])][name_as],
        cal_day.month_index,
        months[cal_day.month_index - 1],
        month_length,
        cal_day.day,
        cal_day.doy,
        cal_year,
        year_len,
        year,
    )


def festival_calendar(
    year,
    calendar=Cal.ATHENIAN,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    event=Seasons.SUMMER_SOLSTICE,
    before_event=False,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.

    Parameters:
    year (int) -- The year for the calendar
    calendar (Cal) -- A Cal constant for the requested calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    event (Season) -- The solar event with the year begins (default: Seasons.SUMMER_SOLSTICE)
    before_event (bool) -- True if the first month of year begins immediately before the solar_event, False (default) if it begins after
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    See calendar_months for documentation of visibility rules.

    Returns a tuple of FestivalDay objected with one member for each
    month. Each member is a tuple of the month name and tuple of start
    and end dates of the month. See calendar_month for details on the
    start and end times.

    If intercalation is necessary, the intercalated month will be
    calculated according the the intercalate parameter.

    If the calendar parameter is None, a generic calendar will be
    returned with the month and month_name members of each
    FestivalDay being None.

    """

    base_cal = __base_festival_calendar(
        year, event=event, before_event=before_event, rule=rule, data=data
    )

    cal_year = arkhon_year(year)

    if calendar is None:
        return tuple(
            [__make_festival_day(d, cal_year, name_as, year) for d in base_cal]
        )

    months = __month_order(calendar, intercalate, len(by_months(base_cal)) > 12)
    month_names = __intercalated_month_name_map(calendar, months)
    return tuple(
        [
            __make_festival_day(
                d,
                cal_year,
                name_as,
                year,
                base_cal[-1].doy,
                calendar,
                months,
                d.month_length,
                month_names,
            )
            for d in base_cal
        ]
    )


def athenian_festival_calendar(
    year,
    intercalate=AthenianMonths.POS,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.
    Parameters:
    year (int) -- The year for the calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Get an Athenian festival calendar (calls festival_calendar with appropriate options).

    """
    return festival_calendar(
        year,
        calendar=Cal.ATHENIAN,
        intercalate=intercalate,
        name_as=name_as,
        event=Seasons.SUMMER_SOLSTICE,
        before_event=False,
        rule=rule,
        data=data,
    )


def delphian_festival_calendar(
    year,
    intercalate=DelphianMonths.POI,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.
    Parameters:
    year (int) -- The year for the calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Get a Delphian festival calendar (calls festival_calendar with appropriate options).

    """
    return festival_calendar(
        year,
        calendar=Cal.DELPHIAN,
        intercalate=intercalate,
        name_as=name_as,
        event=Seasons.SUMMER_SOLSTICE,
        before_event=False,
        rule=rule,
        data=data,
    )


def delian_festival_calendar(
    year,
    intercalate=DelianMonths.PAN,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.
    Parameters:
    year (int) -- The year for the calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Get a Delian festival calendar (calls festival_calendar with appropriate options).

    """
    return festival_calendar(
        year,
        calendar=Cal.DELIAN,
        intercalate=intercalate,
        name_as=name_as,
        event=Seasons.WINTER_SOLSTICE,
        before_event=False,
        rule=rule,
        data=data,
    )


def argive_festival_calendar(
    year,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.
    Parameters:
    year (int) -- The year for the calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Get an Argive  festival calendar (calls festival_calendar with appropriate options).

    """
    return festival_calendar(
        year,
        calendar=Cal.ARGIVE,
        intercalate=intercalate,
        name_as=name_as,
        event=Seasons.AUTUMN_EQUINOX,
        before_event=True,
        rule=rule,
        data=data,
    )


def spartan_festival_calendar(
    year,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.
    Parameters:
    year (int) -- The year for the calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Get a Spartan festival calendar (calls festival_calendar with appropriate options).

    """
    return festival_calendar(
        year,
        calendar=Cal.SPARTAN,
        intercalate=intercalate,
        name_as=name_as,
        event=Seasons.AUTUMN_EQUINOX,
        before_event=True,
        rule=rule,
        data=data,
    )


def corinthian_festival_calendar(
    year,
    intercalate=CorinthianMonths.MAK,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return a tuple representing festival calendar.
    Parameters:
    year (int) -- The year for the calendar
    intercalate (int) -- Month index of month to intercalate if necessary (default: 6)
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    Get a Corinthian festival calendar (calls festival_calendar with appropriate options).

    """
    return festival_calendar(
        year,
        calendar=Cal.CORINTHIAN,
        intercalate=intercalate,
        name_as=name_as,
        event=Seasons.AUTUMN_EQUINOX,
        before_event=True,
        rule=rule,
        data=data,
    )


def jdn_to_festival_calendar(
    jdn,
    year=None,
    calendar=Cal.ATHENIAN,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    # If the year hint is not supplied, extract it from the jdn and recurse
    if not isinstance(year, int):
        return jdn_to_festival_calendar(
            jdn,
            jd.to_julian(jdn)[0],
            calendar=calendar,
            intercalate=intercalate,
            name_as=name_as,
            rule=rule,
            data=data,
        )

    for y in reversed(range(year - 1, year + 1)):
        candidate_cal = CAL_FUNCTION_MAP[calendar](y, intercalate, name_as, rule, data)
        if jdn in [d.jdn for d in candidate_cal]:
            return candidate_cal

    return ()


def jdn_to_festival_day(
    jdn,
    year=None,
    calendar=Cal.ATHENIAN,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Find the Athenian date corresponding to a Julian Day Number

    Parameters:
    jdn (int) -- The Julian Day Number
    year (int) -- Hint for year to find (can usually be +/- 1)
    calendar (Cal) -- A Cal constant for the requested calendar
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    intercalate (Months) -- Month constant for month to intercalate if
    necessary (default Months.POS)
     rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    """
    # If the year hint is not supplied, extract it from the jdn and recurse
    if not isinstance(year, int):
        return jdn_to_festival_day(
            jdn,
            jd.to_julian(jdn)[0],
            calendar=calendar,
            intercalate=intercalate,
            name_as=name_as,
            rule=rule,
            data=data,
        )

    return [
        d
        for d in jdn_to_festival_calendar(
            jdn, year, calendar, intercalate, name_as, rule, data
        )
        if d.jdn == jdn
    ][0]


def julian_to_festival(
    year,
    month,
    day,
    calendar=Cal.ATHENIAN,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Find the Athenian date corresponding to a Julian date

    Parameters:
    year (int) -- The Julian year, negative for BCE
    month (int) -- The Julian month
    day (int) -- The Julian day
    calendar (Cal) -- A Cal constant for the requested calendar
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    intercalate (Months) -- Month constant for month to intercalate if
    necessary (default Months.POS)
     rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    """

    # Convert the year/month/day to JDN and call find_jdn
    return jdn_to_festival_day(
        to_jdn(jd.from_julian(year, month, day)),
        year,
        calendar=calendar,
        intercalate=intercalate,
        name_as=name_as,
        rule=rule,
        data=data,
    )


def gregorian_to_festival(
    year,
    month,
    day,
    calendar=Cal.ATHENIAN,
    intercalate=6,
    name_as=MonthNameOptions.TRANSLITERATION,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Find the Athenian date corresponding to a Gregorian date

    Parameters:
    year (int) -- The Gregorian year, negative for BCE
    month (int) -- The Gregorian month
    day (int) -- The Gregorian day
    calendar (Cal) -- A Cal constant for the requested calendar
    name_as (MonthNameOption) -- Option corresponding to desired version of the month name (transliteration, abbreviation, Greek, default: MonthNameOptions.TRANSLITERATION)
    intercalate (Months) -- Month constant for month to intercalate if
    necessary (default Months.POS)
     rule (Visible) -- Constant from Visible indicating the desired rule
    (default Visible.SECOND_DAY)
    data -- Astronomical data for calculations. By default this is
    returned from load_data()

    """

    # Convert the year/month/day to JDN and call find_jdn
    return jdn_to_festival_day(
        to_jdn(jd.from_gregorian(year, month, day)),
        year,
        calendar=calendar,
        intercalate=intercalate,
        name_as=name_as,
        rule=rule,
        data=data,
    )


def _calendar_groups(c, func):
    """Group calendar by func."""
    return [tuple(g[1]) for g in groupby(c, key=func)]


def by_months(p):
    """Return festival calendar grouped into a tuple of tuples by months."""
    return tuple(_calendar_groups(p, lambda x: x.month_index))


def festival_to_jdn(
    year,
    month,
    day,
    calendar=Cal.ATHENIAN,
    intercalate=6,
    event=Seasons.SUMMER_SOLSTICE,
    before_event=False,
    rule=Visible.NEXT_DAY,
    data=load_data(),
):
    """Return the Julian Day Number for a festival date.

    Parameters:
    year (int) -- The year
    month (Months) -- Constant from Months indicating the desired month
    day (int) -- The day
    calendar (Cal) -- A Cal constant for the requested calendar
    intercalate (Months) -- Month constant for month to intercalate if
    necessary (default Months.POS)
    event (Season) -- The solar event with the year begins (default: Seasons.SUMMER_SOLSTICE)
    before_event (bool) -- True if the first month of year begins immediately before the solar_event, False (default) if it begins after
    rule (Visible) -- Constant from Visible indicating the desired rule
    data -- Astronomical data for calculations. By default this is
    returned from load_data()
    """
    try:

        return [
            d.jdn
            for d in festival_calendar(
                year,
                calendar=calendar,
                intercalate=intercalate,
                event=event,
                before_event=before_event,
                rule=rule,
                data=data,
            )
            if d.month == month and d.day == day
        ][0]
    except IndexError:
        raise HeniautosNoDayInYearError(
            f"There is no day matching month {month}, day {day} in the year {year}"
        )


def version():
    return __version__


CAL_FUNCTION_MAP = {
    Cal.ARGIVE: argive_festival_calendar,
    Cal.ATHENIAN: athenian_festival_calendar,
    Cal.CORINTHIAN: corinthian_festival_calendar,
    Cal.DELPHIAN: delphian_festival_calendar,
    Cal.DELIAN: delian_festival_calendar,
    Cal.SPARTAN: spartan_festival_calendar,
}
