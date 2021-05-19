# Programming with Heniautos

## Overview

The most important functions in Heniautos, if you are lookig to generate calendars, are:

* `festival_calendar()`
* `prytany_calendar()`

To understand the difference between the two, see [Festival Calendar Basics](festival-calendar-basics.md) and [The Conciliar Calendar](conciliar-calendar.md). 

To use these functions you will need to know about some constants, initializing data, and working with BCE years

And if you are working with calendar equations, the important functions are:

* `festival_doy()`
* `prytany_doy()`
* `equations()`
* `collations()`

## Initializing Data

Throughout this guide, we will assume that Heniautos has been imported with this command:

    >>> import heniautos as ha
    
Therefore all Heniautos functions and constants will be prefixed with `ha.`

You will need to initial the Henautos data before using any functions that does calendar calculations. This is necessary to set up some of the configuration required by the [Skyfield](https://rhodesmill.org/skyfield/) that Heniautos uses.

    >>> ha.init_data()
    'de422.bsp'
    
`init_data()` returns the path to the [ephemeris](https://rhodesmill.org/skyfield/planets.html) or file containing astronomical data it is using. By default, this is the first copy of a file named `de422.bsp` it can find in the file path.

If a copy of the file cannot be found it will automatically be downloaded into the current working directory. Since the file is over 600 MB, it is best to avoid this so, perhaps after downloading it the first time, keep a copy where you can remember its location and give the path to the ephemeris to `init_data()`

    >>> ha.init_data(eph="/full/path/to/you/copy/of/de422.bsp")
    '/full/path/to/you/copy/of/de422.bsp'
    
You only need to initailized the data once in a session or script, you cannot reinitialize it without forcing with `ha.init_data(force=True)`


## Constants

There are a number of constants that occur in the return values of many function and can be used as parameted

### `ha.Months`

These constants represent months in the Athenian calendar:

    >>> list(ha.Months)
    [<Months.HEK: 1>, <Months.MET: 2>, <Months.BOE: 3>, 
    <Months.PUA: 4>, <Months.MAI: 5>, <Months.POS: 6>, <Months.GAM: 7>, 
    <Months.ANT: 8>, <Months.ELA: 9>, <Months.MOU: 10>, 
    <Months.THA: 11>, <Months.SKI: 12>, <Months.INT: 13>, 
    <Months.UNC: 14>]
    
You can always use integer values like 1 for Hekatombaiṓn or 9 for Elaphēboliṓn, but it is safer to use `ha.Months.HEK` and `ha.Months.ELA`. An intercalated month is always represented by `INT`. `UNK` is explained under `ha.Visible.DINSMOOR`.

### `ha.Prytanies`

Like months, there are constants for representing prytanies.

    >>> list(ha.Prytanies)
    [<Prytanies.I: 1>, <Prytanies.II: 2>, <Prytanies.III: 3>, 
    <Prytanies.IV: 4>, <Prytanies.V: 5>, <Prytanies.VI: 6>, 
    <Prytanies.VII: 7>, <Prytanies.VIII: 8>, <Prytanies.IX: 9>, 
    <Prytanies.X: 10>, <Prytanies.XI: 11>, <Prytanies.XII: 12>, 
    <Prytanies.XIII: 13>]
    
### Tuple Convention

In many places, a tuple consisting of one of the above constants with an integer for the day of the month or prytany is used to represent a full date. For example, `(ha.Months.ELA, 10)` for Elaphēboliṓn 10, or `(ha.Prytanies.VIII, 21)` for prytany VIII 21.

### Prytany Types

The concilar calendar consisted of a different number of prytanies (10, 12, or 13) at different times in Athens' history, corresponding to the number of _phulaí_ (or tribes) that existed. Some functions for calendar equations need to know how many prytanies are requires. `ha.Prytany` represents these with the following values:

| Value             | Meaning | Years in effect |
|-------------------|---------|-----------------|
| `ha.Prytany.AUTO` | Determine based on year (passed to function separately) | |
| `ha.Prytany.QUASI_SOLAR` | 10 prytanies based on a seeparate 365-day concilar year | 508-410 BCE |
| `ha.Prytany.ALIGNED_10` | 10 prytanies beginning and ending with the festival calendar | 409-308 BCE | 
| `ha.Prytany.ALIGNED_12` | 12 prytanies beginning and ending with the festival calendar | 307-224 BCE, 200-101 BCE |
| `ha.Prytany.ALIGNED_13` | 13 prytanies beginning and ending with the festival calendar | 223-201 BCE |
    
### Visibility Rules

Heniautos approximates the observation of the new by counting is a certain number of dates after the astronomical conjunction. By the default is two days after--that is, if the new moon conjunction is June 10, Heniautos calculates it as vivible June 12 and therefore starts a month on that date. For functions that calculate lunar months you can set this to 1 or 0 days using thee constants:

| Value                    | Meaning  |
|--------------------------|----------|
| `ha.Visible.CONJUNCTION` | New moon observed day of astronomical conjunction |
| `ha.Visible.NEXT_DAY`    | New moon observed 1 day after conjunction |
| `ha.Visible.SECOND_DAY`  | (Default) New moon observed 2 days after conjunction |
| `ha.Visible.DINSMOOR`    | Use dates calculated by Dinsmoor (see below) 

### Other Constants

These are used interally by Heniautos but may be useful for your own programs

#### `ha.Seasons`

Solar events. See `solar_events()`, below.

    >>> list(ha.Seasons)
    [<Seasons.SPRING_EQUINOX: 0>, <Seasons.SUMMER_SOLSTICE: 1>, 
    <Seasons.AUTUMN_EQUINOX: 2>, <Seasons.WINTER_SOLSTICE: 3>]
    
#### `ha.Phases`

Phases of the moon. See `moon_phases()`, below.

    >>> list(ha.Phases)
    [<Phases.NEW: 0>, <Phases.FIRST_Q: 1>, <Phases.FULL: 2>, 
    <Phases.LAST_Q: 3>]
    
#### Month Names, and Abbreviations

These are available, but you should use `month_label()` (and `prytany_label()`), below.

    >>> ha.MONTH_NAMES
    ('Hekatombaiṓn', 'Metageitniṓn', 'Boēdromiṓn', 'Puanopsiṓn', 
    'Maimaktēriṓn', 'Posideiṓn', 'Gamēliṓn', 'Anthestēriṓn', 
    'Elaphēboliṓn', 'Mounuchiṓn', 'Thargēliṓn', 'Skirophoriṓn')

    >>> ha.MONTH_ABBREVS
    ('Hek', 'Met', 'Boe', 'Pua', 'Mai', 'Pos', 'Gam', 'Ant', 'Ela', 'Mou', 
    'Tha', 'Ski')

    >>> ha.MONTH_NAMES_GK
    ('Ἑκατομβαιών', 'Μεταγειτνιών', 'Βοηδρομιών', 'Πυανοψιών', 
    'Μαιμακτηριών', 'Ποσιδειών', 'Γαμηλιών', 'Ἀνθεστηριών', 'Ἑλαφηβολιών', 
    'Μουνυχιών', 'Θαργηλιών', 'Σκιροφοριών')


## Generating Calendars

### `bce_as_negative()`

Calendar calculations require a year, and if since you are working with _ancient_ Greek calendars, those years will probably by BCE. Years BCE are represented as negative numbers counting backwards from 0 = 1 BCE. This means that -99 = 100 BCE, -299 = 300 BCE, etc. To make this simpler, `bce_as_negative()` converts a _positive_ BCE year number to the required negative integer:

    >>> ha.bce_as_negative(300)
    -299

### `festival_calendar()`

This generates a full Athenian calendar for a given year. For instance, to get the calendar for 300 BCE:

    >>> ha.festival_calendar(-349)

Or, using `bce_as_negative()`:    
    
    >>> ha.festival_calendar(ha.bce_as_negative(350))

The return value is a nested data structure (this is what you will probably be looping over to output data from you programs):

| Level | Object   | Type    | Contains |
|-------|----------|---------|-----------------------|
| 0     | Year     | `tuple` | one `dict` per month  |
| 1     | Month    | `dict`  | "month": `str`, "constant": `ha.Months` constant, "days": `tuple` |
| 2     | Days     | `tuple` | one `dict` per day    |
| 3     | Day      | `dict`  | "day": `int`, the day of the month, "date": `Time` object, "doy": `int`, the day of the year     |

    >>> # Get the calendar for 350 BCE
    >>> c = ha.festival_calendar(ha.bce_as_negative(350))
    >>> # How many months?
    >>> len(c)
    12

    >>> # Get the 3rd month
    >>> m = c[2]
    >>> m["month"]
    'Puanopsiṓn'
    >>> m["constant"]
    <Months.PUA: 4>
    >>> # How many days?
    >>> len(m["days"])
    30
    
    >>> # Get the 15th day (Puanopsiṓn 15)
    >>> d = m["days"][14]
    >>> d["day"]
    15
    >>> d["date"]
    <Time tt=1593879.9999935674>
    >>> # What day of the year is it?
    >>> d["doy"]
    104
    
The `Time` object in the "date" member of the "days" `dict` is not very useful by itself (it is a Julian time, a type provided by Skyview), but see below for its use in `as_eet()` and `as_gmt()`

#### Intercalations

Intercalations are made when astronomically necessary--then the twelfth month would end before the summer soltice. By default, this is handled by adding an intercalary Posideiṓn.

    >>> c = ha.festival_calendar(ha.bce_as_negative(300))
    >>> # If there are 13 months, it is intercalary
    >>> len(c)
    13
    >>> # 6th month should be Posideiṓn
    >>> c[5]["month"]
    'Posideiṓn'
    >>> # 7th month would normally be Gamēliṓn but...
    >>> c[6]["month"]
    'Posideiṓn hústeros'
    >>> # The intercalary month is always identified by Months.INT
    >>> c[6]["constant"]
    <Months.INT: 13>
    
Any month could be intercalated. To generate a calendar with a specific intercalation, use the `intercalate` parameter with a `Months` constant:

    >>> c = ha.festival_calendar(ha.bce_as_negative(300), intercalate=ha.Months.GAM)
    >>> len(c)
    13
    >>> c[5]["month"]
    'Posideiṓn'
    >>> c[6]["month"]
    'Gamēliṓn'
    >>> c[7]["month"]
    'Gamēliṓn hústeros'
    >>> # The intercalary month is always identified by Months.INT
    >>> c[7]["constant"]
    <Months.INT: 13>
    
#### Changing the Visibility Rule

As described above, Heniautos has different rules for approximating the day when the new moon becomes visible, and a new month starts. A specific rule can be selected by supplying a `Visibility` constant as the `rule` parameter. The effect is mostly to move the corresponding Julian dates earlier that the default.

    >>> c = ha.festival_calendar(ha.bce_as_negative(350))
    >>> # Julian date of the first day of the first month
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0350-Jul-11'    
    >>> c = ha.festival_calendar(ha.bce_as_negative(350), rule=ha.Visible.NEXT_DAY)
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0350-Jul-10'
    >>> c = ha.festival_calendar(ha.bce_as_negative(350),  rule=ha.Visible.CONJUNCTION)
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0350-Jul-09' 

(see below for the as `as_eet()` function)

#### Dinsmoor "Visibility"

There is one more rule, `Visible.DINSMOOR`. This uses dates as calculated by William Dinsmoor in Dinsmoor (1931) Tables IX-XXV (pp. 424-440).

    >>> c = ha.festival_calendar(ha.bce_as_negative(350), rule=ha.Visible.DINSMOOR)
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0350-Jul-11'
    
In this example, Dinmoor's calculation is the same as as Heniautos' default but this is not always the case. There are some years for which leaves the specific months undetermined. The are identified by the constant `Months.UNC` (for "uncertain"):

    >>> c = ha.festival_calendar(ha.bce_as_negative(311), rule=ha.Visible.DINSMOOR)
    >>> c[0]["constant"]
    <Months.UNC: 14>
    
These dates are provided for their historical interest. Many discussions of the Athenian calendar began with Dinsmoor's dates in the decades after the publication of _The Archons of Athens in the Hellenistic Age_. However, a great number of the inscriptions Dinsmoor relied on as evidence of the character of specific years have since been redated, and can no longer serve the purposes for which Dinmoor used them,

#### Other Parameters

To get the month names as abbreviations use `abbrev=True`. To get them in Greek, use `greek=True`

    >>> c = ha.festival_calendar(ha.bce_as_negative(350))
    >>> c[0]["month"]
    'Hekatombaiṓn'
    >>> c = ha.festival_calendar(ha.bce_as_negative(350), abbrev=True)
    >>> c[0]["month"]
    'Hek'
    >>> c = ha.festival_calendar(ha.bce_as_negative(350), greek=True)
    >>> c[0]["month"]
    'Ἑκατομβαιών'
    
`greek` overrides `abbrev`. See `month_label()` below for using the `Month` constant to get the transliteration, abbreviation, or Greek name.

### Formatting Dates

Every day returned by `festival_calendar()` has a Julian date equivalent. This is a Skyview `Time` object, as noted above. Use `as_eet()` to get a string representation of the date in Athens time (Eastern European Time) or `as_gmt()` to get Greenwich Mean Time.

    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0350-Jul-11'
    >>> ha.as_gmt(c[0]["days"][0]["date"])
    'BCE 0350-Jul-11' 
    
Add `full=True` to get the date _and_ time (this will make the time zone difference apparent)

    >>> ha.as_eet(c[0]["days"][0]["date"], full=True)
    'BCE 0350-Jul-11 13:59:17 EET'
    >>> ha.as_gmt(c[0]["days"][0]["date"], full=True)
    'BCE 0350-Jul-11 11:59:17 GMT'
    
Neither makes any adjustments for Daylight Savings Time.

### `prytany_calendar()`

Use `prytany_calendar` to get the full calendar for the [concilar year](conciliar-year.md):

    >>> c = ha.prytany_calendar(ha.bce_as_negative(350))
    
The return value is a nested data structure, similar to that from `festival_calendar()`

| Level | Object   | Type    | Contains |
|-------|----------|---------|------------------------|
| 0     | Year     | `tuple` | one `dict` per prytany |
| 1     | Month    | `dict`  | "prytany": `str`, "constant": `ha.Prytanies` constant, "days": `tuple` |
| 2     | Days     | `tuple` | one `dict` per day    |
| 3     | Day      | `dict`  | "day": `int`, the day of the prytany, "date": `Time` object, "doy": `int`, the day of the year     |

    >>> c = ha.prytany_calendar(ha.bce_as_negative(350))
    >>> # How many prytanies?
    >>> len(c)
    10
    
    >>> # Get the 3rd prytany
    >>> p = c[2]
    >>> p["prytany"]
    3
    >>> p["constant"]
    <Prytanies.III: 3>
    >>> # How many days?
    >>> len(p["days"])
    36
    
    >>> # Get the 15th day of the prytany
    >>> d = p["days"][14]
    >>> ha.as_eet(d["date"])
    'BCE 0350-Oct-05'
    >>> d["doy"]
    87

By default, the number of prytanies are determined by the year (see table under "Prytany Types" above)

    >>> c = ha.prytany_calendar(ha.bce_as_negative(400))
    >>> len(c)
    10
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300))
    >>> len(c)
    12
    >>> c = ha.prytany_calendar(ha.bce_as_negative(210))
    >>> len(c)
    13
    >>> c = ha.prytany_calendar(ha.bce_as_negative(200))
    >>> len(c)
    12
    >>> c = ha.prytany_calendar(ha.bce_as_negative(100))
    >>> len(c)
    10
    
