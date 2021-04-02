# Heniautos

Naive ancient Attic calendar generator

## Warning

Do _not_ get interested in the ancient Attic calendar. It is a
fascinating but frustrating topic, full of contradictory evidence and
unsolvable puzzles. The further you read, the less anyone can help
you...

## The Basics

`heniautos` (Greek for ["the span of a year"](https://logeion.uchicago.edu/%E1%BC%90%CE%BD%CE%B9%CE%B1%CF%85%CF%84%CF%8C%CF%82)) tries to generate what the ancient Athenian calendar _might have_ been for any given year or span of years. However the Athenians had to make a lot of ad hoc adjustments to keep the calendar aligned with the seasons and the adjustments they made were, for practical purposes, rather random and unpredictable. The only adjustment `heniautos` makes is to add a month ("intercalate") where it seems necessary. These probably do not line up with actual historical intercalations, but it's good enough to get a feel for the Athenian calendar, and to place any date (5th century BCE date, at least) within about a month of a Julian date.

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


