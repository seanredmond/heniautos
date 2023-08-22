.. _festival-calendars:

Festival Calendars
==================

.. currentmodule:: heniautos

This section will cover the function for generating specific festival
calendars:

* :py:func:`athenian_festival_calendar`
* :py:func:`argive_festival_calendar`
* :py:func:`corinthian_festival_calendar`
* :py:func:`delian_festival_calendar`
* :py:func:`delphian_festival_calendar`
* :py:func:`spartan_festival_calendar`
    
as well as a generic function that allows you to choose the parameters
to generate any festival calendar, :py:func:`festival_calendar`.

In addition, it introduces some utility functions:

* :py:func:`bce_as_negative`
* :py:func:`negative_as_bce`
* :py:func:`as_julian`
* :py:func:`as_gregorian`
* :py:func:`by_months`

All the code snippets below assume that you have imported :py:mod:`heniautos` under the name `ha` like so:

>>> import heniautos as ha

The city-specific calendars differ in the times when the years start
and in the names of the months. The generic
:py:func:`festival_calendar` method allows you to choose these
parameters for any other required Greek calendar (the specific methods
above are simply wrappers around :py:func:`festival_calendar`).

The examples below will use :py:func:`athenian_festival_calendar`
since this is the one you are probably most interested in. This and
all the city-specific functions take the same parameters and most
parameters are optional. For the simplest use only the year is
required. The year, however, must be an integer according to
`Astronomical Year Numbering
<https://en.wikipedia.org/wiki/Astronomical_year_numbering>`_. Years
BCE are represented as negative numbers but 1 BCE is 0 (not -1), 2 BCE
is -1, and so on, with the years offset by 1 in the positive
direction. To generate a calendar for 400 BCE:

>>> calendar = ha.athenian_festival_calendar(-399)

If you don't want to work out the astronomical year numbering every time, you can use :py:func:`bce_as_negative`:

>>> ha.bce_as_negative(400)
-399

So these two invocations are equivalent:

>>> calendar = ha.athenian_festival_calendar(-399)
>>> calendar = ha.athenian_festival_calendar(ha.bce_as_negative(400))

:py:func:`bce_as_negative` is its own inverse but, so you don't have to remember that (and because it could lead to some obscure code), there is an explicit inverse function :py:func:`negative_as_bce`:

>>> ha.bce_as_negative(400)
-399
>>> ha.bce_as_negative(-399)
400
>>> ha.negative_as_bce(-399)
400

Year Tuples and :py:class:`FestivalDay` Objects
-----------------------------------------------

The calendar functions return a tuple of :py:class:`FestivalDay`
objects (which are instances of :py:class:`namedtuple`), one
:py:class:`FestivalDay` for each day of the year.

>>> calendar = ha.athenian_festival_calendar(-399)
>>> len(calendar)
354
>>> calendar[0]
FestivalDay(jdn=1575526, month_name='Hekatombaiṓn', month_index=1, month=<AthenianMonths.HEK: 1>, month_length=29, day=1, doy=1, year='BCE 400/399', year_length=354, astronomical_year=-399)

The first item in the tuple in the example above would have these
properties and values:


+-----------------+-----------------------------+---------------+
|Property         |Value                        |Meaning        |
+=================+=============================+===============+
|jdn              |1575526                      |Corresponding  |
|                 |                             |Julian Day     |
|                 |                             |Number         |
+-----------------+-----------------------------+---------------+
|month_name       |'Hekatombaiṓn'               |Name of        |
|                 |                             |Athenian month |
+-----------------+-----------------------------+---------------+
|month_index      |1                            |Order of month |
|                 |                             |in the year    |
+-----------------+-----------------------------+---------------+
|month            |:py:enum:`AthenianMonths.HEK`|Constant       |
|                 |                             |representing   |
|                 |                             |the month      |
+-----------------+-----------------------------+---------------+
|month_length     |29                           |Length of this |
|                 |                             |month          |
+-----------------+-----------------------------+---------------+
|day              |1                            |Day of the     |
|                 |                             |month          |
+-----------------+-----------------------------+---------------+
|doy              |1                            |Day of the year|
+-----------------+-----------------------------+---------------+
|year             |'BCE 400/399'                |Julian year(s) |
|                 |                             |corresponding  |
|                 |                             |to the Athenian|
|                 |                             |year           |
+-----------------+-----------------------------+---------------+
|year_length      |354                          |Length of this |
|                 |                             |year           |
+-----------------+-----------------------------+---------------+
|astronomical_year|-399                         |Astronomical   |
|                 |                             |year           |
+-----------------+-----------------------------+---------------+

