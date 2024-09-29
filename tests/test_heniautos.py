from heniautos import *
import pytest


def test_version():
    assert version() == "2.2.0"


def test_bce_as_negative():
    assert bce_as_negative(100) == -99


def test_negative_as_bce():
    assert negative_as_bce(-99) == 100


def test_as_julian():
    assert as_julian(1685074.3287423) == "BCE 0100-Jun-25"
    assert as_julian(1685074.3287423, True) == "BCE 0100-Jun-25 19:53:23 GMT"
    assert as_julian(1685439.56480925) == "BCE 0099-Jun-26"
    assert as_julian(1685074.3287422964, True) == "BCE 0100-Jun-25 19:53:23 GMT"

    fest = athenian_festival_calendar(-431)
    assert as_julian(fest[0].jdn) == "BCE 0432-Jul-16"
    assert as_julian(fest[0]) == as_julian(fest[0].jdn)


def test_as_alt():
    assert as_julian(1563092.61, True, TZOptions.ALT) == "BCE 0434-Jul-08 04:13:18 ALT"


def test_as_julian_longitude():
    assert as_julian(1685074.3287423, True) == "BCE 0100-Jun-25 19:53:23 GMT"

    # Time in Babylon
    assert as_julian(1685074.3287423, True, tz=44.421111) == "BCE 0100-Jun-25 22:51:04    "


def test_tz_offset():
    assert tz_offset(1685074.3287423, TZOptions.ALT) == 1685074.3946535666

    # Time in Babylon
    assert tz_offset(1685074.3287423, 44.421111) == 1685074.4521342749

    # GMT, no change
    assert tz_offset(1685074.3287423, TZOptions.GMT) == 1685074.3287423
    

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
        == "BCE 0100-Mar-23 16:36:11 GMT"
    )
    assert (
        as_julian(solar_event(-99, Seasons.SUMMER_SOLSTICE), True)
        == "BCE 0100-Jun-25 16:41:03 GMT"
    )
    assert (
        as_julian(solar_event(-99, Seasons.AUTUMN_EQUINOX), True)
        == "BCE 0100-Sep-26 01:40:05 GMT"
    )
    assert (
        as_julian(solar_event(-99, Seasons.WINTER_SOLSTICE), True)
        == "BCE 0100-Dec-23 17:24:52 GMT"
    )


def test_observed_solar_event():
    assert (
        as_julian(observed_solar_event(-99, Seasons.SPRING_EQUINOX), True)
        == "BCE 0100-Mar-23 12:00:00 GMT"
    )
    assert (
        as_julian(observed_solar_event(-99, Seasons.SUMMER_SOLSTICE), True)
        == "BCE 0100-Jun-25 12:00:00 GMT"
    )
    assert (
        as_julian(observed_solar_event(-99, Seasons.AUTUMN_EQUINOX), True)
        == "BCE 0100-Sep-26 12:00:00 GMT"
    )
    assert (
        as_julian(observed_solar_event(-99, Seasons.WINTER_SOLSTICE), True)
        == "BCE 0100-Dec-23 12:00:00 GMT"
    )
    

def test_observed_solar_event_offset():
    assert (
        as_julian(observed_solar_event(-99, Seasons.SPRING_EQUINOX, s_off=0), True)
        == "BCE 0100-Mar-23 12:00:00 GMT"
    )

    assert (
        as_julian(observed_solar_event(-99, Seasons.SPRING_EQUINOX, s_off=-1), True)
        == "BCE 0100-Mar-22 12:00:00 GMT"
    )

    assert (
        as_julian(observed_solar_event(-99, Seasons.SPRING_EQUINOX, s_off=1), True)
        == "BCE 0100-Mar-24 12:00:00 GMT"
    )
    

def test_new_moons():
    p = new_moons(-99)
    assert type(p) is tuple
    assert as_julian(p[0], True) == "BCE 0100-Jan-09 09:31:53 GMT"


