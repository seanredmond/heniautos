from heniautos import *
from heniautos.prytanies import *
import pytest

# Year to test prytany lengths
O_SO = 424  # 354 days, quasi-solar prytanies
O_SO_LONG = 426  # 355 days, quasi-solar prytanies
I_SO = 425  # 384 days, quasi-solar prytanies
O_10 = 369  # 354 days, 10 prytanies
O_10_LONG = 367  # 355 days, 10 prytanies
I_10 = 363  # 384 days, 10 prytanies
O_12 = 291  # 354 days, 12 prytanies
O_12_LONG = 293  # 355 days, 12 prytanies
I_12 = 301  # 384 days, 12 prytanies
O_13 = 209  # 354 days, 13 prytanies
O_13_LONG = 207  # 355 days, 13 prytanies
I_13 = 214  # 384 days, 13 prytanies


def span(a, b):
    return b - a


def test_prytany_label():
    assert prytany_label(Prytanies.I) == "I"
    assert prytany_label(Prytanies.X) == "X"


# def test_pryt_len():
#     d = prytanies._pryt_len(36)
#     assert next(d) == 36
#     assert next(d) == 36
#     assert next(d) == 36
#     assert next(d) == 36
#     assert next(d) == 35
#     assert next(d) == 35

#     e = heniautos.prytanies._pryt_len(39)
#     assert next(e) == 39
#     assert next(e) == 39
#     assert next(e) == 39
#     assert next(e) == 39
#     assert next(e) == 38
#     assert next(e) == 38

#     e = heniautos.prytanies._pryt_len(30, 6)
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 29

#     e = heniautos.prytanies._pryt_len(30, 6)
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 30
#     assert next(e) == 29

#     e = heniautos.prytanies._pryt_len(33, 0)
#     assert next(e) == 32
#     assert next(e) == 32
#     assert next(e) == 32
#     assert next(e) == 32
#     assert next(e) == 32
#     assert next(e) == 32
#     assert next(e) == 32


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


def test_prytany_type():
    
    with pytest.raises(HeniautosError):
        prytany_type(bce_as_negative(509))

    assert prytany_type(bce_as_negative(508)) == Prytany.QUASI_SOLAR
    assert prytany_type(bce_as_negative(410)) == Prytany.QUASI_SOLAR

    assert prytany_type(bce_as_negative(360)) == Prytany.ALIGNED_10
    assert prytany_type(bce_as_negative(308)) == Prytany.ALIGNED_10

    assert prytany_type(bce_as_negative(307)) == Prytany.ALIGNED_12
    assert prytany_type(bce_as_negative(224)) == Prytany.ALIGNED_12

    assert prytany_type(bce_as_negative(223)) == Prytany.ALIGNED_13
    assert prytany_type(bce_as_negative(201)) == Prytany.ALIGNED_13

    assert prytany_type(bce_as_negative(200)) == Prytany.ALIGNED_12
    assert prytany_type(bce_as_negative(101)) == Prytany.ALIGNED_12

    assert prytany_type(bce_as_negative(100)) == Prytany.ALIGNED_10
    assert prytany_type(2021) == Prytany.ALIGNED_10

    # Confirm constants for other tests
    assert prytany_type(bce_as_negative(O_SO)) == Prytany.QUASI_SOLAR
    assert (
        prytany_type(bce_as_negative(O_SO_LONG))
        == Prytany.QUASI_SOLAR
    )
    assert prytany_type(bce_as_negative(I_SO)) == Prytany.QUASI_SOLAR

    assert prytany_type(bce_as_negative(O_10)) == Prytany.ALIGNED_10
    assert (
        prytany_type(bce_as_negative(O_10_LONG)) == Prytany.ALIGNED_10
    )
    assert prytany_type(bce_as_negative(I_10)) == Prytany.ALIGNED_10

    assert prytany_type(bce_as_negative(O_12)) == Prytany.ALIGNED_12
    assert (
        prytany_type(bce_as_negative(O_12_LONG)) == Prytany.ALIGNED_12
    )
    assert prytany_type(bce_as_negative(I_12)) == Prytany.ALIGNED_12

    assert prytany_type(bce_as_negative(O_13)) == Prytany.ALIGNED_13
    assert (
        prytany_type(bce_as_negative(O_13_LONG)) == Prytany.ALIGNED_13
    )
    assert prytany_type(bce_as_negative(I_13)) == Prytany.ALIGNED_13


# def test_pryt_auto_start():
#     # Should return Julian dates from rounded Terrestrial Time

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(500), Prytany.AUTO)
#         )
#         == "BCE 0500-May-01"
#     )

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(425), Prytany.AUTO)
#         )
#         == "BCE 0425-Jun-26"
#     )

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(429), Prytany.AUTO)
#         )
#         == "BCE 0429-Jun-23"
#     )

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(424), Prytany.AUTO)
#         )
#         == "BCE 0424-Jun-27"
#     )

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(421), Prytany.AUTO)
#         )
#         == "BCE 0421-Jun-29"
#     )

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(420), Prytany.AUTO)
#         )
#         == "BCE 0420-Jun-30"
#     )

#     assert (
#         as_julian(
#             prytany_type_start(bce_as_negative(419), Prytany.AUTO)
#         )
#         == "BCE 0419-Jul-01"
#     )


