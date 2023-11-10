.. Heniautos documentation master file, created by
   sphinx-quickstart on Fri Aug  4 22:43:28 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Heniautos
=========

Heniautos (ἐνιαυτός, Greek for ”the span of a year”) generates
examples of possible Greek calendars, ancient or modern, and has
features for exploring the calendar and working with calendar
equations. It is hopefully useful for:

* Learning about and teaching the ancient Athenian and other Greek calendars
* Following along with often complex discussions of dating events
  in ancient Greek history
* Just having fun with questions like ”When would the City Dionysia be
  this year, if it was still being held.”

Heniautos also comes with a command-line application,
:command:`heniautos`, for generating calendars without any programming
required. See the :ref:`documentation <heniautos-command>` for all the
features and options.


Heniautos generates lunisolar calendars as used by ancient Greece
cities based on modern calculations of historical (or modern)
astronomical events—solstices, equinoxes, and phases of the moon. For
fun it can create a calendar for current years. For instance, here’s
what the Athenian calendar might look like in 2023 (as output by the
command-line application):

.. code-block:: console

    $ heniautos 2023 --as-ce -m
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
     CE 2023/2024 | Mounuchiṓn            |  CE 2024-Apr-09 |   30
     CE 2023/2024 | Thargēliṓn            |  CE 2024-May-09 |   29
     CE 2023/2024 | Skirophoriṓn          |  CE 2024-Jun-07 |   29

If you were excited about seeing the tragedies and comedies, make
plans for January because that’s when they would be performed as part
of the Lenaia festival in the Greek month of Gamēliṓn.

For research purposes it can generate a calendar for any year in the
past as a baseline for understanding, For instance, the Athenian
calendar for 431/430 BCE, the year the Peloponnesian War started:

.. code-block:: console

    $ heniautos 431 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 431/430   | Hekatombaiṓn          | BCE 0431-Jul-06 |   29
    BCE 431/430   | Metageitniṓn          | BCE 0431-Aug-04 |   30
    BCE 431/430   | Boēdromiṓn            | BCE 0431-Sep-03 |   29
    BCE 431/430   | Puanopsiṓn            | BCE 0431-Oct-02 |   30
    BCE 431/430   | Maimaktēriṓn          | BCE 0431-Nov-01 |   29
    BCE 431/430   | Posideiṓn             | BCE 0431-Nov-30 |   30
    BCE 431/430   | Posideiṓn hústeros    | BCE 0431-Dec-30 |   29
    BCE 431/430   | Gamēliṓn              | BCE 0430-Jan-28 |   30
    BCE 431/430   | Anthestēriṓn          | BCE 0430-Feb-27 |   29
    BCE 431/430   | Elaphēboliṓn          | BCE 0430-Mar-28 |   30
    BCE 431/430   | Mounuchiṓn            | BCE 0430-Apr-27 |   29
    BCE 431/430   | Thargēliṓn            | BCE 0430-May-26 |   30
    BCE 431/430   | Skirophoriṓn          | BCE 0430-Jun-25 |   29

Since a few aspects of the calendar were subjective or could be
modified Heniautos’ version is no way definitive. But this can be a
starting point in understanding, for instance, discussions about
whether or not the Peloponnesian war started towards the end of the
month of Anthestēriṓn.

There are a few examples in the :ref:`cookbook` to get you started programming with Heniautos.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   festival_calendar
   conciliar_calendar
   equations
   command_line
   cookbook
   func_ref


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
