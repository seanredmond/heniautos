# Heniautos

Naive ancient Attic calendar generator and calendar equation explorer.

## The Basics

Heniautos (Greek for ["the span of a
year"](https://logeion.uchicago.edu/%E1%BC%90%CE%BD%CE%B9%CE%B1%CF%85%CF%84%CF%8C%CF%82))
generates examples of _possible_ Athenian calendars for any given
year, ancient or modern, and provides has features for exploring the
calendar and working with calendar equations. It is hopefully
useful for:

* Learning about and teaching the ancient Athenian Calendar
* Following along with often complex discussions of dating of events in ancient Greek hsitory
* Just having fun with questions like "When would the City Dionysia be this year, if it was still being held."

Heniautos comes with two command-line programs--`heniautos` for genreating calendars, and `calendar-equations` for exploring information provided most by ancient inscriptions--and a Python library for writing your own programs. See the [Guide](guide/) for details.

What A. W. Gomme wrote in 1970 (Gomme, 1945-1981,) 4.264) is
still true today—"It does not seem easy at the present time to make
any statement about the Athenian calendar which is both significant
and undisputed." Still, there are a few certain principals by which the Athenian calendar functioned:

* It was
  [lunisolar](https://en.wikipedia.org/wiki/Lunisolar_calendar),
  depending partly on the sun, partly on the moon.
* There were twelve months. Each began on the new moon and had 30 days
  (called a "full" month) or 29 (called a "hollow" month)
* The year began on the first new moon following the summer solstice
* Twelve lunar months is 11 days shorter than one solar year, so about
  every third year a thirteenth month had to be added ("intercalated") to
  fill out the time until the next solstice.
  
The same principals were followed throughout the ancient Greek world,
although different cities used different names for the months and
began the year at different times. For instance, in Sparta the year
began after the fall equinox.

Beyond this there are many questions. Did the months alternate
regulary between full and hollow? If not, what determined whether a
month was full or hollow. Was there a fixed schedule of intercalations
(as the Julian and Gregorian calendars have a fixed rule for leap
years)? If not how was this determined? Did the Athenians fix the new
moon by observation, by calculation, or even by guessing?


Heniautos generates "naive" calendars, aligning ancient Greek dates
with Julian calendar dates, according to astronomical data \(provided
by the [`Skyfield`](https://rhodesmill.org/skyfield/) library\) using
a few simple rules:

1. Each month begins, by default, on an "observed" new moon two days after the [astronomical conjunction](https://en.wikipedia.org/wiki/New_moon) (though you can choose other values).
2. The year begins on the first observed (by rule #1) new moon on or after the day of the summer solstice.
3. Intercalations are made when _astronomically_ necessary. Essentially, if one year ends close enough to the summer solstice that twelve lunar months will not be enough to reach the next solstice, then the next year will be intercalary.

For example, Heniautos' calendar for 416/415 BCE:

|  # | Month        | Julian Date     | # days|
|---:|--------------|-----------------|------:|
|  1 | Hekatombaiṓn | BCE 0416-Jul-20 | 29    |
|  2 | Metageitniṓn | BCE 0416-Aug-18 | 30    |
|  3 | Boēdromiṓn   | BCE 0416-Sep-17 | 29    |
|  4 | Puanepsiṓn   | BCE 0416-Oct-16 | 30    |
|  5 | Maimaktēriṓn | BCE 0416-Nov-15 | 29    |
|  6 | Poseidēiṓn   | BCE 0416-Dec-14 | 30    |
|  7 | Gamēliṓn     | BCE 0415-Jan-13 | 30    |
|  8 | Anthestēriṓn | BCE 0415-Feb-12 | 30    |
|  9 | Elaphēboliṓn | BCE 0415-Mar-14 | 29    |
| 10 | Mounuchiṓn   | BCE 0415-Apr-12 | 30    |
| 11 | Thargēliṓn   | BCE 0415-May-12 | 29    |
| 12 | Skirophoriṓn | BCE 0415-Jun-10 | 30    |

Notice that the hollow and full months do not alternate regularly
(unless you observed enough over a long enough period of time to see
the actual, natural cycles of the moon). 19-year cycles of
intercalation recognized by the ancients \([Metonic
cycles](https://en.wikipedia.org/wiki/Metonic_cycle), 7 intercalations
every 19 years\) do appear in Heniautos, but by observation rather
than by prescription.

An example of an intercalary year is 417/416 BCE:

|  # | Month        | Julian Date     | # days|
|---:|--------------|-----------------|------:|
|  1 | Hekatombaiṓn | BCE 0417-Jul-01 | 29    |
|  2 | Metageitniṓn | BCE 0417-Jul-30 | 30    |
|  3 | Boēdromiṓn   | BCE 0417-Aug-29 | 29    |
|  4 | Puanopsiṓn   | BCE 0417-Sep-27 | 30    |
|  5 | Maimaktēriṓn | BCE 0417-Oct-27 | 30    |
|  6 | Posideiṓn    | BCE 0417-Nov-26 | 29    |
|  7 | Posideiṓn hústeros | BCE 0417-Dec-25 | 30    |
|  8 | Gamēliṓn     | BCE 0416-Jan-24 | 30    |
|  9 | Anthestēriṓn | BCE 0416-Feb-23 | 29    |
| 10 | Elaphēboliṓn | BCE 0416-Mar-24 | 30    |
| 11 | Mounuchiṓn   | BCE 0416-Apr-23 | 29    |
| 12 | Thargēliṓn   | BCE 0416-May-22 | 30    |
| 13 | Skirophoriṓn | BCE 0416-Jun-21 | 29    |

Since the 12th month ends on June 20, before the solstice (June 28 on
the Julian calendar at this time), this year needed a 13th month to
extend through to the beginning of the next year after the
solstice. Athenians intercalated by repeating one of the months, usually Posideiṓn which Heniautos intercalated by default (you can choose other months).


However the Athenians had to make a lot of ad hoc adjustments to keep
the calendar aligned with the seasons and the adjustments they made
were, for practical purposes, rather random and unpredictable. The
only adjustment Heniautos makes is to add a month ("intercalate")
where it seems necessary. These do not always line up with actual
historical intercalations, but it's good enough to get a feel for the
Athenian calendar, and to place any date within about one or two days
a Julian date with the caution that there is an additional 30 days'
uncertainty without knowing when actual intercalations took place.


## Example
For the sake of a simple example of using the `heniautos`, we can find a "modern" date for the the peace treaty between Athens and Sparta which, according to Thucydides (5.19.1) was signed on this date:

> ἄρχει δὲ τῶν σπονδῶν <ἐν μὲν Λακεδαίμονι> ἔφορος Πλειστόλας
> Ἀρτεμισίου μηνὸς τετάρτῃ φθίνοντος, ἐν δὲ Ἀθήναις ἄρχων Ἀλκαῖος
> Ἐλαφηβολιῶνος μηνὸς ἕκτῃ φθίνοντος. ὤμνυον δὲ οἵδε καὶ ἐσπένδοντο.

> The treaty begins in Lakedaimōn in the ephorate of Pleistolas on the
> fourth day from the end of Artemisios, in Athens in the arkhonship
> of Alkaios on the sixth day from the end of Elaphēboliṓn.

Alkaios was arkhon in 422/421 so to find the sixth day from the end we can start with the calendar for Elaphēboliṓn that year:

    > heniautos 422 --month Ela
         Year     |        Month          | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 422/421   | Elaphēboliṓn          |   1 | BCE 0421-Mar-19 | 237
    BCE 422/421   | Elaphēboliṓn          |   2 | BCE 0421-Mar-20 | 238
    BCE 422/421   | Elaphēboliṓn          |   3 | BCE 0421-Mar-21 | 239
    BCE 422/421   | Elaphēboliṓn          |   4 | BCE 0421-Mar-22 | 240
    BCE 422/421   | Elaphēboliṓn          |   5 | BCE 0421-Mar-23 | 241
    BCE 422/421   | Elaphēboliṓn          |   6 | BCE 0421-Mar-24 | 242
    BCE 422/421   | Elaphēboliṓn          |   7 | BCE 0421-Mar-25 | 243
    BCE 422/421   | Elaphēboliṓn          |   8 | BCE 0421-Mar-26 | 244
    BCE 422/421   | Elaphēboliṓn          |   9 | BCE 0421-Mar-27 | 245
    BCE 422/421   | Elaphēboliṓn          |  10 | BCE 0421-Mar-28 | 246
    BCE 422/421   | Elaphēboliṓn          |  11 | BCE 0421-Mar-29 | 247
    BCE 422/421   | Elaphēboliṓn          |  12 | BCE 0421-Mar-30 | 248
    BCE 422/421   | Elaphēboliṓn          |  13 | BCE 0421-Mar-31 | 249
    BCE 422/421   | Elaphēboliṓn          |  14 | BCE 0421-Apr-01 | 250
    BCE 422/421   | Elaphēboliṓn          |  15 | BCE 0421-Apr-02 | 251
    BCE 422/421   | Elaphēboliṓn          |  16 | BCE 0421-Apr-03 | 252
    BCE 422/421   | Elaphēboliṓn          |  17 | BCE 0421-Apr-04 | 253
    BCE 422/421   | Elaphēboliṓn          |  18 | BCE 0421-Apr-05 | 254
    BCE 422/421   | Elaphēboliṓn          |  19 | BCE 0421-Apr-06 | 255
    BCE 422/421   | Elaphēboliṓn          |  20 | BCE 0421-Apr-07 | 256
    BCE 422/421   | Elaphēboliṓn          |  21 | BCE 0421-Apr-08 | 257
    BCE 422/421   | Elaphēboliṓn          |  22 | BCE 0421-Apr-09 | 258
    BCE 422/421   | Elaphēboliṓn          |  23 | BCE 0421-Apr-10 | 259
    BCE 422/421   | Elaphēboliṓn          |  24 | BCE 0421-Apr-11 | 260
    BCE 422/421   | Elaphēboliṓn          |  25 | BCE 0421-Apr-12 | 261
    BCE 422/421   | Elaphēboliṓn          |  26 | BCE 0421-Apr-13 | 262
    BCE 422/421   | Elaphēboliṓn          |  27 | BCE 0421-Apr-14 | 263
    BCE 422/421   | Elaphēboliṓn          |  28 | BCE 0421-Apr-15 | 264
    BCE 422/421   | Elaphēboliṓn          |  29 | BCE 0421-Apr-16 | 265
    
`heniautos 422 --month Ela` means "show me the calendar for the month Elaphēboliṓn in 422/421 BCE. Counting backwards (inclusively so that the 29th is the first day) the sixth day is April 11, 421 BCE.

This is not to be taken as _truth_. Meritt (1928, 109) first made it
April 9 while Dinsmoor (1931, 334-335) said April 10. Meritt then
citicized Dinsmoor at some length (1932, 146-151) to conclude (1932,
178) that it should be April 11--Heniautos arrives at this date but
by a different path than Meritt. Gomme concludes that it should be
"about March 12" (1945-1981, 4.711-713) because he has a different
view about the intercalations. Most recently, Planeux calculates April
11 again (forthcoming, 187).

That said, the date given by Heniautos is within two days of all
calculations, or thirty days if there is a difference in
intercalation. That is not bad over a span of 2,442 years or over 890,000 days. This margin of error should hold for any ancient
date. The cited discussions are complex, and Heniautos can hopefully help
anyone less steeped in ancient Athenian calendar equations follow
along and check their calculations.

## Learn More

Please read the [Guide](guide/) for more about the Athenian calendar and what calendar equations are and how they're used, as well as for details about the usage of `heniautos` command, the `calendar-equation` command, and the Python library.

## Works Cited

* Dinsmoor, William Bell. 1931. _The Archons of Athens in the
  Hellenistic Age_. Cambridge: Harvard University Press.
* Gomme, A. W., A. Andrewes, and K. J. Dover. 1945-1981. _A Historical
  Commentary on Thucydides_. 5 vols. Oxford: Oxford University Press.
* Meritt, Benjamin D. 1928. _The Athenian Calendar in the Fifth
  Century_. Cambridge: Harvard University Press.
* ----------. 1932. _Athenian Financial Documents of the Fifth
  Century_. Ann Arbor: University of Michigan Press.
* Planeux, Christopher. Forthcoming. _The Athenian Year Primer_.


