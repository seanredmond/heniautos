# Heniautos

Naive ancient Attic calendar generator

## The Basics

`heniautos` (Greek for ["the span of a
year"](https://logeion.uchicago.edu/%E1%BC%90%CE%BD%CE%B9%CE%B1%CF%85%CF%84%CF%8C%CF%82))
generates examples of _possible_ Athenian calendars for any given year, ancient or modern, and provides some features for exploring the calendar and working with calendar equations. `heniautos` is hopefully useful for:

* Learning about and teaching the ancient Athenian Calendar
* Following along with often complex discussions of ancient dating event in ancient Greek hsitory
* Just having fun with questions like "When would the City Dionysia be this year, if it was still being held."

While what A. W. Gomme wrote in 1970[^1] is still true today—"It does
not seem easy at the present time to make any statement about the
Athenian calendar which is both significant and undisputed"—there are a few principalson which the Athenian calendar functioned that are certain:

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

1. Each month begins, by default, on an "observed" new moon two days after the [astronomical conjunction](https://en.wikipedia.org/wiki/New_moon). You can choose other values.
2. The year begins on the first observed (by rule #1) new moon on or after the day of the summer solstice.
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


However the Athenians had to make a lot of ad hoc adjustments to keep the calendar aligned with the seasons and the adjustments they made were, for practical purposes, rather random and unpredictable. The only adjustment `heniautos` makes is to add a month ("intercalate") where it seems necessary. These probably do not line up with actual historical intercalations, but it's good enough to get a feel for the Athenian calendar, and to place any date within about one or two days a Julian date with the caution that there is an additional 30 days' uncertainty without knowing when actual intercalations took place.

## Command-line script

This package installs a command-line script (also `heniautos`) to make lookups easy. The command. The simplest usage takes a year (BCE) and prints out the full calendar. It gives the Greek year, Greek month name, day of that month, Julian date, and day of the year:

    > heniautos 416
    "BCE 416/415"	"Hekatombaiṓn"	1	"BCE 0416-Jul-20"	1
    "BCE 416/415"	"Hekatombaiṓn"	2	"BCE 0416-Jul-21"	2
    "BCE 416/415"	"Hekatombaiṓn"	3	"BCE 0416-Jul-22"	3
    "BCE 416/415"	"Hekatombaiṓn"	4	"BCE 0416-Jul-23"	4
    "BCE 416/415"	"Hekatombaiṓn"	5	"BCE 0416-Jul-24"	5
	...
	"BCE 416/415"	"Skirophoriṓn"	26	"BCE 0415-Jul-05"	351
    "BCE 416/415"	"Skirophoriṓn"	27	"BCE 0415-Jul-06"	352
    "BCE 416/415"	"Skirophoriṓn"	28	"BCE 0415-Jul-07"	353
    "BCE 416/415"	"Skirophoriṓn"	29	"BCE 0415-Jul-08"	354
    "BCE 416/415"	"Skirophoriṓn"	30	"BCE 0415-Jul-09"	355
    
If you save this output to a file it is suitable for importing into a spreadsheet.

You can get a summary of just the months with `-m`:

    > heniautos 416 -m
    "BCE 416/415"	"Hekatombaiṓn"	"BCE 0416-Jul-20"	29
    "BCE 416/415"	"Metageitniṓn"	"BCE 0416-Aug-18"	30
    "BCE 416/415"	"Boēdromiṓn"	"BCE 0416-Sep-17"	29
    "BCE 416/415"	"Puanepsiṓn"	"BCE 0416-Oct-16"	30
    "BCE 416/415"	"Maimaktēriṓn"	"BCE 0416-Nov-15"	29
    "BCE 416/415"	"Poseidēiṓn"	"BCE 0416-Dec-14"	30
    "BCE 416/415"	"Gamēliṓn"	"BCE 0415-Jan-13"	30
    "BCE 416/415"	"Anthestēriṓn"	"BCE 0415-Feb-12"	30
    "BCE 416/415"	"Elaphēboliṓn"	"BCE 0415-Mar-14"	29
    "BCE 416/415"	"Mounuchiṓn"	"BCE 0415-Apr-12"	30
    "BCE 416/415"	"Thargēliṓn"	"BCE 0415-May-12"	29
    "BCE 416/415"	"Skirophoriṓn"	"BCE 0415-Jun-10"	30

If you enter two years you will get the calendar for the span of those years. This is most useful with the year summary (`-y`):

    > heniautos 416 411 -y
    "BCE 416/415"	"O"	"BCE 0416-Jul-20"	355
    "BCE 415/414"	"O"	"BCE 0415-Jul-10"	354
    "BCE 414/413"	"I"	"BCE 0414-Jun-29"	384
    "BCE 413/412"	"O"	"BCE 0413-Jul-17"	354
    "BCE 412/411"	"I"	"BCE 0412-Jul-06"	384
    "BCE 411/410"	"O"	"BCE 0411-Jul-25"	354
    
This output is the Greek year, whether it is normal (O) or intercalary (I), the date on which the year starts, and the number of days in the year.

Years are treated as BCE by default, but you can change this with `--as-ce`:

    heniautos 2020 -m --as-ce
    " CE 2020/2021"	"Hekatombaiṓn"	" CE 2020-Jun-23"	29
    " CE 2020/2021"	"Metageitniṓn"	" CE 2020-Jul-22"	30
    " CE 2020/2021"	"Boēdromiṓn"	" CE 2020-Aug-21"	29
    " CE 2020/2021"	"Puanepsiṓn"	" CE 2020-Sep-19"	29
    " CE 2020/2021"	"Maimaktēriṓn"	" CE 2020-Oct-18"	30
    " CE 2020/2021"	"Poseidēiṓn"	" CE 2020-Nov-17"	29
    " CE 2020/2021"	"Poseidēiṓn hústeros"	" CE 2020-Dec-16"	30
    " CE 2020/2021"	"Gamēliṓn"	" CE 2021-Jan-15"	29
    " CE 2020/2021"	"Anthestēriṓn"	" CE 2021-Feb-13"	30
    " CE 2020/2021"	"Elaphēboliṓn"	" CE 2021-Mar-15"	30
    " CE 2020/2021"	"Mounuchiṓn"	" CE 2021-Apr-14"	29
    " CE 2020/2021"	"Thargēliṓn"	" CE 2021-May-13"	30
    " CE 2020/2021"	"Skirophoriṓn"	" CE 2021-Jun-12"	30

## Example
Thucydides (5.19.1) quotes the peace treaty between Athens and Sparta
which contains this date:

> ἄρχει δὲ τῶν σπονδῶν <ἐν μὲν Λακεδαίμονι> ἔφορος Πλειστόλας
> Ἀρτεμισίου μηνὸς τετάρτῃ φθίνοντος, ἐν δὲ Ἀθήναις ἄρχων Ἀλκαῖος
> Ἐλαφηβολιῶνος μηνὸς ἕκτῃ φθίνοντος. ὤμνυον δὲ οἵδε καὶ ἐσπένδοντο.

> The treaty begins in Lakedaimōn in the ephorate of Pleistolas on the
> fourth day from the end of Artemisios, in Athens in the arkhonship
> of Alkaios on the sixth day from the end of Elaphēboliṓn.

Alkaios was arkhon in 422/421, so we can find the sixth day from the end (counting inclusively) like so:

    heniautos 422 --month Ela |tail -n 6
    "BCE 422/421"	"Elaphēboliṓn"	24	"BCE 0421-Apr-11"	260
    "BCE 422/421"	"Elaphēboliṓn"	25	"BCE 0421-Apr-12"	261
    "BCE 422/421"	"Elaphēboliṓn"	26	"BCE 0421-Apr-13"	262
    "BCE 422/421"	"Elaphēboliṓn"	27	"BCE 0421-Apr-14"	263
    "BCE 422/421"	"Elaphēboliṓn"	28	"BCE 0421-Apr-15"	264
    "BCE 422/421"	"Elaphēboliṓn"	29	"BCE 0421-Apr-16"	265
    
This is not to be taken as _truth_. Meritt first made it April 9[^2] while Dinsmoor[^3] said April 10. Meritt then citicized Dinsmoor at some length[^4] to conclude[^5] that it should be April 11--`heniautos` arrives at this date but by a different path than Meritt. Gomme concludes that it should be "about March 12"[^6] because he has a different view about the intercalations. Most recently, Planeux calculates April 11 again.[^7]

That said, the date given by `heniautos` is within two days of all calculations, or thirty days if there is a difference in intercalation. This margin of error should hold for any ancient date. The cited discussions are complex, and `heniautos` should help anyone less steeped in ancient Athenian calendar equations follow along and check their calculations.


[^1]: Gomme, A. W., Andrewes, and Dover (1945-1981) 4.264.
[^2]: Meritt (1928) 109.
[^3]: Dinsmoor (1931) 334-335.
[^4]: Meritt (1932) 146-151.
[^5]: Meritt (1932) 146-151.
[^6]: Gomme, A. W., Andrewes, and Dover (1945-1981) 4.711-713.
[^7]: Planeaux (forthcoming) 187

## Works Cited

* Dinsmoor, William Bell. 1931. _The Archons of Athens in the Hellenistic Age_. Cambridge: Harvard University Press. 
* Gomme, A. W., A. Andrewes, and K. J. Dover. 1945-1981. _A Historical Commentary on Thucydides_. 5 vols. Oxford: Oxford University Press.
* Meritt, Benjamin D. 1928. _The Athenian Calendar in the Fifth Century_. Cambridge: Harvard University Press. 
* ----------. 1932. _Athenian Financial Documents of the Fifth Century_. Ann Arbor: University of Michigan Press.
* Planeux, Christopher. Forthcoming. _The Athenian Year Primer_.