Altogether, this means that this is the first day (:py:attr:`doy` = 1)
of the Athenian year 400/399 BCE. This year (or actually the beginning
of the year) corresponds to the astronomical year -399 (that is, 400
BCE) and the year is calculated to be 354 days long. It is also the
first day (:py:attr:`day` = 1) of the first month
(:py:attr:`month_index` = 1). The month's name is Hekatombaiṓn, and it
has 29 days.

Grouping by Month
-----------------

The tuples returned by the festival calendar function contain one
object per day. For convenience, there is a :py:func:`by_months`
function that will group this into a tuple of tuples. Each member of
the outer tuple represents a month and contains a tuple of
:py:class:`FestivalDay` objects for the days in that month.

>>> year = ha.athenian_festival_calendar(ha.bce_as_negative(400))
>>> len(year)
354
>>> (year[0].month_name, year[0].day)
('Hekatombaiṓn', 1)
>>> (year[1].month_name, year[1].day)
('Hekatombaiṓn', 2)
>>>
>>> months = ha.by_months(year)
>>> len(months)
12
>>> len(months[0])
29
>>> (months[0][0].month_name, months[0][0].day)
('Hekatombaiṓn', 1)
>>> (months[1][0].month_name, months[1][0].day)
('Metageitniṓn', 1)

Julian Day Numbers
------------------

No modern (that is, Gregorian or Julian) calendar date is included in
:py:class:`FestivalDay` objects, but this can be calculated
:py:attr:`jdn` property. `The Julian Day Number
<https://en.wikipedia.org/wiki/Julian_day>`_ is the number of the day
counting from January 1, 4713 BCE, a system devised by `Joseph
Scaliger <https://en.wikipedia.org/wiki/Joseph_Justus_Scaliger>`_, a
classical scholar, in 1583 and still used by astronomers and
chronologists today. For modern (or modern-like) versions of ancient
dates, historians usually employ the `Proleptic Julian Calendar
<https://en.wikipedia.org/wiki/Proleptic_Julian_calendar>`_, so you
will probably want to use :py:func:`as_julian` to convert the JDN into
a string equivalent of a Julian calendar date:

>>> ha.as_julian(1575526)
'BCE 0400-Jul-22'

For a `Proleptic Gregorian Calendar
<https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar>`_ date,
use :py:func:`as_gregorian()`:

>>> ha.as_gregorian(1575526)
'BCE 0400-Jul-17'

Heniautos uses the :py:mod:`juliandate` package for these
conversations. For more detail refer to that `documentation
<https://github.com/seanredmond/juliandate>`_.

.. attention::
   Note that there is no conversion to a Python date or datetime
   available because the datetime library does not handle BCE dates.


Julian and Gregorian Dates
^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:func:`as_julian` and :py:func:`as_gregorian` have some further
options. With ``full=True`` the output includes the time (HH:MM:SS)
and timezone (GMT by default). Note that Julian Days start at noon, so
any decimal part indicates the fraction of 24 hours following noon and
therefore anything past .5 (midnight) actually falls into the next
(Julio-Gregorian) day

>>> ha.as_julian(1575526, full=True)
'BCE 0400-Jul-22 12:00:00 GMT'
>>> ha.as_julian(1575526.78, full=True)
'BCE 0400-Jul-23 06:43:12 GMT'
>>> ha.as_gregorian(1575526, full=True)
'BCE 0400-Jul-17 12:00:00 GMT'
>>> ha.as_gregorian(1575526.78, full=True)
'BCE 0400-Jul-18 06:43:12 GMT'

.. _time-zones:

Time Zones
^^^^^^^^^^

The ``tz`` parameter takes one of two options:
:py:enum:`TZOptions.GMT` (The default) or
:py:enum:`TZOptions.ALT`. Since there were no time zones and no
daylight savings time in the ancient world, ALT is an invented
"timezone" that advances the time about 1 hour 35 minutes to reflect
the fact that Athens is about 23.73 degrees east of the meridian. That
is, if you were measuring time exactly by the sun, by the time it
reaches noon in Greenwich, it is already almost 1:35 PM in Athens.

>>> ha.as_julian(1575526.78, full=True, tz=ha.TZOptions.ALT)
'BCE 0400-Jul-23 08:18:06 ALT'
>>> ha.as_gregorian(1575526.78, full=True, tz=ha.TZOptions.ALT)
'BCE 0400-Jul-18 08:18:06 ALT'

