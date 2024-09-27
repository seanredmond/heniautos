from heniautos import *
import pytest

def test_athenian_434():
    """Athenian 434/433 should be intercalary, starting on July 9, 434
    and ending on Jul 26, 433

    """
    # Generate generic calendar
    m = festival_calendar(-433, calendar=None)
    assert len(m) == 384
    assert as_julian(m[0].jdn) == "BCE 0434-Jul-09"
    assert as_julian(m[-1].jdn) == "BCE 0433-Jul-26"

    # Make sure generic and specific calendar match
    assert all([d[0].jdn == d[1].jdn for d in zip(m, athenian_festival_calendar(-433))])


def test_athenian_433():
    """Athenian 433/432 should be ordinary, starting on July 27, 433
    and ending on Jul 15, 432

    """
    m = festival_calendar(-432, calendar=None)
    assert len(m) == 354
    assert as_julian(m[0].jdn) == "BCE 0433-Jul-27"
    assert as_julian(m[-1].jdn) == "BCE 0432-Jul-15"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, athenian_festival_calendar(-432))])
    

def test_athenian_432():
    """Athenain 432/431 should be ordinary, startining on July 16, and
    ending on July 5

    """
    m = festival_calendar(-431, calendar=None)
    assert m[0].jdn == 1563832 # July 16, 432 BCE
    assert m[-1].jdn == 1564186 # July 5, 431 BCE
    assert len(m) == 355
    assert all([d[0].jdn == d[1].jdn for d in zip(m, athenian_festival_calendar(-431))])


def test_athenian_424():
    """Athenian 424/423 should be ordinary, starting on July 18, 424
    and ending on Jul 6, 423

    """
    m = festival_calendar(-423, calendar=None)
    assert len(m) == 354
    assert as_julian(m[0].jdn) == "BCE 0424-Jul-18"
    assert as_julian(m[-1].jdn) == "BCE 0423-Jul-06"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, athenian_festival_calendar(-423))])


def test_athenian_423():
    """Athenian 423/422 should be intercalary, starting on July 7, 423
    and ending on July 25, 422
    """
    m = festival_calendar(-422, calendar=None)
    assert len(m) == 384
    assert as_julian(m[0].jdn) == "BCE 0423-Jul-07"
    assert as_julian(m[-1].jdn) == "BCE 0422-Jul-25"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, athenian_festival_calendar(-422))])


def test_athenian_422():
    """Atheian 422/421 should be ordinary, starting on July 26, 422
    and ending on July 13, 421"""
    m = festival_calendar(-421, calendar=None)
    assert len(m) == 354
    assert as_julian(m[0].jdn) == "BCE 0422-Jul-26"
    assert as_julian(m[-1].jdn) == "BCE 0421-Jul-13"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, athenian_festival_calendar(-421))])


def test_delian_435():
    """Delian 435 (= 434/433) should be ordinary, starting on Jan 13, 434
    and ending on Jan 1, 433

    """
    m = festival_calendar(-434, event=Seasons.WINTER_SOLSTICE, calendar=None)
    assert len(m) == 354
    assert as_julian(m[0].jdn) == "BCE 0434-Jan-13"
    assert as_julian(m[-1].jdn) == "BCE 0433-Jan-01"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, delian_festival_calendar(-434))])


def test__delian_434():
    """Delian 434 (= 433/432) should be interclary, starting on Jan 2, 433
    and ending on Jan 19, 432

    """
    m = festival_calendar(-433, event=Seasons.WINTER_SOLSTICE, calendar=None)
    assert len(m) == 384
    assert as_julian(m[0].jdn) == "BCE 0433-Jan-02"
    assert as_julian(m[-1].jdn) == "BCE 0432-Jan-19"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, delian_festival_calendar(-433))])


def test_spartan_424():
    """Spartan 424/423 should be ordinary, starting on Sep 15, 424
    and ending on Sep 3, 423

    """
    m = festival_calendar(-423, event=Seasons.AUTUMN_EQUINOX, before_event=True, calendar=None)
    assert len(m) == 355
    assert as_julian(m[0].jdn) == "BCE 0424-Sep-14"
    assert as_julian(m[-1].jdn) == "BCE 0423-Sep-03"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, spartan_festival_calendar(-423))])


def test_generic_festival_months_spartan_423():
    """Spartan 424/423 should be intercalary, starting on Sep 4, 423
    and ending on Sep 22, 422

    """
    m = festival_calendar(-422, event=Seasons.AUTUMN_EQUINOX, before_event=True, calendar=None)
    assert len(m) == 384
    assert as_julian(m[0].jdn) == "BCE 0423-Sep-04"
    assert as_julian(m[-1].jdn) == "BCE 0422-Sep-22"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, spartan_festival_calendar(-422))])


def test_spartan_422():
    """Spartan 422/421 should be ordinary, starting on Sep 23, 422
    and ending on Sep 11, 421

    """
    m = festival_calendar(-421, event=Seasons.AUTUMN_EQUINOX, before_event=True, calendar=None)
    assert len(m) == 354
    assert as_julian(m[0].jdn) == "BCE 0422-Sep-23"
    assert as_julian(m[-1].jdn) == "BCE 0421-Sep-10"
    assert all([d[0].jdn == d[1].jdn for d in zip(m, spartan_festival_calendar(-421))])







    

    


