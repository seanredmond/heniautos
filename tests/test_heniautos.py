from heniautos import *
import pytest

# import skyfield

# from skyfield.api import load
# from skyfield.api import GREGORIAN_START


# TS = api.load.timescale()
# TS.julian_calendar_cutoff = GREGORIAN_START
# EPH = api.load('de422.bsp')

# Year to test prytany lengths
O_SO = 424  # 354 days, quasi-solar prytanies
O_SO_LONG = 426  # 355 days, quasi-solar prytanies
I_SO = 425  # 384 days, quasi-solar prytanies
O_10 = 400  # 354 days, 10 prytanies
O_10_LONG = 399  # 355 days, 10 prytanies
I_10 = 401  # 384 days, 10 prytanies
O_12 = 291  # 354 days, 12 prytanies
O_12_LONG = 293  # 355 days, 12 prytanies
I_12 = 301  # 384 days, 12 prytanies
O_13 = 209  # 354 days, 13 prytanies
O_13_LONG = 207  # 355 days, 13 prytanies
I_13 = 214  # 384 days, 13 prytanies

# init_data()


def span(a, b):
    return b - a


def test_version():
    assert version() == "1.3.0"


def test_bce_as_negative():
    assert bce_as_negative(100) == -99


def test_negative_as_bce():
    assert negative_as_bce(-99) == 100


def test_is_bce():
    assert is_bce(1685074.3287422964)  # Summer Solstice 100 BCE


# def test_add_hours():
#     sol = summer_solstice(-99)
#     print(sol)
#     print(add_hours(sol, 1))
#     print(add_hours(sol, 1) - sol)
#     assert jd.to_julian(add_hours(sol, 1))[3] == jd.to_julian(sol)[3] + 1


# def test_add_days():
#     sol = summer_solstice(-99)
#     assert jd.to_julian(add_days(sol, 1))[2] == jd.to_julian(sol)[2] + 1
#     assert jd.to_julian(add_days(sol, -1))[2] == jd.to_julian(sol)[2] - 1


def test_as_gmt():
    assert as_gmt(1685074.3287423) == "BCE 0100-Jun-25"
    assert as_gmt(1685074.3287423, True) == "BCE 0100-Jun-25 19:53:23 GMT"
    assert as_gmt(1685439.56480925) == "BCE 0099-Jun-25"
    assert as_gmt(1685074.3287422964, True) == "BCE 0100-Jun-25 19:53:23 GMT"


def test_as_eet():
    assert as_eet(1685074.3287422964) == "BCE 0100-Jun-25"
    assert as_eet(1685074.3287422964, True) == "BCE 0100-Jun-25 21:53:23 EET"


# def test_summer_solstice():
#     assert as_gmt(summer_solstice(-99), True) == "BCE 0100-Jun-25 19:53:23 GMT"


def test_solar_event():
    assert (
        as_gmt(solar_event(-99, Seasons.SPRING_EQUINOX), True)
        == "BCE 0100-Mar-23 19:48:34 GMT"
    )
    assert (
        as_gmt(solar_event(-99, Seasons.SUMMER_SOLSTICE), True)
        == "BCE 0100-Jun-25 19:53:23 GMT"
    )
    assert (
        as_gmt(solar_event(-99, Seasons.AUTUMN_EQUINOX), True)
        == "BCE 0100-Sep-26 04:52:22 GMT"
    )
    assert (
        as_gmt(solar_event(-99, Seasons.WINTER_SOLSTICE), True)
        == "BCE 0100-Dec-23 20:37:06 GMT"
    )


def test_moon_phases():
    p = moon_phases(-99)
    assert type(p) is list
    assert as_gmt(p[0], True) == "BCE 0100-Jan-09 12:44:44 GMT"

    with pytest.raises(HeniautosNoDataError):
        assert (
            as_gmt(moon_phases(-99, Phases.FIRST_Q)[0], True)
            == "BCE 0100-Jan-16 05:57:05 GMT"
        )

    with pytest.raises(HeniautosNoDataError):
        assert (
            as_gmt(moon_phases(-99, Phases.FULL)[0], True)
            == "BCE 0100-Jan-23 15:05:00 GMT"
        )

    with pytest.raises(HeniautosNoDataError):
        assert (
            as_gmt(moon_phases(-99, Phases.LAST_Q)[0], True)
            == "BCE 0100-Jan-01 22:41:55 GMT"
        )


def test_new_moons():
    p = new_moons(-99)
    assert type(p) is list
    assert as_gmt(p[0], True) == "BCE 0100-Jan-09 12:44:44 GMT"


def test_calendar_months_after():
    p = calendar_months(-100)
    assert type(p) is tuple
    assert len(p) == 12
    assert type(p[0]) is tuple
    assert len(p[0]) == 2
    assert as_gmt(p[0][0], True) == "BCE 0101-Jul-16 12:00:00 GMT"
    assert p[0][1] == p[1][0]


def test_calendar_months_before():
    p = calendar_months(-100, before_event=True)
    assert type(p) is tuple
    assert len(p) == 12
    assert type(p[0]) is tuple
    assert len(p[0]) == 2
    assert as_gmt(p[0][0], True) == "BCE 0101-Jun-16 12:00:00 GMT"
    assert p[0][1] == p[1][0]


def test_calendar_months_athenian_424():
    """Make sure calendar_months generates the correct new moons for Athenian 424/423"""
    p = calendar_months(-423)
    assert len(p) == 12
    assert as_gmt(p[0][0]) == "BCE 0424-Jul-18"
    assert as_gmt(p[-1][0]) == "BCE 0423-Jun-08"


def test_calendar_months_spartan_424():
    """Make sure calendar_months generates the correct new moons for Spartan 424/423"""
    p = calendar_months(-423, event=Seasons.AUTUMN_EQUINOX, before_event=True)
    assert len(p) == 12
    assert as_gmt(p[0][0]) == "BCE 0424-Sep-15"
    assert as_gmt(p[-1][0]) == "BCE 0423-Aug-06"


def test_calendar_months_delian_424():
    """Make sure calendar_months generates the correct new moons for Delian 424/423"""
    p = calendar_months(-423, event=Seasons.WINTER_SOLSTICE)
    assert len(p) == 12
    assert as_gmt(p[0][0]) == "BCE 0423-Jan-11"
    assert as_gmt(p[-1][0]) == "BCE 0423-Dec-01"


def test_generic_festival_months_athenian_434():
    """Athenian 434/433 should be intercalary, starting on July 9, 434
    and ending before Jul 27, 433

    """
    m = festival_months(-433)
    assert len(m) == 13
    assert m[0]["month_index"] == 1
    assert m[-1]["month_index"] == 13
    assert as_eet(m[0]["start"]) == "BCE 0434-Jul-09"
    assert as_eet(m[-1]["end"]) == "BCE 0433-Jul-27"


def test_generic_festival_months_athenian_433():
    """Athenian 433/432 should be ordinary, starting on July 27, 433
    and ending before Jul 16, 432

    """
    m = festival_months(-432)
    assert len(m) == 12
    assert as_eet(m[0]["start"]) == "BCE 0433-Jul-27"
    assert as_eet(m[-1]["end"]) == "BCE 0432-Jul-16"