Month Names
-----------

The optional ``name_as`` parameter controls the form of the
``month_name`` property of the :py:class:`FestivalDay` objects. The
choices are: transliteration (default), abbreviation, and Greek. It
takes one of the :py:enum:`MonthNameOptions` values.

The default is transliteration, which you can choose explicitly with
:py:enum:`MonthNameOptions.TRANSLITERATION`:

>>> ha.athenian_festival_calendar(-399)[0].month_name
'Hekatombaiṓn'
>>> ha.athenian_festival_calendar(-399, name_as=ha.MonthNameOptions.TRANSLITERATION)[0].month_name
'Hekatombaiṓn'

For abbreviations use :py:enum:`ha.MonthNameOptions.ABBREV`:

>>> ha.athenian_festival_calendar(-399, name_as=ha.MonthNameOptions.ABBREV)[0].month_name
'Hek'

And to get the month names in Greek, use :py:enum:`ha.MonthNameOptions.GREEK`:

>>> ha.athenian_festival_calendar(-399, name_as=ha.MonthNameOptions.GREEK)[0].month_name
'Ἑκατομβαιών'

Intercalated Month
------------------

When intercalations are required (see Festival Calendar Basics)
Heniautos intercalates some default month (usually the sixth), but
this can be controlled with the ``intercalate`` parameter.

For example, 211/210 BCE should be an intercalary year. By default the intercalated month will be a second Posideiṓn, *Posideiṓn hústeros*.

>>> year = ha.athenian_festival_calendar(-210)
>>> months = ha.by_months(year)
>>> month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...	
('BCE 0211-Jul-04', 'Hekatombaiṓn')
('BCE 0211-Aug-02', 'Metageitniṓn')
('BCE 0211-Aug-31', 'Boēdromiṓn')
('BCE 0211-Sep-30', 'Puanopsiṓn')
('BCE 0211-Oct-29', 'Maimaktēriṓn')
('BCE 0211-Nov-28', 'Posideiṓn')
('BCE 0211-Dec-27', 'Posideiṓn hústeros')
('BCE 0210-Jan-26', 'Gamēliṓn')
('BCE 0210-Feb-24', 'Anthestēriṓn')
('BCE 0210-Mar-26', 'Elaphēboliṓn')
('BCE 0210-Apr-25', 'Mounukhiṓn')
('BCE 0210-May-24', 'Thargēliṓn')
('BCE 0210-Jun-23', 'Skirophoriṓn')

However we know from an inscription, `IG II³,1 1137
<https://inscriptions.packhum.org/text/347432>`_, not only that
211/210 was an interalary year but also that Anthestēriṓn was the
intercalated month. We can recreate this by passing the right month
constant (see Month Constants below), in this case
:py:enum:`AthenianMonths.ANT`:

>>> year = ha.athenian_festival_calendar(-210, intercalate=ha.AthenianMonths.ANT)
>>> months = ha.by_months(year)
>>> month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0211-Jul-04', 'Hekatombaiṓn')
('BCE 0211-Aug-02', 'Metageitniṓn')
('BCE 0211-Aug-31', 'Boēdromiṓn')
('BCE 0211-Sep-30', 'Puanopsiṓn')
('BCE 0211-Oct-29', 'Maimaktēriṓn')
('BCE 0211-Nov-28', 'Posideiṓn')
('BCE 0211-Dec-27', 'Gamēliṓn')
('BCE 0210-Jan-26', 'Anthestēriṓn')
('BCE 0210-Feb-24', 'Anthestēriṓn hústeros')
('BCE 0210-Mar-26', 'Elaphēboliṓn')
('BCE 0210-Apr-25', 'Mounukhiṓn')
('BCE 0210-May-24', 'Thargēliṓn')
('BCE 0210-Jun-23', 'Skirophoriṓn')

.. _first-of-month:


First Day of the Month
----------------------

To the Greeks, "new moon" (νουμηνία) meant the first night that the
first sliver of the waxing crescent was visible (see Festival Calendar
Basics). We can't say exactly when this occured for any given month
since there are many variables involved, nor do we know how much the
Greeks cared about actually sighting this moon over calculating or
even just guestimating when it should be visible. Heniautos uses an
approximation, defining the day of the visible new moon as some ``N`` days
after the date of the conjunction, by default 1.

This can be changed with the ``v_off`` (for "visibility offset")
parameter. Again, the default is 1, so these are equivalent:

