Calendar Equations
==================

.. currentmodule:: heniautos.equations

This section will cover the :py:mod:`heniautos.equations` submodule with its functions for exploring calendar equations:

- :py:func:`festival_doy`
- :py:func:`prytany_doy`
- :py:func:`equations`
- :py:func:`collations`

		   
"Calendar equations" are important evidence for historical Athenian
years. These equations mostly come from inscriptions but can be any
statement that equates afestival calendar date and a conciliar
calendar date (in the case of Athenian calendars since there can be
equations between other calendars as well).

A very simple equation is found, for instance, in the inscription `IG II³,1 338 <https://epigraphy.packhum.org/text/347195>`_, which records a decree of the Athenian assembly with a common dating formula:

    | ἐπὶ Νικοκράτους ἄρχοντος, ἐπὶ τῆς Αἰγηίδος
    | πρώτης πρυτανείας, ἧι Ἀρχέλας Χαιρίου Παλ-
    | ληνεὺς ἐγραμμάτευεν· Μεταγειτνιῶνος ἐνά-
    | τηι ἱσταμένου· ἐνάτηι καὶ τριακοστῆι τῆς ∶
    | πρυτανείας

    Under the arkhon Nikokrates, in the second prytany of Aigeis, for
    which Arkhelas Khairiou of Pallene was the secretary; ninth of
    Metageitnion; thirty-ninth of the prytany

Or, to put the equation more succinctly:

    Metageitnion 9 = Prytany 1.39

Nikokrates was arkhon in 333/332 BCE. The question this is, what can
the calendar tell us about the calendars of that year? The
:py:mod:`heniautos.equations` sub-package has functions for exploring
this question.

The code examples on this page assume that the heniautos packages have
been imported like this:

>>> import heniautos as ha
>>> import heniautos.prytanies as pryt
>>> import heniautos.equations as eq

Day of the Year (Festival)
--------------------------

Because the months can be different lengths (29 or 30 days) and because any month (but the first) might be preceded by an intercalary month, we might first ask what days of the year can Met 9 be? :py:func:`festival_doy` can tell us:

>>> for e in eq.festival_doy(ha.AthenianMonths.MET, 9):
...     e
...
FestivalDOY(date=(<AthenianMonths.MET: 2>, 9), doy=38, preceding=(29,), intercalation=False)
FestivalDOY(date=(<AthenianMonths.MET: 2>, 9), doy=39, preceding=(30,), intercalation=False)
FestivalDOY(date=(<AthenianMonths.MET: 2>, 9), doy=67, preceding=(29, 29), intercalation=True)
FestivalDOY(date=(<AthenianMonths.MET: 2>, 9), doy=68, preceding=(30, 29), intercalation=True)
FestivalDOY(date=(<AthenianMonths.MET: 2>, 9), doy=69, preceding=(30, 30), intercalation=True)

The :py:func:`festival_doy` function takes a month constant (see
:ref:`month-constant`) and the number of a day. It returns a tuple,
containing dicts. Each dict contains the `date`, a possible `doy`, a
tuple, `preceding` containing the lengths of months that must precede
that `doy`, and `intercalation` which will be `True` if one of those
months must be an intercalary month.

The values returned above mean that Metageitnion 9 can be five
possible days of the year: the 38th, 39th, 67th, 68th, or 69th. Since
Metageitnion is the second month of the year, it can only be DOY
39 in an ordinary year if it is preceded by one 30-day month. However,
it could be the 68th day, for instance, if it followed an intercalary
month and one preceding month was 30 days and one 29 days. It does
matter which is 29 and which 30, or which month is the intercalary
month (though in this case it could only be Hekatombaion followed by a
second Hekatombaion).

.. note:: 
   Dates in the middle of the year have more possible DOYs:

   >>> len(eq.festival_doy(ha.AthenianMonths.MET, 10))
   5
   >>> len(eq.festival_doy(ha.AthenianMonths.GAM, 10))
   15
   >>> len(eq.festival_doy(ha.AthenianMonths.SKI, 10))
   6

Days of the Year (Conciliar)
----------------------------

There is a simlar function for determing what days of the year a
conciliar calendar date can have, :py:func:`prytany_doy`. This takes a
prytany constant (:py:enum:`heniautos.prytanies.Prytanies`), a day,
and a prytany type (see :ref:`prytany-types`):

