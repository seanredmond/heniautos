from heniautos import *
from heniautos.prytanies import *
import pytest

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


def span(a, b):
    return b - a


def test_prytany_label():
    assert prytany_label(Prytanies.I) == "I"
    assert prytany_label(Prytanies.X) == "X"


def test_pryt_len():
    d = heniautos.prytanies._pryt_len(36)
    assert next(d) == 36
    assert next(d) == 36
    assert next(d) == 36
    assert next(d) == 36
    assert next(d) == 35
    assert next(d) == 35

    e = heniautos.prytanies._pryt_len(39)
    assert next(e) == 39
    assert next(e) == 39
    assert next(e) == 39
    assert next(e) == 39
    assert next(e) == 38
    assert next(e) == 38

    e = heniautos.prytanies._pryt_len(30, 6)
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 29

    e = heniautos.prytanies._pryt_len(30, 6)
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 30
    assert next(e) == 29

    e = heniautos.prytanies._pryt_len(33, 0)
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32
    assert next(e) == 32


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
    assert sum([q["end"] - q["start"] for q in p]) == 366

    assert p[0]["end"] - p[0]["start"] == 37
    assert p[4]["end"] - p[4]["start"] == 37
    assert p[4]["start"] == 1567981
    assert p[6]["end"] - p[6]["start"] == 36
    assert p[-1]["start"] == 1568163
    assert p[-1]["end"] - p[-1]["start"] == 36


def test_prytanies_solar_leap():
    p = prytanies(-417)
    assert len(p) == 10
    assert sum([q["end"] - q["start"] for q in p]) == 366
    assert p[0]["end"] - p[0]["start"] == 37
    assert p[4]["end"] - p[4]["start"] == 37
    assert p[6]["end"] - p[6]["start"] == 36
    assert p[-1]["end"] - p[-1]["start"] == 36


def test_prytanies_10_ordinary_long():
    c2 = festival_calendar(O_10_LONG)
    p2 = prytanies(O_10_LONG)
    assert len(p2) == 10
    assert sum([span(q["start"], q["end"]) for q in p2]) == 355

    assert p2[0]["prytany"] == 1
    assert as_julian(p2[0]["start"]) == as_julian(c2[0]["start"])
    assert as_julian(p2[-1]["end"]) == as_julian(c2[-1]["end"])

    assert span(p2[0]["start"], p2[0]["end"]) == 36
    assert span(p2[4]["start"], p2[4]["end"]) == 35
    assert span(p2[-1]["start"], p2[-1]["end"]) == 36


def test_prytany_auto():
    with pytest.raises(HeniautosError):
        heniautos.prytanies._pryt_auto(bce_as_negative(509))

    assert heniautos.prytanies._pryt_auto(bce_as_negative(508)) == Prytany.QUASI_SOLAR
    assert heniautos.prytanies._pryt_auto(bce_as_negative(410)) == Prytany.QUASI_SOLAR

    assert heniautos.prytanies._pryt_auto(bce_as_negative(402)) == Prytany.ALIGNED_10
    assert heniautos.prytanies._pryt_auto(bce_as_negative(308)) == Prytany.ALIGNED_10

    assert heniautos.prytanies._pryt_auto(bce_as_negative(307)) == Prytany.ALIGNED_12
    assert heniautos.prytanies._pryt_auto(bce_as_negative(224)) == Prytany.ALIGNED_12

    assert heniautos.prytanies._pryt_auto(bce_as_negative(223)) == Prytany.ALIGNED_13
    assert heniautos.prytanies._pryt_auto(bce_as_negative(201)) == Prytany.ALIGNED_13

    assert heniautos.prytanies._pryt_auto(bce_as_negative(200)) == Prytany.ALIGNED_12
    assert heniautos.prytanies._pryt_auto(bce_as_negative(101)) == Prytany.ALIGNED_12

    assert heniautos.prytanies._pryt_auto(bce_as_negative(100)) == Prytany.ALIGNED_10
    assert heniautos.prytanies._pryt_auto(2021) == Prytany.ALIGNED_10

    # Confirm constants for other tests
    assert heniautos.prytanies._pryt_auto(bce_as_negative(O_SO)) == Prytany.QUASI_SOLAR
    assert (
        heniautos.prytanies._pryt_auto(bce_as_negative(O_SO_LONG))
        == Prytany.QUASI_SOLAR
    )
    assert heniautos.prytanies._pryt_auto(bce_as_negative(I_SO)) == Prytany.QUASI_SOLAR

    assert heniautos.prytanies._pryt_auto(bce_as_negative(O_10)) == Prytany.ALIGNED_10
    assert (
        heniautos.prytanies._pryt_auto(bce_as_negative(O_10_LONG)) == Prytany.ALIGNED_10
    )
    assert heniautos.prytanies._pryt_auto(bce_as_negative(I_10)) == Prytany.ALIGNED_10

    assert heniautos.prytanies._pryt_auto(bce_as_negative(O_12)) == Prytany.ALIGNED_12
    assert (
        heniautos.prytanies._pryt_auto(bce_as_negative(O_12_LONG)) == Prytany.ALIGNED_12
    )
    assert heniautos.prytanies._pryt_auto(bce_as_negative(I_12)) == Prytany.ALIGNED_12

    assert heniautos.prytanies._pryt_auto(bce_as_negative(O_13)) == Prytany.ALIGNED_13
    assert (
        heniautos.prytanies._pryt_auto(bce_as_negative(O_13_LONG)) == Prytany.ALIGNED_13
    )
    assert heniautos.prytanies._pryt_auto(bce_as_negative(I_13)) == Prytany.ALIGNED_13