>>> ha.as_julian(ha.athenian_festival_calendar(-399)[0].jdn)
'BCE 0400-Jul-22'
>>> ha.as_julian(ha.athenian_festival_calendar(-399, v_off=1)[0].jdn)
'BCE 0400-Jul-22'

If you wanted to treat the new moon as visible on the day of the
conjunction you would pass ``v_off=0``. The effect would be shifting all
the dates up one day (which might have an effect on which years all
intercalary).

>>> ha.as_julian(ha.athenian_festival_calendar(-399, v_off=0)[0].jdn)
'BCE 0400-Jul-21'

Or you could use ``v_off=2`` to make the new visible two days after the day of the conjunction.

>>> ha.as_julian(ha.athenian_festival_calendar(-399, v_off=2)[0].jdn)
'BCE 0400-Jul-23'

.. _solstice-day:

Day of the Solstice
-------------------

Just as we can't be sure when (even if) the Ancient Greeks literally
sighted the new moon, we can't be sure when they observed a solstice
or equinox. By default, Heniautos treats the solstices and equinoxes
as observed on the days which they actually occurred but, to handle
the uncertainty, you can adjust this by supplying an integer with the
``s_off`` parameter.

This will only be obvious (at least with reasonable values) in the
case of intercalations. For instance, from strictly judging by
astronomical phenomena, they year 422/421 BCE should begin on July 26,
following an intercalary 423/421

>>> ha.as_julian(ha.athenian_festival_calendar(-421)[0].jdn)
'BCE 0422-Jul-26'

However, the previous new moon, on June 26 would have been very close
to the solstice that year (June 28). If the solstice was observed just
two days early, that would put it on the same day as the June 26 new
moon and the year (at least as Heniautos calculates it) would begin
the next day and in June rather than July, with the intercalation
moved from 423 to 422:

>>> ha.as_julian(ha.athenian_festival_calendar(-421, s_off=-2)[0].jdn)
'BCE 0422-Jun-27'

Something similar can be achieved by combining ``v_off`` and ``s_off``. In
this case using ``s_off=-1`` to indicate a solstice observed one day
before the true solstice and ``v_off=2`` to indicate a new moon observed
two days after the conjunction (rather than 1) you get:

>>> ha.as_julian(ha.athenian_festival_calendar(-421, s_off=-1, v_off=2)[0].jdn)
'BCE 0422-Jun-28'

In general, the default values will be good enough. There are times,
though, that you may want to explore other options. For example,
though the details are not important here, there is some reason to
believe that 422/421 BCE was intercalary and may have begun just
before summer solstice. If this is not of vital interest to you, you
probably never need to worry about ``v_off`` and ``s_off``.

Other Calendars
---------------

The various calendars of different Greek cities had different month
names and began relative to different solstices or equinoxes. They
might also differ in whether the first month followed the solstice or
equinox or the the month in which the solstice or equinox occured.

For instance, in Delphi, the year began, as in Athens, after the
summer solstice so the twelve months have the same dates as the in
Athenian year, but different names:

>>> year = ha.delphian_festival_calendar(-399)
>>> months = ha.by_months(year)
>>> month_names = month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0400-Jul-22', 'Apellaîos')
('BCE 0400-Aug-20', 'Boukátios')
('BCE 0400-Sep-19', 'Boathóos')
('BCE 0400-Oct-18', 'Heraîos')
('BCE 0400-Nov-17', 'Dadaphórios')
('BCE 0400-Dec-17', 'Poitrópios')
('BCE 0399-Jan-16', 'Amálios')
('BCE 0399-Feb-15', 'Búsios')
('BCE 0399-Mar-16', 'Theoxénios')
('BCE 0399-Apr-14', 'Enduspoitrópios')
('BCE 0399-May-14', 'Herákleios')
('BCE 0399-Jun-12', 'Ilaîos')

On Delos, some of the month names were the same as the Athenian, but
the year began after the winter solstice.

>>> year = ha.delian_festival_calendar(-399)
>>> months = ha.by_months(year)
>>> month_names = month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0399-Jan-16', 'Lēnaiṓn')
('BCE 0399-Feb-15', 'Hierós')
('BCE 0399-Mar-16', 'Galaxiṓn')
('BCE 0399-Apr-14', 'Artemisiṓn')
('BCE 0399-May-14', 'Thargēliṓn')
('BCE 0399-Jun-12', 'Pánēmos')
('BCE 0399-Jul-11', 'Hekatombaiṓn')
('BCE 0399-Aug-10', 'Metageitniṓn')
('BCE 0399-Sep-08', 'Bouphoniṓn')
('BCE 0399-Oct-08', 'Apatouriṓn')
('BCE 0399-Nov-06', 'Arēsiṓn')
('BCE 0399-Dec-06', 'Posideiṓn')

