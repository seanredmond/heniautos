from heniautos import *
import pytest

CUSTOM_YEAR = {
    "solstices": (
        (1685074.3287422964, 1),
        (1685439.5648092534, 1),
    ),
    "new_moons": (
        (1684907.0310656228, 0),
        (1684936.490878384, 0),
        (1684965.8702085295, 0),
        (1685291.0009266976, 0),
        (1685320.5018709311, 0),
        (1685349.9050228074, 0),
        (1685704.4562648418, 0),
        (1685733.8966757061, 0),
    ),
}


def test_load_default_data():
    d = load_data()
    assert type(d) is dict
    assert "solstices" in d
    assert "new_moons" in d


def test_earliest_bce():
    assert type(athenian_festival_calendar(-632)) is tuple
    assert type(delian_festival_calendar(-632)) is tuple
    assert type(spartan_festival_calendar(-632)) is tuple
    assert new_moons(-632)[0] == 1490240.6927069575

    with pytest.raises(HeniautosNoDataError) as e:
        athenian_festival_calendar(-633)

    with pytest.raises(HeniautosNoDataError) as e:
        assert new_moons(-633)


def test_latest_bce():
    assert type(athenian_festival_calendar(0)) is tuple
    assert type(delian_festival_calendar(0)) is tuple
    assert type(spartan_festival_calendar(0)) is tuple
    assert new_moons(2)[-1] == 1722144.1667546108

    with pytest.raises(HeniautosNoDataError) as e:
        athenian_festival_calendar(1)

    with pytest.raises(HeniautosNoDataError) as e:
        assert new_moons(3)


def test_earliest_ce():
    assert type(athenian_festival_calendar(1899)) is tuple
    assert type(delian_festival_calendar(1899)) is tuple
    assert type(spartan_festival_calendar(1899)) is tuple
    assert new_moons(1898)[0] == 2414666.451094415

    with pytest.raises(HeniautosNoDataError) as e:
        athenian_festival_calendar(1898)

    with pytest.raises(HeniautosNoDataError) as e:
        assert new_moons(1897)


def test_latest_ce():
    assert type(athenian_festival_calendar(2150)) is tuple
    assert type(delian_festival_calendar(2150)) is tuple
    assert type(spartan_festival_calendar(2150)) is tuple
    assert new_moons(2152)[0] == 2507097.106959081

    with pytest.raises(HeniautosNoDataError) as e:
        athenian_festival_calendar(2151)

    with pytest.raises(HeniautosNoDataError) as e:
        assert new_moons(2153)


def test_solar_event_data_param():
    assert solar_event(-99, Seasons.SUMMER_SOLSTICE) == 1685074.1951805085
    assert (
        solar_event(
            -99,
            Seasons.SUMMER_SOLSTICE,
            data={"solstices": ((1685074.12345, 1),)},
        )
        == 1685074.12345
    )

    with pytest.raises(HeniautosNoDataError):
        solar_event(-99, Seasons.SUMMER_SOLSTICE, data={"solstices": ()})


def test_summer_solstice_data_param():
    assert solar_event(-99, Seasons.SUMMER_SOLSTICE) == 1685074.1951805085
    assert (
        solar_event(
            -99, Seasons.SUMMER_SOLSTICE, data={"solstices": ((1685074.12345, 1),)}
        )
        == 1685074.12345
    )

    with pytest.raises(HeniautosNoDataError):
        solar_event(-99, Seasons.SUMMER_SOLSTICE, data={"solstices": ()})


def test_new_moons_data_param():
    assert new_moons(-99)[0] == 1684906.8971423437
    assert new_moons(-99, data={"new_moons": ((1684900.12345, 0),)})[0] == 1684900.12345

    with pytest.raises(HeniautosNoDataError):
        new_moons(-99, data={"new_moons": ()})


def test_visible_new_moons_data_param():
    print(visible_new_moons(-99))

    assert visible_new_moons(-99)[0] == 1684908
    assert (
        visible_new_moons(-99, data={"new_moons": ((1684900.12345, 0),)})[0] == 1684901
    )

    with pytest.raises(HeniautosNoDataError):
        visible_new_moons(-99, data={"new_moons": ()})


@pytest.mark.xfail(reason="Need better custom data")
def test_calendar_months_data_param():
    assert calendar_months(-99)[0] == (1685084, 1685114)
    assert calendar_months(-99, data=CUSTOM_YEAR) == (
        (1685292, 1685322),
        (1685322, 1685351),
    )

    with pytest.raises(HeniautosNoDataError):
        calendar_months(-99, data={"solstices": (), "new_moons": ()})


@pytest.mark.xfail(reason="Need better custom data")
def test_festival_months_data_param():
    assert len(festival_months(-99)) == 13
    assert len(festival_months(-99, data=CUSTOM_YEAR)) == 2

    with pytest.raises(HeniautosNoDataError):
        festival_months(-99, data={"solstices": (), "new_moons": ()})


@pytest.mark.xfail(reason="Need better custom data")
def test_festival_calendar_data_param():
    assert len(festival_calendar(-99)) == 384
    assert len(festival_calendar(-99, data=CUSTOM_YEAR)) == 59

    with pytest.raises(HeniautosNoDataError):
        festival_calendar(-99, data={"solstices": (), "new_moons": ()})


@pytest.mark.xfail(reason="Need better custom data")
def test_doy_to_julian_data_param():
    assert doy_to_julian(10, -99) == 1685093
    assert doy_to_julian(100, -99) == 1685183

    assert doy_to_julian(10, -99, data=CUSTOM_YEAR) == 1685301

    with pytest.raises(HeniautionNoDayInYearError):
        doy_to_julian(100, -99, data=CUSTOM_YEAR)

    with pytest.raises(HeniautosNoDataError):
        doy_to_julian(10, -99, data={"solstices": (), "new_moons": ()})


def test_festival_to_julian_data_param():
    assert festival_to_jdn(-99, 1, 10) == 1685093
    assert festival_to_jdn(-99, 6, 10) == 1685242

    assert festival_to_jdn(-99, 1, 10, data=CUSTOM_YEAR) == 1685301
    with pytest.raises(HeniautosNoDayInYearError):
        festival_to_jdn(-99, 6, 10, data=CUSTOM_YEAR)

    with pytest.raises(HeniautosNoDataError):
        festival_to_jdn(-99, 1, 10, data={"solstices": (), "new_moons": ()})