Once Roman rule of Athens was firm, the prytany calendar ceased to be used, so the last example, for 100 BCE, is hypothetical. Any year after 201 BCE will have 10 of these "hypothetical" prytanies--this is mainly so you can easily generate a "Classical" prytany calendar for a modern year

    >>> c = ha.prytany_calendar(2021)
    >>> ha.as_eet(c[0]["days"][0]["date"])
    ' CE 2021-Jul-12'
    
You can specify a different number of prytanies via the `pryt_type` parameter, which takes a `Prytany` constant (default `Prytany.AUTO`)

    >>> # There were 12 prytanies in the year 300 BCE
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300))
    >>> len(c)
    12

    >>> # This the default, Prytany.AUTO...
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300), pryt_type=ha.Prytany.AUTO)
    >>> len(c)
    12

    # ...which, for 300 BCE is Prytany.ALIGNED_12  
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300), pryt_type=ha.Prytany.ALIGNED_12)
    >>> len(c)
    12

    >>> # But you can ask for a 10 prytany calendar
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300), pryt_type=ha.Prytany.ALIGNED_10)
    >>> len(c)
    10
    
    >>> # Or a 13 prytany calendar
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300), pryt_type=ha.Prytany.ALIGNED_13)
    >>> len(c)
    13

#### Quasi-solar Conciliar Calendars