.. attention:: Something special to note about this invocation of
   :py:func:`delian_festival_calendar`. Ancient Greek years usually
   span two Julian years (the end of one and beginning of the
   next). This is why we refer to the Athenian year 400/399: because
   it begins in the middle of 400 and ends in the middle of 399. To
   get the calendar from :py:func:`athenian_festival_year` you pass it
   the first year of the span, 400 BCE or, in astronomical year
   numbering, -399. Think of this as the year of the summer solstice
   after which the year begins.

   Because the winter solstice falls near the end of December, a
   lunisolar year following this solstice will frequently not begin
   until the next Julian year. In the example above,
   ``delian_festival_calendar(-399)`` asks for the year following the
   winter solstice of 400 BCE. This year doesn't begin until January
   16, 399, though, and we would have to call it 399/398.

The Corinthian, Argive, and Spartan calendars probably all begin at
the last new moon before the autumn equinox so that the equinox falls
in the first month (unlike the Athenian, where the solstice falls in
the last month)

>>> year = ha.corinthian_festival_calendar(-399)
>>> months = ha.by_months(year)
>>> month_names = month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0400-Sep-19', 'Phoinikaîos')
('BCE 0400-Oct-18', 'Kráneios')
('BCE 0400-Nov-17', 'Lanotropíos')
('BCE 0400-Dec-17', 'Makhaneús')
('BCE 0399-Jan-16', 'Dōdekateús')
('BCE 0399-Feb-15', 'Εúkleios')
('BCE 0399-Mar-16', 'Artemísios')
('BCE 0399-Apr-14', 'Psudreús')
('BCE 0399-May-14', 'Gameílios')
('BCE 0399-Jun-12', 'Agriánios')
('BCE 0399-Jul-11', 'Pánamos')
('BCE 0399-Aug-10', 'Apellaîos')

We don't know all the names of the Spartan months or their order, so
:py:func:`spartan_festival_calendar` returns a generic calendar (see
:ref:`generic-calendar` below) in which the months are simply numbered:

>>> year = ha.spartan_festival_calendar(-399)
>>> months = ha.by_months(year)
>>> month_names = month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0400-Sep-19', '1')
('BCE 0400-Oct-18', '2')
('BCE 0400-Nov-17', '3')
('BCE 0400-Dec-17', '4')
('BCE 0399-Jan-16', '5')
('BCE 0399-Feb-15', '6')
('BCE 0399-Mar-16', '7')
('BCE 0399-Apr-14', '8')
('BCE 0399-May-14', '9')
('BCE 0399-Jun-12', '10')
('BCE 0399-Jul-11', '11')
('BCE 0399-Aug-10', '12')

The months of fully generic calendar (see :ref:`generic-calendar`,
below) have ordinal numbers as Greek names: Πρῶτος, Δεύτερος, etc. So
that a Spartan calendar cannot be confused with a truly generic
calendar, the Greek names of Spartan months are δεῖνα αʹ, δεῖνα βʹ,
etc. (which you can interpret as "Unknown 1", "Unknown 2"):

>>> year = ha.spartan_festival_calendar(-399, name_as=ha.MonthNameOptions.GREEK)
>>> months = ha.by_months(year)
>>> month_names = month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0400-Sep-19', 'δεῖνα αʹ')
('BCE 0400-Oct-18', 'δεῖνα βʹ')
('BCE 0400-Nov-17', 'δεῖνα γʹ')
('BCE 0400-Dec-17', 'δεῖνα δʹ')
('BCE 0399-Jan-16', 'δεῖνα εʹ')
('BCE 0399-Feb-15', 'δεῖνα ϛʹ')
('BCE 0399-Mar-16', 'δεῖνα ζʹ')
('BCE 0399-Apr-14', 'δεῖνα ηʹ')
('BCE 0399-May-14', 'δεῖνα θʹ')
('BCE 0399-Jun-12', 'δεῖνα ιʹ')
('BCE 0399-Jul-11', 'δεῖνα ιαʹ')
('BCE 0399-Aug-10', 'δεῖνα ιβʹ')


.. _generic-calendar:

Generic Calendar
----------------

The a function for creating a generic calendar (the calendar-specific
functions are simply wrappers around this) is :py:func:`festival_calendar`.