def test_generic_festival_months_athenian_424():
    """Athenian 424/423 should be ordinary, starting on July 18, 424
    and ending before Jul 7, 423

    """
    m = festival_months(-423)
    assert len(m) == 12
    assert as_eet(m[0]["start"]) == "BCE 0424-Jul-18"
    assert as_eet(m[-1]["end"]) == "BCE 0423-Jul-07"


def test_generic_festival_months_athenian_423():
    """Athenian 424/423 should be intercalary, starting on July 7, 423
    and ending before Jul 26, 422

    """
    m = festival_months(-422)
    assert len(m) == 13
    assert as_eet(m[0]["start"]) == "BCE 0423-Jul-07"
    assert as_eet(m[-1]["end"]) == "BCE 0422-Jul-26"


def test_generic_festival_months_athenian_422():
    """Athenian 422/421 should be ordinary, starting on Jul 26, 422
    and ending before July 14, 421

    """
    m = festival_months(-421)
    assert len(m) == 12
    assert as_eet(m[0]["start"]) == "BCE 0422-Jul-26"
    assert as_eet(m[-1]["end"]) == "BCE 0421-Jul-14"


def test_generic_festival_months_delian_435():
    """Delian 435 (= 434/433) should be ordinary, starting on Jan 13, 434
    and ending before Jan 2, 433

    """
    m = festival_months(-434, event=Seasons.WINTER_SOLSTICE)
    assert len(m) == 12
    assert as_eet(m[0]["start"]) == "BCE 0434-Jan-13"
    assert as_eet(m[-1]["end"]) == "BCE 0433-Jan-02"


def test_generic_festival_months_delian_434():
    """Delian 434 (= 433/432) should be interclary, starting on Jan 2, 433
    and ending before Jan 20, 432

    """
    m = festival_months(-433, event=Seasons.WINTER_SOLSTICE)
    assert len(m) == 13
    assert as_eet(m[0]["start"]) == "BCE 0433-Jan-02"
    assert as_eet(m[-1]["end"]) == "BCE 0432-Jan-20"


def test_generic_festival_months_spartan_424():
    """Spartan 424/423 should be ordinary, starting on Sep 15, 424
    and ending before Sep 4, 423

    """
    m = festival_months(-423, event=Seasons.AUTUMN_EQUINOX, before_event=True)
    assert len(m) == 12
    assert as_eet(m[0]["start"]) == "BCE 0424-Sep-15"
    assert as_eet(m[-1]["end"]) == "BCE 0423-Sep-04"


def test_generic_festival_months_spartan_423():
    """Spartan 424/423 should be intercalary, starting on Sep 4, 423
    and ending before Sep 23, 422

    """
    m = festival_months(-422, event=Seasons.AUTUMN_EQUINOX, before_event=True)
    assert len(m) == 13
    assert as_eet(m[0]["start"]) == "BCE 0423-Sep-04"
    assert as_eet(m[-1]["end"]) == "BCE 0422-Sep-23"


def test_generic_festival_months_spartan_422():
    """Spartan 422/421 should be ordinary, starting on Sep 23, 422
    and ending before Sep 12, 421

    """
    m = festival_months(-421, event=Seasons.AUTUMN_EQUINOX, before_event=True)
    assert len(m) == 12
    assert as_eet(m[0]["start"]) == "BCE 0422-Sep-23"
    assert as_eet(m[-1]["end"]) == "BCE 0421-Sep-12"


# def test_month_label():
#     assert month_label(Months.HEK) == "Hekatombaiṓn"
#     assert month_label(Months.HEK, abbrev=True) == "Hek"
#     assert month_label(Months.HEK, greek=True) == "Ἑκατομβαιών"


def test_prytany_label():
    assert prytany_label(Prytanies.I) == "I"
    assert prytany_label(Prytanies.X) == "X"


# def test_suffix():
#     assert heniautos._suffix() == " hústeros"
#     assert heniautos._suffix(abbrev=True) == "₂"
#     assert heniautos._suffix(greek=True) == " ὕστερος"
#     assert heniautos._suffix(abbrev=True, greek=True) == " ὕστερος"


# def test_maybe_intercalate():
#     # No intercalations, just the list of ordinary months
#     assert heniautos._maybe_intercalate(12, Months.POS, False, False)[0] == (
#         "Hekatombaiṓn",
#         Months.HEK,
#     )
#     assert heniautos._maybe_intercalate(12, Months.POS, False, False)[3] == (
#         "Puanopsiṓn",
#         Months.PUA,
#     )
#     assert heniautos._maybe_intercalate(12, Months.POS, False, False)[6] == (
#         "Gamēliṓn",
#         Months.GAM,
#     )

#     # Intercalates Pos
#     # Month before Pos unchanged
#     assert heniautos._maybe_intercalate(13, Months.POS, False, False)[3] == (
#         "Puanopsiṓn",
#         Months.PUA,
#     )
#     # The intercalated month
#     assert heniautos._maybe_intercalate(13, Months.POS, False, False)[6] == (
#         "Posideiṓn hústeros",
#         Months.INT,
#     )
#     # Indexes of months after the intercalation 1 more than usual
#     assert heniautos._maybe_intercalate(13, Months.POS, False, False)[7] == (
#         "Gamēliṓn",
#         Months.GAM,
#     )

#     # Intercalated Boe
#     assert heniautos._maybe_intercalate(13, Months.BOE, False, False)[3] == (
#         "Boēdromiṓn hústeros",
#         Months.INT,
#     )
#     assert heniautos._maybe_intercalate(13, Months.BOE, False, False)[6] == (
#         "Posideiṓn",
#         Months.POS,
#     )
#     assert heniautos._maybe_intercalate(13, Months.BOE, False, False)[7] == (
#         "Gamēliṓn",
#         Months.GAM,
#     )


def test_festival_months():
    p = festival_months(-99)
    assert type(p) is tuple
    assert type(p[0]) is dict
    # assert p[0]["month"] == "Hekatombaiṓn"
    assert p[0]["month_index"] == 1
    # assert p[0]["constant"] == Months.HEK
    assert as_gmt(p[0]["start"]) == "BCE 0100-Jul-05"
    assert p[0]["end"] == p[1]["start"]

    # With abbreviations
    # q = festival_months(-99, abbrev=True)
    # assert q[0]["month"] == "Hek"

    # # With Greek names
    # r = festival_months(-99, greek=True)
    # assert r[0]["month"] == "Ἑκατομβαιών"

    # # greek overrides abbrev
    # assert festival_months(-99, abbrev=True, greek=True)[0]["month"] == "Ἑκατομβαιών"

    # # with intercalations
    # s = festival_months(-101)
    # assert len(s) == 13
    # # Default intercalation of Poseidēiṓn hústeros
    # assert s[6]["month"] == "Posideiṓn hústeros"
    # assert s[6]["constant"] == Months.INT

    # t = festival_months(-101, intercalate=Months.BOE)
    # assert t[3]["month"] == "Boēdromiṓn hústeros"
    # assert t[6]["month"] == "Posideiṓn"

    # # intercalation with abbreviation
    # s1 = festival_months(-101, abbrev=True)
    # assert s1[6]["month"] == "Pos₂"

    # With different visibility rules
    # NEXT_DAY is the default
    u = festival_months(-99, rule=Visible.NEXT_DAY)
    assert as_gmt(u[0]["start"]) == as_gmt(p[0]["start"])

    # with SECOND_DAY
    v = festival_months(-99, rule=Visible.SECOND_DAY)
    print(v)
    assert as_gmt(v[0]["start"]) == "BCE 0100-Jul-06"

    # with CONJUNCTION
    v = festival_months(-99, rule=Visible.CONJUNCTION)
    assert as_gmt(v[0]["start"]) == "BCE 0100-Jul-04"


