.. _conciliar-calendars:

Athenian Conciliar Calendars
============================

.. currentmodule:: heniautos.prytanies

This section will cover :py:func:`prytanies.prytany_calendar`, the function for
generating specific festival calendars


Athens had a second calendar, called the conciliar calendar, by which
public business was dated. Instead of months, this calendar had
πρυτανείαι, "prytanies" or "presidencies." Each of the *phulai* or
"tribes" presided, as the *prutaneis* or "presidents," over the
council for one prytany each year.

Conciliar calendar functions are in a sub-package
:py:mod:`heniautos.prytanies` and the examples below assume you have
imported this package like so:

>>> import heniautos.prytanies as pryt

The :py:func:`prytany_calendar` is analogous to
:py:func:`heniautos.athenian_festival_calendar`. The simplest
invocation take a single ``year`` parameter and returns a ``tuple`` of
:py:class:`heniautos.PrytanyDay` objects, which are similar to
:py:class:`heniautos.FestivalDay` objects:

>>> pryt_year = pryt.prytany_calendar(-406)
>>> pryt_year[0]
PrytanyDay(jdn=1572957, prytany_index=1, prytany=<Prytanies.I: 1>, prytany_length=37, day=1, doy=1, year='BCE 407/406', year_length=366, astronomical_year=-406)

The first :py:class:`heniautos.PrytanyDay` object in the above example has the
following properties and values:

+-----------------+---------------------------------+-------------+
|Property         |Value                            |Meaning      |
+=================+=================================+=============+
|jdn              |1572957                          |Corresponding|
|                 |                                 |Julian Day   |
|                 |                                 |Number       |
+-----------------+---------------------------------+-------------+
|prytany_index    |1                                |Order of     |
|                 |                                 |prytany in   |
|                 |                                 |the year     |
+-----------------+---------------------------------+-------------+
|prytany          |:py:class:`Prytanies.I`          |Constant     |
|                 |                                 |representing |
|                 |                                 |the prytany  |
+-----------------+---------------------------------+-------------+
|prytany_length   |37                               |Length of    |
|                 |                                 |this prytany |
+-----------------+---------------------------------+-------------+
|day              |1                                |Day of the   |
|                 |                                 |prytany      |
+-----------------+---------------------------------+-------------+
|doy              |1                                |Day of the   |
|                 |                                 |year         |
+-----------------+---------------------------------+-------------+
|year             |'BCE 407/406'                    |Julian       |
|                 |                                 |year(s)      |
|                 |                                 |corresponding|
|                 |                                 |to the       |
|                 |                                 |conciliar    |
|                 |                                 |year         |
+-----------------+---------------------------------+-------------+
|year_length      |366                              |Length of    |
|                 |                                 |this         |
|                 |                                 |conciliar    |
|                 |                                 |year         |
+-----------------+---------------------------------+-------------+
|astronomical_year|-406                             |Astronomical |
|                 |                                 |year         |
+-----------------+---------------------------------+-------------+

Instead of month constants there are prytany constants,
:py:enum:`Prytanies`, and the prytanies are designated by roman
numerals, which you can get from :py:func:`prytany_label`:

>>> pryt_year = pryt.prytany_calendar(-406)
>>> pryt.prytany_label(pryt_year[0].prytany)
'I'

Or you can simply use the :py:enum:`Prytany` object as an ``int``

>>> pryt_year = pryt.prytany_calendar(-406)
>>> int(pryt_year[0].prytany)
1

All the date formatting functions, like :py:func:`heniautos.as_julian`
and :py:func:`as_gregorian` work just the same on the ``jdn``
property:

>>> pryt_year = pryt.prytany_calendar(-406)
>>> ha.as_julian(pryt_year[0].jdn)
'BCE 0407-Jul-10'
>>> ha.as_gregorian(pryt_year[0].jdn)
'BCE 0407-Jul-05'

