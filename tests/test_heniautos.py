from heniautos import *
import pytest


def test_version():
    assert version() == "1.3.0"


def test_bce_as_negative():
    assert bce_as_negative(100) == -99


def test_negative_as_bce():
    assert negative_as_bce(-99) == 100


def test_is_bce():
    assert is_bce(1685074.3287422964)  # Summer Solstice 100 BCE


def test_as_julian():
    assert as_julian(1685074.3287423) == "BCE 0100-Jun-25"
    assert as_julian(1685074.3287423, True) == "BCE 0100-Jun-25 19:53:23 GMT"
    assert as_julian(1685439.56480925) == "BCE 0099-Jun-25"
    assert as_julian(1685074.3287422964, True) == "BCE 0100-Jun-25 19:53:23 GMT"

    fest = athenian_festival_calendar(-431)
    assert as_julian(fest[0].jdn) == "BCE 0432-Jul-16"
    assert as_julian(fest[0]) == as_julian(fest[0].jdn)


def test_as_alt():
    assert as_julian(1563092.61, True, TZOptions.ALT) == "BCE 0434-Jul-07 04:13:18 ALT"


def test_as_gregorian():
    sol1 = solar_event(-431, Seasons.SUMMER_SOLSTICE)
    assert as_julian(sol1) == "BCE 0432-Jun-28"
    assert as_gregorian(sol1) == "BCE 0432-Jun-23"

    # Should be the same after switch to Gregorian
    sol2 = solar_event(1950, Seasons.SUMMER_SOLSTICE)
    assert as_gregorian(sol2) == " CE 1950-Jun-21"
    assert as_julian(sol2) == as_gregorian(sol2)


def test_solar_event():
    assert (
        as_julian(solar_event(-99, Seasons.SPRING_EQUINOX), True)
        == "BCE 0100-Mar-23 19:48:34 GMT"
    )
    assert (
        as_julian(solar_event(-99, Seasons.SUMMER_SOLSTICE), True)
        == "BCE 0100-Jun-25 19:53:23 GMT"
    )
    assert (
        as_julian(solar_event(-99, Seasons.AUTUMN_EQUINOX), True)
        == "BCE 0100-Sep-26 04:52:22 GMT"
    )
    assert (
        as_julian(solar_event(-99, Seasons.WINTER_SOLSTICE), True)
        == "BCE 0100-Dec-23 20:37:06 GMT"
    )


def test_new_moons():
    p = new_moons(-99)
    assert type(p) is list
    assert as_julian(p[0], True) == "BCE 0100-Jan-09 12:44:44 GMT"


def test_calendar_months_after():
    p = heniautos._calendar_months(-100)
    assert type(p) is tuple
    assert len(p) == 12
    assert type(p[0]) is tuple
    assert len(p[0]) == 2
    assert as_julian(p[0][0], True) == "BCE 0101-Jul-16 12:00:00 GMT"
    assert p[0][1] == p[1][0]


def test_calendar_months_before():
    p = heniautos._calendar_months(-100, before_event=True)
    assert type(p) is tuple
    assert len(p) == 12
    assert type(p[0]) is tuple
    assert len(p[0]) == 2
    assert as_julian(p[0][0], True) == "BCE 0101-Jun-16 12:00:00 GMT"
    assert p[0][1] == p[1][0]


def test_calendar_months_athenian_424():
    """Make sure calendar_months generates the correct new moons for Athenian 424/423"""
    p = heniautos._calendar_months(-423)
    assert len(p) == 12
    assert as_julian(p[0][0]) == "BCE 0424-Jul-18"
    assert as_julian(p[-1][0]) == "BCE 0423-Jun-08"


def test_calendar_months_spartan_424():
    """Make sure calendar_months generates the correct new moons for Spartan 424/423"""
    p = heniautos._calendar_months(
        -423, event=Seasons.AUTUMN_EQUINOX, before_event=True
    )
    assert len(p) == 12
    assert as_julian(p[0][0]) == "BCE 0424-Sep-15"
    assert as_julian(p[-1][0]) == "BCE 0423-Aug-06"


