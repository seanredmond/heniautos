# Copyright (C) 2022 Sean Redmond

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import heniautos
import heniautos.prytanies
from itertools import product

def _fest_doy_ranges(month, day, intercalation):
    """Return possible DOYs with preceding months."""
    pairs = [
        p
        for p in [
            (r, (int(month) + (0 if intercalation else -1)) - r)
            for r in range(int(month) + (1 if intercalation else 0))
        ]
        if p[0] <= 7 and p[1] <= (6 + (1 if intercalation else 0))
    ]

    ranges = [(30,) * p[0] + (29,) * p[1] for p in pairs]

    return [
        {
            "date": (month, day),
            "doy": sum(m) + day,
            "preceding": m,
            "intercalation": intercalation,
        }
        for m in ranges
    ]


def festival_doy(month, day):
    """Return possible DOYs for a given month and day.

    Calculates every possible DOY for a month and day with all the
    possible combinations of full and hollow months preceding it.

    Parameters:
        month (Months): Months constant for the month
        day (int): Day of the month

    Returns a tuple of dicts, one for each DOY, and each consisting of:
        date: Month and day supplied
        doy: The DOY
        preceding: tuple of ints that are the lengths of the months preceding
                   the given date, which goes in the DOY calculation
        intercalation: True if the DOY requires in intercalation among the
                       months preceding the given date. False otherwise

    """
    if month == heniautos.AthenianMonths.HEK:
        return _fest_doy_ranges(month, day, False)

    return tuple(
        sorted(
            _fest_doy_ranges(month, day, False) + _fest_doy_ranges(month, day, True),
            key=lambda m: m["doy"],
        )
    )


def _fest_eq(months):
    try:
        return festival_doy(months[0], months[1])
    except TypeError as e:
        # We got a tuple of tuples
        if "tuple" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        # We got a tuple of tuples, but the len is only 1
        pass

    return tuple([a for b in [_fest_eq(m) for m in months] for a in b])


def _pryt_eq(prytanies, pryt_type=heniautos.prytanies.Prytany.AUTO, year=None):
    try:
        return heniautos.prytanies.prytany_doy(prytanies[0], prytanies[1], pryt_type=pryt_type, year=year)
    except TypeError as e:
        if "'tuple'" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        pass

    return tuple(
        [
            a
            for b in [_pryt_eq(p, pryt_type=pryt_type, year=year) for p in prytanies]
            for a in b
        ]
    )

def equations(months, prytanies, pryt_type=heniautos.prytanies.Prytany.AUTO, year=None):
    """Return possible solutions for a calendar equation

        Parameters:
            month (tuple): A tuple consisting of a Month constant and a day, or a
    tuple of such tuples
            prytanies: A tuple consisting of a Prytany constant and a day, or a
    tuple of such tuples
            year (int): Year, used to calculate prytany type is Prytany.AUTO
            pryt_type (Prytany): Type of prytany calendar to use
    (default Prytany.AUTO)

        Returns a tuple of tuples. Each inner tuple is a pair of dicts,
        one for festival and one for conciliar calendar conditions that
        satisfy the equation for a particular DOY. Each of these dicts
        consists of:

            date: The festival or prytany date
            doy: The DOY of the date
            preceding: A tuple of lengths of the preceding months or prytanies
            intercalation: True if intercalation required for this solution

        Intercalation means something slightly different for the festival
        and conciliar calendar solutions. For the conciliar calendar True
        means that the year is intercalary because that affects the
        lengths of all the prytanies. For the festival calendar True means
        that an intercalation must precede the date because that effects
        the number of months, not the lengths. If a pair has intercalation
        = False in the festival solution but intercalation = True in the
        conciliar, it indicated that that solution is valid for an
        intercalary, but only if the intercalation follows the festival
        date.

    """
    pryt_eqs = _pryt_eq(prytanies, pryt_type, year)
    fest_eqs = _fest_eq(months)

    intersection = sorted(
        set([f["doy"] for f in fest_eqs]) & set([p["doy"] for p in pryt_eqs])
    )

    return tuple(
        [
            a
            for b in [
                tuple(
                    product(
                        [f for f in fest_eqs if f["doy"] == i],
                        [p for p in pryt_eqs if p["doy"] == i],
                    )
                )
                for i in intersection
            ]
            for a in b
            if not _misaligned_intercalation(a)
        ]
    )