Just as the festival calendar functions return a tuple consisting of
one :py:enum:`heniautos.FestivalDay` for each day,
:py:func:`prytany_calendar` returns a tuple of one
:py:enum:`heniautos.PrytanyDay` for each day. This can be grouped into
prytanies with :py:func:`by_prytanies`:

>>> pryt_year = pryt.prytany_calendar(-406)
>>> len(pryt_year)
366
>>> pryts = pryt.by_prytanies(pryt_year)
>>> len(pryts)
10
>>> pryts[0][0].prytany
<Prytanies.I: 1>
>>> pryts[1][0].prytany
<Prytanies.II: 2>

.. _prytany-types:

Types of Conciliar Calendars
----------------------------

The conciliar calendar changed over time, so the length and the number of prytanies depends on the year and the number of tribes that existed at the time. :py:func:`prytany_calendar` has a parameter, ``pryt_type``, to specify this. The default, :py:enum:`Prytany.AUTO` will decide based on the year:

+----------+----------------------------------------+---------+-------+
|Years     |Constant                                |Prytanies|Days   |
+==========+========================================+=========+=======+
|before 508|Raises                                  |         |       |
|          |:py:class:`heniautos.HeniautosError`    |         |       |
|          |                                        |         |       |
|          |                                        |         |       |
|          |                                        |         |       |
|          |                                        |         |       |
+----------+----------------------------------------+---------+-------+
|508–376   |:py:enum:`Prytany.QUASI_SOLAR`          |10       |366    |
+----------+----------------------------------------+---------+-------+
|375-307   |:py:enum:`Prytany.ALIGNED_10`           |10       |354/384|
+----------+----------------------------------------+---------+-------+
|306–224   |:py:enum:`Prytany.ALIGNED_12`           |12       |354/384|
+----------+----------------------------------------+---------+-------+
|223–201   |:py:enum:`Prytany.ALIGNED_13`           |13       |354/384|
+----------+----------------------------------------+---------+-------+
|200–101   |:py:enum:`Prytany.ALIGNED_12`           |12       |354/384|
+----------+----------------------------------------+---------+-------+
|after 101 |:py:enum:`Prytany.ALIGNED_10`           |10       |354/384|
+----------+----------------------------------------+---------+-------+

Use :py:func:`prytany_type` to determine the default type of prytanies
for any year:

>>> pryt.prytany_type(-370)
<Prytany.ALIGNED_10: 2>

Since the conciliar year was created to manage the business of the
democratic ouncil and Assembly, it certainly did not exist before the
establishment of democracy in 508 BCE. :py:func:`prytany_calendar`
with :py:enum:`Prytany.AUTO` will therefore raise an exception if you
give it a year before then.

It almost certainly was not established that early—the first mentions
of prytanies occur in inscriptions which are probably from the 450s
(IG I³ 7, IG I³ 9, IG I³ 10), but :py:enum:`Prytany.AUTO` will treat a
date between 508 and 376 as :py:enum:`Prytany.QUASI_SOLAR`. This is
the most complicated kind of prytany, so we will describe it last.

The "aligned" types all mean the the conciliar year began and ended at
the same time as the festival year. The length of each prytany depends
on the number of prytanies at the time, and whether the year was
ordinary (354 days) or intercalary (384) days

.. _ten-prytanies:

Ten Prytanies
^^^^^^^^^^^^^

For :py:enum:`Prytany.ALIGNED_10`, there are ten prytanies that must
be distributed over 354 or 384 days. Since these numbers do not divide
evenly by 10, the remainder was distributed over a few prytanies so
that four had 36 days and the other six 35. Aristotle tells us that
the longer prytanies came first, followed by the shorter (*AthPol*
43.2). This is called the "Rule of Aristotle":

>>> pryt_year = pryt.prytany_calendar(-347)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 36)
(<Prytanies.II: 2>, 36)
(<Prytanies.III: 3>, 36)
(<Prytanies.IV: 4>, 36)
(<Prytanies.V: 5>, 35)
(<Prytanies.VI: 6>, 35)
(<Prytanies.VII: 7>, 35)
(<Prytanies.VIII: 8>, 35)
(<Prytanies.IX: 9>, 35)
(<Prytanies.X: 10>, 35)