With the default values it returns a calendar that begins after the summer solstice with months that are simply numbered:

>>> year = ha.festival_calendar(-399)
>>> months = ha.by_months(year)
>>> month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0400-Jul-22', '1')
('BCE 0400-Aug-20', '2')
('BCE 0400-Sep-19', '3')
('BCE 0400-Oct-18', '4')
('BCE 0400-Nov-17', '5')
('BCE 0400-Dec-17', '6')
('BCE 0399-Jan-16', '7')
('BCE 0399-Feb-15', '8')
('BCE 0399-Mar-16', '9')
('BCE 0399-Apr-14', '10')
('BCE 0399-May-14', '11')
('BCE 0399-Jun-12', '12')

The Greek option gives the months named by Greek numerals. Some
calendars were actually this generic. For instance, the Achaean
calendar began after the autumn equinox, and the months were simply
numbered. With the corresponding options, we can generate this:

>>> year = ha.festival_calendar(-399, event=ha.Seasons.AUTUMN_EQUINOX, name_as=ha.MonthNameOptions.GREEK)
>>> months = ha.by_months(year)
>>> month_names = [(ha.as_julian(m[0].jdn), m[0].month_name) for m in months]
>>> for m in month_names:
...     print(m)
...
('BCE 0400-Oct-18', 'Πρῶτος')
('BCE 0400-Nov-17', 'Δεύτερος')
('BCE 0400-Dec-17', 'Τρίτος')
('BCE 0399-Jan-16', 'Τέταρτος')
('BCE 0399-Feb-15', 'Πέμπτος')
('BCE 0399-Mar-16', 'Ἕκτος')
('BCE 0399-Apr-14', 'Ἕβδομος')
('BCE 0399-May-14', 'Ὄγδοος')
('BCE 0399-Jun-12', 'Ἔνατος')
('BCE 0399-Jul-11', 'Δέκατος')
('BCE 0399-Aug-10', 'Ἑνδέκατος')
('BCE 0399-Sep-08', 'Δωδέκατος')

The ``data`` Parameter
----------------------

This parameter is used to supply your own astronomical (solstice,
equinox, and new moon data). See "Ephimerides and Custom Data" below.

Constants for Months and Seasons
--------------------------------

This section will cover constants used to identify various calendar
months (:py:enum:`AthenianMonths`, :py:enum:`ArgiveMonths`,
:py:enum:`CorinthianMonths`, :py:enum:`DelianMonths`,
:py:enum:`DelphianMonths`, and :py:enum:`GenericMonths`) and those
used to identify seasons (that is solstices and equinoxes)
:py:enum:`Seasons`

It also introduces functions that use these constants to retrieve
month names and dates for solstices, equinoxes, and new moons.

* :py:func:`solar_event`
* :py:func:`observed_solar_event`
* :py:func:`new_moons`
* :py:func:`visible_new_moons`

.. _month-constant:
  
Months
^^^^^^

Months are represented by one set of constants for each calendar
available in Heniautos. Each constant has an integer value that is the
normal position of the month in the given calendar. For instance, for
the Athenian calendar the constants come from
:py:enum:`AthenianMonths`:

>>> for m in tuple(ha.AthenianMonths):
...     m
...
<AthenianMonths.HEK: 1>
<AthenianMonths.MET: 2>
<AthenianMonths.BOE: 3>
<AthenianMonths.PUA: 4>
<AthenianMonths.MAI: 5>
<AthenianMonths.POS: 6>
<AthenianMonths.GAM: 7>
<AthenianMonths.ANT: 8>
<AthenianMonths.ELA: 9>
<AthenianMonths.MOU: 10>
<AthenianMonths.THA: 11>
<AthenianMonths.SKI: 12>

The integer values can be used:

>>> int(ha.AthenianMonths.SKI)
12
>>> ha.AthenianMonths.SKI > ha.AthenianMonths.HEK
True

The month property of a :py:class:`FestivalDay` contains the month
constant. Due to intercalation, this value may not be the same as the
position of the given month in a given year. The position of the month
in a year should always be determined by the ``month_index`` property
of a :py:class:`FestivalDay`. In an ordinary year, like 426 BCE, the
constant values will correspond to the month indices. If we examine
Elaphēboliṓn (normally the 9th month) 426, for instance:

>>> m = ha.by_months(ha.athenian_festival_calendar(-425))
>>> (m[8][0].month_index, m[8][0].month)
(9, <AthenianMonths.ELA: 9>)	

