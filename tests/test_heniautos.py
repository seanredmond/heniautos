from heniautos import *
import pytest
import skyfield

from skyfield.api import load
from skyfield.api import GREGORIAN_START


# TS = api.load.timescale()
# TS.julian_calendar_cutoff = GREGORIAN_START
# EPH = api.load('de422.bsp')

# Year to test prytany lengths
O_10 = 400      # 354 days, 10 prytanies
O_10_LONG = 399 # 355 days, 10 prytanies
I_10 = 401      # 384 days, 10 prytanies
O_12 = 291      # 354 days, 12 prytanies      
O_12_LONG = 293 # 355 days, 12 prytanies
I_12 = 300      # 384 days, 12 prytanies
O_13 = 209      # 354 days, 13 prytanies
O_13_LONG = 207 # 355 days, 13 prytanies
I_13 = 214      # 384 days, 13 prytanies

init_data()


def test_bce_as_negative():
    assert bce_as_negative(100) == -99


def test_is_bce():
    assert is_bce(summer_solstice(-99))
    assert not is_bce(summer_solstice(99))


def test_add_hours():
    sol = summer_solstice(-99)
    assert add_hours(sol, 1).ut1_calendar()[3] == sol.ut1_calendar()[3] + 1
    assert add_hours(sol, -1).ut1_calendar()[3] == sol.ut1_calendar()[3] - 1


def test_add_days():
    sol = summer_solstice(-99)
    assert add_days(sol, 1).ut1_calendar()[2] == sol.ut1_calendar()[2] + 1
    assert add_days(sol, -1).ut1_calendar()[2] == sol.ut1_calendar()[2] - 1


def test_as_gmt():
    assert as_gmt(summer_solstice(-99)) == "BCE 0100-Jun-25"
    assert as_gmt(summer_solstice(-99), True) == "BCE 0100-Jun-25 19:52:41 GMT"
    assert as_gmt(summer_solstice(100)) == " CE 0100-Jun-23"
    assert as_gmt(summer_solstice(100), True) == " CE 0100-Jun-23 22:19:47 GMT"


def test_as_eet():
    assert as_eet(summer_solstice(-99)) == "BCE 0100-Jun-25"
    assert as_eet(summer_solstice(-99), True) == "BCE 0100-Jun-25 21:52:41 EET"
    assert as_eet(summer_solstice(100)) == " CE 0100-Jun-24"
    assert as_eet(summer_solstice(100), True) == " CE 0100-Jun-24 00:19:47 EET"


def test_summer_solstice():
    assert as_gmt(summer_solstice(-99), True) == "BCE 0100-Jun-25 19:52:41 GMT"


def test_solar_event():
    assert as_gmt(solar_event(-99, Seasons.SPRING_EQUINOX), True) == \
        "BCE 0100-Mar-23 19:47:51 GMT"
    assert as_gmt(solar_event(-99, Seasons.SUMMER_SOLSTICE), True) == \
        "BCE 0100-Jun-25 19:52:41 GMT"
    assert as_gmt(solar_event(-99, Seasons.AUTUMN_EQUINOX), True) == \
        "BCE 0100-Sep-26 04:51:40 GMT"
    assert as_gmt(solar_event(-99, Seasons.WINTER_SOLSTICE), True) == \
        "BCE 0100-Dec-23 20:36:24 GMT"


def test_moon_phases():
    p = moon_phases(-99, Phases.NEW)
    assert type(p) is list
    assert as_gmt(p[0], True) == "BCE 0100-Jan-09 12:44:01 GMT"
    assert as_gmt(moon_phases(-99, Phases.FIRST_Q)[0], True) == \
        "BCE 0100-Jan-16 05:57:05 GMT"
    assert as_gmt(moon_phases(-99, Phases.FULL)[0], True) == \
        "BCE 0100-Jan-23 15:05:00 GMT"
    assert as_gmt(moon_phases(-99, Phases.LAST_Q)[0], True) == \
        "BCE 0100-Jan-01 22:41:55 GMT"


def test_new_moons():
    p = new_moons(-99)
    assert type(p) is list
    assert as_gmt(p[0], True) == "BCE 0100-Jan-09 12:44:01 GMT"
    

def test_calendar_months():
    p = calendar_months(-100)
    assert type(p) is tuple
    assert len(p) == 12
    assert type(p[0]) is tuple
    assert len(p[0]) == 2
    assert as_gmt(p[0][0], True) == "BCE 0101-Jul-17 11:59:17 GMT"
    assert p[0][1] == p[1][0]


def test_suffix():
    assert heniautos._suffix() == " hústeros"
    assert heniautos._suffix(abbrev=True) == "₂"
    assert heniautos._suffix(greek=True) == " ὕστερος"
    assert heniautos._suffix(abbrev=True, greek=True) == " ὕστερος"
    

