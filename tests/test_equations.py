import pytest
from heniautos import *
from heniautos.prytanies import *
from heniautos.equations import *


def test_fest_eq_tuple():
    eq = heniautos.equations._fest_eq((AthenianMonths.MET, 10))
    assert len(eq) == 5
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[-1]["doy"] == 70
    assert eq[-1]["intercalation"] is True

    assert heniautos.equations._fest_eq(
        (AthenianMonths.MET, 10)
    ) == heniautos.equations._fest_eq(((AthenianMonths.MET, 10),))


def test_fest_eq_nested():
    eq = heniautos.equations._fest_eq(
        ((AthenianMonths.MET, 10), (AthenianMonths.MET, 11))
    )
    assert len(eq) == 10
    assert eq[0]["date"] == (AthenianMonths.MET, 10)
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[4]["date"] == (AthenianMonths.MET, 10)
    assert eq[4]["doy"] == 70
    assert eq[4]["intercalation"] is True
    assert eq[5]["date"] == (AthenianMonths.MET, 11)
    assert eq[5]["doy"] == 40
    assert eq[5]["intercalation"] is False
    assert eq[-1]["date"] == (AthenianMonths.MET, 11)
    assert eq[-1]["doy"] == 71
    assert eq[-1]["intercalation"] is True