If 425 BCE is intercalary though, and the intercalary month is the 6th, Posideiṓn, Elaphēboliṓn, will be the tenth month:

>>> m = ha.by_months(ha.athenian_festival_calendar(-424))
>>> (m[5][0].month_index, m[5][0].month)
(6, <AthenianMonths.POS: 6>)
>>> (m[6][0].month_index, m[6][0].month)
(7, <Months.INT: 13>)
>>> (m[9][0].month_index, m[9][0].month)
(10, <AthenianMonths.ELA: 9>)

.. attention:: Note that the intercalary month is always assigned the month
   constant :py:enum:`Months.INT` (regardless of the specific
   calendar).

The other month constants are :py:enum:`ArgiveMonths`,
:py:enum:`CorinthianMonths`, :py:enum:`DelianMonths`,
:py:enum:`DelphianMonths`, and :py:enum:`GenericMonths`. Some months
on different calendars have the same names but they are represented by
different constants. For instance, Hekatombaiṓn occurs both on the
Athenian calendar, as the first month, and the Delian calendar, as the
seventh (though they usually occur at the same time since the Delian
year begins six months before the Athenian). These are represented by
two different constants:

>>> ha.AthenianMonths.HEK
<AthenianMonths.HEK: 1>
>>> ha.DelianMonths.HEK
<DelianMonths.HEK: 7>
>>> ha.AthenianMonths.HEK == ha.DelianMonths.HEK
False

:py:func:`spartan_festival_calendar` returns :py:enum:`GenericMonths`
because we do not know the actual months:

>>> ha.spartan_festival_calendar(-399)[0].month
<GenericMonths.M01: 1>

Use the :py:func:`month_name` function to convert a constant to its
transliterated name (default), abbreviation, or Greek name.

>>> ha.month_name(ha.AthenianMonths.HEK)
'Hekatombaiṓn'
>>> ha.month_name(ha.AthenianMonths.HEK, name_as=ha.MonthNameOptions.ABBREV)
'Hek'
>>> ha.month_name(ha.AthenianMonths.HEK, name_as=ha.MonthNameOptions.GREEK)
'Ἑκατομβαιών'

Seasons
^^^^^^^

We saw the :py:enum:`Seasons` constants above under the
:ref:`generic-calendar`. These identify the solstices and equinoxes
that are important to Greek calendars:

>>> for s in ha.Seasons:
...     s
...
<Seasons.SPRING_EQUINOX: 0>
<Seasons.SUMMER_SOLSTICE: 1>
<Seasons.AUTUMN_EQUINOX: 2>
<Seasons.WINTER_SOLSTICE: 3>

To find the date of a historical solstice or equinox, use
:py:func:`solar_event()` or :py:func:`observed_solar_event` with one
of these constants. The difference between the two is that
:py:func:`solar_event` returns the exact Julian Date of the event
(that is, the astronomical truth):

>>> ha.solar_event(-399, ha.Seasons.SUMMER_SOLSTICE)
1575501.7962411924
>>> ha.as_julian(ha.solar_event(-399, ha.Seasons.SUMMER_SOLSTICE), full=True)
'BCE 0400-Jun-28 07:06:35 GMT'

:py:func:`observed_solar_event` returns the event rounded to the
nearest Julian Day Number, optionally adjusted by the offset ``s_off``
(discussed under :ref:`solstice-day`)

>>> ha.observed_solar_event(-399, ha.Seasons.SUMMER_SOLSTICE)
1575502
>>> ha.as_julian(ha.observed_solar_event(-399, ha.Seasons.SUMMER_SOLSTICE), full=True)
'BCE 0400-Jun-28 12:00:00 GMT'
>>> ha.as_julian(ha.observed_solar_event(-399, ha.Seasons.SUMMER_SOLSTICE, s_off=-1), full=True)
'BCE 0400-Jun-27 12:00:00 GMT'	

Like solar events, there are functions for new moons and visible new
moons. :py:func:`new_moons` returns exact Julian Dates, while
:py:func:`visible_new_moons` are rounded to the nearest Julian Day
Number with an offset. As with ``v_off`` (see :ref:`first-of-month`)
the default offset is 1 day. They also return tuples containing the
dates of all the new moons in the calendar (not the Greek) year