def test_generic_festival_calendar():
    p = festival_calendar(-100, calendar=None)
    assert len(p) == 354
    assert len(by_months(p)) == 12
    assert isinstance(p[0], FestivalDay)
    assert p[0].month is None
    assert p[0].month_name is None
    assert as_eet(p[0].jdn) == "BCE 0101-Jul-16"
    assert as_eet(p[-1].jdn) == "BCE 0100-Jul-04"


def test_generic_festival_calendar_athenian():
    # Athenian should be the default value
    p = festival_calendar(-100)
    assert len(by_months(p)) == 12
    assert p[0].month is AthenianMonths.HEK
    assert p[0].month_name == "Hekatombaiṓn"
    assert as_eet(p[0].jdn) == "BCE 0101-Jul-16"

    # Intercalary year
    p = festival_calendar(-101)
    p_months = by_months(p)
    assert len(p_months) == 13
    # By default, the 7th month should be intercalated
    assert p_months[6][0].month is Months.INT
    assert p_months[6][0].month_name == "Posideiṓn hústeros"

    # Intercalate Hek instead
    p = festival_calendar(-101, intercalate=1)
    p_months = by_months(p)
    assert p_months[1][0].month is Months.INT
    assert p_months[1][0].month_name == "Hekatombaiṓn hústeros"
    assert p_months[6][0].month is AthenianMonths.POS
    assert p_months[6][0].month_name == "Posideiṓn"


def test_athenian_festival_calendar():
    p = athenian_festival_calendar(-100)
    assert len(by_months(p)) == 12
    assert p[0].month is AthenianMonths.HEK
    assert p[0].month_name == "Hekatombaiṓn"
    assert as_eet(p[0].jdn) == "BCE 0101-Jul-16"


def test_generic_festival_calendar_delian():
    p = festival_calendar(-100, calendar=Cal.DELIAN, event=Seasons.WINTER_SOLSTICE)
    assert as_eet(p[0].jdn) == "BCE 0100-Jan-10"
    assert len(by_months(p)) == 12
    assert p[0].month is DelianMonths.LEN
    assert p[0].month_name == "Lēnaiṓn"

    # Intercalary year
    p = festival_calendar(-102, calendar=Cal.DELIAN, event=Seasons.WINTER_SOLSTICE)
    assert as_eet(p[0].jdn) == "BCE 0102-Jan-02"
    p_months = by_months(p)
    assert len(p_months) == 13
    # By default, the 7th month should be intercalated
    assert p_months[6][0].month is Months.INT
    assert p_months[6][0].month_name == "Pánēmos hústeros"

    # Intercalate Hek instead
    p = festival_calendar(
        -102, intercalate=1, calendar=Cal.DELIAN, event=Seasons.WINTER_SOLSTICE
    )
    assert as_eet(p[0].jdn) == "BCE 0102-Jan-02"
    p_months = by_months(p)
    assert p_months[1][0].month is Months.INT
    assert p_months[1][0].month_name == "Lēnaiṓn hústeros"
    assert p_months[6][0].month is DelianMonths.PAN
    assert p_months[6][0].month_name == "Pánēmos"


def test_delian_festival_calendar():
    p = delian_festival_calendar(-100)
    assert len(by_months(p)) == 12
    assert p[0].month is DelianMonths.LEN
    assert p[0].month_name == "Lēnaiṓn"
    assert as_eet(p[0].jdn) == "BCE 0100-Jan-10"


def test_spartan_festival_calendar():
    p = spartan_festival_calendar(-100)
    assert len(by_months(p)) == 12
    assert p[0].month is SpartanMonths.UN1
    assert p[0].month_name == "Unknown 1"
    assert as_eet(p[0].jdn) == "BCE 0101-Sep-13"

    p = spartan_festival_calendar(-102)
    assert len(by_months(p)) == 13
    assert as_eet(p[0].jdn) == "BCE 0103-Sep-06"
    p_months = by_months(p)
    assert p_months[6][0].month is Months.INT
    assert p_months[6][0].month_name == "Unknown 6 hústeros"


def test_festival_calendar():
    p = festival_calendar(-100)

    assert type(p) is tuple

    assert type(p[0]) is FestivalDay
    assert p[0].month_name == "Hekatombaiṓn"
    assert p[0].month == AthenianMonths.HEK
    # assert type(p[0]["days"]) is tuple
    # assert type(p[0]["days"][0]) is dict
    assert p[0].day == 1
    assert as_gmt(p[0].jdn) == "BCE 0101-Jul-16"
    assert p[0].doy == 1

    met = [d for d in p if d.month == AthenianMonths.MET]

    assert met[0].month_name == "Metageitniṓn"
    assert met[0].day == 1
    assert as_gmt(met[0].jdn) == "BCE 0101-Aug-15"
    assert met[0].doy == 31


def test_delian_festival_calendar_434_433():
    c = festival_calendar(-434, event=Seasons.WINTER_SOLSTICE)
    assert len(c) == 354
    c_months = by_months(c)
    assert len(c_months) == 12
    assert as_eet(c_months[0][0].jdn) == "BCE 0434-Jan-13"
    assert as_eet(c_months[-1][0].jdn) == "BCE 0434-Dec-03"

    c = festival_calendar(-433, event=Seasons.WINTER_SOLSTICE)
    assert len(c) == 384
    c_months = by_months(c)
    assert len(c_months) == 13
    assert as_eet(c_months[0][0].jdn) == "BCE 0433-Jan-02"
    assert as_eet(c_months[-1][0].jdn) == "BCE 0433-Dec-21"


def test_find_date():
    d = find_date(-100, AthenianMonths.MET, 1)
    assert d.month_name == "Metageitniṓn"
    assert d.month == AthenianMonths.MET
    assert d.day == 1
    assert as_gmt(d.jdn) == "BCE 0101-Aug-15"
    assert d.doy == 31

    with pytest.raises(HeniautosError):
        find_date(-99, AthenianMonths.MET, 31)


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


def test_by_months():
    p = by_months(festival_calendar(-421))
    assert len(p) == 12

    # make sure the prytany groups are in the right order
    assert [list(set([pi.month_index for pi in pr])) for pr in p] == [
        [1],
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8],
        [9],
        [10],
        [11],
        [12],
    ]


def test_by_prytanies():
    p = by_prytanies(prytany_calendar(-420))
    assert len(p) == 10

    # make sure the prytany groups are in the right order
    assert [list(set([pi.prytany_index for pi in pr])) for pr in p] == [
        [1],
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8],
        [9],
        [10],
    ]


# def test_pryt_len_festival():
#     cal = calendar_months(-100)
#     e = [c for c in heniautos._pryt_len_festival(cal)]
#     assert len(e) == 12
#     assert e[0] == 30
#     assert e[1] == 29
#     assert e[-1] == 29