def test_pryt_eq_tuple():
    eq = heniautos.equations._pryt_eq((Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10)
    assert len(eq) == 4
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[-1]["doy"] == 43
    assert eq[-1]["intercalation"] is True

    assert heniautos.equations._pryt_eq(
        (Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10
    ) == heniautos.equations._pryt_eq(
        ((Prytanies.II, 4),), pryt_type=Prytany.ALIGNED_10
    )


def test_pryt_eq_nested():
    eq = heniautos.equations._pryt_eq(
        ((Prytanies.II, 4), (Prytanies.II, 5)), pryt_type=Prytany.ALIGNED_10
    )
    assert len(eq) == 8
    assert eq[0]["date"] == (Prytanies.II, 4)
    assert eq[0]["doy"] == 39
    assert eq[0]["intercalation"] is False
    assert eq[3]["date"] == (Prytanies.II, 4)
    assert eq[3]["doy"] == 43
    assert eq[3]["intercalation"] is True
    assert eq[-1]["date"] == (Prytanies.II, 5)
    assert eq[-1]["doy"] == 44
    assert eq[-1]["intercalation"] is True


def test_equations_tuples():
    eq = equations(
        (AthenianMonths.MET, 10), (Prytanies.II, 4), pryt_type=Prytany.ALIGNED_10
    )

    # Two solutions to this equation:
    assert len(eq) == 2

    # The first solution is DOY 39 (these should be sorted by DOY)
    assert len(eq[0]) == 2
    f, c = eq[0]

    assert f["doy"] == 39
    assert c["doy"] == 39

    assert f["preceding"] == (29,)
    assert c["preceding"] == (35,)

    assert f["intercalation"] is False
    assert c["intercalation"] is False

    # The second solution is DOY 40
    assert len(eq[1]) == 2
    f, c = eq[1]
    assert f["doy"] == 40
    assert c["doy"] == 40

    assert f["preceding"] == (30,)
    assert c["preceding"] == (36,)

    assert f["intercalation"] is False
    assert c["intercalation"] is False

    eq = equations(
        (AthenianMonths.POS, 14), (Prytanies.V, 36), pryt_type=Prytany.ALIGNED_10
    )

    assert len(eq) == 5
    assert [f[0]["doy"] for f in eq] == [188, 189, 190, 191, 192]
    assert [p[0]["doy"] for p in eq] == [188, 189, 190, 191, 192]


def test_equations_must_be_intercalary():
    eq1 = equations(
        (AthenianMonths.MET, 9), (Prytanies.I, 39), pryt_type=Prytany.ALIGNED_10
    )
    eq2 = equations(
        (AthenianMonths.MET, 6), (Prytanies.I, 36), pryt_type=Prytany.ALIGNED_10
    )

    # There should be only one possibility with I.39 because a 39-day
    # prytany requires an intercalary year
    assert len(eq1) == 1

    # There should be two possibilities because I.36 could be the 36th
    # day of either a 36-day or a 39-day prytany. An ordinary and an
    # intercalary year are both possible
    assert len(eq2) == 2


def test_equations_nested():
    eq = equations(
        ((AthenianMonths.HEK, 30), (AthenianMonths.MET, 1)),
        ((Prytanies.I, 30), (Prytanies.I, 31)),
        pryt_type=Prytany.ALIGNED_10,
    )

    assert all([e[0]["date"] == (AthenianMonths.HEK, 30) for e in eq[0:2]])
    assert all([e[0]["date"] == (AthenianMonths.MET, 1) for e in eq[2:]])

    assert len(eq) == 6


def test_0_prytanies():
    eq = equations(
        (AthenianMonths.MET, 9), (Prytanies.I, 39), pryt_type=Prytany.ALIGNED_10
    )

    assert len(eq) == 1
    assert len(eq[0][1]["preceding"]) == 0


@pytest.mark.skip(reason="probably remove this test")
def test_is_contained_in():
    assert heniautos._is_contained_in(
        (29, 29, 29, 29), (30, 30, 30, 29, 29, 29, 29, 29)
    ) == (30, 30, 30, 29)

    with pytest.raises(HeniautosNoMatchError):
        heniautos._is_contained_in(
            (29, 29, 29, 29), (30, 30, 30, 30, 30, 29, 29, 29)
        ) == (30, 30, 30, 29)

    with pytest.raises(HeniautosNoMatchError):
        heniautos._is_contained_in((29, 29, 29, 29), (29, 29, 29))


@pytest.mark.skip(reason="probably remove this test")
def test_each_overlaps():
    s = [
        (29, 29, 29, 29),
        (30, 30, 30, 29, 29, 29, 29, 29),
        (30, 30, 30, 30, 29, 29, 29, 29, 29),
    ]

    assert heniautos._each_overlaps(s) == ((29, 29, 29, 29), (30, 30, 30, 29), (30,))

    s = [
        (29, 29, 29, 29),
        (30, 30, 30, 29, 29, 29, 29, 29),
        (30, 30, 30, 30, 30, 29, 29, 29, 29),
    ]

    with pytest.raises(HeniautosNoMatchError):
        heniautos._each_overlaps(s) == ((29, 29, 29, 29), (30, 30, 30, 29), (30,))


@pytest.mark.skip(reason="probably remove this test")
def test_no_deintercalations():
    assert heniautos._no_deintercalations((False, False, False))
    assert heniautos._no_deintercalations((True, True, True))
    assert heniautos._no_deintercalations((False, True, True))
    assert heniautos._no_deintercalations((False, False, True))
    assert heniautos._no_deintercalations((True, False, True)) is False
    assert heniautos._no_deintercalations((True, True, False)) is False
    assert heniautos._no_deintercalations((True, False, False)) is False


@pytest.mark.xfail
def test_no_misaligned_intercalations():
    eq = equations(
        [(m, 14) for m in Months],
        [(p, 2) for p in Prytanies],
        year=bce_as_negative(336),
    )

    assert len(eq) == 19

    # Okay for festival intercalation to be False when conciliar
    # intercaltion is True
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (False, True)
    ) == 6

    # Okay for both to be the same
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (True, True)
    ) == 6
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (False, False)
    ) == 7

    # This must be 0. There cannot be festival intercalations
    # alongside an ordinary conciliar year
    assert [(f["intercalation"], p["intercalation"]) for f, p in eq].count(
        (True, False)
    ) == 0


