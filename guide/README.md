# Heniautos Guide

1. Intro
2. [Festival Calendar Basics](festival-calendar-basics.md)
3. [The Conciliar Calendar](conciliar-calendar.md)
5. [`heniautos` Command](heniautos-command.md)
4. [Calendar Equations](calendar-equations.md)
6. [`calendar-equations` Command](calendar-equations-command.md)
7. [Programming with Heniautos](programming-with-heniautos.md)
8. [Reading Dated Inscriptions](reading-dated-inscriptions.md)


If you are new to the Athenian calendar, start with [Festival Calendar Basics](festival-calendar-basics.md) and [The Conciliar Calendar](conciliar-calendar.md). Athenians used these two parallel calendars and it is their differences and overlaps that allow us to explore many of the details about how they reckoned the year.

[`heniautos` Command](heniautos-command.md) has full details about how to use `heniautos` to generate many different views of the Athenian calendar.

Once you are more interested in the nitty-gritty of this calendar, read  [Calendar Equations](calendar-equations.md) and [`calendar-equations` Command](calendar-equations-command.md) to get started on the fascinating (and frustrating) puzzles in the evidence from ancient dated inscriptions.

[Programming with Heniautos](programming-with-heniautos.md) is the full guide to using the Heniautos Python library for writing your own programs.

Finally, [Reading Dated Inscriptions](reading-dated-inscriptions.md) is a very brief overview of the prescripts of dated decrees of the Athenian Ekklēsía that give us so much information about ancient dates. These prescripts follow a fairly inflexible formula, so once you know a few principles, you can easily read many of these inscriptions yourself.

## Ephemeris Files (Important!)

Heniautos relies on a library called [Skyfield](https://rhodesmill.org/skyfield/) for astronomical data and calculations. Skyfield, in turn, requires an [ephemeris](https://rhodesmill.org/skyfield/planets.html) named `de422.bsp` to function. This file comes from [NASA's Jet Propulsion Laboratory](https://ssd.jpl.nasa.gov/?planet_eph_export) and contains data about the positions of celestial objects over time.

Whenever you run the [`heniautos` command](heniautos-command.md) or your own script using [the programming library](programming-with-heniautos.md) your computer will use the first copy of `de422.bsp` it can find on your hard drive.

If a copy of the file cannot be found it will automatically be downloaded into the current working directory. This is normal and safe, but the file is over 600 MB. Once you have a copy, you can tell `heniautos` or the programming library where to find it in order to avoid downloading it again.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
