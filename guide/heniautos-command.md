# `heniautos` Command

[Top: Intro](README.md) | [Previous: Conciliar Calendar](conciliar-calendar.md) | [Next: Calendar Equations](calendar-equations.md)

Heniautos installs a command-line script (`heniautos`) that you can run in a terminal window. This offers convenient access to most of the features of Heniautos. 

## Basic calendars

### Daily

Provide `heniautos` a (Julian) year to get the full festival calendar for the Athenian year that began in that Julian year BCE. For instance, for the 424/3 BCE calendar, `heniautos 424` (output truncated):

    > heniautos 424
         Year     |         Month         | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 424/423   | Hekatombaiṓn          |   1 | BCE 0424-Jul-19 |   1
    BCE 424/423   | Hekatombaiṓn          |   2 | BCE 0424-Jul-20 |   2
    BCE 424/423   | Hekatombaiṓn          |   3 | BCE 0424-Jul-21 |   3
    BCE 424/423   | Hekatombaiṓn          |   4 | BCE 0424-Jul-22 |   4
    ...
    BCE 424/423   | Skirophoriṓn          |  26 | BCE 0423-Jul-04 | 351
    BCE 424/423   | Skirophoriṓn          |  27 | BCE 0423-Jul-05 | 352
    BCE 424/423   | Skirophoriṓn          |  28 | BCE 0423-Jul-06 | 353
    BCE 424/423   | Skirophoriṓn          |  29 | BCE 0423-Jul-07 | 354
    
### Monthly

Adding the `-m` or `--month-summary` option results in a monthly calendar.
    
    > heniautos 424 -m
         Year     |         Month         |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 424/423   | Hekatombaiṓn          | BCE 0424-Jul-19 |   29
    BCE 424/423   | Metageitniṓn          | BCE 0424-Aug-17 |   30
    BCE 424/423   | Boēdromiṓn            | BCE 0424-Sep-16 |   29
    BCE 424/423   | Puanopsiṓn            | BCE 0424-Oct-15 |   29
    BCE 424/423   | Maimaktēriṓn          | BCE 0424-Nov-13 |   30
    BCE 424/423   | Posideiṓn             | BCE 0424-Dec-13 |   30
    BCE 424/423   | Gamēliṓn              | BCE 0423-Jan-12 |   29
    BCE 424/423   | Anthestēriṓn          | BCE 0423-Feb-10 |   30
    BCE 424/423   | Elaphēboliṓn          | BCE 0423-Mar-12 |   30
    BCE 424/423   | Mounuchiṓn            | BCE 0423-Apr-11 |   29
    BCE 424/423   | Thargēliṓn            | BCE 0423-May-10 |   30
    BCE 424/423   | Skirophoriṓn          | BCE 0423-Jun-09 |   29
    
### Yearly

`-y` or `--year-summary` will give you a summary for the year. The "Y"
column indicates whether the year is ordinary (O) or intercalary (I):

    > heniautos 424 -y
         Year     | Y |      Start      | Days
    --------------|---|-----------------|-----
    BCE 424/423   | O | BCE 0424-Jul-19 |  354
    
### Span of Years

You can give two years. The output will be the calendars for the span from the first to the second. This is most useful with the year summary (`-y`) but works withe the monthly and daily calendars as well.

    > heniautos 424 420 -y
         Year     | Y |      Start      | Days
    --------------|---|-----------------|-----
    BCE 424/423   | O | BCE 0424-Jul-19 |  354
    BCE 423/422   | I | BCE 0423-Jul-08 |  384
    BCE 422/421   | O | BCE 0422-Jul-27 |  354
    BCE 421/420   | O | BCE 0421-Jul-15 |  354
    BCE 420/419   | I | BCE 0420-Jul-04 |  384
    
### Years CE