def test_prytanies_solar():
    p = prytanies(-420)
    assert len(p) == 10
    assert sum([q["end"] - q["start"] for q in p]) == 365
    assert p[0]["end"] - p[0]["start"] == 37
    assert p[4]["end"] - p[4]["start"] == 37
    assert p[6]["end"] - p[6]["start"] == 36
    assert p[-1]["end"] - p[-1]["start"] == 36


def test_prytanies_solar_leap():
    p = prytanies(-417)
    assert len(p) == 10
    assert sum([q["end"] - q["start"] for q in p]) == 366
    assert p[0]["end"] - p[0]["start"] == 37
    assert p[4]["end"] - p[4]["start"] == 37
    assert p[6]["end"] - p[6]["start"] == 36
    assert p[-1]["end"] - p[-1]["start"] == 37


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

    # Confirm constants for other tests
    assert heniautos._pryt_auto(bce_as_negative(O_SO)) == Prytany.QUASI_SOLAR
    assert heniautos._pryt_auto(bce_as_negative(O_SO_LONG)) == Prytany.QUASI_SOLAR
    assert heniautos._pryt_auto(bce_as_negative(I_SO)) == Prytany.QUASI_SOLAR

    assert heniautos._pryt_auto(bce_as_negative(O_10)) == Prytany.ALIGNED_10
    assert heniautos._pryt_auto(bce_as_negative(O_10_LONG)) == Prytany.ALIGNED_10
    assert heniautos._pryt_auto(bce_as_negative(I_10)) == Prytany.ALIGNED_10

    assert heniautos._pryt_auto(bce_as_negative(O_12)) == Prytany.ALIGNED_12
    assert heniautos._pryt_auto(bce_as_negative(O_12_LONG)) == Prytany.ALIGNED_12
    assert heniautos._pryt_auto(bce_as_negative(I_12)) == Prytany.ALIGNED_12

    assert heniautos._pryt_auto(bce_as_negative(O_13)) == Prytany.ALIGNED_13
    assert heniautos._pryt_auto(bce_as_negative(O_13_LONG)) == Prytany.ALIGNED_13
    assert heniautos._pryt_auto(bce_as_negative(I_13)) == Prytany.ALIGNED_13


def test_pryt_auto_start():
    # Should return Julian dates from rounded Terrestrial Time

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(500), Prytany.AUTO), True)
        == "BCE 0500-Jul-04 13:59:59 EET"
    )

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(425), Prytany.AUTO), True)
        == "BCE 0425-Jul-04 13:59:59 EET"
    )

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(429), Prytany.AUTO), True)
        == "BCE 0429-Jul-04 13:59:59 EET"
    )

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(424), Prytany.AUTO), True)
        == "BCE 0424-Jul-07 13:59:59 EET"
    )

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(421), Prytany.AUTO), True)
        == "BCE 0421-Jul-07 13:59:59 EET"
    )

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(420), Prytany.AUTO), True)
        == "BCE 0420-Jul-08 13:59:59 EET"
    )

    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(419), Prytany.AUTO), True)
        == "BCE 0419-Jul-09 13:59:59 EET"
    )

    # Provide your own start day
    assert (
        as_eet(heniautos._pryt_auto_start(bce_as_negative(419), 1), True)
        == "BCE 0419-Jul-01 13:59:59 EET"
    )


def test_pryt_solar_end():
    # One quasi-solar year should end at the next quasi solar year
    year_start = heniautos._pryt_auto_start(bce_as_negative(426), Prytany.AUTO)
    year_end = heniautos._pryt_solar_end(year_start)
    next_year = heniautos._pryt_auto_start(bce_as_negative(425), Prytany.AUTO)
    assert year_end == next_year


def test_prytany_calendar_solar():
    p = by_prytanies(prytany_calendar(-420))

    assert len(p) == 10
    assert p[0][0].prytany_index == 1
    assert as_gmt(p[0][0].jdn) == "BCE 0421-Jul-07"
    assert len(p[0]) == 37

    assert p[-1][-1].prytany_index == 10
    assert as_gmt(p[-1][-1].jdn) == "BCE 0420-Jul-06"
    assert len(p[-1]) == 36
    assert p[-1][-1].doy == 365

    p2 = prytany_calendar(bce_as_negative(429))
    assert as_gmt(p2[0].jdn) == "BCE 0429-Jul-04"


def test_prytany_calendar_solar_leap():
    p = by_prytanies(prytany_calendar(-417))

    assert len(p) == 10
    assert p[0][0].prytany_index == 1
    assert as_gmt(p[0][0].jdn) == "BCE 0418-Jul-09"
    assert len(p[0]) == 37

    assert p[-1][-1].prytany_index == 10
    assert as_gmt(p[-1][-1].jdn) == "BCE 0417-Jul-08"
    assert len(p[-1]) == 37
    assert p[-1][-1].doy == 366


# Ten prytanies: 409-308 BCE


def test_prytanies_10_ordinary():
    year = bce_as_negative(O_10)
    c3 = festival_months(year)
    p3 = prytanies(year)

    # 10 prytanies in 354 days
    assert len(p3) == 10
    assert sum([q["end"] - q["start"] for q in c3]) == 354
    assert sum([q["end"] - q["start"] for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert as_gmt(p3[0]["start"]) == as_gmt(c3[0]["start"])
    assert as_gmt(p3[-1]["end"]) == as_gmt(c3[-1]["end"])

    # 354 day year. I-IV should be 36 days, the rest 35
    assert p3[0]["end"] - p3[0]["start"] == 36
    assert p3[4]["end"] - p3[4]["start"] == 35
    assert p3[-1]["end"] - p3[-1]["start"] == 35


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
    assert span(p3[0]["start"], p3[0]["end"]) == 30  # not 29
    assert span(p3[2]["start"], p3[2]["end"]) == 30  # not 29
    assert span(p3[-3]["start"], p3[-3]["end"]) == 29  # not 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29  # not 30
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29  # this one the same


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
    assert span(p3[0]["start"], p3[0]["end"]) == 30  # not 29
    assert span(p3[1]["start"], p3[1]["end"]) == 30
    assert span(p3[-4]["start"], p3[-4]["end"]) == 29  # not 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29
    assert span(p3[-1]["start"], p3[-1]["end"]) == 30  # not 29


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

    # All prytanies are 32 days long
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

    # Prytanies I-III 28 days long, the rest 27 days
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
    assert span(p3[1]["start"], p3[1]["end"]) == 30  # not 29
    assert span(p3[-3]["start"], p3[-3]["end"]) == 29  # not 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 29
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29


def test_prytany_calendar_10_ordinary():
    year = bce_as_negative(O_10)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))

    assert len(p3) == 10

    # Make sure the calendars are the same number of days
    assert c3[-1][-1].doy == 354
    assert p3[-1][-1].doy == 354

    assert p3[0][0].prytany_index == 1

    # Make sure the calendars end on the same day
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    # Specific prytany lengths
    assert len(p3[0]) == 36
    assert len(p3[4]) == 35
    assert len(p3[-1]) == 35


def test_prytany_calendar_10_ordinary_long():
    year = bce_as_negative(O_10_LONG)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 10
    assert p3[-1][-1].doy == 355

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 36
    assert len(p3[4]) == 35
    assert len(p3[-1]) == 36