The "aligned" version of the conciliar calendar begin and end on the same days as the festival calendar. For most of the fifth century BCE, though, the concilar calendar was a 365-day "solar" year that began on it's own day (although this day changed over time)

    >>> c = ha.festival_calendar(ha.bce_as_negative(430))
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0430-Jul-25'
    >>> c = ha.prytany_calendar(ha.bce_as_negative(430))
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0430-Jul-04'
    
The default start days are taken from Meritt (1961) 218. These "quasi-solar" conciliar years always started in June, but you can specify a different day in July with the `pryt_start` parameter:

    >>> # Default for 430 BCE
    >>> c = ha.prytany_calendar(ha.bce_as_negative(430))
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0430-Jul-04'
    
    >>> # DIfferent day in July
    >>> c = ha.prytany_calendar(ha.bce_as_negative(430), pryt_start=10)
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0430-Jul-10'
    
    >>> # July 9 is the default day for "Hypothetical" quasi-solar 
    >>> # conciliar calendars
    >>> c = ha.prytany_calendar(ha.bce_as_negative(300), pryt_type=ha.Prytany.QUASI_SOLAR)
    >>> ha.as_eet(c[0]["days"][0]["date"])
    'BCE 0300-Jul-09'

Heniautos does not try to handle gracefully the transition from "quasi-solar" to "aligned" conciliar years between 410 and 409 BCE.