To treat the years as CE rather than BCE, use `--as-ce`:

    > heniautos 2021 -m --as-ce
         Year     |         Month         |      Start      | Days
    --------------|-----------------------|-----------------|-----
     CE 2021/2022 | Hekatombaiṓn          |  CE 2021-Jul-12 |   29
     CE 2021/2022 | Metageitniṓn          |  CE 2021-Aug-10 |   30
     CE 2021/2022 | Boēdromiṓn            |  CE 2021-Sep-09 |   29
     CE 2021/2022 | Puanopsiṓn            |  CE 2021-Oct-08 |   29
     CE 2021/2022 | Maimaktēriṓn          |  CE 2021-Nov-06 |   30
     CE 2021/2022 | Posideiṓn             |  CE 2021-Dec-06 |   29
     CE 2021/2022 | Gamēliṓn              |  CE 2022-Jan-04 |   30
     CE 2021/2022 | Anthestēriṓn          |  CE 2022-Feb-03 |   29
     CE 2021/2022 | Elaphēboliṓn          |  CE 2022-Mar-04 |   30
     CE 2021/2022 | Mounuchiṓn            |  CE 2022-Apr-03 |   29
     CE 2021/2022 | Thargēliṓn            |  CE 2022-May-02 |   30
     CE 2021/2022 | Skirophoriṓn          |  CE 2022-Jun-01 |   30
     
### Conciliar years

The `-c` or `--conciliar` options will output the conciliar year. 

    > heniautos 396 -c
         Year     |        Prytany        | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 396/395   | I                     |   1 | BCE 0396-Jul-10 |   1
    BCE 396/395   | I                     |   2 | BCE 0396-Jul-11 |   2
    BCE 396/395   | I                     |   3 | BCE 0396-Jul-12 |   3
    BCE 396/395   | I                     |   4 | BCE 0396-Jul-13 |   4
    ...
    BCE 396/395   | X                     |  32 | BCE 0395-Jun-25 | 351
    BCE 396/395   | X                     |  33 | BCE 0395-Jun-26 | 352 
    BCE 396/395   | X                     |  34 | BCE 0395-Jun-27 | 353
    BCE 396/395   | X                     |  35 | BCE 0395-Jun-28 | 354

All options such as `-m`, `-y`, and `--as-ce` work with `-c` as expected.

### Intercalations

When intercalations are necessary,`heniautos` intercalates Posideiṓn by default: 

    > heniautos 395 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 395/394   | Hekatombaiṓn          | BCE 0395-Jun-29 |   29
    BCE 395/394   | Metageitniṓn          | BCE 0395-Jul-28 |   30
    BCE 395/394   | Boēdromiṓn            | BCE 0395-Aug-27 |   29
    BCE 395/394   | Puanopsiṓn            | BCE 0395-Sep-25 |   30
    BCE 395/394   | Maimaktēriṓn          | BCE 0395-Oct-25 |   29
    BCE 395/394   | Posideiṓn             | BCE 0395-Nov-23 |   30
    BCE 395/394   | Posideiṓn hústeros    | BCE 0395-Dec-23 |   29
    BCE 395/394   | Gamēliṓn              | BCE 0394-Jan-21 |   30
    BCE 395/394   | Anthestēriṓn          | BCE 0394-Feb-20 |   29
    BCE 395/394   | Elaphēboliṓn          | BCE 0394-Mar-21 |   30
    BCE 395/394   | Mounuchiṓn            | BCE 0394-Apr-20 |   29
    BCE 395/394   | Thargēliṓn            | BCE 0394-May-19 |   30
    BCE 395/394   | Skirophoriṓn          | BCE 0394-Jun-18 |   29
    