def test_generic_festival_calendar():
    p = festival_calendar(-100, calendar=None)
    assert len(p) == 354
    assert len(by_months(p)) == 12
    assert isinstance(p[0], FestivalDay)
    assert p[0].month is None
    assert p[0].month_name is None
    assert as_julian(p[0]) == "BCE 0101-Jul-16"
    assert as_julian(p[-1]) == "BCE 0100-Jul-04"

    p = festival_calendar(-101)
    p_months = by_months(p)
    assert len(p_months) == 13
    # By default, the 7th month should be intercalated
    assert p_months[6][0].month is Months.INT
    assert p_months[6][0].month_name == "6 hústeros"

    p = festival_calendar(-101, intercalate=1)
    p_months = by_months(p)
    assert p_months[1][0].month is Months.INT
    assert p_months[1][0].month_name == "1 hústeros"
    assert p_months[6][0].month is GenericMonths.M06
    assert p_months[6][0].month_name == "6"


    p = festival_calendar(-101, intercalate=1, name_as=MonthNameOptions.GREEK)
    p_months = by_months(p)
    assert p_months[1][0].month_name == "Πρῶτος ὕστερος"
    assert p_months[6][0].month_name == "Ἕκτος"

    p = festival_calendar(-101, intercalate=1, name_as=MonthNameOptions.ABBREV)
    p_months = by_months(p)
    assert p_months[1][0].month_name == "1₂"
    assert p_months[6][0].month_name == "6"


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
    assert p[0].month is GenericMonths.M01
    assert p[0].month_name == "1"
    assert as_julian(p[0]) == "BCE 0101-Sep-13"

    p = spartan_festival_calendar(-102)
    assert len(by_months(p)) == 13
    assert as_julian(p[0]) == "BCE 0103-Sep-06"
    p_months = by_months(p)
    assert p_months[6][0].month is Months.INT
    assert p_months[6][0].month_name == "6 hústeros"


def test_festival_calendar():
    p = festival_calendar(-100)

    assert type(p) is tuple

    assert type(p[0]) is FestivalDay
    assert p[0].month_name == "1"
    assert p[0].month is GenericMonths.M01
    assert p[0].day == 1
    assert as_julian(p[0]) == "BCE 0101-Jul-16"
    assert p[0].doy == 1

    met = [d for d in p if d.month is GenericMonths.M02]

    assert met[0].month_name == "2"
    assert met[0].day == 1
    assert as_julian(met[0]) == "BCE 0101-Aug-14"
    assert met[0].doy == 30


def test_festival_calendar_solar_offset():
    p = festival_calendar(-421)
    assert as_julian(p[0]) == "BCE 0422-Jul-26"

    p = festival_calendar(-421, s_off=-3)
    assert as_julian(p[0]) == "BCE 0422-Jun-26"



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


def test_festival_to_julian_athenian():
    assert (
        as_julian(festival_to_jdn(bce_as_negative(332), AthenianMonths.ELA, 19))
        == "BCE 0331-Apr-01"
    )

    assert (
        as_julian(
            festival_to_jdn(
                bce_as_negative(332), AthenianMonths.ELA, 19, v_off=2
            )
        )
        == "BCE 0331-Apr-02"
    )

    assert (
        as_julian(
            festival_to_jdn(
                bce_as_negative(332), AthenianMonths.ELA, 19, v_off=0
            )
        )
        == "BCE 0331-Mar-31"
    )


def test_festival_to_julian_other_calendars():
    assert (
        as_julian(
            festival_to_jdn(
                bce_as_negative(332),
                CorinthianMonths.GAM,
                19,
                calendar=Cal.CORINTHIAN,
                event=Seasons.AUTUMN_EQUINOX,
                before_event=True,
            )
        )
        == "BCE 0331-May-29"
    )

    assert (
        as_julian(
            festival_to_jdn(
                bce_as_negative(332),
                DelianMonths.BOU,
                19,
                v_off=2,
                calendar=Cal.DELIAN,
                event=Seasons.WINTER_SOLSTICE,
            )
        )
        == "BCE 0331-Sep-26"
    )