def test_pryt_auto_start():
    # Should return Julian dates from rounded Terrestrial Time

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(500), Prytany.AUTO))
        == "BCE 0500-May-01"
    )

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(425), Prytany.AUTO))
        == "BCE 0425-Jun-26"
    )

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(429), Prytany.AUTO))
        == "BCE 0429-Jun-23"
    )

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(424), Prytany.AUTO))
        == "BCE 0424-Jun-27"
    )

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(421), Prytany.AUTO))
        == "BCE 0421-Jun-29"
    )

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(420), Prytany.AUTO))
        == "BCE 0420-Jun-30"
    )

    assert (
        as_julian(heniautos.prytanies._pryt_auto_start(bce_as_negative(419), Prytany.AUTO))
        == "BCE 0419-Jul-01"
    )


def test_pryt_solar_end():
    # One quasi-solar year should end at the next quasi solar year
    year_start = heniautos.prytanies._pryt_auto_start(
        bce_as_negative(426), Prytany.AUTO
    )
    year_end = heniautos.prytanies._pryt_solar_end(year_start)
    next_year = heniautos.prytanies._pryt_auto_start(bce_as_negative(425), Prytany.AUTO)
    assert year_end == next_year


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
    assert prytany_calendar(-420, rule=Visible.CONJUNCTION)[0].jdn == 1567832
    assert prytany_calendar(-420, rule=Visible.SECOND_DAY)[0].jdn == 1567834


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


# Ten prytanies: 409-308 BCE