>>> eq.prytany_doy(pryt.Prytanies.I, 39, pryt.Prytany.ALIGNED_10)
(PrytanyDOY(date=(<Prytanies.I: 1>, 39), doy=39, preceding=(), intercalation=True),)

Since we know the year, we can use :py:func:`heniautos.prytanies.prytany_type`
to find the correct (default) prytany type constant:

>>> eq.prytany_doy(pryt.Prytanies.I, 39, pryt.prytany_type(-332))
(PrytanyDOY(date=(<Prytanies.I: 1>, 39), doy=39, preceding=(), intercalation=True),)


The return value is analogous to :py:func:`festival_doy`. In this
case, with ten prytanues the 39th day of a prytany can only occur in
an intercalary year. Since it is the first prytany it cannot be
preceded by any, so ``preceding`` is empty.

Putting the Two Together
------------------------

So, what day then is Met 9 = Prytany 1.39? Because this example is
simple, we can easily see the answer. The prytany date can be only one
DOY, the 39th, and only in an intercalary year. The festival date can
be the 39th DOY also, if it is preceded by one 30-day month. Therefor,
the year 333/332 was intercalary, and began with a 30-day
Hekatombaion. That is the only solution to the calendar equation!

.. note:: ``intercalation`` means something different for festival and
   conciliar equations. In conciliar equations it means that the
   corresponding year *must* be intercalary. For festival equations
   ``intercalation: True`` means the month in the equation must be
   preceded by an intercalation (and therefore must be in an
   intercalary year), but ``intercalation: False`` only means that the
   month is not preceded by an intercalary month, but *it could be
   followed by one*.  There is no contradition in the above example
   between ``intercalation: False`` in the festival year and
   ``intercalation: True`` in the conciliar year.

:py:func:`equations` will do this for us. It takes a tuple (or list)
containing the month constant and date, a tuple (or list) with the
prytany constant and date, and the prytany type:

>>> eq.equations((ha.AthenianMonths.MET, 9), (pryt.Prytanies.I, 39), pryt.prytany_type(-332))
((FestivalDOY(date=(<AthenianMonths.MET: 2>, 9), doy=39, preceding=(30,), intercalation=False), PrytanyDOY(date=(<Prytanies.I: 1>, 39), doy=39, preceding=(), intercalation=True)),)


The return value is a tuple of solutions. Each solution is a tuple
containing a matching festival DOY and prytany DOY. Since there is
only one solution for our example, there is only one item in the
tuple.

An example with more possibilities is represented by a few
inscriptions from the year 332/331: `IG II³,1 344
<https://epigraphy.packhum.org/text/347201>`_, `IG II³,1 345
<https://epigraphy.packhum.org/text/347202>`_, `IG II³,1 346
<https://epigraphy.packhum.org/text/347203>`_, and `IG II³,1 347
<https://epigraphy.packhum.org/text/347204>`_. The equation is Ela 19
= Prytany 8.7:

>>> for e in eq.equations((ha.AthenianMonths.ELA, 19), (pryt.Prytanies.VIII, 7), pryt.prytany_type(-331)):
...     e[0]
...     e[1]
...     print("-"*10)
...
FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=253, preceding=(30, 30, 29, 29, 29, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=253, preceding=(36, 35, 35, 35, 35, 35, 35), intercalation=False)
----------
FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=254, preceding=(30, 30, 30, 29, 29, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=254, preceding=(36, 36, 35, 35, 35, 35, 35), intercalation=False)
----------
FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=255, preceding=(30, 30, 30, 30, 29, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=255, preceding=(36, 36, 36, 35, 35, 35, 35), intercalation=False)
----------
FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=256, preceding=(30, 30, 30, 30, 30, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=256, preceding=(36, 36, 36, 36, 35, 35, 35), intercalation=False)
----------


This could equate, then, to DOY 253–256. The prytany dates indicate an
ordinary year, which agrees with none of the festival dates following
an intercalation. We would now look to other details to decide if any
of the possibilities were better than others. The more even the number
of full and hollow months the better, so DOY 253 looks problematic
because it requires Elaphebolion to be preceded by 2 full and six
hollow months, which would mean at least two hollow months in a
row. Since this is the the period of the :ref:`ten prytanies
<ten-prytanies>` the whole year will have four 36-day prytanies and
six 35-day prytanies. If you believe the Rule of Aristotle that all
the long prutanies should come at the beginining of the year, only the
DOY 256 solution fits this criterion.

