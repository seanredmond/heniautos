from heniautos import *
import pytest


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
