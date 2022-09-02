from heniautos import *
import pytest


def test_summer_solstice_data_param():
    assert summer_solstice(-99) == 1685074.3287422964
    assert summer_solstice(-99, data={"solstices": ((1685074, 1685074.12345, 1),)}) == 1685074.12345
    
    with pytest.raises(HeniautosNoDataError):
        summer_solstice(-99, data={"solstices": ()})


def test_moon_phases_data_param():
    print(load_data()["new_moons"][0])
    assert moon_phases(-99)[0] == 1684907.0310656228
    assert moon_phases(-99, data={"new_moons": ((1684907, 1684907.12345, 0),)})[0] == 1684907.12345

    with pytest.raises(HeniautosNoDataError):
        moon_phases(-99, data={"new_moons": ()})