# def test_pryt_solar_end():
#     # One quasi-solar year should end at the next quasi solar year
#     year_start = prytany_type_start(
#         bce_as_negative(426), Prytany.AUTO
#     )
#     year_end = heniautos.prytanies._pryt_solar_end(year_start)
#     next_year = prytany_type_start(bce_as_negative(425), Prytany.AUTO)
#     assert year_end == next_year


def test_prytany_calendar_408():
    p = by_prytanies(prytany_calendar(-407))
    assert as_julian(p[0][0].jdn) == "BCE 0408-Jul-09"
    assert as_julian(p[-1][-1].jdn) == "BCE 0407-Jul-09"


def test_prytany_calendar_solar():
    p = by_prytanies(prytany_calendar(-420))

    assert len(p) == 10
    assert p[0][0].prytany_index == 1
    assert as_julian(p[0][0].jdn) == "BCE 0421-Jun-29"
    assert len(p[0]) == 37

    assert p[-1][-1].prytany_index == 10
    assert as_julian(p[-1][-1].jdn) == "BCE 0420-Jun-29"
    assert len(p[-1]) == 36
    assert p[-1][-1].doy == 366

    p2 = prytany_calendar(bce_as_negative(429))
    assert as_julian(p2[0].jdn) == "BCE 0429-Jun-23"


def test_prytany_calendar_solar_rule():
    assert prytany_calendar(-420)[0].jdn == 1567833
    assert prytany_calendar(-420, v_off=0)[0].jdn == 1567832
    assert prytany_calendar(-420, v_off=2)[0].jdn == 1567834


def test_prytany_calendar_solar_supplied_jdn():
    assert prytany_calendar(-420)[0].jdn == 1567833
    assert prytany_calendar(-420, pryt_start=1572952)[0].jdn == 1567828
    assert prytany_calendar(-420, pryt_start=1572962)[0].jdn == 1567838


def test_prytany_calendar_solar_leap():
    p = by_prytanies(prytany_calendar(-417))

    assert len(p) == 10
    assert p[0][0].prytany_index == 1
    assert as_julian(p[0][0].jdn) == "BCE 0418-Jul-02"
    assert len(p[0]) == 37

    assert p[-1][-1].prytany_index == 10
    assert as_julian(p[-1][-1].jdn) == "BCE 0417-Jul-01"
    assert len(p[-1]) == 36
    assert p[-1][-1].doy == 366


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
    assert p3[-1][-1].doy == 354

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 36
    assert len(p3[4]) == 35
    assert len(p3[-1]) == 35


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
    assert len(p3[-2]) == 29
    assert len(p3[-1]) == 30


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
    assert p3[-1][-1].doy == 354

    assert p3[0][0].prytany == 1
    assert p3[-1][-1].jdn == c3[-1][-1].jdn

    assert len(p3[0]) == 28
    assert len(p3[3]) == 27
    assert len(p3[-1]) == 27


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
    assert len(p3[0]) == 29
    assert len(p3[1]) == 30
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


def test_prytany_to_julian():
    assert (
        as_julian(prytany_to_julian(bce_as_negative(332), Prytanies.VIII, 7).jdn)
        == "BCE 0331-Apr-01"
    )

    assert (
        as_julian(
            prytany_to_julian(
                bce_as_negative(332), Prytanies.VIII, 7, v_off=2
            ).jdn
        )
        == "BCE 0331-Apr-02"
    )

    assert (
        as_julian(
            prytany_to_julian(
                bce_as_negative(332), Prytanies.VIII, 7, v_off=0
            ).jdn
        )
        == "BCE 0331-Mar-31"
    )

    with pytest.raises(HeniautosNoDayInYearError):
        assert (
            as_julian(
                prytany_to_julian(
                    bce_as_negative(332), Prytanies.VIII, 39, v_off=0
                ).jdn
            )
            == "BCE 0331-Mar-31"
        )


def test_jdn_to_prytany_with_year_hint():
    day = jdn_to_prytany_day(1572957, -406)
    assert day.jdn == 1572957
    assert day.prytany == Prytanies.I
    assert day.day == 1
    assert day.year == "BCE 407/406"


def test_jdn_to_prytany_without_year_hint():
    day = jdn_to_prytany_day(1572957)
    assert day.jdn == 1572957
    assert day.prytany == Prytanies.I
    assert day.day == 1
    assert day.year == "BCE 407/406"


def test_julian_to_prytany():
    d = julian_to_prytany_day(-406, 7, 10)
    assert d.jdn == 1572957
    assert d.prytany == Prytanies.I
    assert d.day == 1


def test_gregorian_to_prytany():
    d = gregorian_to_prytany_day(-406, 7, 10)
    assert d.jdn == 1572962
    assert d.prytany == Prytanies.I
    assert d.day == 6


def test_prytany_day():
    d = julian_to_prytany_day(-406, 7, 10)
    assert d.jdn == 1572957
    assert d.prytany_index == 1
    assert d.prytany == Prytanies.I
    assert d.prytany_length == 37
    assert d.day == 1
    assert d.doy == 1
    assert d.year == "BCE 407/406"
    assert d.year_length == 366
    assert d.astronomical_year == -406
