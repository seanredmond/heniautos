# Heniautos

Naive ancient Attic calendar generator and calendar equation explorer.

## Installation

    pip install heniautos
    
## Usage

### Command Line

Generate a calendar for 416 BCE:

    heniautos 416
        
### In a Program

Generate a calendar for 416 BCE

    import heniautos as ha
    ha.athenian_festival_calendar(ha.bce_as_negative(416))

## The Basics

Heniautos (Greek for ["the span of a
year"](https://logeion.uchicago.edu/%E1%BC%90%CE%BD%CE%B9%CE%B1%CF%85%CF%84%CF%8C%CF%82))
generates examples of _possible_ Athenian calendars for any given
year, ancient or modern, and provides has features for exploring the
calendar and working with calendar equations. It is hopefully useful
for:

* Learning about and teaching the ancient Athenian Calendar
* Following along with often complex discussions of dating of events
  in ancient Greek history
* Just having fun with questions like "When would the City Dionysia be this year, if it was still being held."

Heniautos comes with two command-line programs--`heniautos` for
generating calendars, and `calendar-equation` for exploring
information provided mostly by ancient inscriptions--and a Python
library for writing your own programs. See the [Guide](guide/) for
details.

What A. W. Gomme wrote in 1970 (Gomme, 1945-1981,) 4.264) is still
true today—"It does not seem easy at the present time to make any
statement about the Athenian calendar which is both significant and
undisputed." Still, there are a few certain principals by which the
Athenian calendar functioned:

* It was
  [lunisolar](https://en.wikipedia.org/wiki/Lunisolar_calendar),
  depending partly on the sun, partly on the moon.
* There were twelve months. Each began on the new moon and had 30 days
  (called a "full" month) or 29 (called a "hollow" month)
* The year began on the first new moon following the summer solstice
* Twelve lunar months are 11 days shorter than one solar year, so about
  every third year a thirteenth month had to be added ("intercalated") to
  fill out the time until the next solstice.
  
The same principals were followed throughout the ancient Greek world,
although different cities used different names for the months and
began the year at different times. For instance, in Sparta the year
began after the fall equinox.

Beyond this there are many questions. Did the months alternate
regularly between full and hollow? If not, what determined whether a
month was full or hollow? Was there a fixed schedule of intercalations
(as the Julian and Gregorian calendars have a fixed rule for leap
years)? If not how was this determined? Did the Athenians fix the new
moon by observation, by calculation, or even by guessing?


Heniautos generates "naive" calendars, aligning ancient Greek dates
with Julian calendar dates, according to astronomical data using a few
simple rules:

1. Each month begins, by default, on an "observed" new moon one days
   after the [astronomical
   conjunction](https://en.wikipedia.org/wiki/New_moon) (though you
   can choose other values).
2. The year begins on the first observed new moon (by rule #1) on or
   after the day of the summer solstice.
3. Intercalations are made when _astronomically_
   necessary. Essentially, if one year ends close enough to the summer
   solstice that twelve lunar months will not be enough to reach the
   next solstice, then the next year will be intercalary.

For example, Heniautos' calendar for 416/415 BCE:

|  # | Month        | Julian Date     | # days|
|---:|--------------|-----------------|------:|
| 1  | Hekatombaiṓn | BCE 0416-Jul-19 | 29    |
| 2  | Metageitniṓn | BCE 0416-Aug-17 | 30    |
| 3  | Boēdromiṓn   | BCE 0416-Sep-16 | 29    |
| 4  | Puanopsiṓn   | BCE 0416-Oct-15 | 30    |
| 5  | Maimaktēriṓn | BCE 0416-Nov-14 | 30    |
| 6  | Posideiṓn    | BCE 0416-Dec-14 | 29    |
| 7  | Gamēliṓn     | BCE 0415-Jan-14 | 30    |
| 8  | Anthestēriṓn | BCE 0415-Feb-11 | 30    |
| 9  | Elaphēboliṓn | BCE 0415-Mar-13 | 29    |
| 10 | Mounuchiṓn   | BCE 0415-Apr-11 | 30    |
| 11 | Thargēliṓn   | BCE 0415-May-11 | 29    |
| 12 | Skirophoriṓn | BCE 0415-Jun-09 | 30    |

Notice that the hollow and full months do not alternate regularly
(unless you observed enough over a long enough period of time to see
the actual, natural cycles of the moon). 19-year cycles of
intercalation recognized by the ancients \([Metonic
cycles](https://en.wikipedia.org/wiki/Metonic_cycle), 7 intercalations
every 19 years\) do appear in Heniautos, but by orbital calculations,
rather than by prescription.

417/416 BCE is an example of an intercalary year:

|  # | Month              | Julian Date     | # days|
|---:|--------------------|-----------------|------:|
| 1  | Hekatombaiṓn       | BCE 0417-Jun-30 | 29    |
| 2  | Metageitniṓn       | BCE 0417-Jul-29 | 30    |
| 3  | Boēdromiṓn         | BCE 0417-Aug-28 | 29    |
| 4  | Puanopsiṓn         | BCE 0417-Sep-26 | 30    |
| 5  | Maimaktēriṓn       | BCE 0417-Oct-26 | 30    |
| 6  | Posideiṓn          | BCE 0417-Nov-25 | 30    |
| 7  | Posideiṓn hústeros | BCE 0417-Dec-25 | 29    |
| 8  | Gamēliṓn           | BCE 0416-Jan-23 | 30    |
| 9  | Anthestēriṓn       | BCE 0416-Feb-22 | 30    |
| 10 | Elaphēboliṓn       | BCE 0416-Mar-24 | 29    |
| 11 | Mounuchiṓn         | BCE 0416-Apr-22 | 30    |
| 12 | Thargēliṓn         | BCE 0416-May-22 | 29    |
| 13 | Skirophoriṓn       | BCE 0416-Jun-20 | 29    |


Posideiṓn hústeros ("later Posideiṓn") is the intercalated
month. Without this extra month, the 12th month would end on June 19,
before the solstice (June 28 on the Julian calendar at this
time). Athenians intercalated by repeating one of the months, most
commonly Posideiṓn as shown here, which Heniautos intercalates by
default (you can choose other months).

## Example

Aristotle (or Pseudo-Aristotle) tells us in [_Athenaion Politeia_
32](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0046%3Achapter%3D32)
that The 400, an oligarchic faction that briefly took control of
Athens during the Peloponnesian War, came into power on Thargelion 21
in the year 412/411. `heniautos` can give you this overview of the
year:

    > heniautos 412 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|------
    BCE 412/411   | Hekatombaiṓn          | BCE 0412-Jul-05 |   30
    BCE 412/411   | Metageitniṓn          | BCE 0412-Aug-04 |   29
    BCE 412/411   | Boēdromiṓn            | BCE 0412-Sep-02 |   30
    BCE 412/411   | Puanopsiṓn            | BCE 0412-Oct-02 |   30
    BCE 412/411   | Maimaktēriṓn          | BCE 0412-Nov-01 |   29
    BCE 412/411   | Posideiṓn             | BCE 0412-Nov-30 |   30
    BCE 412/411   | Posideiṓn hústeros    | BCE 0412-Dec-30 |   29
    BCE 412/411   | Gamēliṓn              | BCE 0411-Jan-28 |   29
    BCE 412/411   | Anthestēriṓn          | BCE 0411-Feb-26 |   30
    BCE 412/411   | Elaphēboliṓn          | BCE 0411-Mar-28 |   29
    BCE 412/411   | Mounuchiṓn            | BCE 0411-Apr-26 |   30
    BCE 412/411   | Thargēliṓn            | BCE 0411-May-26 |   29
    BCE 412/411   | Skirophoriṓn          | BCE 0411-Jun-24 |   30

`heniautos 412 -m` means show me the calendar for the Athenian year
that started in 412 BCE (`heniautos 412`), but only show the months
(`-m`). The month of Posideiṓn is repeated because Heniautos
calculates this as an intercalary year. Without the `-m` you can see
the whole calendar, which might be a bit much, but you can limit it to
a single month:

    heniautos 412 --month 12
         Year     |        Month          | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|-----
    BCE 412/411   | Thargēliṓn            |   1 | BCE 0411-May-26 | 326
    BCE 412/411   | Thargēliṓn            |   2 | BCE 0411-May-27 | 327
    BCE 412/411   | Thargēliṓn            |   3 | BCE 0411-May-28 | 328
    BCE 412/411   | Thargēliṓn            |   4 | BCE 0411-May-29 | 329
    BCE 412/411   | Thargēliṓn            |   5 | BCE 0411-May-30 | 330
    BCE 412/411   | Thargēliṓn            |   6 | BCE 0411-May-31 | 331
    BCE 412/411   | Thargēliṓn            |   7 | BCE 0411-Jun-01 | 332
    BCE 412/411   | Thargēliṓn            |   8 | BCE 0411-Jun-02 | 333
    BCE 412/411   | Thargēliṓn            |   9 | BCE 0411-Jun-03 | 334
    BCE 412/411   | Thargēliṓn            |  10 | BCE 0411-Jun-04 | 335
    BCE 412/411   | Thargēliṓn            |  11 | BCE 0411-Jun-05 | 336
    BCE 412/411   | Thargēliṓn            |  12 | BCE 0411-Jun-06 | 337
    BCE 412/411   | Thargēliṓn            |  13 | BCE 0411-Jun-07 | 338
    BCE 412/411   | Thargēliṓn            |  14 | BCE 0411-Jun-08 | 339
    BCE 412/411   | Thargēliṓn            |  15 | BCE 0411-Jun-09 | 340
    BCE 412/411   | Thargēliṓn            |  16 | BCE 0411-Jun-10 | 341
    BCE 412/411   | Thargēliṓn            |  17 | BCE 0411-Jun-11 | 342
    BCE 412/411   | Thargēliṓn            |  18 | BCE 0411-Jun-12 | 343
    BCE 412/411   | Thargēliṓn            |  19 | BCE 0411-Jun-13 | 344
    BCE 412/411   | Thargēliṓn            |  20 | BCE 0411-Jun-14 | 345
    BCE 412/411   | Thargēliṓn            |  21 | BCE 0411-Jun-15 | 346
    BCE 412/411   | Thargēliṓn            |  22 | BCE 0411-Jun-16 | 347
    BCE 412/411   | Thargēliṓn            |  23 | BCE 0411-Jun-17 | 348
    BCE 412/411   | Thargēliṓn            |  24 | BCE 0411-Jun-18 | 349
    BCE 412/411   | Thargēliṓn            |  25 | BCE 0411-Jun-19 | 350
    BCE 412/411   | Thargēliṓn            |  26 | BCE 0411-Jun-20 | 351
    BCE 412/411   | Thargēliṓn            |  27 | BCE 0411-Jun-21 | 352
    BCE 412/411   | Thargēliṓn            |  28 | BCE 0411-Jun-22 | 353
    BCE 412/411   | Thargēliṓn            |  29 | BCE 0411-Jun-23 | 354

From the previous output we can see that Thargelion was the 12th month
of the year and `heniautos 412 --month 12` means "show me the calendar
for just the 12th month of 412/411." Thargelion 21, when the 400 took
power was June 15, 411 BCE.

This should be correct within about a day. There are very serious
questions about which years are intercalary, especially in the 5th
century BCE, and sometimes which month was intercalated. For serious
purposes Heniautos' calculations should only be taken as a baseline.

For fun, Heniautos can generate calendars for current years. For
example, `heniautos 2023 --as-ce -m` will show what the Athenian
calendar _would be_ for 2023 CE:

    heniautos 2023 --as-ce -m
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

## Learn More

Please read the [Guide](guide/) for more about the Athenian calendar
and what calendar equations are and how they're used, as well as for
details about the usage of `heniautos` command, the
`calendar-equation` command, and the Python library.

## Note about M1 Macintoshes

Heniautos has its own data for the 5th-1st centuries BCE and 20th-21st
centuries CE. For years outside these ranges you can use a a package
named [Skyfield](https://rhodesmill.org/skyfield/) for astronomical
data. Skyfield, in turn, requires [NumPy](https://numpy.org/) which
cannot always be installed the normal way on a Macintosh with an M1
processor. These steps should work to install Skyfield on an M1 Mac:

    pip install cython
    pip install --no-binary :all: --no-use-pep517 numpy
    pip install skyfield
    
(See this [StackOverflow comment](https://stackoverflow.com/a/66456204/131226))