def test_prytany_calendar_10_intercalated():
    year = bce_as_negative(I_10)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 10
    assert p3[-1][-1].doy == 384

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 39
    assert len(p3[4]) == 38
    assert len(p3[-1]) == 38


def test_prytany_calendar_12_ordinary():
    year = bce_as_negative(O_12)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 12
    assert p3[-1][-1].doy == 354

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 29
    assert len(p3[1]) == 29
    assert len(p3[2]) == 30
    assert len(p3[-2]) == 30
    assert len(p3[-1]) == 29


def test_prytany_calendar_12_ordinary_aristotle():
    year = bce_as_negative(O_12)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year, rule_of_aristotle=True))
    assert len(p3) == 12
    assert p3[-1][-1].doy == 354

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 30
    assert len(p3[1]) == 30
    assert len(p3[2]) == 30
    assert len(p3[-2]) == 29
    assert len(p3[-1]) == 29


def test_prytany_calendar_12_long():
    year = bce_as_negative(O_12_LONG)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 12
    assert p3[-1][-1].doy == 355

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    # Like the festival calendar, prytanies are 29 or 30 days
    # Festival months:
    #
    #    H F H F F F H F F H H F
    #
    assert len(p3[0]) == 29
    assert len(p3[1]) == 30
    assert len(p3[-2]) == 29
    assert len(p3[-1]) == 30


def test_prytany_calendar_12_long_aristotle():
    year = bce_as_negative(O_12_LONG)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year, rule_of_aristotle=True))
    assert len(p3) == 12
    assert p3[-1][-1].doy == 355

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 30
    assert len(p3[1]) == 30
    assert len(p3[-2]) == 29
    assert len(p3[-1]) == 30


def test_prytany_calendar_12_intercalated():
    year = bce_as_negative(I_12)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 12
    assert p3[-1][-1].doy == 384

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 32
    assert len(p3[6]) == 32
    assert len(p3[-1]) == 32


def test_prytany_calendar_13_ordinary():
    year = bce_as_negative(O_13)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 13
    assert p3[-1][-1].doy == 354

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 28
    assert len(p3[3]) == 27
    assert len(p3[-1]) == 27


def test_prytany_calendar_13_long():
    year = bce_as_negative(O_13_LONG)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 13
    assert p3[-1][-1].doy == 355

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 28
    assert len(p3[3]) == 27
    assert len(p3[-1]) == 28


def test_prytany_calendar_13_intercalated():
    year = bce_as_negative(I_13)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year))
    assert len(p3) == 13
    assert p3[-1][-1].doy == 384

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    # Prytanies follow the festival calendar
    # The festival months of 214 are:
    #
    #     F H F H F F F H F H F H H
    #
    assert len(p3[0]) == 30
    assert len(p3[1]) == 29
    assert len(p3[-3]) == 30
    assert len(p3[-2]) == 29
    assert len(p3[-1]) == 29


def test_prytany_calendar_13_intercalated_aristotle():
    year = bce_as_negative(I_13)
    c3 = by_months(festival_calendar(year))
    p3 = by_prytanies(prytany_calendar(year, rule_of_aristotle=True))
    assert len(p3) == 13
    assert p3[-1][-1].doy == 384

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 30
    assert len(p3[1]) == 30
    assert len(p3[-2]) == 29
    assert len(p3[-1]) == 29


def test_fest_doy_ranges():
    r = heniautos._fest_doy_ranges(AthenianMonths.ELA, 19, False)
    assert len(r) == 6
    assert min([m["doy"] for m in r]) == 253
    assert max([m["doy"] for m in r]) == 258

    r = heniautos._fest_doy_ranges(AthenianMonths.ELA, 19, True)
    assert len(r) == 6
    assert min([m["doy"] for m in r]) == 282
    assert max([m["doy"] for m in r]) == 287

    r = heniautos._fest_doy_ranges(AthenianMonths.MAI, 19, False)
    assert len(r) == 5
    assert min([m["doy"] for m in r]) == 135
    assert max([m["doy"] for m in r]) == 139

    r = heniautos._fest_doy_ranges(AthenianMonths.MAI, 19, True)
    assert len(r) == 6
    assert min([m["doy"] for m in r]) == 164
    assert max([m["doy"] for m in r]) == 169

    r = heniautos._fest_doy_ranges(AthenianMonths.MOU, 27, False)
    assert len(r) == 5
    assert min([m["doy"] for m in r]) == 291
    assert max([m["doy"] for m in r]) == 295

    r = heniautos._fest_doy_ranges(AthenianMonths.MOU, 27, True)
    assert len(r) == 5
    assert min([m["doy"] for m in r]) == 320
    assert max([m["doy"] for m in r]) == 324


def test_festival_doy():
    # 1st month, no intercalation possible
    doy = festival_doy(AthenianMonths.HEK, 5)
    assert len(doy) == 1
    assert doy[0]["doy"] == 5
    assert len(doy[0]["preceding"]) == 0

    assert doy[0]["intercalation"] is False
    assert not any([d["intercalation"] for d in doy])

    # 2nd month
    doy = festival_doy(AthenianMonths.MET, 5)
    print(doy)
    assert len(doy) == 5
    assert doy[0]["doy"] == 34
    assert len(doy[0]["preceding"]) == 1
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 65
    assert len(doy[-1]["preceding"]) == 2
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 63])
    assert all([d["intercalation"] for d in doy if d["doy"] > 35])

    # 5th month
    doy = festival_doy(AthenianMonths.MAI, 27)
    assert len(doy) == 11
    assert doy[0]["doy"] == 143
    assert len(doy[0]["preceding"]) == 4
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 177
    assert len(doy[-1]["preceding"]) == 5
    assert doy[-1]["intercalation"] is True
    assert not any([d["intercalation"] for d in doy if d["doy"] < 172])
    assert all([d["intercalation"] for d in doy if d["doy"] > 147])

    doy = festival_doy(AthenianMonths.MOU, 27)
    assert len(doy) == 10
    assert doy[0]["doy"] == 291
    assert len(doy[0]["preceding"]) == 9
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 324
    assert len(doy[-1]["preceding"]) == 10
    assert doy[-1]["intercalation"] is True
    assert not any([d["intercalation"] for d in doy if d["doy"] < 320])
    assert all([d["intercalation"] for d in doy if d["doy"] > 295])


def test_prytany_doy_quasi_solar():
    # 1st prytany
    doy = prytany_doy(Prytanies.I, 10, pryt_type=Prytany.QUASI_SOLAR)
    assert len(doy) == 1
    assert doy[0]["doy"] == 10
    assert len(doy[0]["preceding"]) == 0

    # There is no intercalation in the quasi-solar conciliar year
    assert doy[0]["intercalation"] is None

    # 2nd prytany
    doy = prytany_doy(Prytanies.II, 10, pryt_type=Prytany.QUASI_SOLAR)

    assert len(doy) == 2

    assert doy[0]["doy"] == 46
    assert len(doy[0]["preceding"]) == 1
    assert doy[0]["intercalation"] is None

    assert doy[-1]["doy"] == 47
    assert len(doy[-1]["preceding"]) == 1
    assert doy[-1]["intercalation"] is None

    assert not any([d["intercalation"] for d in doy])

    # 9th prytany
    doy = prytany_doy(Prytanies.IX, 10, pryt_type=Prytany.QUASI_SOLAR)

    assert len(doy) == 3

    assert doy[0]["doy"] == 301
    assert len(doy[0]["preceding"]) == 8
    assert doy[0]["intercalation"] is None

    assert doy[-1]["doy"] == 303
    assert len(doy[-1]["preceding"]) == 8
    assert doy[-1]["intercalation"] is None

    # assert not any([d["intercalation"] for d in doy])
    assert all([d["intercalation"] is None for d in doy])

    # All prytanies are 36 or 37 days
    assert all([all([m in (36, 37) for m in d["preceding"]]) for d in doy])