def test_intercalate():
    assert heniautos._intercalate(12, Months.POS, False, False)[0] == \
        ("Hekatombaiṓn", Months.HEK)
    assert heniautos._intercalate(12, Months.POS, False, False)[3] == \
        ("Puanepsiṓn", Months.PUA)
    assert heniautos._intercalate(12, Months.POS, False, False)[6] == \
        ("Gamēliṓn", Months.GAM)

    assert heniautos._intercalate(13, Months.POS, False, False)[3] == \
        ("Puanepsiṓn", Months.PUA)
    assert heniautos._intercalate(13, Months.POS, False, False)[6] == \
        ("Poseidēiṓn hústeros", Months.INT)
    assert heniautos._intercalate(13, Months.POS, False, False)[7] == \
        ("Gamēliṓn", Months.GAM)

    assert heniautos._intercalate(13, Months.BOE, False, False)[3] == \
        ("Boēdromiṓn hústeros", Months.INT)
    assert heniautos._intercalate(13, Months.BOE, False, False)[6] == \
        ("Poseidēiṓn", Months.POS)
    assert heniautos._intercalate(13, Months.BOE, False, False)[7] == \
        ("Gamēliṓn", Months.GAM)
    

def test_festival_months():
    p = festival_months(-99)
    assert type(p) is tuple
    assert type(p[0]) is dict
    assert p[0]["month"] == "Hekatombaiṓn"
    assert p[0]["constant"] == Months.HEK
    assert as_gmt(p[0]["start"]) == "BCE 0100-Jul-06"
    assert p[0]["end"] == p[1]["start"]

    # With abbreviations
    q = festival_months(-99, abbrev=True)
    assert q[0]["month"] == "Hek"

    # With Greek names
    r = festival_months(-99, greek=True)
    assert r[0]["month"] == "Ἑκατομβαιών"

    # greek overrides abbrev
    assert festival_months(-99, abbrev=True, greek=True)[0]["month"] == "Ἑκατομβαιών"

    # with intercalations
    s = festival_months(-101)
    assert len(s) == 13
    # Default intercalation of Poseidēiṓn hústeros
    assert s[6]["month"] == "Poseidēiṓn hústeros"
    assert s[6]["constant"] == Months.INT

    t = festival_months(-101, intercalate=Months.BOE)
    assert t[3]["month"] == "Boēdromiṓn hústeros"
    assert t[6]["month"] == "Poseidēiṓn"
    
    # intercalation with abbreviation
    s1 = festival_months(-101, abbrev=True)
    assert s1[6]["month"] == "Pos₂"

    # With different visibility rules
    # SECOND_DAY is the default
    u = festival_months(-99, rule=Visible.SECOND_DAY)
    assert as_gmt(u[0]["start"]) == as_gmt(p[0]["start"])
    
    # with NEXT_DAY
    v = festival_months(-99, rule=Visible.NEXT_DAY)
    assert as_gmt(v[0]["start"]) == "BCE 0100-Jul-05"

    # with CONJUNCTION
    v = festival_months(-99, rule=Visible.CONJUNCTION)
    assert as_gmt(v[0]["start"]) == "BCE 0100-Jul-04"


def test_festival_calendar():
    p = festival_calendar(-100)
    assert type(p) is tuple
    assert type(p[0]) is dict
    assert p[0]["month"] == "Hekatombaiṓn"
    assert p[0]["constant"] == Months.HEK
    assert type(p[0]["days"]) is tuple
    assert type(p[0]["days"][0]) is dict
    assert p[0]["days"][0]["day"] == 1
    assert as_gmt(p[0]["days"][0]["date"]) == "BCE 0101-Jul-17"
    assert p[0]["days"][0]["doy"] == 1

    assert p[1]["month"] == "Metageitniṓn"
    assert p[1]["days"][0]["day"] == 1
    assert as_gmt(p[1]["days"][0]["date"]) == "BCE 0101-Aug-16"
    assert p[1]["days"][0]["doy"] == 31


def test_find_date():
    d = find_date(-100, Months.MET, 1)
    assert d["month"] == "Metageitniṓn"
    assert d["constant"] == Months.MET
    assert d["day"] == 1
    assert as_gmt(d["date"]) == "BCE 0101-Aug-16"
    assert d["doy"] == 31

    with pytest.raises(HeniautosError):
        find_date(-99, Months.MET, 31)


def test_pryt_len():
    d = heniautos._pryt_len(36)
    assert next(d) == 36
    assert next(d) == 36
    assert next(d) == 36
    assert next(d) == 36
    assert next(d) == 35
    assert next(d) == 35

    e = heniautos._pryt_len(39)
    assert next(e) == 39
    assert next(e) == 39
    assert next(e) == 39
    assert next(e) == 39
    assert next(e) == 38
    assert next(e) == 38

    e = heniautos._pryt_len(30, 6)
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 29

    e = heniautos._pryt_len(30, 6)
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 29

    e = heniautos._pryt_len(33, 0)
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32


def test_pryt_len_festival():
    cal = calendar_months(-100)
    e = [c for c in heniautos._pryt_len_festival(cal)]
    assert len(e) == 12
    assert e[0] == 30
    assert e[1] == 29
    assert e[-1] == 29


def test_prytanies_solar():
    p = prytanies(-420)
    assert len(p) == 10
    assert sum([span(q["start"], q["end"]) for q in p]) == 365
    assert span(p[0]["start"], p[0]["end"]) == 37
    assert span(p[4]["start"], p[4]["end"]) == 37
    assert span(p[6]["start"], p[6]["end"]) == 36
    assert span(p[-1]["start"], p[-1]["end"]) == 36