def _misaligned_intercalation(i):
    """Check if festival is intercalated but conciliar not."""
    if i[0]["intercalation"] is True and i[1]["intercalation"] is False:
        return True

    return False


def _no_deintercalations(i, pre=False):
    """Check festival intercalation sequence.

    Recursively check a sequence of festival month equation
    intercalation requirements. In festival month equation one with no
    intercalation can precede one with intercalation (because it's
    about when the intercalation occurse). Once one of the equations
    requires an intecalation before (True) none that follow can
    require no intercalation (False)

    """
    if not i:
        # If we got to then end of the sequence, it is good
        return True

    if pre is False and i[0] is False:
        # Proceed, no intercalation yet
        return _no_deintercalations(i[1:], False)

    if pre is True and i[0] is True:
        # Proceed, we have intercalation
        return _no_deintercalations(i[1:], True)

    if pre is False and i[0] is True:
        # Proceed, switch from no intercalation to intercalation
        return _no_deintercalations(i[1:], True)

    # The only condition left in pre == True and i[0] == False.
    # The forbidden condition. We have a precedeing intercalation
    # but the current equation requires none
    return False


def _is_contained_in(a, b):
    """Test whether the values in first tuple are contained in second."""
    if not len(a):
        # Successfully exhausted the first tuple. Return remainder
        return b

    try:
        i = b.index(a[0])
        return _is_contained_in(a[1:], b[:i] + b[i + 1 :])
    except ValueError as e:
        raise heniautos.HeniautosNoMatchError(f"{a[0]} not found in {b}")


def _each_overlaps(b, a=tuple()):
    """Test overlapping series of months or prytanies."""
    if not a:
        # First pass
        return _each_overlaps(b[1:], a + (b[0],))

    if not b:
        # Finished succesfully. Results in a
        return a

    # Just use a flattened version of a, results are the same
    # raises HeniautosNoMatchError if unsuccessful
    c = _is_contained_in([x for y in a for x in y], b[0])

    return _each_overlaps(b[1:], (a + (c,)))


def collations(*args, failures=False):
    """Collate multiple equations, looking for those that fit together.

    Take an arbitrary number of calendar equation results (args,
    i.e. results from equations()) and find those that fit together
    according to the following criteria:

        1) required conciliar years are all normal or all intercalary
        2) all equations that require festival year intercalation follow any
           that require no intercalations
        3) Each sequence of month and prytany lengths fits into the following
           sequences.

    Each equation results probably has multiple solutions. This test
    all combinations of solutions. Returns results as a tuple of dicts,
    each consiting of

        partitions: a dict with two members: "festival" and
        "conciliar." Each is a list of month or prytany lengths
        partitioned according to the requirements of the
        equations. For instance, ((30, 29), (30, 29), (30, 30, 29))
        means that the first equation must be preceded by one full and
        one hollow month; after the first equation but before the
        second there must by on full and one hollow month; after the
        second but before the third there must be two full and one
        hollow.

        equations: a list of equations making up this combined
        solution. Each is identical to a result returned from
        equations().

    If the optional "failures" parameter is true, return combinations
    that cannot be fitted together, as a list of combinations

    """
    successes = tuple()
    not_successes = tuple()

    for p in product(*args):
        try:
            # Criterion #1
            if len(set([c[1]["intercalation"] for c in p])) > 1:
                raise HeniautosNoMatchError()

            # Criterion #2
            if not _no_deintercalations([c[0]["intercalation"] for c in p]):
                raise HeniautosNoMatchError()

            # Criterion #3
            fest_partitions = _each_overlaps([c[0]["preceding"] for c in p])
            pryt_partitions = _each_overlaps([c[1]["preceding"] for c in p])
            successes = successes + (
                {
                    "partitions": {
                        "festival": fest_partitions,
                        "conciliar": pryt_partitions,
                    },
                    "equations": p,
                },
            )

        except heniautos.HeniautosNoMatchError as e:
            not_successes = not_successes + (p,)

    if failures is True:
        return not_successes

    return successes


