from skyfield import api
from skyfield import almanac
from skyfield.api import GREGORIAN_START
from enum import IntEnum

class Phases(IntEnum):
    """Constants representing lunar phases."""

    NEW = 0
    FIRSTQ = 1
    FULL = 2
    LASTQ = 3


def init_ephemeris(cfg={}, eph="de422.bsp", lat=37.983972, lon=23.727806, force=False):
    """Initialize data required for calculations.

    :param eph: Path to ephemeris file
    :type eph: str
    :param lat: Latitude for calculations (default 37.983972)
    :type lat: float
    :param lon: Longitude for calculations (default 23.727806)
    :type lon: float
    :param force: Force reinitialization
    :type force: bool
    :return: A dictionary of ephemeris details
    :rtype: dict


    If an ephemeris file cannot be found in the path and no file is
    specified by the eph parameter, de422.bsp will be downloaded.

    Longitude and latitude are set for Athens by default but can be changed.

    Initialization will only be done once unless the force parameter is True.
    """
    if cfg.get("init", False) is True and not force:
        return cfg

    if cfg is not None:
        cfg["eph_file"] = eph

    cfg["eph"] = api.load(cfg["eph_file"])
    cfg["eph_path"] = api.load.path_to(cfg["eph_file"])
    cfg["ts"] = api.load.timescale()
    cfg["ts"].julian_calendar_cutoff = GREGORIAN_START
    cfg["loc"] = api.wgs84.latlon(lat, lon)
    cfg["init"] = True

    return cfg


def _solar_events(year1, year2, eph):
    return tuple(
        [
            (s[0].tt, s[1])
            for s in zip(
                *almanac.find_discrete(
                    eph["ts"].ut1(year1, 1, 31),
                    eph["ts"].ut1(year2, 12, 31),
                    almanac.seasons(eph["eph"]),
                )
            )
        ]
    )


def _get_solar_events(year1, year2=None, eph={}):
    if year2 is not None:
        return _solar_events(year1 - 1, year2 + 1, eph)

    return _solar_events(year1 - 1, year1 + 1, eph)


def _moon_phases(year1, year2, eph={}, phase=0):
    """Return Time objects for all moon phases in year y."""
    return tuple(
        [
            (p[0].tt, p[1])
            for p in zip(
                *almanac.find_discrete(
                    eph["ts"].ut1(year1, 1, 1),
                    eph["ts"].ut1(year2, 12, 31, 23, 59, 59),
                    almanac.moon_phases(eph["eph"]),
                )
            )
            if p[1] == phase
        ]
    )


def _get_new_moons(year1, year2=None, eph={}):
    if year2 is not None:
        return _moon_phases(year1 - 1, year2 + 1, eph)

    return _moon_phases(year1 - 1, year1 + 1, eph)


def get_ephemeris_data(year1, year2=None, eph=None):
    """Get data for use by calendar functions

    :param year1: Year or start year for data
    :type year1: int
    :param year2: End year for data (default: None)
    :type year2: int
    :param eph: initialized ephemeris
    :type eph: dict
    :returns: A data object for use by calendar functions
    :rtype: dict

    The `eph` parameter should be a dict as returned by
    :func:`init_ephemeris`. For `year1` or a span of `year1` to
    `year2` (inclusive), returns a dictionary containg the dates of
    solar events (solstices and equinoxes), and new moons, suitable to
    be passed as the `data` parameter of calendar functions.

    """

    return {
        "solstices": _get_solar_events(year1, year2, eph),
        "new_moons": _get_new_moons(year1, year2, eph),
    }
