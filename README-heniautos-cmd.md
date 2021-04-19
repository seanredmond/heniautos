# Heniautos Command Line

`heniautos` provides a command-line script to provide convenient access to the most common features. You should be able to run this command in a terminal. To get the various options, just type `heniautos -h`:

	> heniautos -h
	usage: heniautos [-h]
	                 [--month {Hek,Met,Boe,Pua,Mai,Pos,Gam,Ant,Ela,Mou,Tha,Ski}]
	                 [--day DAY] [-m] [-y]
	                 [--intercalate {Hek,Met,Boe,Pua,Mai,Pos,Gam,Ant,Ela,Mou,Tha,Ski}]
	                 [-c] [--arabic]
	                 [--prytany {I,II,III,IV,V,VI,VII,VIII,IX,X,XI,XII,XIII}]
	                 [--as-ce] [-a] [-g] [--new-moons] [--solstices] [--gmt]
	                 [-r {0,1,2,d}]
	                 start_year [end_year]
	
	positional arguments:
	  start_year
	  end_year
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --month {Hek,Met,Boe,Pua,Mai,Pos,Gam,Ant,Ela,Mou,Tha,Ski}
	                        Only show selected month
	  --day DAY             Only show selected day
	  -m, --month-summary
	  -y, --year-summary
	  --intercalate {Hek,Met,Boe,Pua,Mai,Pos,Gam,Ant,Ela,Mou,Tha,Ski}
	                        Month after which to intercalate
	  -c, --conciliar       Output conciliar calendar (prytanies)
	  --arabic              Display prytany numbers as Arabic rather than Roman
	                        numerals
	  --prytany {I,II,III,IV,V,VI,VII,VIII,IX,X,XI,XII,XIII}
	                        Only show selected prytany
	  --as-ce               Treat dates as CE rather than BCE
	  -a, --abbreviations   Abbreviate month names
	  -g, --greek-names     Use Greek names for months
	  --new-moons           Only list times of astronomical new moons
	  --solstices           Only list dates of solstices
	  --gmt                 Format times as GMT (rather than EET)
	  -r {0,1,2,d}, --rule {0,1,2,d}
	                        Rule for determining date of new moon. 0, 1, 2 days
	                        after astronomical conjunction, or d for
	                        Dinsmoor(default: 2)
                        
                        	
## Days, Months, Years

