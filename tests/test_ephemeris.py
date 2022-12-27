from heniautos import *
import heniautos.ephemeris as heph
import pytest


@pytest.mark.eph
def test_init_ephemeris():
    e = heph.init_ephemeris()
    assert e["eph_file"] == "de422.bsp"
    assert e["init"]


@pytest.mark.eph
def test_get_data():
    e = heph.init_ephemeris()
    data = heph.get_ephemeris_data(-99, eph=e)
    assert as_gmt(data["solstices"][0][0], True) == "BCE 0101-Mar-23 13:58:40 GMT"
    assert data["solstices"][0][1] == 0
    assert as_gmt(data["solstices"][-1][0], True) == "BCE 0099-Dec-23 02:21:41 GMT"
    assert data["solstices"][-1][1] == 3

    assert as_gmt(data["new_moons"][0][0], True) == "BCE 0101-Jan-05 19:44:48 GMT"
    assert as_gmt(data["new_moons"][-1][0], True) == "BCE 0099-Dec-26 20:10:25 GMT"


@pytest.mark.eph
def test_summer_solstice():
    e = heph.init_ephemeris()
    assert (
        as_gmt(summer_solstice(100, data=heph.get_ephemeris_data(100, eph=e)))
        == " CE 0100-Jun-24"
    )
    assert (
        as_gmt(summer_solstice(100, data=heph.get_ephemeris_data(100, eph=e)), True)
        == " CE 0100-Jun-24 22:20:29 GMT"
    )


@pytest.mark.eph
def test_festival_calendar():
    e = heph.init_ephemeris()
    p = festival_calendar(100, data=heph.get_ephemeris_data(100, eph=e))
    assert as_gmt(p[0].jdn) == " CE 0100-Jun-26"
    assert as_gmt(p[-1].jdn) == " CE 0101-Jul-14"


@pytest.mark.eph
def test_moon_phases():
    e = heph.init_ephemeris()

    p = moon_phases(100, data=heph.get_ephemeris_data(100, eph=e))
    assert type(p) is list
    assert as_gmt(p[0], True) == " CE 0100-Jan-28 04:26:03 GMT"

    assert (
        as_gmt(
            moon_phases(100, Phases.FIRST_Q, data=heph.get_ephemeris_data(100, eph=e))[
                0
            ],
            True,
        )
        == " CE 0100-Jan-07 13:59:48 GMT"
    )

    assert (
        as_gmt(
            moon_phases(100, Phases.FULL, data=heph.get_ephemeris_data(100, eph=e))[0],
            True,
        )
        == " CE 0100-Jan-14 00:33:16 GMT"
    )

    assert (
        as_gmt(
            moon_phases(100, Phases.LAST_Q, data=heph.get_ephemeris_data(100, eph=e))[
                0
            ],
            True,
        )
        == " CE 0100-Jan-21 17:24:36 GMT"
    )

@pytest.mark.eph
def test_moon_phases_gregorian():
    e = heph.init_ephemeris()

    p = moon_phases(2023, data=heph.get_ephemeris_data(2023, eph=e))
    assert as_gmt(p[0], True) == " CE 2023-Jan-21 20:54:24 GMT"