def test_prytany_doy_aligned_10():
    # 1st prytany
    doy = prytany_doy(Prytanies.I, 10, pryt_type=Prytany.ALIGNED_10)
    assert len(doy) == 2
    assert doy[0]["doy"] == 10
    assert len(doy[0]["preceding"]) == 0
    assert doy[0]["intercalation"] is False

    # Always an intercalated result (even if its identical to ordinary)
    assert doy[-1]["doy"] == 10
    assert len(doy[-1]["preceding"]) == 0
    assert doy[-1]["intercalation"] is True

    doy = prytany_doy(Prytanies.II, 10, pryt_type=Prytany.ALIGNED_10)
    assert len(doy) == 4

    assert doy[0]["doy"] == 45
    assert len(doy[0]["preceding"]) == 1
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 49
    assert len(doy[-1]["preceding"]) == 1
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 48])
    assert all([d["intercalation"] for d in doy if d["doy"] > 46])

    doy = prytany_doy(Prytanies.IX, 10, pryt_type=Prytany.ALIGNED_10)
    assert len(doy) == 6

    assert doy[0]["doy"] == 292
    assert len(doy[0]["preceding"]) == 8
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 318
    assert len(doy[-1]["preceding"]) == 8
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 316])
    assert all([d["intercalation"] for d in doy if d["doy"] > 294])

    # All ordinary prytanies are 35 or 36 days
    assert all(
        [
            all([m in (35, 36) for m in d["preceding"]])
            for d in doy
            if not d["intercalation"]
        ]
    )

    # All intercalary prytanies are 38 or 39 days
    assert all(
        [
            all([m in (38, 39) for m in d["preceding"]])
            for d in doy
            if d["intercalation"]
        ]
    )

    doy = prytany_doy(Prytanies.I, 39, pryt_type=Prytany.ALIGNED_10)
    print(doy)

    assert len(doy) == 1


def test_prytany_doy_aligned_12():
    # 1st prytany
    doy = prytany_doy(Prytanies.I, 10, pryt_type=Prytany.ALIGNED_12)
    assert len(doy) == 2
    assert doy[0]["doy"] == 10
    assert len(doy[0]["preceding"]) == 0
    assert doy[0]["intercalation"] is False

    # Always an intercalated result (even if its identical to ordinary)
    assert doy[-1]["doy"] == 10
    assert len(doy[-1]["preceding"]) == 0
    assert doy[-1]["intercalation"] is True

    # 2nd prytany
    doy = prytany_doy(Prytanies.II, 10, pryt_type=Prytany.ALIGNED_12)
    assert len(doy) == 3

    assert doy[0]["doy"] == 39
    assert len(doy[0]["preceding"]) == 1
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 42
    assert len(doy[-1]["preceding"]) == 1
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 42])
    assert all([d["intercalation"] for d in doy if d["doy"] > 40])

    # 9th prytany
    doy = prytany_doy(Prytanies.IX, 10, pryt_type=Prytany.ALIGNED_12)
    assert len(doy) == 6

    assert doy[0]["doy"] == 245
    assert len(doy[0]["preceding"]) == 8
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 266
    assert len(doy[-1]["preceding"]) == 8
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 266])
    assert all([d["intercalation"] for d in doy if d["doy"] > 249])

    # All ordinary prytanies are 29 or 30 days
    assert all(
        [
            all([m in (29, 30) for m in d["preceding"]])
            for d in doy
            if not d["intercalation"]
        ]
    )

    # All intercalary prytanies are 32 days
    assert all(
        [all([m in (32,) for m in d["preceding"]]) for d in doy if d["intercalation"]]
    )


def test_prytany_doy_aligned_13():
    # 1st prytany
    doy = prytany_doy(Prytanies.I, 10, pryt_type=Prytany.ALIGNED_13)
    assert len(doy) == 2
    assert doy[0]["doy"] == 10
    assert len(doy[0]["preceding"]) == 0
    assert doy[0]["intercalation"] is False

    # Always an intercalated result (even if its identical to ordinary)
    assert doy[-1]["doy"] == 10
    assert len(doy[-1]["preceding"]) == 0
    assert doy[-1]["intercalation"] is True

    # 2nd prytany
    doy = prytany_doy(Prytanies.II, 10, pryt_type=Prytany.ALIGNED_13)
    assert len(doy) == 4

    assert doy[0]["doy"] == 37
    assert len(doy[0]["preceding"]) == 1
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 40
    assert len(doy[-1]["preceding"]) == 1
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 39])
    assert all([d["intercalation"] for d in doy if d["doy"] > 38])

    # 9th prytany
    doy = prytany_doy(Prytanies.IX, 10, pryt_type=Prytany.ALIGNED_13)
    assert len(doy) == 10

    assert doy[0]["doy"] == 226
    assert len(doy[0]["preceding"]) == 8
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 249
    assert len(doy[-1]["preceding"]) == 8
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 244])
    assert all([d["intercalation"] for d in doy if d["doy"] > 229])

    # All ordinary prytanies are 27 or 28 days
    assert all(
        [
            all([m in (27, 28) for m in d["preceding"]])
            for d in doy
            if not d["intercalation"]
        ]
    )

    # All intercalary prytanies are 29 or 30 days
    assert all(
        [
            all([m in (29, 30) for m in d["preceding"]])
            for d in doy
            if d["intercalation"]
        ]
    )


def test_prytany_doy_auto():
    # QUASI_SOLAR, all prytanies 36 or 37 days
    assert all(
        [
            all([p in (36, 37) for p in d["preceding"]])
            for d in prytany_doy(Prytanies.IV, 10, Prytany.AUTO, bce_as_negative(O_SO))
        ]
    )

    # ALIGNED_10, all prytanies 35, 36, 38, or 39 days
    assert all(
        [
            all([p in (35, 36, 38, 39) for p in d["preceding"]])
            for d in prytany_doy(Prytanies.IV, 10, Prytany.AUTO, bce_as_negative(O_10))
        ]
    )

    # ALIGNED_12, all prytanies 29, 30, or 32 days
    assert all(
        [
            all([p in (29, 30, 32) for p in d["preceding"]])
            for d in prytany_doy(Prytanies.IV, 10, Prytany.AUTO, bce_as_negative(O_12))
        ]
    )

    # ALIGNED_13, all prytanies 27, 28, 29, or 30 days
    assert all(
        [
            all([p in (27, 28, 29, 30) for p in d["preceding"]])
            for d in prytany_doy(Prytanies.IV, 10, Prytany.AUTO, bce_as_negative(O_13))
        ]
    )

    # Error if you choose Prytany.AUTO and forget to give a year
    with pytest.raises(HeniautosError):
        prytany_doy(Prytanies.IV, 10, Prytany.AUTO)


