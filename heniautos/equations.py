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

from itertools import product
from collections import namedtuple

FestivalDOY = namedtuple(
    "FestivalDOY",
    (
        "date",
        "doy",
        "preceding",
        "intercalation",
    ),
)

PrytanyDOY = namedtuple(
    "PrytanyDOY",
    (
        "date",
        "doy",
        "preceding",
        "intercalation",
    ),
)

Equation = namedtuple(
    "Equation",
    (
        "festival",
        "conciliar",
    ),
)

Partition = namedtuple(
    "Partition",
    (
        "festival",
        "conciliar",
    ),
)

Collation = namedtuple(
    "Collation",
    (
        "equations",
        "partitions",
    ),
)


def __fest_doy_ranges(month, day, intercalation):
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
        FestivalDOY(
            (month, day),
            sum(m) + day,
            m,
            intercalation,
        )
        for m in ranges
    ]


def festival_doy(month, day):
    """Return possible DOYs for a given month and day.

    :param month: Months constant for the month.
    :type month: :py:enum:`heniautos.CalendarMonth`
    :param day: Day of the month.
    :type  day: int
    :return: List of possible days of the year.
    :rtype: tuple

    Calculates every possible DOY for a month and day with all the
    possible combinations of full and hollow months preceding it.

    Returns a tuple of :py:class:`FestivalDOY` objects, one for each
    DOY, and each consisting of:

    * :py:attr:`date`: Month and day supplied
    * :py:attr:`doy`: The day of the year
    * :py:attr:`preceding`: tuple of ints that are the lengths of the months
      preceding the given date, which goes in the DOY calculation
    * :py:attr:`intercalation`: :py:obj:`True` if the DOY requires an
      intercalation among the months preceding the given date.
      :py:obj:`False` otherwise

    """
    if month == 1:
        return __fest_doy_ranges(month, day, False)

    return tuple(
        sorted(
            __fest_doy_ranges(month, day, False) + __fest_doy_ranges(month, day, True),
            key=lambda m: m.doy,
        )
    )


def __max_or_fewer(n, mx):
    """Return n if n is less than mx, otherwise mx."""
    return n if n < mx else mx


def __pryt_long_count(n, pryt_type, intercalated):
    """Return the number of long prytanies allowed for prytany type."""
    from heniautos.prytanies import Prytany

    if pryt_type == Prytany.QUASI_SOLAR:
        return __max_or_fewer(n - 1, 5)

    if pryt_type == Prytany.ALIGNED_10:
        return __max_or_fewer(n - 1, 4)

    if pryt_type == Prytany.ALIGNED_12:
        return __max_or_fewer(n - 1, 7)

    if pryt_type == Prytany.ALIGNED_13 and not intercalated:
        return __max_or_fewer(n - 1, 3)

    if pryt_type == Prytany.ALIGNED_13 and intercalated:
        return __max_or_fewer(n - 1, 7)

    raise HeniautosError("Unhandled")


def __pryt_short_count(n, pryt_type, intercalated):
    """Return the number of short prytanies allowed for prytany type."""
    from heniautos.prytanies import Prytany

    if pryt_type == Prytany.QUASI_SOLAR:
        return __max_or_fewer(n - 1, 5)

    if pryt_type == Prytany.ALIGNED_10:
        return __max_or_fewer(n - 1, 6)

    if pryt_type == Prytany.ALIGNED_12:
        return __max_or_fewer(n - 1, 5)

    if pryt_type == Prytany.ALIGNED_13 and not intercalated:
        return __max_or_fewer(n - 1, 10)

    if pryt_type == Prytany.ALIGNED_13 and intercalated:
        return __max_or_fewer(n - 1, 6)

    raise HeniautosError("Unhandled")


def __pryt_doy_ranges(pry, day, pryt_type, lng, intercalation):
    """Return possible DOYs with preceding prytanies."""

    from heniautos.prytanies import Prytany

    if pryt_type == Prytany.ALIGNED_12 and intercalation:
        return [
            PrytanyDOY(
                (pry, day),
                sum(r) + day,
                r,
                intercalation,
            )
            for r in ((32,) * (pry - 1),)
        ]

    max_long = __pryt_long_count(pry, pryt_type, intercalation)
    max_short = __pryt_short_count(pry, pryt_type, intercalation)
    min_long = int(pry - 1) - max_short
    min_short = int(pry - 1) - max_long

    pairs = [
        p
        for p in product(range(min_long, max_long + 1), range(min_short, max_short + 1))
        if sum(p) == pry - 1
    ]

    ranges = [(lng,) * p[0] + (lng - 1,) * p[1] for p in pairs]

    return [
        PrytanyDOY(
            (pry, day),
            sum(r) + day,
            r,
            intercalation,
        )
        for r in ranges
    ]


