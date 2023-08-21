*************************
Command-Line Applications
*************************

:command:`heniautos`
====================

.. program:: heniautos


The :command:`heniautos` command-line application gives you access to most of the calendar calculations described in :ref:`festival-calendars` and :ref:`conciliar-calendars`. There are quite a few options. Use :option:`-h` to see them in the console:

.. code-block:: console

    $ heniautos -h
    usage: heniautos [-h] [-c {argos,athens,delos,delphi,sparta,corinth,generic}]
                 [--month {1,2,3,4,5,6,7,8,9,10,11,12,13}] [--day DAY]
                 [--doy DOY] [-m] [-y]
                 [--intercalate {1,2,3,4,5,6,7,8,9,10,11,12}] [-C] [--arabic]
                 [--prytany {I,II,III,IV,V,VI,VII,VIII,IX,X,XI,XII,XIII}]
                 [--as-ce] [-a] [-g] [--new-moons] [--full-moons]
                 [--summer-solstice] [--spring-equinox] [--autumn-equinox]
                 [--winter-solstice] [--gmt] [-v N] [-s N]
                 [--calendar-start {summer,fall,winter,spring}] [-E] [-e FILE]
                 [--julian] [--julian-solar-events] [--julian-new-moons]
                 [--tab] [--version]
                 start_year [end_year]

    Ancient Athenian calendar generator

    positional arguments:
      start_year
      end_year

    optional arguments:
      -h, --help            show this help message and exit
      -c {argos,athens,delos,delphi,sparta,corinth,generic}, --calendar {argos,athens,delos,delphi,sparta,corinth,generic}
                        Festival calendar to display
      --month {1,2,3,4,5,6,7,8,9,10,11,12,13}
                        Only show requested month
      --day DAY             Only show selected day
      --doy DOY             Only show selected day of year
      -m, --month-summary
      -y, --year-summary
      --intercalate {1,2,3,4,5,6,7,8,9,10,11,12}
                        Month after which to intercalate
      -C, --conciliar       Output conciliar calendar (prytanies)
      --arabic              Display prytany numbers as Arabic rather than Roman
                            numerals
      --prytany {I,II,III,IV,V,VI,VII,VIII,IX,X,XI,XII,XIII}
                        Only show selected prytany
      --as-ce               Treat dates as CE rather than BCE
      -a, --abbreviations   Abbreviate month names
      -g, --greek-names     Use Greek names for months
      --new-moons           Only list times of astronomical new moons
      --full-moons          Only list times of astronomical full moons
      --summer-solstice     Only list dates of solstices
      --spring-equinox      Only list dates of spring equinox
      --autumn-equinox      Only list dates of autumn equinox
      --winter-solstice     Only list dates of winter solstice
      --gmt                 Format times as GMT (rather than EET)
      -v N, --visibility-offset N
                            Offset for determining date of new moon. N days after
                            astronomical conjunction(default: 1)
      -s N, --solar-offset N
                            Offset for determining the date of solstices and
                            equinoxes
      --calendar-start {summer,fall,winter,spring}
                            Season for beginning of the year (with -c generic,
                            default: summer
      -E, --use-ephemeris   Use ephemeris for data
      -e FILE, --ephemeris FILE
                            Use existing ephemeris FILE (if it cannot
                            automatically be found)
      --julian              Just output Julian calendar dates
      --julian-solar-events
                            Include solstices and equinoxes in Julian calendar
                            output
      --julian-new-moons    Include new moons in Julian calendar output
      --tab                 Output in tab-delimited format
      --version             Print version and exit

Basic Usage
-----------

.. _athens-festival:

Athenian Festival Calendar
^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplest use is provide a single year. This will be interpreted as
a year BCE, and :command:`heniautos` will output a festival calendar
for the year (many lines not shown):

.. code-block:: console

    $ heniautos 400
         Year     |        Month          | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|-----
    BCE 400/399   | Hekatombaiṓn          |   1 | BCE 0400-Jul-22 |   1
    BCE 400/399   | Hekatombaiṓn          |   2 | BCE 0400-Jul-23 |   2
    BCE 400/399   | Hekatombaiṓn          |   3 | BCE 0400-Jul-24 |   3
    BCE 400/399   | Hekatombaiṓn          |   4 | BCE 0400-Jul-25 |   4
    ...
    BCE 400/399   | Skirophoriṓn          |  27 | BCE 0399-Jul-08 | 352
    BCE 400/399   | Skirophoriṓn          |  28 | BCE 0399-Jul-09 | 353
    BCE 400/399   | Skirophoriṓn          |  29 | BCE 0399-Jul-10 | 354

The `year` column shows the *Greek* year, which probably spans two
Julian years. The `start` column is the proleptic Julian date (for
BCE) or Gregorian date (for CE) of the Greek date. `DOY` is the day of
the year.

Use the :option:`-m` switch to summarize by month:

.. code-block:: console

    $ heniautos 400 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 400/399   | Hekatombaiṓn          | BCE 0400-Jul-22 |   29
    BCE 400/399   | Metageitniṓn          | BCE 0400-Aug-20 |   30
    BCE 400/399   | Boēdromiṓn            | BCE 0400-Sep-19 |   29
    BCE 400/399   | Puanopsiṓn            | BCE 0400-Oct-18 |   30
    BCE 400/399   | Maimaktēriṓn          | BCE 0400-Nov-17 |   30
    BCE 400/399   | Posideiṓn             | BCE 0400-Dec-17 |   30
    BCE 400/399   | Gamēliṓn              | BCE 0399-Jan-16 |   30
    BCE 400/399   | Anthestēriṓn          | BCE 0399-Feb-15 |   29
    BCE 400/399   | Elaphēboliṓn          | BCE 0399-Mar-16 |   29
    BCE 400/399   | Mounukhiṓn            | BCE 0399-Apr-14 |   30
    BCE 400/399   | Thargēliṓn            | BCE 0399-May-14 |   29
    BCE 400/399   | Skirophoriṓn          | BCE 0399-Jun-12 |   29

Instead of the `DOY` column, the month summary shows the length of the
month under `Days`.

Or :option:`-y` to summarize by year:

.. code-block:: console

    $ heniautos 400 -y
         Year     | Y |      Start      | Days
    --------------|---|-----------------|------
    BCE 400/399   | O | BCE 0400-Jul-22 |  354

The `Y` column indicates whether the year is ordinary (O) or intercalary (I).

You can provide two years to see a calendar spanning the full range of
years given. This is easiest to illustrate in the year summary:

.. code-block:: console

    $ heniautos 400 395 -y
         Year     | Y |      Start      | Days
    --------------|---|-----------------|------
    BCE 400/399   | O | BCE 0400-Jul-22 |  354
    BCE 399/398   | O | BCE 0399-Jul-11 |  355
    BCE 398/397   | I | BCE 0398-Jul-01 |  384
    BCE 397/396   | O | BCE 0397-Jul-19 |  355
    BCE 396/395   | I | BCE 0396-Jul-09 |  383
    BCE 395/394   | O | BCE 0395-Jul-27 |  354

With :option:`--as-ce`, the year or years will be interpreted as CE. With this you can generate a calendar for a modern year:

.. code-block:: console

    $ heniautos 2023 -m --as-ce
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
     CE 2023/2024 | Hekatombaiṓn          |  CE 2023-Jul-18 |   30
     CE 2023/2024 | Metageitniṓn          |  CE 2023-Aug-17 |   30
     CE 2023/2024 | Boēdromiṓn            |  CE 2023-Sep-16 |   29
     CE 2023/2024 | Puanopsiṓn            |  CE 2023-Oct-15 |   30
     CE 2023/2024 | Maimaktēriṓn          |  CE 2023-Nov-14 |   29
     CE 2023/2024 | Posideiṓn             |  CE 2023-Dec-13 |   30
     CE 2023/2024 | Gamēliṓn              |  CE 2024-Jan-12 |   29
     CE 2023/2024 | Anthestēriṓn          |  CE 2024-Feb-10 |   30
     CE 2023/2024 | Elaphēboliṓn          |  CE 2024-Mar-11 |   29
     CE 2023/2024 | Mounukhiṓn            |  CE 2024-Apr-09 |   30
     CE 2023/2024 | Thargēliṓn            |  CE 2024-May-09 |   29
     CE 2023/2024 | Skirophoriṓn          |  CE 2024-Jun-07 |   29

Use :option:`-a` to show the month names as abbreviations:

.. code-block:: console
    
    $ heniautos 400 -m -a
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 400/399   | Hek                   | BCE 0400-Jul-22 |   29
    BCE 400/399   | Met                   | BCE 0400-Aug-20 |   30
    BCE 400/399   | Boe                   | BCE 0400-Sep-19 |   29
    ...

And :option:`-g` to show them in Greek:

.. code-block:: console
    
    $ heniautos 400 -m -g
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 400/399   | Ἑκατομβαιών           | BCE 0400-Jul-22 |   29
    BCE 400/399   | Μεταγειτνιών          | BCE 0400-Aug-20 |   30
    BCE 400/399   | Βοηδρομιών            | BCE 0400-Sep-19 |   29
    ...


.. _import-spreadsheet:
   
Importing into Spreadsheets
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Anything can be output with tab-delimites columns by using :option:`--tab`:

.. code-block:: console

    $ heniautos 400 395 -y --tab
    "BCE 400/399"	"O"	"BCE 0400-Jul-22"	354
    "BCE 399/398"	"O"	"BCE 0399-Jul-11"	355
    "BCE 398/397"	"I"	"BCE 0398-Jul-01"	384
    "BCE 397/396"	"O"	"BCE 0397-Jul-19"	355
    "BCE 396/395"	"I"	"BCE 0396-Jul-09"	383
    "BCE 395/394"	"O"	"BCE 0395-Jul-27"	354

This is useful for importing into spreadsheets. You can either save the output to a file, that you can open or import into a spreadsheet

.. code-block:: console

    $ heniautos 400 395 -y --tab > 400_to_395.tsc

Or you can send it to the clipboard so you can then just paste it in. On a Mac you can do this with :command:`pbcopy`:

.. code-block:: console

    $ heniautos 400 395 -y --tab | pbcopy

    
    
Intercalations
^^^^^^^^^^^^^^

Intercalations are handled automatically, and Posideiṓn is intercalated by default:

.. code-block:: console
    
    $ heniautos 401 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 401/400   | Hekatombaiṓn          | BCE 0401-Jul-03 |   29
    BCE 401/400   | Metageitniṓn          | BCE 0401-Aug-01 |   30
    BCE 401/400   | Boēdromiṓn            | BCE 0401-Aug-31 |   30
    BCE 401/400   | Puanopsiṓn            | BCE 0401-Sep-30 |   30
    BCE 401/400   | Maimaktēriṓn          | BCE 0401-Oct-30 |   29
    BCE 401/400   | Posideiṓn             | BCE 0401-Nov-28 |   30
    BCE 401/400   | Posideiṓn hústeros    | BCE 0401-Dec-28 |   30
    BCE 401/400   | Gamēliṓn              | BCE 0400-Jan-27 |   29
    BCE 401/400   | Anthestēriṓn          | BCE 0400-Feb-25 |   30
    BCE 401/400   | Elaphēboliṓn          | BCE 0400-Mar-27 |   29
    BCE 401/400   | Mounukhiṓn            | BCE 0400-Apr-25 |   29
    BCE 401/400   | Thargēliṓn            | BCE 0400-May-24 |   29
    BCE 401/400   | Skirophoriṓn          | BCE 0400-Jun-22 |   30

To choose another month for intercalation, use :option:`--intercalate` with the number of the desired month. For instance, 8 for Anthestēriṓn:

.. code-block:: console    

    $ heniautos 401 -m --intercalate 8
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 401/400   | Hekatombaiṓn          | BCE 0401-Jul-03 |   29
    BCE 401/400   | Metageitniṓn          | BCE 0401-Aug-01 |   30
    BCE 401/400   | Boēdromiṓn            | BCE 0401-Aug-31 |   30
    BCE 401/400   | Puanopsiṓn            | BCE 0401-Sep-30 |   30
    BCE 401/400   | Maimaktēriṓn          | BCE 0401-Oct-30 |   29
    BCE 401/400   | Posideiṓn             | BCE 0401-Nov-28 |   30
    BCE 401/400   | Gamēliṓn              | BCE 0401-Dec-28 |   30
    BCE 401/400   | Anthestēriṓn          | BCE 0400-Jan-27 |   29
    BCE 401/400   | Anthestēriṓn hústeros | BCE 0400-Feb-25 |   30
    BCE 401/400   | Elaphēboliṓn          | BCE 0400-Mar-27 |   29
    BCE 401/400   | Mounukhiṓn            | BCE 0400-Apr-25 |   29
    BCE 401/400   | Thargēliṓn            | BCE 0400-May-24 |   29
    BCE 401/400   | Skirophoriṓn          | BCE 0400-Jun-22 |   30


Athenian Conciliar Calendar
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Show the Athenian concilar calendar with :option:`-C`

.. code-block:: console
    
    $ heniautos 400 -m -C
         Year     |        Prytany        |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 400/399   | I                     | BCE 0400-Jul-15 |   37
    BCE 400/399   | II                    | BCE 0400-Aug-21 |   37
    BCE 400/399   | III                   | BCE 0400-Sep-27 |   37
    BCE 400/399   | IV                    | BCE 0400-Nov-03 |   37
    BCE 400/399   | V                     | BCE 0400-Dec-10 |   37
    BCE 400/399   | VI                    | BCE 0399-Jan-16 |   37
    BCE 400/399   | VII                   | BCE 0399-Feb-22 |   36
    BCE 400/399   | VIII                  | BCE 0399-Mar-30 |   36
    BCE 400/399   | IX                    | BCE 0399-May-05 |   36
    BCE 400/399   | X                     | BCE 0399-Jun-10 |   36

The number of prytanies will be based on the year as described in :ref:`prytany-types`.

If you want the prytanies numbered with Arabic rather than Roman numerals, use the :option:`--arabic` switch.

Other Calendars
---------------

You can see festival calendars from a few other Greek cities besides
Athens with :option:`-c`:

.. code-block:: console

    $ heniautos 400 -m -c corinth
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 400/399   | Phoinikaîos           | BCE 0400-Sep-19 |   29
    BCE 400/399   | Kráneios              | BCE 0400-Oct-18 |   30
    BCE 400/399   | Lanotropíos           | BCE 0400-Nov-17 |   30
    BCE 400/399   | Makhaneús             | BCE 0400-Dec-17 |   30
    BCE 400/399   | Dōdekateús            | BCE 0399-Jan-16 |   30
    BCE 400/399   | Εúkleios              | BCE 0399-Feb-15 |   29
    BCE 400/399   | Artemísios            | BCE 0399-Mar-16 |   29
    BCE 400/399   | Psudreús              | BCE 0399-Apr-14 |   30
    BCE 400/399   | Gameílios             | BCE 0399-May-14 |   29
    BCE 400/399   | Agriánios             | BCE 0399-Jun-12 |   29
    BCE 400/399   | Pánamos               | BCE 0399-Jul-11 |   30
    BCE 400/399   | Apellaîos             | BCE 0399-Aug-10 |   29

All the options shown under :ref:`athens-festival` work with these
calendars.

Generic Calendar
^^^^^^^^^^^^^^^^

Calendars from various Greek cities differ not only in the names of
their months but also in when they start, which can be immediately
before or after any any solstice ot equinox. For example, the Athenian
calendar begins just after the summer solstice, the Corinthian just
before the autumn equinox.

You can generate a "generic" calendar that simple has numbered
months. By default this will start after the summer solstice (like the
Athenian calendar), but you can use :option:`--calendar-start` to
choose another season. For example, this creates a "generic" calendar
that starts after the spring equinox:

.. code-block:: console

    $ heniautos 400 -m -c generic --calendar-start spring
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 400/399   | 1                     | BCE 0400-Mar-27 |   29
    BCE 400/399   | 2                     | BCE 0400-Apr-25 |   29
    BCE 400/399   | 3                     | BCE 0400-May-24 |   29
    BCE 400/399   | 4                     | BCE 0400-Jun-22 |   30
    BCE 400/399   | 5                     | BCE 0400-Jul-22 |   29
    BCE 400/399   | 6                     | BCE 0400-Aug-20 |   30
    BCE 400/399   | 6 hústeros            | BCE 0400-Sep-19 |   29
    BCE 400/399   | 7                     | BCE 0400-Oct-18 |   30
    BCE 400/399   | 8                     | BCE 0400-Nov-17 |   30
    BCE 400/399   | 9                     | BCE 0400-Dec-17 |   30
    BCE 400/399   | 10                    | BCE 0399-Jan-16 |   30
    BCE 400/399   | 11                    | BCE 0399-Feb-15 |   29
    BCE 400/399   | 12                    | BCE 0399-Mar-16 |   29

.. note::

   The Spartan calendar is a special case of the generic
   calendar. Because we do not know the names of all the months or
   their order, Spartan months are numbered.

Other Astronomical Data
-----------------------

Julian Years
^^^^^^^^^^^^

The :option:`--julian` option will output a *Julian* calendar for the year or years requested. The first column is the Julian Day Number.

.. code-block:: console

    $ heniautos 400 --julian
    1575324|BCE 0400-Jan-01||
    1575325|BCE 0400-Jan-02||
    1575326|BCE 0400-Jan-03||
    ...
    1575686|BCE 0400-Dec-29||
    1575687|BCE 0400-Dec-30||
    1575688|BCE 0400-Dec-31||

.. note::

   This will actually output a Gregorian calendar for years forllowing the Gregorian reform

With :option:`--julian-solar-events` and/or :option:`--julian-new-moons`, columns will be added for solstices and equinoxes, and new moons


.. code-block:: console

    $ heniautos 400 --julian --julian-solar-events --julian-new-moons
    1575324|BCE 0400-Jan-01||
    1575325|BCE 0400-Jan-02||
    ...
    1575348|BCE 0400-Jan-25||
    1575349|BCE 0400-Jan-26||NM
    1575350|BCE 0400-Jan-27||
    ...
    1575407|BCE 0400-Mar-25||
    1575408|BCE 0400-Mar-26|SpEq|NM
    1575409|BCE 0400-Mar-27||
    ...

This is the underlying data that :py:mod:`heniautos` uses to generate
calendars, so you can use this to check the work of
:py:mod:`heniautos` or come up with yout own ideas.

.. note:: The new moons marked by :option:`--julian-new-moons` are
   conjunctions, not visible new moons. Neither the new moons or
   solstices/equinoxes are affected by :option:`--visibility-offset`
   or :option:`--solar-offset`

Option Reference
----------------

.. option:: start_year

    A year, or the first year of a range to display (required). Years
    will be treated as BCE unless :option:`--as-ce` is used
      
.. option:: end_year

    If provided, this and :option:`start_year` will be treated as the
    first and last years of a range. They must be provided in the
    correct order or an error will be raised

.. option:: -a, --abbreviations

    Show month names as abbreviations

.. option:: --arabic

    Display prytany numbers as Arabic rather than Roman numerals

.. option:: --as-ce

    Treat dates as CE rather than BCE

.. option:: -c <city>

    Show calender for specific city (default Athens). Choices are
    argos, athens, delos, delphi, sparta, corinth, generic

.. option:: -C, --conciliar

    Output conciliar calendar (prytanies)

.. option:: --calendar-start <season>

    Season for beginning of the year (with :option:`-c` generic). Choices are one of: summer, fall, winter,
    spring. Default: summer

.. option:: -g, --greek-names

    Show month names in Greek

.. option:: -h

    Show help


.. option:: --intercalate <month number>

    Month after which to intercalate    

.. option:: --julian

    Output a Julian Calendar (Gregorian if after the Gregorian reform)

.. option:: --julian-new-moons

    TK

.. option:: --julian-solar-events

    TK

.. option:: -m, --month-summary

    Summarize calendar by month

.. option:: -s, --solar-offset

    TK

.. option:: --tab

    Format output with tabs. Good for importing into spreadsheets (see :ref:`import-spreadsheet`)

.. option:: -v, --visibility-offset

    TK

.. option:: -y, --year-summary

    Summarize calendar by year