def test_calendar_months_delian_424():
    """Make sure calendar_months generates the correct new moons for Delian 424/423"""
    p = heniautos._calendar_months(-423, event=Seasons.WINTER_SOLSTICE)
    assert len(p) == 12
    assert as_julian(p[0][0]) == "BCE 0423-Jan-11"
    assert as_julian(p[-1][0]) == "BCE 0423-Dec-01"


def test_generic_festival_calendar():
    p = festival_calendar(-100, calendar=None)
    assert len(p) == 354
    assert len(by_months(p)) == 12
    assert isinstance(p[0], FestivalDay)
    assert p[0].month is None
    assert p[0].month_name is None
    assert as_julian(p[0]) == "BCE 0101-Jul-16"
    assert as_julian(p[-1]) == "BCE 0100-Jul-04"


def test_generic_festival_calendar_athenian():
    # Athenian should be the default value
    p = festival_calendar(-100)
    assert len(by_months(p)) == 12
    assert p[0].month is AthenianMonths.HEK
    assert p[0].month_name == "Hekatombaiṓn"
    assert as_julian(p[0]) == "BCE 0101-Jul-16"

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
    assert as_julian(p[0]) == "BCE 0101-Jul-16"


def test_generic_festival_calendar_delian():
    p = festival_calendar(-100, calendar=Cal.DELIAN, event=Seasons.WINTER_SOLSTICE)
    assert as_julian(p[0]) == "BCE 0100-Jan-10"
    assert len(by_months(p)) == 12
    assert p[0].month is DelianMonths.LEN
    assert p[0].month_name == "Lēnaiṓn"

    # Intercalary year
    p = festival_calendar(-102, calendar=Cal.DELIAN, event=Seasons.WINTER_SOLSTICE)
    assert as_julian(p[0]) == "BCE 0102-Jan-02"
    p_months = by_months(p)
    assert len(p_months) == 13
    # By default, the 7th month should be intercalated
    assert p_months[6][0].month is Months.INT
    assert p_months[6][0].month_name == "Pánēmos hústeros"

    # Intercalate Hek instead
    p = festival_calendar(
        -102, intercalate=1, calendar=Cal.DELIAN, event=Seasons.WINTER_SOLSTICE
    )
    assert as_julian(p[0]) == "BCE 0102-Jan-02"
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
    assert as_julian(p[0]) == "BCE 0100-Jan-10"


def test_spartan_festival_calendar():
    p = spartan_festival_calendar(-100)
    assert len(by_months(p)) == 12
    assert p[0].month is SpartanMonths.UN1
    assert p[0].month_name == "Unknown 1"
    assert as_julian(p[0]) == "BCE 0101-Sep-13"

    p = spartan_festival_calendar(-102)
    assert len(by_months(p)) == 13
    assert as_julian(p[0]) == "BCE 0103-Sep-06"
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
    assert as_julian(p[0]) == "BCE 0101-Jul-16"
    assert p[0].doy == 1

    met = [d for d in p if d.month == AthenianMonths.MET]

    assert met[0].month_name == "Metageitniṓn"
    assert met[0].day == 1
    assert as_julian(met[0]) == "BCE 0101-Aug-15"
    assert met[0].doy == 31


def test_delian_festival_calendar_434_433():
    c = festival_calendar(-434, event=Seasons.WINTER_SOLSTICE)
    assert len(c) == 354
    c_months = by_months(c)
    assert len(c_months) == 12
    assert as_julian(c_months[0][0]) == "BCE 0434-Jan-13"
    assert as_julian(c_months[-1][0]) == "BCE 0434-Dec-03"

    c = festival_calendar(-433, event=Seasons.WINTER_SOLSTICE)
    assert len(c) == 384
    c_months = by_months(c)
    assert len(c_months) == 13
    assert as_julian(c_months[0][0]) == "BCE 0433-Jan-02"
    assert as_julian(c_months[-1][0]) == "BCE 0433-Dec-21"


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


def test_doy_to_julian():
    assert as_julian(doy_to_julian(256, bce_as_negative(332))) == "BCE 0331-Apr-01"

    assert (
        as_julian(doy_to_julian(256, bce_as_negative(332), rule=Visible.SECOND_DAY))
        == "BCE 0331-Apr-02"
    )
    assert (
        as_julian(doy_to_julian(256, bce_as_negative(332), rule=Visible.CONJUNCTION))
        == "BCE 0331-Mar-31"
    )