def prytany_doy(pry, day, pryt_type):
    """Return possible DOYs for a given prytany and day.


    :param pry: Prytany
    :type pry: heniautos.prytanies.Prytanies
    :param day: Day of the prytany
    :type day: int
    :param pryt_type: Type of prytany
    :type pryt_type: heniautos.prytanies.Prytanies
    :return: List of possible days of the year
    :rtype: tuple
    :raises heniautos.HeniautosError: If :py:class:`heniautos.prytanies.Prytany.AUTO` or other unrecognized prytany type is supplied


    Calculates every possible DOY for a prytany and day with all the
    possible combinations of long and short prytanies preceding
    it. Returns a tuple of :py:class:`FestivalDOY` objects, one for
    each DOY.

    """
    from heniautos import HeniautosError
    from heniautos.prytanies import Prytany

    if pryt_type == Prytany.QUASI_SOLAR:
        return tuple(
            sorted(
                __pryt_doy_ranges(pry, day, pryt_type, 37, None), key=lambda p: p.doy
            )
        )

    if pryt_type == Prytany.ALIGNED_10:
        if day > 36:
            # Must be intercalary
            return tuple(
                sorted(
                    __pryt_doy_ranges(pry, day, pryt_type, 39, True),
                    key=lambda p: p.doy,
                )
            )

        return tuple(
            sorted(
                __pryt_doy_ranges(pry, day, pryt_type, 36, False)
                + __pryt_doy_ranges(pry, day, pryt_type, 39, True),
                key=lambda p: p.doy,
            )
        )

    if pryt_type == Prytany.ALIGNED_12:
        if day > 30:
            return tuple(
                sorted(
                    __pryt_doy_ranges(pry, day, pryt_type, 32, True),
                    key=lambda p: p.doy,
                )
            )

        return tuple(
            sorted(
                __pryt_doy_ranges(pry, day, pryt_type, 30, False)
                + __pryt_doy_ranges(pry, day, pryt_type, 32, True),
                key=lambda p: p.doy,
            )
        )

    if pryt_type == Prytany.ALIGNED_13:
        if day > 28:
            return tuple(
                sorted(
                    __pryt_doy_ranges(pry, day, pryt_type, 30, True),
                    key=lambda p: p.doy,
                )
            )

        return tuple(
            sorted(
                __pryt_doy_ranges(pry, day, pryt_type, 28, False)
                + __pryt_doy_ranges(pry, day, pryt_type, 30, True),
                key=lambda p: p.doy,
            )
        )

    raise HeniautosError(f"Unhandled prytany type: {pryt_type}")


def __fest_eq(months):
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

    return tuple([a for b in [__fest_eq(m) for m in months] for a in b])


def __pryt_eq(prytanies, pryt_type):
    try:
        return prytany_doy(prytanies[0], prytanies[1], pryt_type=pryt_type)
    except TypeError as e:
        if "'tuple'" in e.__str__():
            pass
        else:
            raise e
    except IndexError:
        pass

    return tuple(
        [a for b in [__pryt_eq(p, pryt_type=pryt_type) for p in prytanies] for a in b]
    )