You can change this with `--intercalate` which takes one of these abbreviations: Hek, Met, Boe, Pua, Mai, Pos, Gam, Ant, Ela, Mou, Tha, Ski. For instance, to intercalate Maimaktēriṓn:

    > heniautos 395 -m --intercalate Mai
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 395/394   | Hekatombaiṓn          | BCE 0395-Jun-29 |   29
    BCE 395/394   | Metageitniṓn          | BCE 0395-Jul-28 |   30
    BCE 395/394   | Boēdromiṓn            | BCE 0395-Aug-27 |   29
    BCE 395/394   | Puanopsiṓn            | BCE 0395-Sep-25 |   30
    BCE 395/394   | Maimaktēriṓn          | BCE 0395-Oct-25 |   29
    BCE 395/394   | Maimaktēriṓn hústeros | BCE 0395-Nov-23 |   30
    BCE 395/394   | Posideiṓn             | BCE 0395-Dec-23 |   29
    BCE 395/394   | Gamēliṓn              | BCE 0394-Jan-21 |   30
    BCE 395/394   | Anthestēriṓn          | BCE 0394-Feb-20 |   29
    BCE 395/394   | Elaphēboliṓn          | BCE 0394-Mar-21 |   30
    BCE 395/394   | Mounuchiṓn            | BCE 0394-Apr-20 |   29
    BCE 395/394   | Thargēliṓn            | BCE 0394-May-19 |   30
    BCE 395/394   | Skirophoriṓn          | BCE 0394-Jun-18 |   29
    
## Limiting

### By Month

To only see a single month of the output, use `--month` with the same abbreviations as `--intercalate`:

    > heniautos 395 -m --month Ela
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 395/394   | Elaphēboliṓn          | BCE 0394-Mar-21 |   30 
    
This works, of course, with the daily calendar as well. With a span of years the month for each year will be shown

### By Day

The `--day` option will limit output to the chosen day. This is most useful with the `--month` option:

    > heniautos 395 --month Ela --day 8
         Year     |        Month          | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 395/394   | Elaphēboliṓn          |   8 | BCE 0394-Mar-28 | 273
    
With no `--month` the specified day of each month would be output.

### By Prytany

With `-c` you can use `--prytany` to limit output to a single prytany:

    > heniautos 395 -c -m --prytany VIII
         Year     |        Prytany        |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 395/394   | VIII                  | BCE 0394-Mar-26 |   38
    
This works with `--day` as well: 

    > heniautos 395 -c --prytany VIII --day 3
         Year     |        Prytany        | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 395/394   | VIII                  |   3 | BCE 0394-Mar-28 | 273
    
### By Day of the Year

Use `--doy` to limit output to a specific day of the festival or conciliar year:

    > heniautos 395 --doy 273
         Year     |        Month          | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 395/394   | Elaphēboliṓn          |   8 | BCE 0394-Mar-28 | 273

    > heniautos 395 --doy 273 -c
         Year     |        Prytany        | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 395/394   | VIII                  |   3 | BCE 0394-Mar-28 | 273 
    
## Astronomical Information

### Solstices

`--solstices` will output the dates and times of the summer solstice in the given year or span of years (BCE unless `--as-ce` is specified):

    > heniautos 395 390 --solstices
    BCE 0395-Jun-28 14:01:39 EET
    BCE 0394-Jun-28 19:51:26 EET
    BCE 0393-Jun-28 01:34:50 EET
    BCE 0392-Jun-28 07:19:13 EET
    BCE 0391-Jun-28 13:14:16 EET
    BCE 0390-Jun-28 19:01:14 EET
    
### New Moons    

`--new-moons` will output the dates and times of each new moon:

    > heniautos 395 --new-moons
    BCE 0395-Jan-30 08:00:45 EET
    BCE 0395-Feb-28 20:51:53 EET
    BCE 0395-Mar-30 10:44:33 EET
    BCE 0395-Apr-29 01:19:43 EET
    BCE 0395-May-28 16:13:21 EET
    BCE 0395-Jun-27 07:06:55 EET
    BCE 0395-Jul-26 21:45:58 EET
    BCE 0395-Aug-25 11:53:37 EET
    BCE 0395-Sep-24 01:10:40 EET
    BCE 0395-Oct-23 13:25:28 EET
    BCE 0395-Nov-22 00:43:18 EET
    BCE 0395-Dec-21 11:23:17 EET
    
### GMT

Use the `--gmt` option to output solstice and new moon times as Greenwich Mean Time (GMT) instead of Athens time (Eastern European Time, EET)

    > heniautos 395 --solstices --gmt
    BCE 0395-Jun-28 12:01:39 GMT
    
### Visible New Moon Rules