def test_festival_to_julian_intercalation():
    assert (
        as_julian(festival_to_jdn(bce_as_negative(320), AthenianMonths.ELA, 19))
        == "BCE 0319-Apr-18"
    )

    assert (
        as_julian(
            festival_to_jdn(bce_as_negative(320), AthenianMonths.ELA, 19, intercalate=6)
        )
        == "BCE 0319-Apr-18"
    )

    assert (
        as_julian(
            festival_to_jdn(bce_as_negative(320), AthenianMonths.ELA, 19, intercalate=1)
        )
        == "BCE 0319-Apr-18"
    )

    assert (
        as_julian(
            festival_to_jdn(
                bce_as_negative(320), AthenianMonths.ELA, 19, intercalate=12
            )
        )
        == "BCE 0319-Mar-20"
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

    assert "100" in str(e1)

    with pytest.raises(HeniautosNoDataError) as e2:
        new_moons(-999)

    assert "-999" in str(e2)


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

    cal_320 = festival_calendar(bce_as_negative(320), v_off=2)

    # With the two day rule, 320 is ordinary
    assert cal_320[-1].doy == 355

    # It starts on Jul 8
    assert as_julian(cal_320[0]) == "BCE 0320-Jul-08"
    # and ends on Jun 27
    assert as_julian(cal_320[-1]) == "BCE 0319-Jun-27"

    months = dict(zip(Months, [[d for d in cal_320 if d.month == m] for m in Months]))

    assert [as_julian(d) for d in cal_320 if d.day == 1] == [
        "BCE 0320-Jul-08",
        "BCE 0320-Aug-07",
        "BCE 0320-Sep-05",
        "BCE 0320-Oct-05",
        "BCE 0320-Nov-04",
        "BCE 0320-Dec-03",
        "BCE 0319-Jan-02",
        "BCE 0319-Feb-01",
        "BCE 0319-Mar-03",
        "BCE 0319-Apr-01",
        "BCE 0319-May-01",
        "BCE 0319-May-30",
    ]

    # With the 1-day rule it is intercalary
    assert festival_calendar(bce_as_negative(320), v_off=1)[-1].doy == 384

    # Likewise with the 0-day rule it is intercalary
    assert (
        festival_calendar(bce_as_negative(320), v_off=0)[-1].doy == 384
    )


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
        == "δεῖνα αʹ"
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


def test_to_jd():
    # From test for removed find_festival_date()
    d = festival_to_jdn(-406, 1, 1)

    assert d == 1572957

    with pytest.raises(HeniautosNoDayInYearError) as e:
        festival_to_jdn(-406, 1, 30)


def test_julian_to_festival_day():
    d = julian_to_festival_day(-406, 7, 10)
    assert d.jdn == 1572957
    assert d.month == AthenianMonths.HEK
    assert d.day == 1


def test_gregorian_to_festival_day():
    d = gregorian_to_festival_day(-406, 7, 10)
    assert d.jdn == 1572962
    assert d.month == AthenianMonths.HEK
    assert d.day == 6


def test_festival_day_day():
    d = julian_to_festival_day(-406, 7, 10)
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


def test_month_name():
    assert month_name(AthenianMonths.GAM) == "Gamēliṓn"
    assert (
        month_name(AthenianMonths.GAM, MonthNameOptions.TRANSLITERATION) == "Gamēliṓn"
    )
    assert month_name(AthenianMonths.GAM, MonthNameOptions.ABBREV) == "Gam"
    assert month_name(AthenianMonths.GAM, MonthNameOptions.GREEK) == "Γαμηλιών"

    with pytest.raises(HeniautosError):
        assert month_name(Months.UNC)

def test_octaeteris():
    oct = octaeteris(1, -432, -423, calendar=Cal.ATHENIAN)
    assert len(oct) == 10
    assert [len(y) < 356 for y in oct] == [True, True, False, True, False, True, True, False, True, True]

    oct = octaeteris(3, -432, -423, calendar=Cal.ATHENIAN)
    assert [len(y) < 356 for y in oct] == [False, True, False, True, True, False, True, True, False, True]

def test_octaeteris_rollover():
    oct = octaeteris(9, -432, -423, calendar=Cal.ATHENIAN)
    assert len(oct) == 10
    assert [len(y) < 356 for y in oct] == [True, True, False, True, False, True, True, False, True, True]
    
