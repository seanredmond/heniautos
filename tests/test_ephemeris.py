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
    data = heph.get_ephemeris_data(-99)
    assert as_gmt(data["solstices"][0][0], True) == "BCE 0101-Mar-23 13:58:40 GMT"
    assert data["solstices"][0][1] == 0
    assert as_gmt(data["solstices"][-1][0], True) == "BCE 0099-Dec-23 02:21:41 GMT"
    assert data["solstices"][-1][1] == 3

    assert as_gmt(data["new_moons"][0][0], True) == "BCE 0101-Jan-20 22:23:57 GMT"
    assert as_gmt(data["new_moons"][-1][0], True) == "BCE 0099-Dec-18 22:32:05 GMT"


@pytest.mark.eph
def test_summer_solstice():
    assert as_gmt(summer_solstice(100, data=heph.get_ephemeris_data(100))) == " CE 0100-Jun-24"
    assert as_gmt(summer_solstice(100, data=heph.get_ephemeris_data(100)), True) == " CE 0100-Jun-24 22:20:29 GMT"
    

@pytest.mark.eph
def test_festival_calendar():
    p = festival_calendar(100, data=heph.get_ephemeris_data(100))
    assert as_gmt(p[0]["days"][0]["date"]) == " CE 0100-Jun-27"
    assert as_gmt(p[-1]["days"][-1]["date"]) == " CE 0101-Jul-15"

        