There are not always solution, often because there are hidden
intercalary days in the equations. `IG II³,1 368
<https://epigraphy.packhum.org/text/347225>`_, from 325/324, contains
an equation, Tha 22 = Prytany 10.5, with no solutions:

>>> eq.equations((ha.AthenianMonths.THA, 22), (pryt.Prytanies.X, 5), pryt.prytany_type(-324))
()

If we look at the festival and prytany parts separately we can see why:

>>> [e.doy for e in eq.festival_doy(ha.AthenianMonths.THA, 22)]
[316, 317, 318, 319, 345, 346, 347, 348]
>>> [e.doy for e in eq.prytany_doy(pryt.Prytanies.X, 5, pryt.prytany_type(-324))]
[323, 324, 350, 351]

There is no overlap of the possible DOYs of Tha 22 with those of
Prytany 10.5. Pritchett and Neugebauer who believe in the Rule of
Aristotle and the absolute regularity of prytanies hypothesize that
intercalated days earlier in the calendar (*The Calendars of
Athens*. Cambridge: Harvard University Press, 1947, p. 56). This could
result, for instance in Tha 22 not being DOY 348 but DOY 351 if three
days had been added anywhere earlier in the year (or net 3 days added
since days could be subtracted as well). Meritt, who did not believe
in either the Rule of Aristotle and thought the festival calendar was
as regular as possible, hypothesized a few extra days in Thargelion
with two long prytanies followed by the six short and then that
remaining two long (Meritt, Benjamin D. *The Athenian Year*. Sather
Classical Lectures 32. Berkeley: University of California Press, 1961,
pp. 102–104). For the record, I believe Pritchett and Neugebauer are
correct.

Collations
----------

Returning to 332/331, besides Ela 19 = Prytany 8.7 there two more
inscriptions (`IG II³,1 348
<https://epigraphy.packhum.org/text/347205>`_ and `IG II³,1 349
<https://epigraphy.packhum.org/text/347206>`_) with a second equation
for the same year, Tha 11 = Prytany 9.23:

>>> for e in eq.equations((ha.AthenianMonths.THA, 11), (pryt.Prytanies.IX, 23), pryt.prytany_type(-331)):
...     e[0]
...     e[1]
...     print("-"*10)
...
FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=305, preceding=(30, 30, 30, 30, 29, 29, 29, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=305, preceding=(36, 36, 35, 35, 35, 35, 35, 35), intercalation=False)
----------
FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=306, preceding=(30, 30, 30, 30, 30, 29, 29, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=306, preceding=(36, 36, 36, 35, 35, 35, 35, 35), intercalation=False)
----------
FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=307, preceding=(30, 30, 30, 30, 30, 30, 29, 29, 29, 29), intercalation=False)
PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=307, preceding=(36, 36, 36, 36, 35, 35, 35, 35), intercalation=False)
----------

We had four solutions for the first equation and now three for this
second. We might ask if any of these possible soultions fit together
and if so, how. :py:func:`collations` will take any number of results
from :py:func:`equations` and test and report on each possible
combination. The output is a bit complicated:

>>> import pprint
>>> pp = pprint.PrettyPrinter(indent=2)
>>> e1 = eq.equations((ha.AthenianMonths.ELA, 19), (pryt.Prytanies.VIII, 7), pryt.prytany_type(-331))
>>> e2 = eq.equations((ha.AthenianMonths.THA, 11), (pryt.Prytanies.IX, 23), pryt.prytany_type(-331))
>>> pp.pprint(eq.collations(e1, e2))
( { 'equations': ( ( FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=253, preceding=(30, 30, 29, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=253, preceding=(36, 35, 35, 35, 35, 35, 35), intercalation=False)),
                   ( FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=305, preceding=(30, 30, 30, 30, 29, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=305, preceding=(36, 36, 35, 35, 35, 35, 35, 35), intercalation=False))),
    'partitions': { 'conciliar': ((36, 35, 35, 35, 35, 35, 35), (36,)),
                    'festival': ((30, 30, 29, 29, 29, 29, 29, 29), (30, 30))}},
  { 'equations': ( ( FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=254, preceding=(30, 30, 30, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=254, preceding=(36, 36, 35, 35, 35, 35, 35), intercalation=False)),
                   ( FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=305, preceding=(30, 30, 30, 30, 29, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=305, preceding=(36, 36, 35, 35, 35, 35, 35, 35), intercalation=False))),
    'partitions': { 'conciliar': ((36, 36, 35, 35, 35, 35, 35), (35,)),
                    'festival': ((30, 30, 30, 29, 29, 29, 29, 29), (30, 29))}},
  { 'equations': ( ( FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=254, preceding=(30, 30, 30, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=254, preceding=(36, 36, 35, 35, 35, 35, 35), intercalation=False)),
                   ( FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=306, preceding=(30, 30, 30, 30, 30, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=306, preceding=(36, 36, 36, 35, 35, 35, 35, 35), intercalation=False))),
    'partitions': { 'conciliar': ((36, 36, 35, 35, 35, 35, 35), (36,)),
                    'festival': ((30, 30, 30, 29, 29, 29, 29, 29), (30, 30))}},
  { 'equations': ( ( FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=255, preceding=(30, 30, 30, 30, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=255, preceding=(36, 36, 36, 35, 35, 35, 35), intercalation=False)),
                   ( FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=306, preceding=(30, 30, 30, 30, 30, 29, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=306, preceding=(36, 36, 36, 35, 35, 35, 35, 35), intercalation=False))),
    'partitions': { 'conciliar': ((36, 36, 36, 35, 35, 35, 35), (35,)),
                    'festival': ((30, 30, 30, 30, 29, 29, 29, 29), (30, 29))}},
  { 'equations': ( ( FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=255, preceding=(30, 30, 30, 30, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=255, preceding=(36, 36, 36, 35, 35, 35, 35), intercalation=False)),
                   ( FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=307, preceding=(30, 30, 30, 30, 30, 30, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=307, preceding=(36, 36, 36, 36, 35, 35, 35, 35), intercalation=False))),
    'partitions': { 'conciliar': ((36, 36, 36, 35, 35, 35, 35), (36,)),
                    'festival': ((30, 30, 30, 30, 29, 29, 29, 29), (30, 30))}},
  { 'equations': ( ( FestivalDOY(date=(<AthenianMonths.ELA: 9>, 19), doy=256, preceding=(30, 30, 30, 30, 30, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.VIII: 8>, 7), doy=256, preceding=(36, 36, 36, 36, 35, 35, 35), intercalation=False)),
                   ( FestivalDOY(date=(<AthenianMonths.THA: 11>, 11), doy=307, preceding=(30, 30, 30, 30, 30, 30, 29, 29, 29, 29), intercalation=False),
                     PrytanyDOY(date=(<Prytanies.IX: 9>, 23), doy=307, preceding=(36, 36, 36, 36, 35, 35, 35, 35), intercalation=False))),
    'partitions': { 'conciliar': ((36, 36, 36, 36, 35, 35, 35), (35,)),
                    'festival': ((30, 30, 30, 30, 30, 29, 29, 29), (30, 29))}})


The results are a tuple of "collation" dicts, six in this case. Each
collation has two parts, the equations and the partitions. The
partitions are groups of lengths of months and prytanies. The
equations are groups of equations solutions that go together given the
related partitions.

The idea behind the partitions is that each equation is preceded by
some number of months or prytanies of certain lengths, and later
equations must include the same number and combination of lengths as
the earlier ones. In The first collation, the equations are solutions
for Ela 19 = Prytany 8.7 = DOY 253, and Tha 11 = Prytany 9.23 =
DOY 305.

The partitions are:

- conciliar: (36, 35, 35, 35, 35, 35, 35), (36)
- festival: (30, 30, 29, 29, 29, 29, 29, 29), (30, 30)

This means that for Ela 19 = Prytany 8.7 to be DOY 253, it must be
preceded by the first groups of month and prytany lengths (two full
months and six hollow; one long prytany and six short). For Tha 11 =
Prytany 9.23 to be DOY 305, if must be preceded by *the same first
partition*, plus two more full months and one more long prytany.

This is an unlikely number of hollow months in a row and it violates the rule of Aristotle. The final collation looks better. Ela 19 = Prytany 8.7 = DOY 256, and Tha 11 = Prytany 9.23 = DOY 307 with the following partitions:

- conciliar: (36, 36, 36, 36, 35, 35, 35), (35)
- festival: (30, 30, 30, 30, 30, 29, 29, 29), (30, 29)

This is a more even number of hollow and full months, and satisfies
the Rule of Aristotle.


