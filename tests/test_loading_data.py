from heniautos import *
import pytest

CUSTOM_YEAR = {
    "solstices": (
        (1685074, 1685074.3287422964, 1),
        (1685439, 1685439.5648092534, 1),
    ),
    "new_moons": (
        (1684907, 1684907.0310656228, 0),
        (1684936, 1684936.490878384, 0),
        (1684965, 1684965.8702085295, 0),
        (1685291, 1685291.0009266976, 0),
        (1685320, 1685320.5018709311, 1),
        (1685349, 1685349.9050228074, 0),
    ),
}


def test_solar_event_data_param():
    assert solar_event(-99, Seasons.SUMMER_SOLSTICE) == 1685074.3287422964
    assert (
        solar_event(
            -99,
            Seasons.SUMMER_SOLSTICE,
            data={"solstices": ((1685074, 1685074.12345, 1),)},
        )
        == 1685074.12345
    )

    with pytest.raises(HeniautosNoDataError):
        solar_event(-99, Seasons.SUMMER_SOLSTICE, data={"solstices": ()})


def test_summer_solstice_data_param():
    assert summer_solstice(-99) == 1685074.3287422964
    assert (
        summer_solstice(-99, data={"solstices": ((1685074, 1685074.12345, 1),)})
        == 1685074.12345
    )

    with pytest.raises(HeniautosNoDataError):
        summer_solstice(-99, data={"solstices": ()})


def test_moon_phases_data_param():
    assert moon_phases(-99)[0] == 1684907.0310656228
    assert (
        moon_phases(-99, data={"new_moons": ((1684900, 1684900.12345, 0),)})[0]
        == 1684900.12345
    )

    with pytest.raises(HeniautosNoDataError):
        moon_phases(-99, data={"new_moons": ()})


def test_new_moons_data_param():
    assert new_moons(-99)[0] == 1684907.0310656228
    assert (
        new_moons(-99, data={"new_moons": ((1684900, 1684900.12345, 0),)})[0]
        == 1684900.12345
    )

    with pytest.raises(HeniautosNoDataError):
        new_moons(-99, data={"new_moons": ()})


def test_visible_new_moons_data_param():
    print(visible_new_moons(-99))

    assert visible_new_moons(-99)[0] == 1684909
    assert (
        visible_new_moons(-99, data={"new_moons": ((1684900, 1684900.12345, 0),)})[0]
        == 1684902
    )

    with pytest.raises(HeniautosNoDataError):
        visible_new_moons(-99, data={"new_moons": ()})


def test_calendar_months_data_param():
    assert calendar_months(-99)[0] == (1685085, 1685115)
    assert calendar_months(-99, data=CUSTOM_YEAR) == (
        (1685293, 1685323),
        (1685323, 1685352),
    )

    with pytest.raises(HeniautosNoDataError):
        calendar_months(-99, data={"solstices": (), "new_moons": ()})


def test_festival_months_data_param():
    assert len(festival_months(-99)) == 13
    assert len(festival_months(-99, data=CUSTOM_YEAR)) == 2

    with pytest.raises(HeniautosNoDataError):
        festival_months(-99, data={"solstices": (), "new_moons": ()})


def test_festival_calendar_data_param():
    # print(festival_calendar(-99))

    assert len(festival_calendar(-99)) == 13
    assert len(festival_calendar(-99, data=CUSTOM_YEAR)) == 2

    with pytest.raises(HeniautosNoDataError):
        festival_calendar(-99, data={"solstices": (), "new_moons": ()})


def test_doy_to_julian_data_param():
    assert doy_to_julian(10, -99) == 1685094
    assert doy_to_julian(100, -99) == 1685184

    assert doy_to_julian(10, -99, data=CUSTOM_YEAR) == 1685302

    with pytest.raises(HeniautionNoDayInYearError):
        doy_to_julian(100, -99, data=CUSTOM_YEAR)

    with pytest.raises(HeniautosNoDataError):
        doy_to_julian(10, -99, data={"solstices": (), "new_moons": ()})


def test_festival_to_julian_data_param():
    assert festival_to_julian(-99, 1, 10) == 1685094
    assert festival_to_julian(-99, 6, 10) == 1685243

    assert festival_to_julian(-99, 1, 10, data=CUSTOM_YEAR) == 1685302
    with pytest.raises(HeniautionNoDayInYearError):
        festival_to_julian(-99, 6, 10, data=CUSTOM_YEAR)

    with pytest.raises(HeniautosNoDataError):
        festival_to_julian(-99, 1, 10, data={"solstices": (), "new_moons": ()})