def test_fest_eq_tuple():
    eq = heniautos._fest_eq((AthenianMonths.MET, 10))
    assert len(eq) == 5
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[-1]["doy"] == 70
    assert eq[-1]["intercalation"] is True

    assert heniautos._fest_eq((AthenianMonths.MET, 10)) == heniautos._fest_eq(
        ((AthenianMonths.MET, 10),)
    )


def test_fest_eq_nested():
    eq = heniautos._fest_eq(((AthenianMonths.MET, 10), (AthenianMonths.MET, 11)))
    assert len(eq) == 10
    assert eq[0]["date"] == (AthenianMonths.MET, 10)
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[4]["date"] == (AthenianMonths.MET, 10)
    assert eq[4]["doy"] == 70
    assert eq[4]["intercalation"] is True
    assert eq[5]["date"] == (AthenianMonths.MET, 11)
    assert eq[5]["doy"] == 40
    assert eq[5]["intercalation"] is False
    assert eq[-1]["date"] == (AthenianMonths.MET, 11)
    assert eq[-1]["doy"] == 71
    assert eq[-1]["intercalation"] is True


def test_pryt_eq_tuple():
    eq = heniautos._pryt_eq((Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10)
    assert len(eq) == 4
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[-1]["doy"] == 43
    assert eq[-1]["intercalation"] is True

    assert heniautos._pryt_eq(
        (Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10
    ) == heniautos._pryt_eq(((Prytanies.II, 4),), pryt_type=Prytany.ALIGNED_10)


def test_pryt_eq_nested():
    eq = heniautos._pryt_eq(
        ((Prytanies.II, 4), (Prytanies.II, 5)), pryt_type=Prytany.ALIGNED_10
    )
    assert len(eq) == 8
    assert eq[0]["date"] == (Prytanies.II, 4)
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[3]["date"] == (Prytanies.II, 4)
    assert eq[3]["doy"] == 43
    assert eq[3]["intercalation"] is True
    assert eq[-1]["date"] == (Prytanies.II, 5)
    assert eq[-1]["doy"] == 44
    assert eq[-1]["intercalation"] is True


def test_equations_tuples():
    eq = equations(
        (AthenianMonths.MET, 10), (Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10
    )

    # Two solutions to this equation:
    assert len(eq) == 2

    # The first solution is DOY 39 (these should be sorted by DOY)
    assert len(eq[0]) == 2
    f, c = eq[0]

    assert f["doy"] == 39
    assert c["doy"] == 39

    assert f["preceding"] == (29,)
    assert c["preceding"] == (35,)

    assert f["intercalation"] is False
    assert c["intercalation"] is False

    # The second solution is DOY 40
    assert len(eq[1]) == 2
    f, c = eq[1]
    assert f["doy"] == 40
    assert c["doy"] == 40

    assert f["preceding"] == (30,)
    assert c["preceding"] == (36,)

    assert f["intercalation"] is False
    assert c["intercalation"] is False

    eq = equations(
        (AthenianMonths.POS, 14), (Prytanies.V, 36), pryt_type=Prytany.ALIGNED_10
    )

    assert len(eq) == 5
    assert [f[0]["doy"] for f in eq] == [188, 189, 190, 191, 192]
    assert [p[0]["doy"] for p in eq] == [188, 189, 190, 191, 192]


def test_equations_must_be_intercalary():
    eq1 = equations(
        (AthenianMonths.MET, 9), (Prytanies.I, 39), pryt_type=Prytany.ALIGNED_10
    )
    eq2 = equations(
        (AthenianMonths.MET, 6), (Prytanies.I, 36), pryt_type=Prytany.ALIGNED_10
    )

    # There should be only one possibility with I.39 because a 39-day
    # prytany requires an intercalary year
    assert len(eq1) == 1

    # There should be two possibilities because I.36 could be the 36th
    # day of either a 36-day or a 39-day prytany. An ordinary and an
    # intercalary year are both possible
    assert len(eq2) == 2


def test_equations_nested():
    eq = equations(
        ((AthenianMonths.HEK, 30), (AthenianMonths.MET, 1)),
        ((Prytanies.I, 30), (Prytanies.I, 31)),
        pryt_type=Prytany.ALIGNED_10,
    )

    assert all([e[0]["date"] == (AthenianMonths.HEK, 30) for e in eq[0:2]])
    assert all([e[0]["date"] == (AthenianMonths.MET, 1) for e in eq[2:]])

    assert len(eq) == 6


def test_0_prytanies():
    eq = equations(
        (AthenianMonths.MET, 9), (Prytanies.I, 39), pryt_type=Prytany.ALIGNED_10
    )

    assert len(eq) == 1
    assert len(eq[0][1]["preceding"]) == 0


@pytest.mark.skip(reason="probably going to remove")
def test_dinsmoor():
    c = festival_calendar(-430, rule=Visible.DINSMOOR)
    pos = [d for d in c if d.month_index == 6]

    assert pos[0].month_name == "Posideiṓn"
    assert as_eet(pos[0].jdn) == "BCE 0431-Nov-29"
    assert pos[0].doy == 148
    assert pos[-1].doy == 177

    pos2 = [d for d in c if d.month_index == 7]
    assert pos2[0].month_name == "Posideiṓn hústeros"
    assert as_eet(pos2[0].jdn) == "BCE 0431-Dec-29"
    assert pos2[0].doy == 178
    assert pos2[-1].doy == 206

    e = festival_calendar(-310, rule=Visible.DINSMOOR)
    assert e[0].month_name == "Uncertain"
    assert as_eet(e[0].jdn) == "BCE 0311-Jun-29"


@pytest.mark.skip(reason="probably going to remove")
def test_dinsmoor_months():
    assert dinsmoor_months(-430)[5]["month"] == "Posideiṓn"
    assert as_eet(dinsmoor_months(-430)[5]["start"]) == "BCE 0431-Nov-29"
    assert as_eet(dinsmoor_months(-430)[5]["end"]) == "BCE 0431-Dec-29"
    assert dinsmoor_months(-430)[6]["month"] == "Posideiṓn hústeros"
    assert dinsmoor_months(-430, abbrev=True)[6]["month"] == "Pos₂"
    assert dinsmoor_months(-430, greek=True)[6]["month"] == "Ποσιδειών ὕστερος"

    assert dinsmoor_months(-310)[0]["month"] == "Uncertain"
    assert dinsmoor_months(-310, abbrev=True)[0]["month"] == "Unc"
    assert dinsmoor_months(-310, greek=True)[0]["month"] == "Uncertain"


def test_doy_to_julian():
    assert as_eet(doy_to_julian(256, bce_as_negative(332))) == "BCE 0331-Apr-01"

    assert (
        as_eet(doy_to_julian(256, bce_as_negative(332), rule=Visible.SECOND_DAY))
        == "BCE 0331-Apr-02"
    )
    assert (
        as_eet(doy_to_julian(256, bce_as_negative(332), rule=Visible.CONJUNCTION))
        == "BCE 0331-Mar-31"
    )


def test_festival_to_julian():
    assert (
        as_eet(festival_to_julian(bce_as_negative(332), AthenianMonths.ELA, 19))
        == "BCE 0331-Apr-01"
    )

    assert (
        as_eet(
            festival_to_julian(
                bce_as_negative(332), AthenianMonths.ELA, 19, rule=Visible.SECOND_DAY
            )
        )
        == "BCE 0331-Apr-02"
    )

    assert (
        as_eet(
            festival_to_julian(
                bce_as_negative(332), AthenianMonths.ELA, 19, rule=Visible.CONJUNCTION
            )
        )
        == "BCE 0331-Mar-31"
    )


def test_prytany_to_julian():
    assert (
        as_gmt(prytany_to_julian(bce_as_negative(332), Prytanies.VIII, 7).jdn)
        == "BCE 0331-Apr-01"
    )

    assert (
        as_gmt(
            prytany_to_julian(
                bce_as_negative(332), Prytanies.VIII, 7, rule=Visible.SECOND_DAY
            ).jdn
        )
        == "BCE 0331-Apr-02"
    )

    assert (
        as_gmt(
            prytany_to_julian(
                bce_as_negative(332), Prytanies.VIII, 7, rule=Visible.CONJUNCTION
            ).jdn
        )
        == "BCE 0331-Mar-31"
    )

    with pytest.raises(HeniautionNoDayInYearError):
        assert (
            as_gmt(
                prytany_to_julian(
                    bce_as_negative(332), Prytanies.VIII, 39, rule=Visible.CONJUNCTION
                ).jdn
            )
            == "BCE 0331-Mar-31"
        )


def test_no_sun_data():
    with pytest.raises(HeniautosNoDataError) as e1:
        festival_calendar(100)

    assert "100 CE" in str(e1)

    with pytest.raises(HeniautosNoDataError) as e2:
        festival_calendar(-999)

    assert "1000 BCE" in str(e2)


def test_no_moon_no_data():
    with pytest.raises(HeniautosNoDataError) as e1:
        new_moons(100)

    assert "100 CE" in str(e1)

    with pytest.raises(HeniautosNoDataError) as e2:
        new_moons(-999)

    assert "1000 BCE" in str(e2)


def test_320():
    # Bug: For the year 320 (2-day rule), the boundaries betwee many
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

    cal_320 = festival_calendar(bce_as_negative(320), rule=Visible.SECOND_DAY)

    # With the two day rule, 320 is ordinary
    assert cal_320[-1].doy == 354

    # It starts on Jul 9
    assert as_eet(cal_320[0].jdn) == "BCE 0320-Jul-09"
    # and ends on Jun 27
    assert as_eet(cal_320[-1].jdn) == "BCE 0319-Jun-27"

    months = dict(
        zip(Months, [[d.jdn for d in cal_320 if d.month == m] for m in Months])
    )

    assert [as_gmt(d.jdn) for d in cal_320 if d.day == 1] == [
        "BCE 0320-Jul-09",
        "BCE 0320-Aug-07",
        "BCE 0320-Sep-05",
        "BCE 0320-Oct-05",
        "BCE 0320-Nov-04",
        "BCE 0320-Dec-04",
        "BCE 0319-Jan-02",
        "BCE 0319-Feb-01",
        "BCE 0319-Mar-03",
        "BCE 0319-Apr-01",
        "BCE 0319-May-01",
        "BCE 0319-May-30",
    ]

    # With the 1-day rule it is intercalary
    assert festival_calendar(bce_as_negative(320), rule=Visible.NEXT_DAY)[-1].doy == 384

    # Likewise with the 0-day rule it is intercalary
    assert (
        festival_calendar(bce_as_negative(320), rule=Visible.CONJUNCTION)[-1].doy == 384
    )


@pytest.mark.skip(reason="probably remove this test")
def test_is_contained_in():
    assert heniautos._is_contained_in(
        (29, 29, 29, 29), (30, 30, 30, 29, 29, 29, 29, 29)
    ) == (30, 30, 30, 29)

    with pytest.raises(HeniautosNoMatchError):
        heniautos._is_contained_in(
            (29, 29, 29, 29), (30, 30, 30, 30, 30, 29, 29, 29)
        ) == (30, 30, 30, 29)

    with pytest.raises(HeniautosNoMatchError):
        heniautos._is_contained_in((29, 29, 29, 29), (29, 29, 29))


@pytest.mark.skip(reason="probably remove this test")
def test_each_overlaps():
    s = [
        (29, 29, 29, 29),
        (30, 30, 30, 29, 29, 29, 29, 29),
        (30, 30, 30, 30, 29, 29, 29, 29, 29),
    ]

    assert heniautos._each_overlaps(s) == ((29, 29, 29, 29), (30, 30, 30, 29), (30,))

    s = [
        (29, 29, 29, 29),
        (30, 30, 30, 29, 29, 29, 29, 29),
        (30, 30, 30, 30, 30, 29, 29, 29, 29),
    ]

    with pytest.raises(HeniautosNoMatchError):
        heniautos._each_overlaps(s) == ((29, 29, 29, 29), (30, 30, 30, 29), (30,))


@pytest.mark.skip(reason="probably remove this test")
def test_no_deintercalations():
    assert heniautos._no_deintercalations((False, False, False))
    assert heniautos._no_deintercalations((True, True, True))
    assert heniautos._no_deintercalations((False, True, True))
    assert heniautos._no_deintercalations((False, False, True))
    assert heniautos._no_deintercalations((True, False, True)) is False
    assert heniautos._no_deintercalations((True, True, False)) is False
    assert heniautos._no_deintercalations((True, False, False)) is False


@pytest.mark.xfail
def test_no_misaligned_intercalations():
    eq = equations(
        [(m, 14) for m in Months],
        [(p, 2) for p in Prytanies],
        year=bce_as_negative(336),
    )

    assert len(eq) == 19

    # Okay for festival intercalation to be False when conciliar
    # intercaltion is True
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (False, True)
    ) == 6

    # Okay for both to be the same
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (True, True)
    ) == 6
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (False, False)
    ) == 7

    # This must be 0. There cannot be festival intercalations
    # alongside an ordinary conciliar year
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (True, False)
    ) == 0