`heniautos` needs at least one year. By default the year is treated as a year BCE and the command outputs the entire calendar for the year that _begins_ in that year. That is, since ancient Greek years span two Julian years, to see the calendar for 421/42`, use `heniautos 422` (output truncated):

    > heniautos 422
	"BCE 422/421"	"Hekatombaiṓn"	1	"BCE 0422-Jul-27"	1
	"BCE 422/421"	"Hekatombaiṓn"	2	"BCE 0422-Jul-28"	2
	"BCE 422/421"	"Hekatombaiṓn"	3	"BCE 0422-Jul-29"	3
	"BCE 422/421"	"Hekatombaiṓn"	4	"BCE 0422-Jul-30"	4
	"BCE 422/421"	"Hekatombaiṓn"	5	"BCE 0422-Jul-31"	5
	...
	"BCE 422/421"	"Skirophoriṓn"	26	"BCE 0421-Jul-10"	350
	"BCE 422/421"	"Skirophoriṓn"	27	"BCE 0421-Jul-11"	351
	"BCE 422/421"	"Skirophoriṓn"	28	"BCE 0421-Jul-12"	352
	"BCE 422/421"	"Skirophoriṓn"	29	"BCE 0421-Jul-13"	353
	"BCE 422/421"	"Skirophoriṓn"	30	"BCE 0421-Jul-14"	354

	
The fields are: Julian years, Greek month, day, Julian date, and day of the Greek year.

You can get a monthly summary with the `-m` option:

	> heniautos 422 -m
	"BCE 422/421"	"Hekatombaiṓn"	"BCE 0422-Jul-27"	30
	"BCE 422/421"	"Metageitniṓn"	"BCE 0422-Aug-26"	29
	"BCE 422/421"	"Boēdromiṓn"	"BCE 0422-Sep-24"	29
	"BCE 422/421"	"Puanepsiṓn"	"BCE 0422-Oct-23"	30
	"BCE 422/421"	"Maimaktēriṓn"	"BCE 0422-Nov-22"	29
	"BCE 422/421"	"Poseidēiṓn"	"BCE 0422-Dec-21"	30
	"BCE 422/421"	"Gamēliṓn"	"BCE 0421-Jan-20"	29
	"BCE 422/421"	"Anthestēriṓn"	"BCE 0421-Feb-18"	30
	"BCE 422/421"	"Elaphēboliṓn"	"BCE 0421-Mar-19"	29
	"BCE 422/421"	"Mounuchiṓn"	"BCE 0421-Apr-17"	30
	"BCE 422/421"	"Thargēliṓn"	"BCE 0421-May-17"	29
	"BCE 422/421"	"Skirophoriṓn"	"BCE 0421-Jun-15"	30

In the month summary the fields are: Julian years, Greek month, Julian date of the first day of the month, number of days in the month.

Enter two years to see the calendar spanning the range of those years. This is most useful with the year summary (`-y`):

	> heniautos 421 415 -y
	"BCE 422/421"	"O"	"BCE 0422-Jul-27"	354
	"BCE 421/420"	"O"	"BCE 0421-Jul-15"	354
	"BCE 420/419"	"I"	"BCE 0420-Jul-04"	384
	"BCE 419/418"	"O"	"BCE 0419-Jul-23"	354
	"BCE 418/417"	"O"	"BCE 0418-Jul-12"	355
	"BCE 417/416"	"I"	"BCE 0417-Jul-01"	384
	"BCE 416/415"	"O"	"BCE 0416-Jul-20"	355
	"BCE 415/414"	"O"	"BCE 0415-Jul-10"	354

Here the fields are: Julian years, whether the year is normal (O) or intercalary (I), number of days in the year.

### Limiting output

You can limit the view to a single month by using the `--month` parameter with one of the following abbreviations: `Hek`, `Met`, `Boe`, `Pua`, `Mai`, `Pos`, `Gam`, `Ant`, `Ela`, `Mou`, `Tha`, `Ski`. For instance, to get the calendar for just Elaphēboliṓn in 421:

	> heniautos 422 --month Ela
	"BCE 422/421"	"Elaphēboliṓn"	1	"BCE 0421-Mar-19"	237
	"BCE 422/421"	"Elaphēboliṓn"	2	"BCE 0421-Mar-20"	238
	"BCE 422/421"	"Elaphēboliṓn"	3	"BCE 0421-Mar-21"	239
	"BCE 422/421"	"Elaphēboliṓn"	4	"BCE 0421-Mar-22"	240
	"BCE 422/421"	"Elaphēboliṓn"	5	"BCE 0421-Mar-23"	241
	"BCE 422/421"	"Elaphēboliṓn"	6	"BCE 0421-Mar-24"	242
	"BCE 422/421"	"Elaphēboliṓn"	7	"BCE 0421-Mar-25"	243
	"BCE 422/421"	"Elaphēboliṓn"	8	"BCE 0421-Mar-26"	244
	"BCE 422/421"	"Elaphēboliṓn"	9	"BCE 0421-Mar-27"	245
	"BCE 422/421"	"Elaphēboliṓn"	10	"BCE 0421-Mar-28"	246
	"BCE 422/421"	"Elaphēboliṓn"	11	"BCE 0421-Mar-29"	247
	"BCE 422/421"	"Elaphēboliṓn"	12	"BCE 0421-Mar-30"	248
	"BCE 422/421"	"Elaphēboliṓn"	13	"BCE 0421-Mar-31"	249
	"BCE 422/421"	"Elaphēboliṓn"	14	"BCE 0421-Apr-01"	250
	"BCE 422/421"	"Elaphēboliṓn"	15	"BCE 0421-Apr-02"	251
	"BCE 422/421"	"Elaphēboliṓn"	16	"BCE 0421-Apr-03"	252
	"BCE 422/421"	"Elaphēboliṓn"	17	"BCE 0421-Apr-04"	253
	"BCE 422/421"	"Elaphēboliṓn"	18	"BCE 0421-Apr-05"	254
	"BCE 422/421"	"Elaphēboliṓn"	19	"BCE 0421-Apr-06"	255
	"BCE 422/421"	"Elaphēboliṓn"	20	"BCE 0421-Apr-07"	256
	"BCE 422/421"	"Elaphēboliṓn"	21	"BCE 0421-Apr-08"	257
	"BCE 422/421"	"Elaphēboliṓn"	22	"BCE 0421-Apr-09"	258
	"BCE 422/421"	"Elaphēboliṓn"	23	"BCE 0421-Apr-10"	259
	"BCE 422/421"	"Elaphēboliṓn"	24	"BCE 0421-Apr-11"	260
	"BCE 422/421"	"Elaphēboliṓn"	25	"BCE 0421-Apr-12"	261
	"BCE 422/421"	"Elaphēboliṓn"	26	"BCE 0421-Apr-13"	262
	"BCE 422/421"	"Elaphēboliṓn"	27	"BCE 0421-Apr-14"	263
	"BCE 422/421"	"Elaphēboliṓn"	28	"BCE 0421-Apr-15"	264
	"BCE 422/421"	"Elaphēboliṓn"	29	"BCE 0421-Apr-16"	265
	
You can combine this with `--day` to find a specific Athenian date:

	> heniautos 422 --month Ela --day 24
	"BCE 422/421"	"Elaphēboliṓn"	24	"BCE 0421-Apr-11"	260
	
### CE dates

Years are treated as BCE by default. Use `--as-ce` to change this (this is how you would get the notional calendar for a modern year):

    > heniautos 2020 --as-ce -m
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


## Abreviations, Greek Names

Use `-a` to get abbreviated month names:

    > heniautos 420 -m -a
    "BCE 420/419"	"Hek"	"BCE 0420-Jul-04"	30
	"BCE 420/419"	"Met"	"BCE 0420-Aug-03"	30
	"BCE 420/419"	"Boe"	"BCE 0420-Sep-02"	29
	"BCE 420/419"	"Pua"	"BCE 0420-Oct-01"	30
	"BCE 420/419"	"Mai"	"BCE 0420-Oct-31"	30
	"BCE 420/419"	"Pos"	"BCE 0420-Nov-30"	29
	"BCE 420/419"	"Pos₂"	"BCE 0420-Dec-29"	30
	"BCE 420/419"	"Gam"	"BCE 0419-Jan-28"	29
	"BCE 420/419"	"Ant"	"BCE 0419-Feb-26"	29
	"BCE 420/419"	"Ela"	"BCE 0419-Mar-27"	30
	"BCE 420/419"	"Mou"	"BCE 0419-Apr-26"	29
	"BCE 420/419"	"Tha"	"BCE 0419-May-25"	29
	"BCE 420/419"	"Ski"	"BCE 0419-Jun-23"	30

Note that with abbreviations an intercalated month is indicated with a subscript "2".

Use `-g` to get the names in Greek

    >heniautos 420 -m -a
	"BCE 420/419"	"Ἑκατομβαιών"	"BCE 0420-Jul-04"	30
	"BCE 420/419"	"Μεταγειτνιών"	"BCE 0420-Aug-03"	30
	"BCE 420/419"	"Βοηδρομιών"	"BCE 0420-Sep-02"	29
	"BCE 420/419"	"Πυανεψιών"	"BCE 0420-Oct-01"	30
	"BCE 420/419"	"Μαιμακτηριών"	"BCE 0420-Oct-31"	30
	"BCE 420/419"	"Ποσιδηϊών"	"BCE 0420-Nov-30"	29
	"BCE 420/419"	"Ποσιδηϊών ὕστερος"	"BCE 0420-Dec-29"	30
	"BCE 420/419"	"Γαμηλιών"	"BCE 0419-Jan-28"	29
	"BCE 420/419"	"Ἀνθεστηριών"	"BCE 0419-Feb-26"	29
	"BCE 420/419"	"Ἑλαφηβολιών"	"BCE 0419-Mar-27"	30
	"BCE 420/419"	"Μουνυχιών"	"BCE 0419-Apr-26"	29
	"BCE 420/419"	"Θαργηλιών"	"BCE 0419-May-25"	29
	"BCE 420/419"	"Σκιροφοριών"	"BCE 0419-Jun-23"	30
	
## Conciliar Years

To see the conciliar rather than festival calendar, use `-c` or `--conciliar` (output truncated):

	>heniautos 399 -c 
	"BCE 399/398"	"I"	1	"BCE 0399-Jul-12"	1
	"BCE 399/398"	"I"	2	"BCE 0399-Jul-13"	2
	"BCE 399/398"	"I"	3	"BCE 0399-Jul-14"	3
	"BCE 399/398"	"I"	4	"BCE 0399-Jul-15"	4
	"BCE 399/398"	"I"	5	"BCE 0399-Jul-16"	5
	...
	"BCE 399/398"	"X"	32	"BCE 0398-Jun-27"	351
	"BCE 399/398"	"X"	33	"BCE 0398-Jun-28"	352
	"BCE 399/398"	"X"	34	"BCE 0398-Jun-29"	353
	"BCE 399/398"	"X"	35	"BCE 0398-Jun-30"	354
	"BCE 399/398"	"X"	36	"BCE 0398-Jul-01"	355
	
You can use `-y` and `-m` options as with the festival calendar:

	> heniautos 397 -c -m
	"BCE 397/396"	"I"	"BCE 0397-Jul-20"	36
	"BCE 397/396"	"II"	"BCE 0397-Aug-25"	36
	"BCE 397/396"	"III"	"BCE 0397-Sep-30"	36
	"BCE 397/396"	"IV"	"BCE 0397-Nov-05"	36
	"BCE 397/396"	"V"	"BCE 0397-Dec-11"	35
	"BCE 397/396"	"VI"	"BCE 0396-Jan-15"	35
	"BCE 397/396"	"VII"	"BCE 0396-Feb-19"	35
	"BCE 397/396"	"VIII"	"BCE 0396-Mar-26"	35
	"BCE 397/396"	"IX"	"BCE 0396-Apr-30"	35
	"BCE 397/396"	"X"	"BCE 0396-Jun-04"	35
	
And limit output with `	--prytany` (which takes a roman numeral) and `--day`:

	> heniautos 397 -c --prytany VII --day 10
	"BCE 397/396"	"VII"	10	"BCE 0396-Feb-28"	224

Use `--arabic` to have the prytany numbers output as Arabic rather than Roman numerals:

	>heniautos 397 -c -m --arabic
	"BCE 397/396"	1	"BCE 0397-Jul-20"	36
	"BCE 397/396"	2	"BCE 0397-Aug-25"	36
	"BCE 397/396"	3	"BCE 0397-Sep-30"	36
	"BCE 397/396"	4	"BCE 0397-Nov-05"	36
	"BCE 397/396"	5	"BCE 0397-Dec-11"	35
	"BCE 397/396"	6	"BCE 0396-Jan-15"	35
	"BCE 397/396"	7	"BCE 0396-Feb-19"	35
	"BCE 397/396"	8	"BCE 0396-Mar-26"	35
	"BCE 397/396"	9	"BCE 0396-Apr-30"	35
	"BCE 397/396"	10	"BCE 0396-Jun-04"	35

Since the number, length, and starting dates of prytanies varied over time, `heniautos` determines the correct values from the year. While we are not sure when prytanies began they certainly did not exist before Kleisthenes' reforms in 508 BCE, so `heniautos` will print an error and exit if you ask for the conciliar calendar before then.

For years after the 1st century BCE--by which time the Julian calendar had replaced the traditional Athenian one--`heniautos` whill output ten prytanies beginning and ending with the festival year (the system used in the 5th and 4th centuries BCE).

## Intercalations

When an intercalation is required, `heniautos` intercalates a second Poseidēiṓn by default. This seemed to be the ancient "default" as well. However, any month _could_ be intercalated and select a different one use `--intercalated` with the same abbreviations as the `--month` parameter, above. For instance, to force an intercalated Metageitniṓn:

    heniautos 420 -m --intercalate Met
	"BCE 420/419"	"Hekatombaiṓn"	"BCE 0420-Jul-04"	30
	"BCE 420/419"	"Metageitniṓn"	"BCE 0420-Aug-03"	30
	"BCE 420/419"	"Metageitniṓn hústeros"	"BCE 0420-Sep-02"	29
	"BCE 420/419"	"Boēdromiṓn"	"BCE 0420-Oct-01"	30
	"BCE 420/419"	"Puanepsiṓn"	"BCE 0420-Oct-31"	30
	"BCE 420/419"	"Maimaktēriṓn"	"BCE 0420-Nov-30"	29
	"BCE 420/419"	"Poseidēiṓn"	"BCE 0420-Dec-29"	30
	"BCE 420/419"	"Gamēliṓn"	"BCE 0419-Jan-28"	29
	"BCE 420/419"	"Anthestēriṓn"	"BCE 0419-Feb-26"	29
	"BCE 420/419"	"Elaphēboliṓn"	"BCE 0419-Mar-27"	30
	"BCE 420/419"	"Mounuchiṓn"	"BCE 0419-Apr-26"	29
	"BCE 420/419"	"Thargēliṓn"	"BCE 0419-May-25"	29
	"BCE 420/419"	"Skirophoriṓn"	"BCE 0419-Jun-23"	30

## Date of Observed New Moon

One the questions about the Athenian calendar still unresolved after more than a century of research is the extent to which it was based on theory, practice, and/or observation. The ancient astronomers understood the geometry of the full and new moons to calculate conjunctions (that they could not see) with some precision (Dinsmoor, 1931, 314) so they had the _ability_ to define the beginning of their months astronomically, as Dinmoor believes Meton had done. 

`heniautos` creates calendars as if they were based on observation (because this is where a computer is most helpful) but observation is not precise. The crescent of the new moon is first visible is visible about 1-3 days after the conjunction (Dunn, 1998, 214-217). By default, `heniautos` splits this difference and defines the first day of the month as falling two days after the conjunction. You can change this with `-r` or `--rule`. The acceptable values are 0, 1, or 2 (the default) for the number of days after the conjunction to start the new month. `-r 0` essentially uses the astronomical conjunction as the start of the month:

    > heniautos 400 -y
	"BCE 400/399"	"O"	"BCE 0400-Jul-23"	354
	> heniautos 400 -y -r 1
	"BCE 400/399"	"O"	"BCE 0400-Jul-22"	354
	> heniautos 400 -y -r 0
	"BCE 400/399"	"O"	"BCE 0400-Jul-21"	354

This has the effect of advancing all the Julian dates by 1 or 2 days relative to the default. However, the effect can be large when the first new moon falls very close to the solstice, as it did in 414 BCE:

    heniautos 415 413 -y
	"BCE 415/414"	"O"	"BCE 0415-Jul-10"	354
	"BCE 414/413"	"I"	"BCE 0414-Jun-29"	384
	"BCE 413/412"	"O"	"BCE 0413-Jul-17"	354
	> heniautos 415 413 -y -r 1
	"BCE 415/414"	"I"	"BCE 0415-Jul-09"	384
	"BCE 414/413"	"O"	"BCE 0414-Jul-28"	354
	"BCE 413/412"	"O"	"BCE 0413-Jul-16"	354
	> heniautos 415 413 -y -r 0
	"BCE 415/414"	"I"	"BCE 0415-Jul-08"	384
	"BCE 414/413"	"O"	"BCE 0414-Jul-27"	354
	"BCE 413/412"	"O"	"BCE 0413-Jul-15"	354

As you can see, the two-day default has the effect of making 414/13 intercalary, while one- or zero- day rule make 415/14 the intercalary year.

There is one more, special value for the `-r` parameter. Using `-r d` will use months as calculated by Dinsmoor (1931). Since his tables for the years 432-109 BCE (1931, 424-440) are used as a reference and point of departure for much of the debate that followed him, they are included as a useful option in `heniautos`. They are also as different as you can get from `heniautos`s versions, since Dinsmoor uses the conjunction (`-r 0`) and tries to keep as near a perfect alternation of full as hollow months as possible:

    > heniautos 415 -m -r d
	"BCE 415/414"	"Hekatombaiṓn"	"BCE 0415-Jul-08"	29
	"BCE 415/414"	"Hekatombaiṓn hústeros"	"BCE 0415-Aug-06"	30
	"BCE 415/414"	"Metageitniṓn"	"BCE 0415-Sep-05"	29
	"BCE 415/414"	"Boēdromiṓn"	"BCE 0415-Oct-04"	30
	"BCE 415/414"	"Puanepsiṓn"	"BCE 0415-Nov-03"	29
	"BCE 415/414"	"Maimaktēriṓn"	"BCE 0415-Dec-02"	30
	"BCE 415/414"	"Poseidēiṓn"	"BCE 0414-Jan-01"	29
	"BCE 415/414"	"Gamēliṓn"	"BCE 0414-Jan-30"	30
	"BCE 415/414"	"Anthestēriṓn"	"BCE 0414-Mar-01"	30
	"BCE 415/414"	"Elaphēboliṓn"	"BCE 0414-Mar-31"	29
	"BCE 415/414"	"Mounuchiṓn"	"BCE 0414-Apr-29"	30
	"BCE 415/414"	"Thargēliṓn"	"BCE 0414-May-29"	29
	"BCE 415/414"	"Skirophoriṓn"	"BCE 0414-Jun-27"	30 

## Solstices and New Moons

If you want to see the underlying data by which `heniautos` makes its calculations, you can get the dates and times of the solstices:

    > heniautos 415 413 --solstices
	BCE 0415-Jun-28 18:09:34 EET
	BCE 0414-Jun-28 23:48:17 EET
	BCE 0413-Jun-28 05:31:29 EET

and of the the new moons:

	> heniautos 414 --new-moons
	BCE 0414-Jan-30 16:48:28 EET
	BCE 0414-Mar-01 09:34:31 EET
	BCE 0414-Mar-31 02:26:32 EET
	BCE 0414-Apr-29 18:13:57 EET
	BCE 0414-May-29 08:12:12 EET
	BCE 0414-Jun-27 20:20:07 EET
	BCE 0414-Jul-27 07:09:08 EET
	BCE 0414-Aug-25 17:20:02 EET
	BCE 0414-Sep-24 03:24:20 EET
	BCE 0414-Oct-23 13:39:17 EET
	BCE 0414-Nov-22 00:16:18 EET
	BCE 0414-Dec-21 11:31:46 EET

Here we can see the new moon of June 27, 414 BCE that is very close to the solstice on June 28.

Note that these options treat years as Julian years and not Greek equivalents. So `414` will generate a calendar the begins in the summer 414 and ends in the summer 413, with `--new-moons` it shows the new moons in the Julian year.

Times are, by default, in Eastern European Time (EET, the time zone of Athens) _without_ any adjustments for Daylight Savings Time. If you like, you can ask for times in Greenwich Mean Time:

   	> heniautos 415 413 --solstices --gmt
	BCE 0415-Jun-28 16:09:34 GMT
	BCE 0414-Jun-28 21:48:17 GMT
	BCE 0413-Jun-28 03:31:29 GMT
	
## Ephemeris File

The first time (or any time) you run `heniautos` it may download a large file named `de422.bsp`. This file is an "ephemeris"--data about astronomical objects--that `heniautos` needs for its calculations. `heniautos` will use an existing copy if it can find one instead of downloading another. You can explicitly provide the path to an existing copy using the `-e` or `--ephemeris` option:

    > heniautos 415 -e /full/path/to/your/copy/of/de422.bsp
	
## Works Cited
* Dinsmoor, William Bell. 1931. _The Archons of Athens in the Hellenistic Age_. Cambridge: Harvard University Press.
* Dunn, Francis M. 1998. “Tampering with the Calendar.” _Zeitschrift Für Papyrologie Und Epigraphik_ 123: 213–31.