>>> ha.new_moons(-399)
(1575348.655074811, 1575378.1413952103, 1575407.517358738, 1575436.8253117797, 1575466.1110969426, 1575495.4158226792, 1575524.7752166032, 1575554.222185349, 1575583.7858906111, 1575613.4801067342, 1575643.281607354, 1575673.119159554)
>>> ha.visible_new_moons(-399)
(1575350, 1575379, 1575409, 1575438, 1575467, 1575496, 1575526, 1575555, 1575585, 1575614, 1575644, 1575674)
>>> ha.visible_new_moons(-399, v_off=2)
(1575351, 1575380, 1575410, 1575439, 1575468, 1575497, 1575527, 1575556, 1575586, 1575615, 1575645, 1575675)

Internally, these functions are used to determine the dates of months
in the Greek year, and most importantly, when the year starts. If the
observed summer solstice of 400 BCE is on JDN 1575502 (June 28), then
the next year begins at the first visible new moon after, which falls
on JDN 1575526 (July 22) and the following months begin on each
following visible new moon.

.. _finding-dates:


Finding Festival Calendar Dates
-------------------------------

You can find a festival calendar date from a Julian Day Number with
:py:func:`jdn_to_festival_day`:

>>> fest_day = ha.jdn_to_festival_day(1575526)
>>> fest_day
FestivalDay(jdn=1575526, month_name='Hekatombaiṓn', month_index=1, month=<AthenianMonths.HEK: 1>, month_length=29, day=1, doy=1, year='BCE 400/399', year_length=354, astronomical_year=-399)
>>> ha.as_julian(fest_day)
'BCE 0400-Jul-22'

With :py:func:`julian_to_festival_day` you can find a festival
calendar date with a Julian year, month, and day. As usual, the year
must be given in `Astronomical Year Numbering
<https://en.wikipedia.org/wiki/Astronomical_year_numbering>`_, the
month and day must be integers:

>>> julian_day = ha.julian_to_festival_day(-399, 7, 22)
>>> julian_day
FestivalDay(jdn=1575526, month_name='Hekatombaiṓn', month_index=1, month=<AthenianMonths.HEK: 1>, month_length=29, day=1, doy=1, year='BCE 400/399', year_length=354, astronomical_year=-399)
>>> ha.as_julian(julian_day)
'BCE 0400-Jul-22'
>>> ha.as_gregorian(julian_day)
'BCE 0400-Jul-17'

:py:func:`gregorian_to_festival_day` works similarly:

>>> gregorian_day = ha.gregorian_to_festival_day(-399, 7, 22)
>>> gregorian_day
FestivalDay(jdn=1575531, month_name='Hekatombaiṓn', month_index=1, month=<AthenianMonths.HEK: 1>, month_length=29, day=6, doy=6, year='BCE 400/399', year_length=354, astronomical_year=-399)
>>> ha.as_julian(gregorian_day)
'BCE 0400-Jul-27'
>>> ha.as_gregorian(gregorian_day)
'BCE 0400-Jul-22'

.. _ephemerides:

Ephimerides and Custom Data
---------------------------

Heniautos comes with solstice/equinox and new moon data from 605 to 1
BCE and 1896 to 2104 CE. This range should allow generating calendars
for most of the interesting years in the time of the Greeks as well as
decent coverage for hypothetical modern day calendars. This data has
been derived from the `DE431 ephemeris
<https://ssd.jpl.nasa.gov/doc/de430_de431.html>`_ published by the Jet
Propulsion Laboratory.

If you want to use a different data source or data for different years there are two ways to do it

`data` Parameter
^^^^^^^^^^^^^^^^

All the functions that rely on solar and lunar data for calculations
have an optional `data` parameter. The data provided should be a
`dict` with a `solstices` and `new_moons` keys. Each values should be
`tuple` containg more tuples of Julian Dates and codes for the kind of
date. For lunar data the only code is `0` for the new moon. For solar
data, the values are `0` = spring equinox, `1` = summer solstice, `2`
= autumn equinox, `3` = winter solstice. For instance:

>>> custom_data = {
    "solstices": (
        (1685074.3287422964, 1),
        (1685439.5648092534, 1),
    ),
    "new_moons": (
        (1684907.0310656228, 0),
        (1684936.490878384, 0),
        (1684965.8702085295, 0),
        (1685291.0009266976, 0),
        (1685320.5018709311, 0),
        (1685349.9050228074, 0),
        (1685704.4562648418, 0),
        (1685733.8966757061, 0),
    ),
}

You can also provide a function that will return data in the proper
format. This is how Heniautos works internally. The default value of
the `data` parameter is a private function that returns the default
data.

Use Ephemeris
^^^^^^^^^^^^^