def test_festival_to_julian():
    assert (
        as_julian(festival_to_julian(bce_as_negative(332), AthenianMonths.ELA, 19))
        == "BCE 0331-Apr-01"
    )

    assert (
        as_julian(
            festival_to_julian(
                bce_as_negative(332), AthenianMonths.ELA, 19, rule=Visible.SECOND_DAY
            )
        )
        == "BCE 0331-Apr-02"
    )

    assert (
        as_julian(
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
    assert as_julian(cal_320[0]) == "BCE 0320-Jul-09"
    # and ends on Jun 27
    assert as_julian(cal_320[-1]) == "BCE 0319-Jun-27"

    months = dict(zip(Months, [[d for d in cal_320 if d.month == m] for m in Months]))

    assert [as_julian(d) for d in cal_320 if d.day == 1] == [
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


def test_to_jd():
    d = find_festival_date(-406, 1, 1)

    assert d.jdn == 1572957

    with pytest.raises(HeniautosDateNotFoundError) as e:
        find_festival_date(-406, 1, 30)


def test_name_as():
    assert athenian_festival_calendar(-406)[0].month_name == "Hekatombaiṓn"
    assert (
        athenian_festival_calendar(-406, name_as=MonthNameOptions.ABBREV)[0].month_name
        == "Hek"
    )
    assert (
        athenian_festival_calendar(-406, name_as=MonthNameOptions.GREEK)[0].month_name
        == "Ἑκατομβαιών"
    )

    assert (
        delphian_festival_calendar(-406, name_as=MonthNameOptions.GREEK)[0].month_name
        == "Ἀπελλαῖος"
    )
    assert (
        delian_festival_calendar(-406, name_as=MonthNameOptions.GREEK)[0].month_name
        == "Ληναιών"
    )
    assert (
        argive_festival_calendar(-406, name_as=MonthNameOptions.GREEK)[0].month_name
        == "Ἀγύειος"
    )
    assert (
        spartan_festival_calendar(-406, name_as=MonthNameOptions.GREEK)[0].month_name
        == "Unknown 1"
    )
    assert (
        corinthian_festival_calendar(-406, name_as=MonthNameOptions.GREEK)[0].month_name
        == "Φοινικαῖος"
    )


def test_find_jdn_with_year_hint():
    day = jdn_to_festival_day(1572957, -406)
    assert day.jdn == 1572957
    assert day.month == AthenianMonths.HEK
    assert day.day == 1


def test_find_jdn_without_year_hint():
    day = jdn_to_festival_day(1572957)
    assert day.jdn == 1572957
    assert day.month == AthenianMonths.HEK
    assert day.day == 1


def test_find_jdn_argos():
    day = jdn_to_festival_day(1572957, calendar=Cal.ARGIVE)
    assert day.jdn == 1572957
    assert day.month == ArgiveMonths.PAN
    assert day.day == 1


def test_julian_to_festival():
    d = julian_to_festival(-406, 7, 10)
    assert d.jdn == 1572957
    assert d.month == AthenianMonths.HEK
    assert d.day == 1


def test_gregorian_to_festival():
    d = gregorian_to_festival(-406, 7, 10)
    assert d.jdn == 1572962
    assert d.month == AthenianMonths.HEK
    assert d.day == 6


def test_festival_day():
    d = julian_to_festival(-406, 7, 10)
    assert d.jdn == 1572957
    assert d.month_name == "Hekatombaiṓn"
    assert d.month_index == 1
    assert d.month == AthenianMonths.HEK
    assert d.month_length == 29
    assert d.day == 1
    assert d.doy == 1
    assert d.year == "BCE 407/406"
    assert d.year_length == 355
    assert d.astronomical_year == -406


def test_jdn_to_festival_calendar():
    y = jdn_to_festival_calendar(1572957)

    assert y[0].year == "BCE 407/406"
    assert y[0].month == AthenianMonths.HEK
    assert y[0].day == 1