def test_collations():
    # Equation 1: Boe 11 = II 31
    eq1 = equations(
        (AthenianMonths.MAI, 11), (Prytanies.IV, 21), year=bce_as_negative(319)
    )

    eq2 = equations(
        (AthenianMonths.ELA, 12), (Prytanies.VII, 34), year=bce_as_negative(319)
    )

    eq3 = equations(
        (AthenianMonths.MOU, 12), (Prytanies.VIII, 29), year=bce_as_negative(319)
    )

    c = collations(eq1, eq2, eq3)
    assert len(c) == 8

    # Festival year partitions
    assert c[0]["partitions"]["festival"] == ((29, 29, 29, 29), (30, 30, 29, 29), (30,))

    assert c[0]["partitions"]["conciliar"] == ((36, 35, 35), (36, 35, 35), (35,))

    # Festival DOYs
    assert [e[0]["doy"] for e in c[0]["equations"]] == [127, 246, 276]

    # Conciliar DOYs
    assert [e[1]["doy"] for e in c[0]["equations"]] == [127, 246, 276]

    # Festival Intercalations
    assert [e[0]["intercalation"] for e in c[0]["equations"]] == [False, False, False]
    # Conciliar Intercalations
    assert [e[1]["intercalation"] for e in c[0]["equations"]] == [False, False, False]

    c = collations(eq1, eq2, eq3, failures=True)
    assert len(c) == 19
