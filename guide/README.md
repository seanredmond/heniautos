# Heniautos Guide

1. Intro
2. [Festival Calendar Basics](festival-calendar-basics.md)
3. [The Conciliar Calendar](conciliar-calendar.md)
5. [`heniautos` Command](heniautos-command.md)
6. [`calendar-equations` Command](calendar-equations-command.md)
7. [Programming with Heniautos](programming-with-heniautos.md)
8. [API Reference](api-reference.md)
	9. heniautos
	10. heniautos.prytanies
	11. heniautos.equations
	12. heniautos.ep
8. [Reading Dated Inscriptions](reading-dated-inscriptions.md)
4. [Calendar Equations](calendar-equations.md)

Heniautos generates lunisolar calendars as used by ancient Greece cities based on modern calculations of historical (or modern) astronomical events—solstices, equinoxes, and phases of the moon. For fun it can create a calendar for current years so you can, for instance, see when important festivals would occur if they were still going on today. For instance, here's what the Athenian calendar might look like in 2023:

    > heniautos 2023 --as-ce -m
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

If you were excited about seeing the tragedies and comedies, make plans for January when they would be performed as part of the Lenaia festival in the Greek month of Gamēliṓn.


For research it can generate a calendar for any year in the past as a baseline for understanding, For instance, the Athenian calendar for 431/430 BCE, the year the Peloponnesian War starte

    > heniautos 431 -m
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

Since a few aspects of the calendar were subjective or could be modified Heniautos' version is no way definitive. But this can be a starting point in uderstanding discussions around whether or not the war started towards the end of the month of Anthestēriṓn.

If you are new to the Greek calendar, start with [Festival Calendar Basics](festival-calendar-basics.md) and [The Conciliar Calendar](conciliar-calendar.md). Athenians used two parallel calendars and it is their differences and overlaps that allow us to explore many of the details about how they reckoned the year. Heniautos can generate both.

[`heniautos` Command](heniautos-command.md) has full details about how to use `heniautos` to generate many different views of the Athenian calendar.

[Programming with Heniautos](programming-with-heniautos.md) and the [API Reference](api-reference) are the full guide to using the Heniautos Python library for writing your own programs.

[Reading Dated Inscriptions](reading-dated-inscriptions.md) is a very brief overview of the prescripts of dated decrees of the Athenian Ekklēsía that give us so much information about ancient dates. These prescripts follow a fairly inflexible formula, so once you know a few principles, you can easily read many of these inscriptions yourself.

Once you are more interested in the nitty-gritty of this calendar, read  [Calendar Equations](calendar-equations.md) and [`calendar-equations` Command](calendar-equations-command.md) to get started on the fascinating (and frustrating) puzzles in the evidence from ancient dated inscriptions.


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
