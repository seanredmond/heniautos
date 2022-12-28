from heniautos import *
import pytest

# import skyfield

# from skyfield.api import load
# from skyfield.api import GREGORIAN_START


# TS = api.load.timescale()
# TS.julian_calendar_cutoff = GREGORIAN_START
# EPH = api.load('de422.bsp')


# init_data()


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