def test_prytanies_solar_leap():
    p = prytanies(-417)
    assert len(p) == 10
    assert sum([span(q["start"], q["end"]) for q in p]) == 366
    assert span(p[0]["start"], p[0]["end"]) == 37
    assert span(p[4]["start"], p[4]["end"]) == 37
    assert span(p[6]["start"], p[6]["end"]) == 36
    assert span(p[-1]["start"], p[-1]["end"]) == 37


@pytest.mark.xfail
def test_prytanies_10_ordinary_long():
    c2 = festival_months(O_10_LONG)
    p2 = prytanies(O_10_LONG)
    assert len(p2) == 10
    assert sum([span(q["start"], q["end"]) for q in p2]) == 355

    assert p2[0]["prytany"] == 1
    assert as_gmt(p2[0]["start"]) == as_gmt(c2[0]["start"])
    assert as_gmt(p2[-1]["end"]) == as_gmt(c2[-1]["end"])

    assert span(p2[0]["start"], p2[0]["end"]) == 36
    assert span(p2[4]["start"], p2[4]["end"]) == 35
    assert span(p2[-1]["start"], p2[-1]["end"]) == 36

def test_prytany_auto():
    with pytest.raises(HeniautosError):
        heniautos._pryt_auto(bce_as_negative(509))

    assert heniautos._pryt_auto(bce_as_negative(508)) == Prytany.QUASI_SOLAR
    assert heniautos._pryt_auto(bce_as_negative(410)) == Prytany.QUASI_SOLAR

    assert heniautos._pryt_auto(bce_as_negative(409)) == Prytany.ALIGNED_10
    assert heniautos._pryt_auto(bce_as_negative(308)) == Prytany.ALIGNED_10

    assert heniautos._pryt_auto(bce_as_negative(307)) == Prytany.ALIGNED_12
    assert heniautos._pryt_auto(bce_as_negative(224)) == Prytany.ALIGNED_12

    assert heniautos._pryt_auto(bce_as_negative(223)) == Prytany.ALIGNED_13
    assert heniautos._pryt_auto(bce_as_negative(201)) == Prytany.ALIGNED_13

    assert heniautos._pryt_auto(bce_as_negative(200)) == Prytany.ALIGNED_12
    assert heniautos._pryt_auto(bce_as_negative(101)) == Prytany.ALIGNED_12

    assert heniautos._pryt_auto(bce_as_negative(100)) == Prytany.ALIGNED_10
    assert heniautos._pryt_auto(2021) == Prytany.ALIGNED_10


def test_pryt_auto_start():
    # Should return Julian dates from rounded Terrestrial Time
    
    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(500),
            Prytany.AUTO), True) == "BCE 0500-Jul-04 13:59:17 EET"
    
    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(425),
            Prytany.AUTO), True) == "BCE 0425-Jul-04 13:59:17 EET"

    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(429),
            Prytany.AUTO), True) == "BCE 0429-Jul-04 13:59:17 EET"
    
    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(424),
            Prytany.AUTO), True) == "BCE 0424-Jul-07 13:59:17 EET"

    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(421),
            Prytany.AUTO), True) == "BCE 0421-Jul-07 13:59:17 EET"
    
    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(420),
            Prytany.AUTO), True) == "BCE 0420-Jul-08 13:59:17 EET"
    
    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(419),
            Prytany.AUTO), True) == "BCE 0419-Jul-09 13:59:17 EET"

    # Provide your own start day
    assert as_eet(
        heniautos._pryt_auto_start(
            bce_as_negative(419), 1), True) == "BCE 0419-Jul-01 13:59:17 EET"


def test_pryt_solar_end():
    # One quasi-solar year should end at the next quasi solar year
    year_start = heniautos._pryt_auto_start(bce_as_negative(426),
                                            Prytany.AUTO)
    year_end = heniautos._pryt_solar_end(year_start)
    next_year = heniautos._pryt_auto_start(bce_as_negative(425),
                                           Prytany.AUTO)
    assert year_end == next_year
    

def test_prytany_calendar_solar():
    year = bce_as_negative(421)
    p = prytany_calendar(year)

    assert len(p) == 10
    assert p[0]["prytany"] == 1
    assert as_eet(p[0]["days"][0]["date"]) == "BCE 0421-Jul-07"
    assert len(p[0]["days"]) == 37

    assert p[-1]["prytany"] == 10
    assert as_eet(p[-1]["days"][-1]["date"]) == "BCE 0420-Jul-06"
    assert len(p[-1]["days"]) == 36
    assert p[-1]["days"][-1]["doy"] == 365

    p2 = prytany_calendar(bce_as_negative(429))
    assert as_eet(p2[0]["days"][0]["date"]) == "BCE 0429-Jul-04"