#### Rule of Aristotle

They conciliar year usually had prytanies of two different lengths. For instance, an ordinary 10-prytany year had four 36-day prytanies and six 35-day prytanies. A passage in _Athenaion Politeia_ ([43.2](http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0045%3Achapter%3D43%3Asection%3D2)) implies that the longer prytanies all came at the beginning of the year. This has come to be known as the "Rule of Aristotle" which different scholars have believed operated to different degrees.

Heniautos produces conciliar calendars that follow Rule of Aristotle--out of expediency because, unlike the festival calendar and the moon, there no other external guide to the ordering of long and short prytanies. In this example you can see that the first four prytanies are 36-days long and the remaining 35:

    >>> c = ha.prytany_calendar(ha.bce_as_negative(350))
    >>> [len(m["days"]) for m in c]
    [36, 36, 36, 36, 35, 35, 35, 35, 35, 35]

There are two cases where the Rule is not followed by default. In ordinary years in the period of twelve _phulaí_, because there were twelve prytanies and twelve festival months, the lengths of the prytanies simply follow the festival calendar. The same is true for intercalary years in the period of thirteen _phulaí_, when there were _thirteen_ prytanies and _thirteen_ festival months. With `rule_of_aristotle=True` you can force the Rule during these periods as well.

    >>> # Lengths of lunar festival months in 297 BCE
    >>> c = ha.festival_calendar(ha.bce_as_negative(297))
    >>> [len(m["days"]) for m in c]
    [30, 30, 29, 30, 29, 30, 29, 29, 30, 29, 30, 29]
    
    >>> # Lengths of 12 prytanies the same
    >>> c = ha.prytany_calendar(ha.bce_as_negative(297))
    >>> [len(m["days"]) for m in c]
    [30, 30, 29, 30, 29, 30, 29, 29, 30, 29, 30, 29]    
    
    >>> # Apply the rule to put all the 30-day prytanies first
    >>> c = ha.prytany_calendar(ha.bce_as_negative(297), rule_of_aristotle=True)
    >>> [len(m["days"]) for m in c]
    [30, 30, 30, 30, 30, 30, 29, 29, 29, 29, 29, 29]
    