While an intercalary festival year had thirteen months rather than
twelve, the conciliar still had ten prytanies, distributed now over
384 days into four prytanies of 39 days and six of 38:

>>> pryt_year = pryt.prytany_calendar(-348)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 39)
(<Prytanies.II: 2>, 39)
(<Prytanies.III: 3>, 39)
(<Prytanies.IV: 4>, 39)
(<Prytanies.V: 5>, 38)
(<Prytanies.VI: 6>, 38)
(<Prytanies.VII: 7>, 38)
(<Prytanies.VIII: 8>, 38)
(<Prytanies.IX: 9>, 38)
(<Prytanies.X: 10>, 38)

Twelve Prytanies
^^^^^^^^^^^^^^^^

In 306, two more tribes were added. Under twelve tribes, prytanies had
29 and 30 days in ordinary years (:py:enum:`Prytany.ALIGNED_12`), just
like the festival calendar. We generally believe that these prytanies
followed the pattern of hollow and full months exactly. If you were to
compare this conciliar calendar example for the year 300 with the
festival calendar generated for the same year, you would see the 29-
and 30-day months and prytanies were the same:

>>> pryt_year = pryt.prytany_calendar(-299)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 29)
(<Prytanies.II: 2>, 29)
(<Prytanies.III: 3>, 30)
(<Prytanies.IV: 4>, 29)
(<Prytanies.V: 5>, 30)
(<Prytanies.VI: 6>, 30)
(<Prytanies.VII: 7>, 29)
(<Prytanies.VIII: 8>, 30)
(<Prytanies.IX: 9>, 30)
(<Prytanies.X: 10>, 29)
(<Prytanies.XI: 11>, 30)
(<Prytanies.XII: 12>, 29)

However, there is another possibility. A strict application of the
"Rule of Aristotle" would mean that the 30-day prytanies would all
come at the beginning of the year, even if this meant the months and
prytanies were only slighltly out of sync. This can be forced with
``rule_of_aristotle=True``, which makes the conciliar calendar of 300
look like this:

>>> pryt_year = pryt.prytany_calendar(-299, rule_of_aristotle=True)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 30)
(<Prytanies.II: 2>, 30)
(<Prytanies.III: 3>, 30)
(<Prytanies.IV: 4>, 30)
(<Prytanies.V: 5>, 30)
(<Prytanies.VI: 6>, 30)
(<Prytanies.VII: 7>, 29)
(<Prytanies.VIII: 8>, 29)
(<Prytanies.IX: 9>, 29)
(<Prytanies.X: 10>, 29)
(<Prytanies.XI: 11>, 29)
(<Prytanies.XII: 12>, 29)

In intercalary years, prytanies are uniformly 32-days long:

>>> pryt_year = pryt.prytany_calendar(-300)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 32)
(<Prytanies.II: 2>, 32)
(<Prytanies.III: 3>, 32)
(<Prytanies.IV: 4>, 32)
(<Prytanies.V: 5>, 32)
(<Prytanies.VI: 6>, 32)
(<Prytanies.VII: 7>, 32)
(<Prytanies.VIII: 8>, 32)
(<Prytanies.IX: 9>, 32)
(<Prytanies.X: 10>, 32)
(<Prytanies.XI: 11>, 32)
(<Prytanies.XII: 12>, 32)

Thirteen Tribes
^^^^^^^^^^^^^^^

From 223 to 201 there were thirteen tribes
(:py:enum:`Prytany.ALIGNED_13`). Prytanies are 28 or 27 days long in
ordinary years and the Rule of Aristotle always applies