def test_prytany_calendar_solar_leap():
    p = prytany_calendar(-417)

    assert len(p) == 10
    assert p[0]["prytany"] == 1
    assert as_eet(p[0]["days"][0]["date"]) == "BCE 0418-Jul-09"
    assert len(p[0]["days"]) == 37

    assert p[-1]["prytany"] == 10
    assert as_eet(p[-1]["days"][-1]["date"]) == "BCE 0417-Jul-08"
    assert len(p[-1]["days"]) == 37
    assert p[-1]["days"][-1]["doy"] == 366


# Ten prytanies: 409-308 BCE

def test_prytanies_10_ordinary():
    year = bce_as_negative(O_10)
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 10 prytanies in 354 days
    assert len(p3) == 10
    assert sum([span(q["start"], q["end"]) for q in c3]) == 354
    assert sum([span(q["start"], q["end"]) for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # 354 day year. I-IV should be 36 days, the rest 35
    assert span(p3[0]["start"], p3[0]["end"]) == 36
    assert span(p3[4]["start"], p3[4]["end"]) == 35
    assert span(p3[-1]["start"], p3[-1]["end"]) == 35


def test_prytanies_10_ordinary_long():
    year = bce_as_negative(O_10_LONG)    
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 10 prytanies in 355 days
    assert len(p3) == 10
    assert sum([span(q["start"], q["end"]) for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # 355 day year. I-IV should be 36 days, the rest 35
    # except the last has the 355th day added, so it is 36 days
    assert span(p3[0]["start"], p3[0]["end"]) == 36
    assert span(p3[4]["start"], p3[4]["end"]) == 35
    assert span(p3[-1]["start"], p3[-1]["end"]) == 36


def test_prytanies_10_intercalated():
    year = bce_as_negative(I_10)
    c = festival_months(year)
    p = prytanies(year)

    # 10 prytanies in 384 days
    assert len(p) == 10
    assert sum([span(q["start"], q["end"]) for q in p]) == 384

    assert p[0]["prytany"] == 1
    assert as_gmt(p[0]["start"]) == as_gmt(c[0]["start"])
    assert as_gmt(p[-1]["end"]) == as_gmt(c[-1]["end"])

    # 384 day year. I-IV should by 39 days, the rest 38
    assert span(p[0]["start"], p[0]["end"]) == 39
    assert span(p[4]["start"], p[4]["end"]) == 38
    assert span(p[-1]["start"], p[-1]["end"]) == 38


# Twelve prytanies: 307-224 BCE & 200-101 BCE

def test_prytanies_12_ordinary():
    year = bce_as_negative(O_12)
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 12 prytanies in 354 days
    assert len(p3) == 12
    assert sum([span(q["start"], q["end"]) for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # Like the festival calendar, prytanies are 29 or 30 days
    assert span(p3[0]["start"], p3[0]["end"]) == 29
    assert span(p3[1]["start"], p3[1]["end"]) == 29
    assert span(p3[2]["start"], p3[2]["end"]) == 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 30
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29


def test_prytanies_12_ordinary_aristotle():
    year = bce_as_negative(O_12)
    c3 = festival_months(year)
    p3 = prytanies(year, rule_of_aristotle=True)

    # 12 prytanies in 354 days
    assert len(p3) == 12
    assert sum([span(q["start"], q["end"]) for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # All the 30 day prytanies are at the beginning of the year,
    # all the 29-day prytanies are at the end
    # The festival months of 291 are:
    #
    #     H H F H F H F F H F F H
    #
    # But the prytanies should be 6 30-day and 6 29-day
    #
    #     F F F F F F H H H H H H
    #
    assert span(p3[0]["start"], p3[0]["end"]) == 30   # not 29
    assert span(p3[2]["start"], p3[2]["end"]) == 30   # not 29
    assert span(p3[-3]["start"], p3[-3]["end"]) == 29 # not 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29 # not 30
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29 # this one the same


def test_prytanies_12_long():
    year = bce_as_negative(O_12_LONG)
    c3 = festival_months(year) 
    p3 = prytanies(year)

    # 12 prtyanies in 355 days
    assert len(p3) == 12
    assert sum([span(q["start"], q["end"]) for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # Like the festival calendar, prytanies are 29 or 30 days
    # Festival months:
    #
    #    H F H F F F H F F H H F
    #
    assert span(p3[0]["start"], p3[0]["end"]) == 29
    assert span(p3[1]["start"], p3[1]["end"]) == 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29
    assert span(p3[-1]["start"], p3[-1]["end"]) == 30


def test_prytanies_12_long_aristotle():
    year = bce_as_negative(O_12_LONG)
    c3 = festival_months(year)
    p3 = prytanies(year, rule_of_aristotle=True)
    assert len(p3) == 12
    assert sum([span(q["start"], q["end"]) for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # All the 30 day prytanies are at the beginning of the year,
    # all the 29-day prytanies are at the end
    # The festival months of 293 are:
    #
    #     H F H F F F H F F H H F
    #
    # But the prytanies should be 6 30-day and 6 29-day
    # except the last prytany is 30 because it has the
    # additional 355th day
    #
    #     F F F F F F H H H H H F
    #
    assert span(p3[0]["start"], p3[0]["end"]) == 30   # not 29
    assert span(p3[1]["start"], p3[1]["end"]) == 30
    assert span(p3[-4]["start"], p3[-4]["end"]) == 29 # not 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29 
    assert span(p3[-1]["start"], p3[-1]["end"]) == 30 # not 29


def test_prytanies_12_intercalated():
    year = bce_as_negative(I_12)    
    c3 = festival_months(year)
    p3 = prytanies(year)

    # Twelve prytanies in 385 days
    assert len(p3) == 12
    assert sum([span(q["start"], q["end"]) for q in p3]) == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # Are prytanies are 32 days long
    assert span(p3[0]["start"], p3[0]["end"]) == 32
    assert span(p3[6]["start"], p3[6]["end"]) == 32
    assert span(p3[-1]["start"], p3[-1]["end"]) == 32


# Thirteen prytanies: 223-201 BCE
    
def test_prytanies_13_ordinary():
    year = bce_as_negative(O_13)
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 13 prytanies in 354 days
    assert len(p3) == 13
    assert sum([span(q["start"], q["end"]) for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # Prytanies I-III 29 days long, the rest 27 days
    assert span(p3[0]["start"], p3[0]["end"]) == 28
    assert span(p3[3]["start"], p3[3]["end"]) == 27
    assert span(p3[-1]["start"], p3[-1]["end"]) == 27


def test_prytanies_13_long():
    year = bce_as_negative(O_13_LONG)
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 13 prytanies in 355 days
    assert len(p3) == 13
    assert sum([span(q["start"], q["end"]) for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # Prytanies I-III 28 days long, the rest 27 days except for the last
    # prytany which as 29 days long since it has the extra 355th day added
    assert span(p3[0]["start"], p3[0]["end"]) == 28
    assert span(p3[3]["start"], p3[3]["end"]) == 27
    assert span(p3[-1]["start"], p3[-1]["end"]) == 28

    
def test_prytanies_13_intercalated():
    year = bce_as_negative(I_13)
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 13 prytanies in 384 days
    assert len(p3) == 13
    assert sum([span(q["start"], q["end"]) for q in p3]) == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # Prytanies follow the festival calendar
    # The festival months of 214 are:
    #
    #     F H F H F F F H F H F H H
    #
    assert span(p3[0]["start"], p3[0]["end"]) == 30
    assert span(p3[1]["start"], p3[1]["end"]) == 29
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29


def test_prytanies_13_intercalated_aristotle():
    year = bce_as_negative(214)
    c3 = festival_months(year)
    p3 = prytanies(year, rule_of_aristotle=True)

    # 13 prytanies in 384 days
    assert len(p3) == 13
    assert sum([span(q["start"], q["end"]) for q in p3]) == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # All the 30 day prytanies are at the beginning of the year,
    # all the 29-day prytanies are at the end
    # The festival months of 293 are:
    #
    #     F H F H F F F H F H F H H
    #
    # But the prytanies should be 7 30-day and 6 29-day
    #
    #     F F F F F F F H H H H H H
    #
    assert span(p3[0]["start"], p3[0]["end"]) == 30
    assert span(p3[1]["start"], p3[1]["end"]) == 30   # not 29
    assert span(p3[-3]["start"], p3[-3]["end"]) == 29 # not 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29


def test_prytany_calendar_10_ordinary():
    year = bce_as_negative(O_10)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)

    assert len(p3) == 10
    assert c3[-1]['days'][-1]['doy'] == 354
    assert p3[-1]['days'][-1]['doy'] == 354
        
    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 36
    assert len(p3[4]["days"]) == 35
    assert len(p3[-1]["days"]) == 35


def test_prytany_calendar_10_ordinary_long():
    year = bce_as_negative(O_10_LONG)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 10
    assert p3[-1]['days'][-1]['doy'] == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 36
    assert len(p3[4]["days"]) == 35
    assert len(p3[-1]["days"]) == 36
    

def test_prytany_calendar_10_intercalated():
    year = bce_as_negative(I_10)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 10
    assert p3[-1]['days'][-1]['doy'] == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 39
    assert len(p3[4]["days"]) == 38
    assert len(p3[-1]["days"]) == 38

def test_prytany_calendar_12_ordinary():
    year = bce_as_negative(O_12)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 12
    assert p3[-1]['days'][-1]['doy'] == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])


    assert len(p3[0]["days"]) == 29
    assert len(p3[1]["days"]) == 29
    assert len(p3[2]["days"]) == 30
    assert len(p3[-2]["days"]) == 30
    assert len(p3[-1]["days"]) == 29


def test_prytany_calendar_12_ordinary_aristotle():
    year = bce_as_negative(O_12)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year, rule_of_aristotle=True)
    assert len(p3) == 12
    assert p3[-1]['days'][-1]['doy'] == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])


    assert len(p3[0]["days"]) == 30
    assert len(p3[1]["days"]) == 30
    assert len(p3[2]["days"]) == 30
    assert len(p3[-2]["days"]) == 29
    assert len(p3[-1]["days"]) == 29


def test_prytany_calendar_12_long():
    year = bce_as_negative(O_12_LONG)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 12
    assert p3[-1]['days'][-1]['doy'] == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    # Like the festival calendar, prytanies are 29 or 30 days
    # Festival months:
    #
    #    H F H F F F H F F H H F
    #
    assert len(p3[0]["days"]) == 29
    assert len(p3[1]["days"]) == 30
    assert len(p3[-2]["days"]) == 29
    assert len(p3[-1]["days"]) == 30


def test_prytany_calendar_12_long_aristotle():
    year = bce_as_negative(O_12_LONG)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year, rule_of_aristotle=True)
    assert len(p3) == 12
    assert p3[-1]['days'][-1]['doy'] == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 30
    assert len(p3[1]["days"]) == 30
    assert len(p3[-2]["days"]) == 29
    assert len(p3[-1]["days"]) == 30


def test_prytany_calendar_12_intercalated():
    year = bce_as_negative(I_12)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 12
    assert p3[-1]['days'][-1]['doy'] == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 32
    assert len(p3[6]["days"]) == 32
    assert len(p3[-1]["days"]) == 32


def test_prytany_calendar_13_ordinary():
    year = bce_as_negative(O_13)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 13
    assert p3[-1]['days'][-1]['doy'] == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 28
    assert len(p3[3]["days"]) == 27
    assert len(p3[-1]["days"]) == 27


def test_prytany_calendar_13_long():
    year = bce_as_negative(O_13_LONG)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 13
    assert p3[-1]['days'][-1]['doy'] == 355

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    assert len(p3[0]["days"]) == 28
    assert len(p3[3]["days"]) == 27
    assert len(p3[-1]["days"]) == 28


def test_prytany_calendar_13_intercalated():
    year = bce_as_negative(I_13)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year)
    assert len(p3) == 13
    assert p3[-1]['days'][-1]['doy'] == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])

    # Prytanies follow the festival calendar
    # The festival months of 214 are:
    #
    #     F H F H F F F H F H F H H
    #
    assert len(p3[0]["days"]) == 30
    assert len(p3[1]["days"]) == 29
    assert len(p3[-3]["days"]) == 30
    assert len(p3[-2]["days"]) == 29
    assert len(p3[-1]["days"]) == 29


def test_prytany_calendar_13_intercalated_aristotle():
    year = bce_as_negative(I_13)
    c3 = festival_calendar(year)
    p3 = prytany_calendar(year, rule_of_aristotle=True)
    assert len(p3) == 13
    assert p3[-1]['days'][-1]['doy'] == 384

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["days"][0]["date"]) == as_gmt(p3[0]["days"][0]["date"])
    assert as_gmt(p3[-1]["days"][-1]["date"]) == \
        as_gmt(c3[-1]["days"][-1]["date"])


    assert len(p3[0]["days"]) == 30
    assert len(p3[1]["days"]) == 30
    assert len(p3[-2]["days"]) == 29
    assert len(p3[-1]["days"]) == 29


def test_months_sum():
    s = ((30, 0), (29, 8))
    assert heniautos._months_sum(s) == 232


def test_cal_lengths_ordinary_12th():
    c = heniautos._cal_lengths(12, 12, 19, ((False, (30, 29)),), 0, 12, 5, 5)

    assert min([d["lengths"][0][1] for d in c]) == 4
    assert min([d["lengths"][1][1] for d in c]) == 4


def test_cal_lengths_ordinary_6th():
    c = heniautos._cal_lengths(6, 6, 19, ((False, (30, 29)),), 0, 12, 5, 5)

    assert min([d["lengths"][0][1] for d in c]) == 0
    assert min([d["lengths"][1][1] for d in c]) == 0


def test_cal_lengths_ordinary_9th():
    c = heniautos._cal_lengths(9, 9, 19, ((False, (30, 29)),), 0, 12, 5, 5)

    assert min([d["lengths"][0][1] for d in c]) == 1
    assert min([d["lengths"][1][1] for d in c]) == 1


def test_cal_lengths_intercalary_12th():
    c = heniautos._cal_lengths(12, 12, 19, ((False, (30, 29)),), 0, 13, 6, 5)
    print(c)

    assert min([d["lengths"][0][1] for d in c]) == 4
    assert min([d["lengths"][1][1] for d in c]) == 3



@pytest.mark.skip(reason="reevaluating max_diff")
def test_cal_lengths_default_max():
    c = heniautos._cal_lengths(9, 9, 28, ((False, (30, 29)),), 3)
    assert len(c) == 3
    assert [d["doy"] for d in c] == [263, 264, 265]


@pytest.mark.skip(reason="reevaluating max_diff")
def test_cal_lengths_choose_max():
    c = heniautos._cal_lengths(9, 9, 28, ((False, (30, 29)),), 5)
    assert len(c) == 5
    assert [d["doy"] for d in c] == [262, 263, 264, 265, 266]


@pytest.mark.skip(reason="reevaluating max_diff")
def test_cal_lengths_no_max():
    c = heniautos._cal_lengths(9, 9, 28, ((False, (30, 29)),), 0)
    assert len(c) == 9
    assert [d["doy"] for d in c] == [260, 261, 262, 263, 264, 265, 266,
                                     267, 268]


def test_prytany_doy_aligned_12():
    doy = prytany_doy(9, 28, pryt_type=Prytany.ALIGNED_12)
    print(doy)
    assert isinstance(doy, tuple)
    assert len(doy) == 8
    assert doy[0]["doy"] == 261
    assert doy[0]["intercalated"] == False
    assert doy[-1]["doy"] == 284
    assert doy[-1]["intercalated"] == True


def test_festival_doy():
    doy = festival_doy(Months.MAI, 27)
    assert isinstance(doy, tuple)
    assert len(doy) == 11
    assert doy[0]["doy"] == 143
    assert doy[0]["intercalated"] == False
    assert doy[-1]["doy"] == 177
    assert doy[-1]["intercalated"] == True


def test_festival_doy_no_max():
    doy = festival_doy(Months.MAI, 27, max_diff=0)
    assert isinstance(doy, tuple)
    assert len(doy) == 11
    assert doy[0]["doy"] == 143
    assert doy[0]["intercalated"] == False
    assert doy[-1]["doy"] == 177
    assert doy[-1]["intercalated"] == True


def test_fest_eq_tuple():
    eq = heniautos._fest_eq((Months.MET, 10))
    assert len(eq) == 5
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalated"] == False
    assert eq[-1]["doy"] == 70
    assert eq[-1]["intercalated"] == True

    assert heniautos._fest_eq((Months.MET, 10)) == \
        heniautos._fest_eq(((Months.MET, 10),))


def test_fest_eq_nested():
    eq = heniautos._fest_eq(((Months.MET, 10), (Months.MET, 11)))
    assert len(eq) == 10
    assert eq[0]["date"] == (Months.MET, 10)
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalated"] == False
    assert eq[4]["date"] == (Months.MET, 10)
    assert eq[4]["doy"] == 70
    assert eq[4]["intercalated"] == True
    assert eq[5]["date"] == (Months.MET, 11)
    assert eq[5]["doy"] == 40
    assert eq[5]["intercalated"] == False
    assert eq[-1]["date"] == (Months.MET, 11)
    assert eq[-1]["doy"] == 71
    assert eq[-1]["intercalated"] == True


def test_pryt_eq_tuple():
    eq = heniautos._pryt_eq((Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10)
    assert len(eq) == 4
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalated"] == False
    assert eq[-1]["doy"] == 43
    assert eq[-1]["intercalated"] == True

    assert heniautos._pryt_eq(
        (Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10) == \
        heniautos._pryt_eq(((Prytanies.II, 4),), pryt_type=Prytany.ALIGNED_10)



def test_pryt_eq_nested():
    eq = heniautos._pryt_eq(((Prytanies.II, 4), (Prytanies.II, 5)),
                            pryt_type=Prytany.ALIGNED_10)
    assert len(eq) == 8
    assert eq[0]["date"] == (Prytanies.II, 4)
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalated"] == False
    assert eq[3]["date"] == (Prytanies.II, 4)
    assert eq[3]["doy"] == 43
    assert eq[3]["intercalated"] == True
    assert eq[-1]["date"] == (Prytanies.II, 5)
    assert eq[-1]["doy"] == 44
    assert eq[-1]["intercalated"] == True


def test_equations_tuples():
    eq = equations((Months.MET, 10), (Prytanies.II, 4),
                   pryt_type=Prytany.ALIGNED_10)
    print(eq)
    assert len(eq) == 2
    assert eq[0]["doy"] == 39
    assert len(eq[0]["equations"]) == 2


def test_equations_nested():
    eq = equations(((Months.HEK, 30), (Months.MET, 1)),
                   ((Prytanies.I, 30), (Prytanies.I, 31)),
                   pryt_type=Prytany.ALIGNED_10)

    assert len(eq) == 2
    assert eq[0]["doy"] == 30
    assert len(eq[0]["equations"]["festival"]) == 2
    assert eq[0]["equations"]["festival"][0]["date"] == (Months.HEK, 30)
    assert eq[0]["equations"]["festival"][1]["date"] == (Months.MET, 1)
    assert len(eq[0]["equations"]["conciliar"]) == 2
    assert eq[0]["equations"]["conciliar"][0]["date"] == (Prytanies.I, 30)
    assert eq[0]["equations"]["conciliar"][0]["intercalated"] == False
    assert eq[0]["equations"]["conciliar"][1]["date"] == (Prytanies.I, 30)
    assert eq[0]["equations"]["conciliar"][1]["intercalated"] == True

    
@pytest.mark.skip(reason="reevaluating if this needs a test")
def test_0_prytanies():
    eq = equations((Months.MET, 9), (Prytanies.I, 39),
                   pryt_type=Prytany.ALIGNED_10)

    assert len(eq) == 1
    assert len(eq[0]["equations"]["conciliar"]) == 1
    

def test_dinsmoor():
    c = festival_calendar(-430, rule=Visible.DINSMOOR)
    assert c[5]["month"] == "Poseidēiṓn"
    assert (as_eet(c[5]["days"][0]["date"])) == "BCE 0431-Nov-29"
    assert c[5]["days"][0]["doy"] == 148
    assert c[5]["days"][-1]["doy"] == 177

    d = festival_calendar(-430, rule=Visible.DINSMOOR)
    assert d[6]["month"] == "Poseidēiṓn hústeros"
    assert (as_eet(d[6]["days"][0]["date"])) == "BCE 0431-Dec-29"
    assert d[6]["days"][0]["doy"] == 178
    assert d[6]["days"][-1]["doy"] == 206

    e = festival_calendar(-310, rule=Visible.DINSMOOR)
    assert e[0]["month"] == "Uncertain"
    assert (as_eet(e[0]["days"][0]["date"])) == "BCE 0311-Jun-29"

    
def test_dinsmoor_months():
    assert dinsmoor_months(-430)[5]["month"] == "Poseidēiṓn"
    assert as_eet(dinsmoor_months(-430)[5]["start"]) == "BCE 0431-Nov-29"
    assert as_eet(dinsmoor_months(-430)[5]["end"]) == "BCE 0431-Dec-29"
    assert dinsmoor_months(-430)[6]["month"] == "Poseidēiṓn hústeros"
    assert dinsmoor_months(-430, abbrev=True)[6]["month"] == \
        "Pos₂"
    assert dinsmoor_months(-430, greek=True)[6]["month"] == \
        "Ποσιδηϊών ὕστερος"


    assert dinsmoor_months(-310)[0]["month"] == "Uncertain"
    assert dinsmoor_months(-310, abbrev=True)[0]["month"] == "Unc"
    assert dinsmoor_months(-310, greek=True)[0]["month"] == "Uncertain"


def test_320():
    # Bug: For the year 320 (2-day rule), the boundaries betweem many
    # months had problems.
    #
    # Some days were doubled:
    #
    #     Aug  7: Hek 30 AND Met 1
    #     Oct  5: Boe 30 AND Pua 1
    #     Jan  2: Pos 30 AND Gam 1
    #     Apr  1: Ela 30 AND Mou 1
    #     May 30: Tha 30 AND Ski 1
    #
    # while others were skipped:
    #
    #     Met 29 = Sep 4,  Boe 1 = Sep 6 (No Sep 5)
    #     Pua 29 = Nov 2,  Mai 2 = Nov 4 (No Nov 3)
    #     Mou 29 = Apr 29, Tha 1 = May 1 (No Apr 30)
    #
    # This was due to bad "rounding" of days. Fixed by rounding (using
    # round()) Julian days rather than using just the integer part
    # (with int())

    cal_320 = festival_calendar(bce_as_negative(320))

    # With the two day rule, 320 is ordinary
    assert cal_320[-1]["days"][-1]["doy"] == 354

    # It starts on Jul 9
    assert as_eet(cal_320[0]["days"][0]["date"]) == "BCE 0320-Jul-09"
    # and ends on Jun 27
    assert as_eet(cal_320[-1]["days"][-1]["date"]) == "BCE 0319-Jun-27"

    # Last day of Hek 
    assert as_eet(cal_320[0]["days"][-1]["date"]) == "BCE 0320-Aug-06"
    # First day of Met
    assert as_eet(cal_320[1]["days"][0]["date"]) == "BCE 0320-Aug-07"

    # Last day of Met
    assert as_eet(cal_320[1]["days"][-1]["date"]) == "BCE 0320-Sep-04"
    # First day of Boe
    assert as_eet(cal_320[2]["days"][0]["date"]) == "BCE 0320-Sep-05"

    # Last day of Boe
    assert as_eet(cal_320[2]["days"][-1]["date"]) == "BCE 0320-Oct-04"
    # First day of Pua
    assert as_eet(cal_320[3]["days"][0]["date"]) == "BCE 0320-Oct-05"
    
    # Last day of Pua
    assert as_eet(cal_320[3]["days"][-1]["date"]) == "BCE 0320-Nov-03"
    # First day of Mai
    assert as_eet(cal_320[4]["days"][0]["date"]) == "BCE 0320-Nov-04"

    # Last day of Pos
    assert as_eet(cal_320[5]["days"][-1]["date"]) == "BCE 0319-Jan-01"
    # First day of Gam
    assert as_eet(cal_320[6]["days"][0]["date"]) == "BCE 0319-Jan-02"

    # Last day of Ela
    assert as_eet(cal_320[8]["days"][-1]["date"]) == "BCE 0319-Mar-31"
    # First day of Mou
    assert as_eet(cal_320[9]["days"][0]["date"]) == "BCE 0319-Apr-01"

    # Last day of Mou
    assert as_eet(cal_320[9]["days"][-1]["date"]) == "BCE 0319-Apr-30"
    # First day of Tha
    assert as_eet(cal_320[10]["days"][0]["date"]) == "BCE 0319-May-01"
    
    # Last day of Tha
    assert as_eet(cal_320[10]["days"][-1]["date"]) == "BCE 0319-May-29"
    # First day of Ski
    assert as_eet(cal_320[11]["days"][0]["date"]) == "BCE 0319-May-30"

    # With the 1-day rule it is intercalary
    assert festival_calendar(
        bce_as_negative(320),
        rule=Visible.NEXT_DAY)[-1]["days"][-1]["doy"] == 384

    # Likewise with the 0-day rule it is intercalary
    assert festival_calendar(
        bce_as_negative(320),
        rule=Visible.CONJUNCTION)[-1]["days"][-1]["doy"] == 384
    