def test_prytanies_10_ordinary():
    year = bce_as_negative(O_10)
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 10 prytanies in 354 days
    assert len(p3) == 10
    assert len(c3) == 354
    assert sum([q["end"] - q["start"] for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

    # 354 day year. I-IV should be 36 days, the rest 35
    assert p3[0]["end"] - p3[0]["start"] == 36
    assert p3[4]["end"] - p3[4]["start"] == 35
    assert p3[-1]["end"] - p3[-1]["start"] == 35


def test_prytanies_10_ordinary_long():
    year = bce_as_negative(O_10_LONG)
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 10 prytanies in 355 days
    assert len(p3) == 10
    assert sum([q["end"] - q["start"] for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

    # 355 day year. I-IV should be 36 days, the rest 35
    # except the last has the 355th day added, so it is 36 days
    assert span(p3[0]["start"], p3[0]["end"]) == 36
    assert span(p3[4]["start"], p3[4]["end"]) == 35
    assert span(p3[-1]["start"], p3[-1]["end"]) == 36


def test_prytanies_10_intercalated():
    year = bce_as_negative(I_10)
    c = festival_calendar(year)
    p = prytanies(year)

    # 10 prytanies in 384 days
    assert len(p) == 10
    assert sum([q["end"] - q["start"] for q in p]) == 384

    assert p[0]["prytany"] == 1
    assert p[0]["start"] == c[0].jdn
    assert p[-1]["end"] - 1 == c[-1].jdn

    # 384 day year. I-IV should by 39 days, the rest 38
    assert span(p[0]["start"], p[0]["end"]) == 39
    assert span(p[4]["start"], p[4]["end"]) == 38
    assert span(p[-1]["start"], p[-1]["end"]) == 38


# Twelve prytanies: 307-224 BCE & 200-101 BCE


def test_prytanies_12_ordinary():
    year = bce_as_negative(O_12)
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 12 prytanies in 354 days
    assert len(p3) == 12
    assert sum([q["end"] - q["start"] for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

    # Like the festival calendar, prytanies are 29 or 30 days
    assert span(p3[0]["start"], p3[0]["end"]) == 29
    assert span(p3[1]["start"], p3[1]["end"]) == 29
    assert span(p3[2]["start"], p3[2]["end"]) == 30
    assert span(p3[-2]["start"], p3[-2]["end"]) == 30
    assert span(p3[-1]["start"], p3[-1]["end"]) == 29


def test_prytanies_12_ordinary_aristotle():
    year = bce_as_negative(O_12)
    c3 = festival_calendar(year)
    p3 = prytanies(year, rule_of_aristotle=True)

    # 12 prytanies in 354 days
    assert len(p3) == 12
    assert sum([q["end"] - q["start"] for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

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
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 12 prtyanies in 355 days
    assert len(p3) == 12
    assert sum([q["end"] - q["start"] for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

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
    c3 = festival_calendar(year)
    p3 = prytanies(year, rule_of_aristotle=True)
    assert len(p3) == 12
    assert sum([q["end"] - q["start"] for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

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
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # Twelve prytanies in 385 days
    assert len(p3) == 12
    assert sum([q["end"] - q["start"] for q in p3]) == 384

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

    # All prytanies are 32 days long
    all([(q["end"] - q["start"]) == 32 for q in p3])


# Thirteen prytanies: 223-201 BCE


def test_prytanies_13_ordinary():
    year = bce_as_negative(O_13)
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 13 prytanies in 354 days
    assert len(p3) == 13
    assert sum([q["end"] - q["start"] for q in p3]) == 354

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

    # Prytanies I-III 28 days long, the rest 27 days
    assert span(p3[0]["start"], p3[0]["end"]) == 28
    assert span(p3[3]["start"], p3[3]["end"]) == 27
    assert span(p3[-1]["start"], p3[-1]["end"]) == 27


def test_prytanies_13_long():
    year = bce_as_negative(O_13_LONG)
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 13 prytanies in 355 days
    assert len(p3) == 13
    assert sum([q["end"] - q["start"] for q in p3]) == 355

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

    # Prytanies I-III 28 days long, the rest 27 days except for the last
    # prytany which as 29 days long since it has the extra 355th day added
    assert span(p3[0]["start"], p3[0]["end"]) == 28
    assert span(p3[3]["start"], p3[3]["end"]) == 27
    assert span(p3[-1]["start"], p3[-1]["end"]) == 28


def test_prytanies_13_intercalated():
    year = bce_as_negative(I_13)
    c3 = festival_calendar(year)
    p3 = prytanies(year)

    # 13 prytanies in 384 days
    assert len(p3) == 13
    assert sum([q["end"] - q["start"] for q in p3]) == 384

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

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
    c3 = festival_calendar(year)
    p3 = prytanies(year, rule_of_aristotle=True)

    # 13 prytanies in 384 days
    assert len(p3) == 13
    assert sum([q["end"] - q["start"] for q in p3]) == 384

    assert p3[0]["prytany"] == 1
    assert p3[0]["start"] == c3[0].jdn
    assert p3[-1]["end"] - 1 == c3[-1].jdn

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


def test_prytany_to_julian():
    assert (
        as_julian(prytany_to_julian(bce_as_negative(332), Prytanies.VIII, 7).jdn)
        == "BCE 0331-Apr-01"
    )

    assert (
        as_julian(
            prytany_to_julian(
                bce_as_negative(332), Prytanies.VIII, 7, rule=Visible.SECOND_DAY
            ).jdn
        )
        == "BCE 0331-Apr-02"
    )

    assert (
        as_julian(
            prytany_to_julian(
                bce_as_negative(332), Prytanies.VIII, 7, rule=Visible.CONJUNCTION
            ).jdn
        )
        == "BCE 0331-Mar-31"
    )

    with pytest.raises(HeniautionNoDayInYearError):
        assert (
            as_julian(
                prytany_to_julian(
                    bce_as_negative(332), Prytanies.VIII, 39, rule=Visible.CONJUNCTION
                ).jdn
            )
            == "BCE 0331-Mar-31"
        )