def equations(months, prytanies, pryt_type):
    """Return possible solutions for a calendar equation


    :param month: (tuple): A tuple consisting of a :py:class:`heniautos.CalendarMonth` constant and a day (:py:class:`int`), or a tuple of such tuples
    :type month: tuple
    :param prytanies: A tuple consisting of a :py:class:`heniautos.prytanies.Prytanies` constant and a day (:py:class:`int`), or a tuple of such tuples
    :param pryt_type: Type of prytany calendar to use
    :type pryt_type: heniautos.prytanies.Prytanies
    :return: List of matching :py:class:`Equation` objects
    :rtype: tuple
    :raises heniautos.HeniautosError: If :py:class:`heniautos.prytanies.Prytany.AUTO` or other unrecognized prytany type is supplied


    Returns a tuple of :py:class:`Equation` objects, each containing a pair of :py:class:`FestivalDOY` and :py:class:`PrytanyDOY` that together a solution for the given calendar equation(s) (:py:obj:`months` = :py:obj:`prytanies`)

    Intercalation means something slightly different for the festival
    and conciliar calendar solutions. For the conciliar calendar
    :py:class:`True` means that the year is intercalary because that
    affects the lengths of all the prytanies. For the festival
    calendar, :py:class:`True` means that an intercalation must
    precede the date because that effects the number of months, not
    the lengths. If a pair has :py:attr:`intercalation` =
    :py:class:`False` in the festival solution but
    py:attr:`intercalation` = :py:class:`True` in the conciliar, it
    indicates that that solution is valid for an intercalary, but only
    if the intercalation follows the festival date.

    """
    pryt_eqs = __pryt_eq(prytanies, pryt_type)
    fest_eqs = __fest_eq(months)

    intersection = sorted(
        set([f.doy for f in fest_eqs]) & set([p.doy for p in pryt_eqs])
    )

    return tuple(
        [
            Equation(*a)
            for b in [
                tuple(
                    product(
                        [f for f in fest_eqs if f.doy == i],
                        [p for p in pryt_eqs if p.doy == i],
                    )
                )
                for i in intersection
            ]
            for a in b
            if not __misaligned_intercalation(a)
        ]
    )


def __misaligned_intercalation(i):
    """Check if festival is intercalated but conciliar not."""
    if i[0].intercalation is True and i[1].intercalation is False:
        return True

    return False


def __no_deintercalations(i, pre=False):
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
        return __no_deintercalations(i[1:], False)

    if pre is True and i[0] is True:
        # Proceed, we have intercalation
        return __no_deintercalations(i[1:], True)

    if pre is False and i[0] is True:
        # Proceed, switch from no intercalation to intercalation
        return __no_deintercalations(i[1:], True)

    # The only condition left in pre == True and i[0] == False.
    # The forbidden condition. We have a precedeing intercalation
    # but the current equation requires none
    return False


def __is_contained_in(a, b):
    """Test whether the values in first tuple are contained in second."""
    from heniautos import HeniautosNoMatchError

    if not len(a):
        # Successfully exhausted the first tuple. Return remainder
        return b

    try:
        i = b.index(a[0])
        return __is_contained_in(a[1:], b[:i] + b[i + 1 :])
    except ValueError as e:
        raise HeniautosNoMatchError(f"{a[0]} not found in {b}")


def __each_overlaps(b, a=tuple()):
    """Test overlapping series of months or prytanies."""
    if not a:
        # First pass
        return __each_overlaps(b[1:], a + (b[0],))

    if not b:
        # Finished succesfully. Results in a
        return a

    # Just use a flattened version of a, results are the same
    # raises HeniautosNoMatchError if unsuccessful
    c = __is_contained_in([x for y in a for x in y], b[0])

    return __each_overlaps(b[1:], (a + (c,)))


def collations(*args, failures=False):
    """Collate multiple equations, looking for those that fit together.

    :param args: Arbitrary number of equation results
    :type args: heniautos.equations.Equation
    :return: tuple of :py:class:`Collation` objects

    Take an arbitrary number of calendar :py:class:`Equation` results
    (i.e. results from :py:func:`equations`) and find those that fit
    together according to the following criteria:

    1. required conciliar years are all normal or all intercalary
    2. all equations that require festival year intercalation follow any
       that require no intercalations
    3. Each sequence of month and prytany lengths fits into the following
       sequences.

    Each equation result probably has multiple solutions. This tests
    all combinations of solutions. Returns results as a tuple
    :py:class:`Collation` objects.

    """
    from heniautos import HeniautosNoMatchError

    successes = tuple()
    not_successes = tuple()

    for p in product(*args):
        try:
            # Criterion #1
            if len(set([c[1].intercalation for c in p])) > 1:
                raise HeniautosNoMatchError()

            # Criterion #2
            if not __no_deintercalations([c[0].intercalation for c in p]):
                raise HeniautosNoMatchError()

            # Criterion #3
            fest_partitions = __each_overlaps([c[0].preceding for c in p])
            pryt_partitions = __each_overlaps([c[1].preceding for c in p])
            successes = successes + (
                Collation(
                    p,
                    Partition(
                        fest_partitions,
                        pryt_partitions,
                    ),
                ),
            )

        except HeniautosNoMatchError as e:
            not_successes = not_successes + (p,)

    if failures is True:
        return not_successes

    return successes