def test_collations():
    # Equation 1: Boe 11 = II 31
    eq1 = equations(
        (AthenianMonths.MAI, 11), (Prytanies.IV, 21), year=bce_as_negative(319)
    )

    eq2 = equations(
        (AthenianMonths.ELA, 12), (Prytanies.VII, 34), year=bce_as_negative(319)
    )

    eq3 = equations(
        (AthenianMonths.MOU, 12), (Prytanies.VIII, 29), year=bce_as_negative(319)
    )

    c = collations(eq1, eq2, eq3)
    assert len(c) == 8

    # Festival year partitions
    assert c[0]["partitions"]["festival"] == ((29, 29, 29, 29), (30, 30, 29, 29), (30,))

    assert c[0]["partitions"]["conciliar"] == ((36, 35, 35), (36, 35, 35), (35,))

    # Festival DOYs
    assert [e[0]["doy"] for e in c[0]["equations"]] == [127, 246, 276]

    # Conciliar DOYs
    assert [e[1]["doy"] for e in c[0]["equations"]] == [127, 246, 276]

    # Festival Intercalations
    assert [e[0]["intercalation"] for e in c[0]["equations"]] == [False, False, False]
    # Conciliar Intercalations
    assert [e[1]["intercalation"] for e in c[0]["equations"]] == [False, False, False]

    c = collations(eq1, eq2, eq3, failures=True)
    assert len(c) == 19


def test_fest_doy_ranges():
    r = heniautos.equations._fest_doy_ranges(AthenianMonths.ELA, 19, False)
    assert len(r) == 6
    assert min([m["doy"] for m in r]) == 253
    assert max([m["doy"] for m in r]) == 258

    r = heniautos.equations._fest_doy_ranges(AthenianMonths.ELA, 19, True)
    assert len(r) == 6
    assert min([m["doy"] for m in r]) == 282
    assert max([m["doy"] for m in r]) == 287

    r = heniautos.equations._fest_doy_ranges(AthenianMonths.MAI, 19, False)
    assert len(r) == 5
    assert min([m["doy"] for m in r]) == 135
    assert max([m["doy"] for m in r]) == 139

    r = heniautos.equations._fest_doy_ranges(AthenianMonths.MAI, 19, True)
    assert len(r) == 6
    assert min([m["doy"] for m in r]) == 164
    assert max([m["doy"] for m in r]) == 169

    r = heniautos.equations._fest_doy_ranges(AthenianMonths.MOU, 27, False)
    assert len(r) == 5
    assert min([m["doy"] for m in r]) == 291
    assert max([m["doy"] for m in r]) == 295

    r = heniautos.equations._fest_doy_ranges(AthenianMonths.MOU, 27, True)
    assert len(r) == 5
    assert min([m["doy"] for m in r]) == 320
    assert max([m["doy"] for m in r]) == 324


def test_festival_doy():
    # 1st month, no intercalation possible
    doy = festival_doy(AthenianMonths.HEK, 5)
    assert len(doy) == 1
    assert doy[0]["doy"] == 5
    assert len(doy[0]["preceding"]) == 0

    assert doy[0]["intercalation"] is False
    assert not any([d["intercalation"] for d in doy])

    # 2nd month
    doy = festival_doy(AthenianMonths.MET, 5)
    print(doy)
    assert len(doy) == 5
    assert doy[0]["doy"] == 34
    assert len(doy[0]["preceding"]) == 1
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 65
    assert len(doy[-1]["preceding"]) == 2
    assert doy[-1]["intercalation"] is True

    assert not any([d["intercalation"] for d in doy if d["doy"] < 63])
    assert all([d["intercalation"] for d in doy if d["doy"] > 35])

    # 5th month
    doy = festival_doy(AthenianMonths.MAI, 27)
    assert len(doy) == 11
    assert doy[0]["doy"] == 143
    assert len(doy[0]["preceding"]) == 4
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 177
    assert len(doy[-1]["preceding"]) == 5
    assert doy[-1]["intercalation"] is True
    assert not any([d["intercalation"] for d in doy if d["doy"] < 172])
    assert all([d["intercalation"] for d in doy if d["doy"] > 147])

    doy = festival_doy(AthenianMonths.MOU, 27)
    assert len(doy) == 10
    assert doy[0]["doy"] == 291
    assert len(doy[0]["preceding"]) == 9
    assert doy[0]["intercalation"] is False

    assert doy[-1]["doy"] == 324
    assert len(doy[-1]["preceding"]) == 10
    assert doy[-1]["intercalation"] is True
    assert not any([d["intercalation"] for d in doy if d["doy"] < 320])
    assert all([d["intercalation"] for d in doy if d["doy"] > 295])