>>> pryt_year = pryt.prytany_calendar(-219)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 28)
(<Prytanies.II: 2>, 28)
(<Prytanies.III: 3>, 28)
(<Prytanies.IV: 4>, 27)
(<Prytanies.V: 5>, 27)
(<Prytanies.VI: 6>, 27)
(<Prytanies.VII: 7>, 27)
(<Prytanies.VIII: 8>, 27)
(<Prytanies.IX: 9>, 27)
(<Prytanies.X: 10>, 27)
(<Prytanies.XI: 11>, 27)
(<Prytanies.XII: 12>, 27)
(<Prytanies.XIII: 13>, 27)

In the intercalary years the thirteen prytanies are 29 and 30 days. By
default they follow the festival months:

>>> pryt_year = pryt.prytany_calendar(-218)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 29)
(<Prytanies.II: 2>, 30)
(<Prytanies.III: 3>, 29)
(<Prytanies.IV: 4>, 30)
(<Prytanies.V: 5>, 29)
(<Prytanies.VI: 6>, 30)
(<Prytanies.VII: 7>, 29)
(<Prytanies.VIII: 8>, 30)
(<Prytanies.IX: 9>, 29)
(<Prytanies.X: 10>, 30)
(<Prytanies.XI: 11>, 30)
(<Prytanies.XII: 12>, 29)
(<Prytanies.XIII: 13>, 30)

But you can choose to apply the Rule of Aristotle:

>>> pryt_year = pryt.prytany_calendar(-218, rule_of_aristotle=True)
>>> pryts = pryt.by_prytanies(pryt_year)
>>> for p in pryts:
...     (p[0].prytany, len(p))
...
(<Prytanies.I: 1>, 30)
(<Prytanies.II: 2>, 30)
(<Prytanies.III: 3>, 30)
(<Prytanies.IV: 4>, 30)
(<Prytanies.V: 5>, 30)
(<Prytanies.VI: 6>, 30)
(<Prytanies.VII: 7>, 30)
(<Prytanies.VIII: 8>, 29)
(<Prytanies.IX: 9>, 29)
(<Prytanies.X: 10>, 29)
(<Prytanies.XI: 11>, 29)
(<Prytanies.XII: 12>, 29)
(<Prytanies.XIII: 13>, 29)

The 2nd Century and Beyond
^^^^^^^^^^^^^^^^^^^^^^^^^^

In 200 number of prytanies was reduced to 12 again , which lasted for
the rest of the 2nd century (:py:enum:`Prytany.ALIGNED_12`).

About the beginning of the first century BCE, the Greek lunisolar
calendar was replaced by the Julian calendar. From 101 BCE on,
:py:enum:`Prytany.AUTO` will generate 10-tribe
(:py:enum:`Prytany.ALIGNED_10`) prytanies. At this point the Greek
calendars are purely imaginary, and the ten tribe calendar is probably
the most interesting if you want to generate a hypthetical calendar
for, say, the current year.

The Quasi-Solar Conciliar Year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the 5th century BCE the conciliar year was 366 days long: six
37-day prytanies and four 36-day. This is sometimes called
"quasi-solar" since it is almost a true solar year (some have
theorized that it *was* truly solar--365 days with an occasional leap
day--but all the best evidence indicates 366). We can't say for
certain when Athenians began to use this, or when they changed to the
"aligned years" except that the quasi-solar year was probably in use
in the 450s when inscriptions first mention prytanies (IG I³ 7, IG I³
9, IG I³ 10), and when still in use in 407 we have the last
inscription with evidence for it (IG I³ 377).

:py:enum:`Prytany.AUTO` assigns :py:enum:`Prytany:QUASI_SOLAR` to the
year 508 to 376. 508 is the earliest it *could* have been in use
because democracy was established at Athens that year and the calendar
was created to manage the business of the democratic Assembly. The
Assembly almost certainly did not function yet as it would after the
450s, 508 will do for lack of a better starting year. Since, the last
year that the quasi-solar calendar was in use is 407 and the first
year we have evidence for the "aligned calendar" is 346 (IG XII,6
1.261), 376 is chosen simply as midway between the two. For serious
use then, be very skeptical of concilar calendars generated with
:py:enum:`Prytany.AUTO` before about 435 and between 407 and 346.