The math of these prytany lengths was calculated for ordinary years with 354 and intercalary years of 384 days. Some years, though, have one day more or one day fewer. In these years the last day is added or subtracted producing a "pseudo-long" or "pseudo-short" prytany that appears to violate the Rule, or an inconsistent prytany length:

    >>> # 346 BCE has 355 days
    >>> c = ha.festival_calendar(ha.bce_as_negative(346))
    >>> sum([len(m["days"]) for m in c])
    355
    >>> # The conciliar year ends with a pseudo-long prytany
    >>> c = ha.prytany_calendar(ha.bce_as_negative(346))
    >>> [len(m["days"]) for m in c]
    [36, 36, 36, 36, 35, 35, 35, 35, 35, 36]
    
    >>> # 306 has 383 days
    >>> c = ha.festival_calendar(ha.bce_as_negative(306))
    >>> sum([len(m["days"]) for m in c])
    383
    >>> # The prytanies have 32-days, except for the last
    >>> c = ha.prytany_calendar(ha.bce_as_negative(306))
    >>> [len(m["days"]) for m in c]
    [32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 31]

#### Visibility Rules

`prytany_calendar()` also take a `rule` parameter. This has no effect for quasi-solar conciliar years. For all other years types of conciliar calendar the visibility rule is used to detemine the first and last days of the year, as well as the start days of all prytanies for the periods when these follow the lunar months

