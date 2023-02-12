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
    assert type(d["solstices"]) is tuple
    assert type(d["solstices"][0]) is tuple
    assert type(d["solstices"][0][0]) is float
    assert type(d["solstices"][0][1]) is int
    assert d["solstices"][0] == (1500533.0682705436, 0)
    assert [m for m in d["solstices"] if m[0] < 2000000][-1] == (1721414.3908799929, 3)
    assert d["solstices"][-1] == (2489885.302570413, 3)

    assert "new_moons" in d
    assert type(d["new_moons"]) is tuple
    assert type(d["new_moons"][0]) is tuple
    assert type(d["new_moons"][0][0]) is float
    assert type(d["new_moons"][0][1]) is int
    assert d["new_moons"][0] == (1500458.8964768478, 0)
    assert [m for m in d["new_moons"] if m[0] < 2000000][-1] == (1721406.2574824847, 0)
    assert d["new_moons"][-1] == (2489881.083336255, 0)


def test_solar_event_data_param():
    assert solar_event(-99, Seasons.SUMMER_SOLSTICE) == 1685074.3287422964
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
    assert solar_event(-99, Seasons.SUMMER_SOLSTICE) == 1685074.3287422964
    assert (
        solar_event(
            -99, Seasons.SUMMER_SOLSTICE, data={"solstices": ((1685074.12345, 1),)}
        )
        == 1685074.12345
    )

    with pytest.raises(HeniautosNoDataError):
        solar_event(-99, Seasons.SUMMER_SOLSTICE, data={"solstices": ()})


def test_new_moons_data_param():
    assert new_moons(-99)[0] == 1684907.0310656228
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