We also are not certain of the first and/or last day of any particular
quasi-solar calendar year. The "aligned years" can be calculated, like
the festival years, from solstices and new moons. Instead we need a
"calendar equation" that will tell us the same day on the festival and
conciliar calendars. The best such equation comes from `IG I³ 377
<https://epigraphy.packhum.org/text/389?hs=3212-3227%2C3241-3271%2C3372-3387%2C3405-3426>`_
lines 24–25 and tells that in 407 BCE Hekatombaiṓn 20 was also Prytany
1.20 which in turn means that Hek 1 = Prytany 1.1 (this looks the same
as the "aligned" calendar but is just a coincidence). Heniautos
calculates that Hek 1, 407 was July 10

>>> ha.as_julian(ha.athenian_festival_calendar(-406)[0].jdn)
'BCE 0407-Jul-10'

By default, this is as the date from which all
:py:enum:`Prytany.QUASI_SOLAR` calendars are calculated:

>>> ha.as_julian(pryt.prytany_calendar(-406)[0].jdn)
'BCE 0407-Jul-10'

Based in this, the beginning of the next conciliar year would be 366
days later, while the beginning of the next festival year would be 354
days later (and thus they would be out of sync again)

>>> ha.as_julian(pryt.prytany_calendar(-405)[0].jdn)
'BCE 0406-Jul-11'
>>> ha.as_julian(ha.athenian_festival_calendar(-405)[0].jdn)
'BCE 0406-Jun-30'

You can change this reference point by providing a JDN as the
`pryt_start` parameter of :py:func:`prytany_calendar`. This JDN will
be treated as Prytany 1.1 in whatever year it occurs, and all other
:py:enum:`Prytany.QUASI_SOLAR` conciliar years will begin some
multiple fo 366 days before or after this. The default value is
1572957 (Hek 1, 407 = July 10, 407 BCE)

>>> pryt.prytany_calendar(-406)[0].jdn
1572957

If you wanted to see what the conciliar calendar would look like if it
began 10 days earlier that this, you would assign 1572847 to
`pryt_start`:

>>> ha.as_julian(pryt.prytany_calendar(-406, pryt_start=1572947)[0].jdn)
'BCE 0407-Jun-30'

Lunar and Solar Offsets
-----------------------

Because a festival calendar must usually be calculated in order to
match a conciliar calendar to it, :py:func:`prytany_calendar`, and
other prytany functions, have `v_off` and `s_off` parameters, like
:py:func:`heniautos.athenian_festival_calendar` (see
:ref:`first-of-month` and :ref:`solstice-day`)

Finding Conciliar Calendar Dates
--------------------------------

There are functions for finding concilar calendar dates by JDN,
Julian, and Gregorian dates, simlar to the festival calendar (see
:ref:`finding-dates`).

:py:func:`jdn_to_prytany_day`

>>> pryt_day = pryt.jdn_to_prytany_day(1575526)
>>> pryt_day
PrytanyDay(jdn=1575526, prytany_index=1, prytany=<Prytanies.I: 1>, prytany_length=37, day=8, doy=8, year='BCE 400/399', year_length=366, astronomical_year=-399)
>>> ha.as_julian(pryt_day)
'BCE 0400-Jul-22'

:py:func:`julian_to_prytany_day`

>>> julian_day = pryt.julian_to_prytany_day(-399, 7, 22)
>>> julian_day
PrytanyDay(jdn=1575526, prytany_index=1, prytany=<Prytanies.I: 1>, prytany_length=37, day=8, doy=8, year='BCE 400/399', year_length=366, astronomical_year=-399)

:py:func:`gregorian_to_prytany_day`

>>> gregorian_day = pryt.gregorian_to_prytany_day(-399, 7, 22)
>>> gregorian_day
PrytanyDay(jdn=1575531, prytany_index=1, prytany=<Prytanies.I: 1>, prytany_length=37, day=13, doy=13, year='BCE 400/399', year_length=366, astronomical_year=-399)
