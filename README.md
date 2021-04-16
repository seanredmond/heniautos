# Heniautos

Naive ancient Attic calendar generator

## The Basics

`heniautos` (Greek for ["the span of a
year"](https://logeion.uchicago.edu/%E1%BC%90%CE%BD%CE%B9%CE%B1%CF%85%CF%84%CF%8C%CF%82))
tries to generate what the ancient Athenian calendar _might have_ been
for any given year.

The Athenian calendar functioned according to a few certain principals:

* It was
  [lunisolar](https://en.wikipedia.org/wiki/Lunisolar_calendar),
  depending partly on the sun, partly on the moon.
* There were twelve months. Each began on the new moon and had 30 days
  (called a "full" month) or 29 (called "hollow")
* The year began on the first new moon following the summer solstice
* Twelve lunar months is 11 days shorter than one solar year, so about
  every third year a thirteenth month to be added ("intercalated") to
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
moon by observation, by calculation, or even by guessing? and there
seem to be as many answers to these questions as there are scholars
studying them.


`heniautos` generates "naive" calendars, aligning ancient Greek dates with Julian calendar dates, according to astronomical data \(provided by the [`Skyfield`](https://rhodesmill.org/skyfield/) library\) using a few simple rules:

1. Each month begins on the "observed" new moon, two days after the [astronomical conjunction](https://en.wikipedia.org/wiki/New_moon)
2. The year begins on the first observed new moon on or after the day of the summer solstice.
3. Intercalations are made when _astronomically_ necessary. Essentially, if one year ends close enough to the summer solstice that twelve lunar months will not be enough to reach the next solstice, then the next year will be intercalary.

For example, `heniautos`' calendar for 416/415 BCE:

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

Notice that the hollow and full months do not alternate regularly (unless you observed enough over a long enough period of time to see the actual, natural cycles of the moon). 19-year cycles of intercalation recognized by the ancients \([Metonic cycles](https://en.wikipedia.org/wiki/Metonic_cycle), 7 intercalations every 19 years\) do appear in `heniautos`, but by observation rather than by prescription.

An example of an intercalary year is 417/416 BCE:

|  # | Month        | Julian Date     | # days|
|---:|--------------|-----------------|------:|
|  1 | Hekatombaiṓn | BCE 0417-Jul-01 | 29    |
|  2 | Metageitniṓn | BCE 0417-Jul-30 | 30    |
|  3 | Boēdromiṓn   | BCE 0417-Aug-29 | 29    |
|  4 | Puanepsiṓn   | BCE 0417-Sep-27 | 30    |
|  5 | Maimaktēriṓn | BCE 0417-Oct-27 | 30    |
|  6 | Poseidēiṓn   | BCE 0417-Nov-26 | 29    |
|  7 | Poseidēiṓn hústeros | BCE 0417-Dec-25 | 30    |
|  8 | Gamēliṓn     | BCE 0416-Jan-24 | 30    |
|  9 | Anthestēriṓn | BCE 0416-Feb-23 | 29    |
| 10 | Elaphēboliṓn | BCE 0416-Mar-24 | 30    |
| 11 | Mounuchiṓn   | BCE 0416-Apr-23 | 29    |
| 12 | Thargēliṓn   | BCE 0416-May-22 | 30    |
| 13 | Skirophoriṓn | BCE 0416-Jun-21 | 29    |

Since the 12th month ends on June 20, before the solstice (June 28 on the Julian calendar at this time), a year needed a 13th month to extend  through to the beginning of the next year, after the solstice. Athenians intercalated by repeating one of the months. By default, `heniautos` intercalates a second Poseidēiṓn which seems most common, but you can choose other months.


However the Athenians had to make a lot of ad hoc adjustments to keep the calendar aligned with the seasons and the adjustments they made were, for practical purposes, rather random and unpredictable. The only adjustment `heniautos` makes is to add a month ("intercalate") where it seems necessary. These probably do not line up with actual historical intercalations, but it's good enough to get a feel for the Athenian calendar, and to place any date (5th century BCE date, at least) within about a month of a Julian date.

The ancient Greeks used a [lunisolar](https://en.wikipedia.org/wiki/Lunisolar_calendar) calendar in which the months were determined bylunar rhythms but the year governed by solar events. The mismatch of two made it all very complicated. Similar calendars with different names for the months and different times for the start of the new year were used across most of Greece and Greek colonies. `heniautos` is limited to the Athenian calendar, the for which we have the most evidence.

The main principles of the Attic calendar are:

1. There are 12 months:
	1. Hekatombaiṓn
  	1. Metageitniṓn
  	1. Boēdromiṓn
  	1. Puanepsiṓn
  	1. Maimaktēriṓn
  	1. Poseidēiṓn
  	1. Gamēliṓn
  	1. Anthestēriṓn
  	1. Elaphēboliṓn
  	1. Mounuchiṓn
  	1. Thargēliṓn
  	1. Skirophoriṓn 
1. The year begins on the first new moon after the summer solstice.
2. Months starts on the _visible_ new moon, when the first sliver of the waxing crescent can be seen.
3. Days begin and end at sundown.

We tend to think of the "new moon" as the _absence_ of any moon in the sky because that is the conceptual opposite of the full moon. For the ancient Greeks (and many cultures then and now) the new moon was the first sliver of moon to appear as it started to wax. When that was observed 

`heniautos` uses [`Skyfield`](https://rhodesmill.org/skyfield/) to find these astronomical events in the past and construct a "naive" calendar around them. The _visible_ new moon is taken to be the date calculated by `Skyfield` + 2 days. The moment of the modern astronomical definition of the ["new moon"](https://en.wikipedia.org/wiki/New_moon) takes place during the daytime


The first two principles affect how we identify the beginning of a month based on modern astronomical calculations find a particular conjunction which is not actually visible (except during a solar eclipse). Skyview, which Heniautos uses, date the new moon the the day (or night, really) _before_ this conjunction when the moon is _about to disappear_. Therefore the visible new moon is one day after Skyview's calculated new moon.


Thucydides (5.19.1) quotes the peace treaty between Athens and Sparta
which contains this date:

> ἄρχει δὲ τῶν σπονδῶν <ἐν μὲν Λακεδαίμονι> ἔφορος Πλειστόλας
> Ἀρτεμισίου μηνὸς τετάρτῃ φθίνοντος, ἐν δὲ Ἀθήναις ἄρχων Ἀλκαῖος
> Ἐλαφηβολιῶνος μηνὸς ἕκτῃ φθίνοντος. ὤμνυον δὲ οἵδε καὶ ἐσπένδοντο.

> The treaty begins in Lakedaimōn in the ephorate of Pleistolas on the
> fourth day from the end of Artemisios, in Athens in the arkhonship
> of Alkaios on the sixth day from the end of Elaphēboliṓn.

First, A year is named according to magistrates who served for the year. At Sparta the was one of the _éphoroi_, at Athens the _árkhōn epṓnumos_ or "eponymous archon." Alkaios held this position in 422/1 BCE. Why the year is written that way, as spanning two years and why it can be hard to pin down a Greek date to a specific Julian date depends on the specifics of how Attic calendar (an those of other cities) operated.

Some essentials:

* We conventionally use the [Julian
  calendar](https://en.wikipedia.org/wiki/Julian_calendar) for ancient
  dates. This means there are leap years, but not
  [Gregorian](https://en.wikipedia.org/wiki/Gregorian_calendar)
  corrections. Since there is no year 0, the leap years are "off" by
  one--421 BCE is a leap year, not 420.
* The Attic calendar begins after the summer solstice. So Alkaios took
  office in summer 422 and the year and his term ran until
  summer 421. Hence "422/1." The summer solstice today occurs July 20
  or 21 but, Because of the slight inaccuracy of the Julian calendar,
  the drifts later for ancient dates. In the 5th century BCE, it falls
  usually on the 28th.
* The Attic calendar consisted of twelve months, and each began on the
  "visible" new moon, meaning when the first sliver of the waxing moon
  could be seen in the night sky. This comes one night after modern,
  mathematical calculations of the new moon. Thus the year began on
  the first _visible_ new moon after the summer solstice. The months
  are, in order:
  
* Days were reckoned from sundown to sundown, so the first day of the
  month began during the evening when the new moon was first
  visible. The "business" hours were what we might think of as the
  next day.