### Month and Prytany Names

Use `month_label()` to get a human-readable name for a `Months` constant. This takes the same `abbrev` and `greek` parameters described for `festival_calendar()`:

    >>> ha.month_label(ha.Months.ELA)
    'Elaphēboliṓn'
    >>> ha.month_label(ha.Months.ELA, abbrev=True)
    'Ela'
    >>> ha.month_label(ha.Months.ELA, greek=True)
    'Ἑλαφηβολιών'
    
Roman numerals are conventionally used for prytanies. Use `prytany_label` to get these for `Prytanies` constants
    
    >>> ha.prytany_label(ha.Prytanies.VIII)
    'VIII'
    
## Finding Dates Directly

Rather than generating an entire calendar, you may only want find the Athenian date for a Julian date or vice versa.

`find_date()` will find the Athenan calendar date

def find_date(year, month, day, intercalate=Months.POS, abbrev=False,
def festival_to_julian(month, day, year, rule=Visible.SECOND_DAY):
def prytany_to_julian(prytany, day, year, rule=Visible.SECOND_DAY):


def is_bce(t):
def tt_day(t):
def tt_round(t, adv=0):
def date(y, m, d, h=9):
def add_hours(t, h):
def add_days(t, d):
def add_years(t, y):
def span(first, second):
def solar_event(year, e):
def summer_solstice(year):
def moon_phases(year, p):
def new_moons(year):
def visible_new_moons(year, rule=Visible.SECOND_DAY):
def calendar_months(year, rule=Visible.SECOND_DAY):
def festival_months(year, intercalate=Months.POS, abbrev=False, greek=False,
def phulai_count(year):
def prytanies(year, pryt_type=Prytany.AUTO, pryt_start=Prytany.AUTO,
def festival_doy(month, day):
def prytany_doy(pry, day, pryt_type=Prytany.AUTO, year=None):
def doy_to_julian(doy, year, rule=Visible.SECOND_DAY):
def equations(months, prytanies, pryt_type=Prytany.AUTO, year=None):

## Works Cited

* Dinsmoor, William Bell. 1931. _The Archons of Athens in the Hellenistic Age_. Cambridge: Harvard University Press.
* Meritt, Benjamin D. 1961. _The Athenian Year_. Sather Classical Lectures 32. Berkeley: University of California Press.