By default, `heniautos` approximates the first visibility of the crescent of the moon, and therefore the start of the month, as the second day after the conjunction or "astronomical new moon" (which is what `--new-moons` outputs). You can change this with `-r`. `-r 2` is the same as the default:

    > heniautos 394 -m --month Hek -r 2
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 394/393   | Hekatombaiṓn          | BCE 0394-Jul-17 |   30
    
The next day after the conjunction is an almost equally good approximation. You can see this with `-r 1` which mostly has the effect of moving the dates up one day:

    > heniautos 394 -m --month Hek -r 1
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 394/393   | Hekatombaiṓn          | BCE 0394-Jul-16 |   30
    
However, when a new moon is _very_ close to a solstice, this single day can mean the difference between an ordinary and an intercalary year:

    > heniautos 396 394 -y -r 2
         Year     | Y |      Start      | Days
    --------------|---|-----------------|-----
    BCE 396/395   | O | BCE 0396-Jul-10 |  354
    BCE 395/394   | I | BCE 0395-Jun-29 |  383
    BCE 394/393   | O | BCE 0394-Jul-17 |  354
    
    > heniautos 396 394 -y -r 1
         Year     | Y |      Start      | Days
    --------------|---|-----------------|-----
    BCE 396/395   | I | BCE 0396-Jul-09 |  383
    BCE 395/394   | O | BCE 0395-Jul-27 |  354
    BCE 394/393   | O | BCE 0394-Jul-16 |  354
    
`-r 0` will use the conjunction:

    > heniautos 394 -m --month Hek -r 0
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 394/393   | Hekatombaiṓn          | BCE 0394-Jul-15 |   30
    
### Dinsmoor Dates

There is one more, special option for `-r`. `-r d` will output the dates for months as calculated by William Dinsmoor and published in _The Archons of Athens in the Hellenistic Age_ (Cambridge: Harvard University Press, 1930). Though modern astronomical calculations are better, this may be useful or interesting because his tables were used as the starting point for much work on the Athenian calendar that followed.

    > heniautos 424 -m -r d
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 424/423   | Hekatombaiṓn          | BCE 0424-Jul-17 |   29
    BCE 424/423   | Metageitniṓn          | BCE 0424-Aug-15 |   30
    BCE 424/423   | Boēdromiṓn            | BCE 0424-Sep-14 |   29
    BCE 424/423   | Puanopsiṓn            | BCE 0424-Oct-13 |   30
    BCE 424/423   | Maimaktēriṓn          | BCE 0424-Nov-12 |   29
    BCE 424/423   | Posideiṓn             | BCE 0424-Dec-11 |   30
    BCE 424/423   | Gamēliṓn              | BCE 0423-Jan-10 |   30
    BCE 424/423   | Anthestēriṓn          | BCE 0423-Feb-09 |   29
    BCE 424/423   | Elaphēboliṓn          | BCE 0423-Mar-10 |   30
    BCE 424/423   | Mounuchiṓn            | BCE 0423-Apr-09 |   29
    BCE 424/423   | Thargēliṓn            | BCE 0423-May-08 |   30
    BCE 424/423   | Skirophoriṓn          | BCE 0423-Jun-07 |   29

## Other options

`--tab` will output data separated by tabs rather than the tabular format illustrated above. This tab-delimited format is suitable for importing into a spreadsheet. For instance, this command:

    > heniautos 424 --tab > year424.tsv
    
 Will save the tab-delimted data for the calendar of 424/3 BCE in the file `year424.tsv` which could by imported into any spreadsheet.

`--arabic` will output prytany numbers as Arabic rather than Roman numerals.

`-a` or `--abbreviations` will output month names as abbreviations.

`-g` or `--greek-names` will output month names in Greek.

If `heniautos` cannot find the ephemeris file `de422.bsp` it will download a copy. Use `-e` or `--ephemeris` with the full path and name of the file to specify an existing copy. programming-with-heniautos.md#initializing-data

`-h` will output help.

[Top: Intro](README.md) | [Previous: Conciliar Calendar](conciliar-calendar.md) | [Next: Calendar Equations](calendar-equations.md)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
