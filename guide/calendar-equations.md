# Calendar Equations

This guide has included many caveats about the accuracy of `heniautos` and noted two documented intercalary years that `heniautos` gets wrong. On the other hand, what might `heniautos` get right, and how could we know? Welcome to the fascinating world of "calendar equations." These bits of evidence from the historical record allow us to test different theories of how the Athenians really used their calendar, and some cases, give confidence to reconstructions.


## What are Calendar Equations?

A "calendar equation" is any piece of evidence that relates one calendar to another. In Greek epigraphy it commonly refers to an inscription that records a date on both the Athenian festival calendar and conciliar calendar. 

[A previous section](conciliar-calendar.md#the-start-of-4332) looked at an inscription that implied the calendar equations **Hek 18 = I 13** and **Met 12 = I 37**, but there are many inscriptions with _explicit_ calendar equations. In the latter part of the fourth century BCE, Athenians started "double dating" their decrees with a prytany date and a festival date. The first surviving instance is from 346/5, [IG XII,6 1,261](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20XII%206,%201,%20261) from the Athenian colony on Samos. Often these inscriptions are fragmentary and require knowledge of the calendar to restore, which is why so much of the initial investigations of the Athenian calendar in the 20th century were done by epigraphers, Like Benjamin D. Meritt and W. Kendrick Pritchett. There is also the risk of circular reasoning since assumptions about the calendar go into the restoration of the inscriptions which then, if you are not careful, might be used to "prove" what they assume (see Pritchett [1970] for Pritchett's criticisms of Meritt on this point)

### IG II³ 1,338

There are, however, perfectly preserved examples, that we can begin with, such as  [IG II³ 1,338](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20II_III%C2%B3%201,%20338) (=IG II² 338). This has a completely standard prescript with no restorations needed:

    ἐπὶ Νικοκράτους ἄρχοντος, ἐπὶ τῆς Αἰγηίδος
    πρώτης πρυτανείας, ἧι Ἀρχέλας Χαιρίου Παλ–
    ληνεὺς ἐγραμμάτευεν· Μεταγειτνιῶνος ἐνά–
    τηι ἱσταμένου· ἐνάτηι καὶ τριακοστῆι τῆς
    πρυτανείας

The parts of this prescript are:

1. The árkhōn: ἐπὶ Νικοκράτους ἄρχοντος, "in the árkhōnship of Nikokrátēs..." 333/2 BCE.
1. The prytany and tribe that held it: ἐπὶ τῆς Αἰγηίδος πρώτης πρυτανείας, "...in the first prytany, of Aigēis..."
1. The secretary: ἧι Ἀρχέλας Χαιρίου Παλληνεὺς ἐγραμμάτευεν, "...for which Arkhélas son of Khairías from Pallēnē was secretary..."
1. The festival date: Μεταγειτνιῶνος ἐνάτηι ἱσταμένου, "...9th of Metageitniṓn..."
1. The prytany day: ἐνάτηι καὶ τριακοστῆι τῆς πρυτανείας, "...39th of the prytany"

For a good introduction to these types of inscriptions, see Rhodes and Osborne (2003) xiii-xxiii. The two dates in the inscription provide a calendar equation:

**Metageitniṓn 9 = Prytany I 39**

or, for short:

**Met 9 = I 39**

In some cases, the equation provides useful data about the calendar for the year, or the calendar in general. For instance, this inscription tells us three things:

1. The year (333/332 BCE, which we know from the árkhōn) was intercalary because this prytany (the first) has 39 days. In [this period](conciliar-calendar.md#409-308-bce) the longest prytanies in ordinary years were 36 days.
1. Hekatombaiṓn was full. If the 39th day of the prytany is Metageitniṓn 9, the 31st would be Metageitniṓn 1, and therefore the 30th has to be Hekatombaiṓn 30.
1. The intercalated month was not Hekatombaiṓn because having a second Hekatombaiṓn before Metageitniṓn would push Metageitniṓn into the second prytany. This is hardly surprising, but it is worth keeping in mind.

I 39 is the 39th day of the year, as is Metageitniṓn 9 if Hekatombaiṓn is full (30 + 9 = 39). The "solution" to this equation, then, is

**Met 9 = I 39 = DOY 39**

"Solving" the equation means being able to assign it, with some confidence, to a specific day of the year. Once we have a solution we are often able to limit the range of possibilities for other aspects of the calendar for the same year. For instance, we can say that 333/2 was intercalary, not ordinary, and that Hekatombaiṓn was full, not hollow.

What does `heniautos` calculate for this year?

    > heniautos -m 333
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 333/332   | Hekatombaiṓn          | BCE 0333-Jul-03 |   29
    BCE 333/332   | Metageitniṓn          | BCE 0333-Aug-01 |   30
    BCE 333/332   | Boēdromiṓn            | BCE 0333-Aug-31 |   29
    BCE 333/332   | Puanopsiṓn            | BCE 0333-Sep-29 |   30
    BCE 333/332   | Maimaktēriṓn          | BCE 0333-Oct-29 |   29
    BCE 333/332   | Posideiṓn             | BCE 0333-Nov-27 |   30
    BCE 333/332   | Posideiṓn hústeros    | BCE 0333-Dec-27 |   29
    BCE 333/332   | Gamēliṓn              | BCE 0332-Jan-25 |   30
    BCE 333/332   | Anthestēriṓn          | BCE 0332-Feb-24 |   29
    BCE 333/332   | Elaphēboliṓn          | BCE 0332-Mar-25 |   30
    BCE 333/332   | Mounuchiṓn            | BCE 0332-Apr-24 |   29
    BCE 333/332   | Thargēliṓn            | BCE 0332-May-23 |   30
    BCE 333/332   | Skirophoriṓn          | BCE 0332-Jun-22 |   29

It correctly calculates 333/2 as an intercalary year but, based on the astronomy, makes Hekatombaiṓn hollow. Since Metageitniṓn calculated as full we can "fix" this by simply moving the start date of Metageitniṓn so that Hekatombaiṓn is full instead. 

     Year     |        Month          |      Start       | Days
--------------|-----------------------|------------------|-----
BCE 333/332   | Hekatombaiṓn          | BCE 0333-Jul-03  |   30‡
BCE 333/332   | Metageitniṓn          | BCE 0333-Aug-02† |   29‡
BCE 333/332   | Boēdromiṓn            | BCE 0333-Aug-31  |   29
etc...|

Here the dagger (†) indicates what has been changed (the date of Met 1) and the double daggers (‡) what has been affected by this change (the length of Hek and Met). This does not disturb the rest of the calculated calendar and means we can be slightly more accurate about dates in Hekatombaiṓn and Metageitniṓn. For the rest of the year, we have no better evidence than astronomy. The important point, as before, is that if you need historical accuracy the calculations made by Heniautos are a framework for examining other evidence. If you need an approximate date Heniautos (and just about any other reconstruction) are close enough/

We can provisionally put a Julian date to our equation. Since we know the day of the year, we can look it up with the `--doy` option:

    heniautos 333 --doy 39
         Year     |        Month          | Day |      Start      | DOY
    --------------|-----------------------|-----|-----------------|----
    BCE 333/332   | Metageitniṓn          |  10 | BCE 0333-Aug-10 |  39
    
(Heniautos calculates the festival date as Metageitniṓn 10, remember, because it is still working with a hollow Hekatombaiṓn. We are only interested here in the Julian date of DOY 39)
    
**Met 9 = I 39 = DOY 39 = ✸Aug 10, 333 BCE**

We will use the star symbol ✸ to mark anything that comes from an astronomical calculation and therefore has a margin of error as long as we are not certain how the beginnings of months were observed or calculated. Using `-r 0` or `-r 1` as the "visibility rule" will shift the date to Aug 8 or 9 respectively.

## `calendar-equations`

### IG II³ 1,338 Again

Along with the `heniautos` command, Heniautos, installs a second command, `calendar-equation` for working with these equations.

    > calendar_equation.py -y 333 -e Met 9 I 39
    Met  9 ( 2-) =    I 39 =  DOY  39 (I) [F, ∅]
    
`calendar-equation` take a year (`-y`) and an equation (`-e`) in the format "month-abbreviation day prytany-number day." The prytany number needs to be a Roman numeral but it does not matter if it or the month abbreviation is capitalized.

The output is rather terse, but you can see that it contains the basic calendar equation. The `( 2-)` after `Met  9` means that Metageitniṓn is the second month (`2`) and is _not_ preceded by an intercalation (`-`). If it were preceded by an intercalation, this would be `( 3+)`. The `(I)` after `DOY  39` indicates that this solution requires an intercalary year; `(O)` would mean it was an ordinary year. `[F, ∅]` indicates the count of festival months and prytanies that must precede this solution--one full month `F`, and no prytanies, `∅` (that is, "null") since this is the first prytany. Hopefully this will become clear with more examples. This solution from `calendar-equation` contains all the facts that we worked out ourselves for this simple equation, and the fact that it only output a single solution indicates that it is the _only_ solution for this equation.

We will use `calendar-equation` for examples in the rest this guide.

### IG XII,6 1,261

We mentioned IG XII,6 1,261 above as the earliest recorded example of a double dated inscription. It comes from Samos, but it seems safe to assume that the Athenian colony there was using the same calendar as at Athens (Pritchett and Neugebauer 1947, 41-2; Meritt 1961, 72-3). The date is in ll. 56-7:

    ἐπὶ Πεισίλεω ἄρχοντος, μηνὸς Ποσιδειῶνος τετράδι φθίνοντος, ἐπὶ τῆς
    Πανδιονίδος πέμπτης πρυτανείας μιᾶι καὶ τριακοστεῖ
    

The prytany date is V 31. The festival date is in Posideiṓn, and τετράδι φθίνοντος is the earlier form of the backwards count of days at the end of the month (see ["Days of the Month"](reading-dated-inscriptions.md#days-of-the-month)). Essentially, it means "fourth from the last". Counting inclusively, that would be the 27th of a full month or the 26th of a hollow month. The first version of the equation, then, is:

**Pos 26/27 = V 31**

`calendar-equation` can accommodate the multiple options in the date with "/":

    > calendar_equation -e Pos 26/27 V 31
    Pos 26 ( 6-) =    V 31 =  DOY 171 (O) [HHHHH, SSSS]
    Pos 26 ( 6-) =    V 31 =  DOY 172 (O) [FHHHH, LSSS]
    Pos 27 ( 6-) =    V 31 =  DOY 172 (O) [HHHHH, LSSS]
    Pos 26 ( 6-) =    V 31 =  DOY 173 (O) [FFHHH, LLSS]
    Pos 27 ( 6-) =    V 31 =  DOY 173 (O) [FHHHH, LLSS]
    Pos 26 ( 6-) =    V 31 =  DOY 174 (O) [FFFHH, LLLS]
    Pos 27 ( 6-) =    V 31 =  DOY 174 (O) [FFHHH, LLLS]
    Pos 26 ( 6-) =    V 31 =  DOY 175 (O) [FFFFH, LLLL]
    Pos 27 ( 6-) =    V 31 =  DOY 175 (O) [FFFHH, LLLL]
    
Now we have more potential solutions than we did with the previous equations. They all require an ordinary year, and amount to this day falling somewhere in the range of DOY 171-175. We can dismiss the first and third solutions since they require five hollow months in a row (`calendar-equations` will output combinations that are simply mathematically possible).

Interpretations of this date have revolved around the [Rule of Aristotle](conciliar-calendar.md#the-rule-of-aristotle). Pritchett and Neugebaur (1947, 42) opted for **Pos 27 = V 31 = DOY 175** since "it appears that Prytanies I-IV contained 36 days each" (that is, the Rule). Meritt, who did not believe in the Rule, pointed out  (1961, 73) only that "it is equally legitimate to take Ποσιδειῶνος τετράδι φθίνοντος as the 26th day of a hollow month" and that **Pos 26 = V 31 = DOY 174** was valid and "would require that only three of the first four prytanies have 36 days each."

Both are correct. Both solutions require three full and two hollow months in the first five, which is what `heniautos` calculates for 346:

    > heniautos 346 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 346/345   | Hekatombaiṓn          | BCE 0346-Jul-26 |   30
    BCE 346/345   | Metageitniṓn          | BCE 0346-Aug-25 |   29
    BCE 346/345   | Boēdromiṓn            | BCE 0346-Sep-23 |   30
    BCE 346/345   | Puanopsiṓn            | BCE 0346-Oct-23 |   29
    BCE 346/345   | Maimaktēriṓn          | BCE 0346-Nov-21 |   30
    BCE 346/345   | Posideiṓn             | BCE 0346-Dec-21 |   30
    BCE 346/345   | Gamēliṓn              | BCE 0345-Jan-20 |   30
    BCE 346/345   | Anthestēriṓn          | BCE 0345-Feb-19 |   29
    BCE 346/345   | Elaphēboliṓn          | BCE 0345-Mar-19 |   30
    BCE 346/345   | Mounuchiṓn            | BCE 0345-Apr-18 |   29
    BCE 346/345   | Thargēliṓn            | BCE 0345-May-17 |   30
    BCE 346/345   | Skirophoriṓn          | BCE 0345-Jun-16 |   29

`heniautos` makes Posideiṓn full which we might see as giving support to Pritchett and Neugebaur, but that cannot stand for much on its own if we freely adjusted the lengths of Hekatombaiṓn and Metageitniṓn, above, to match the evidence of IG II³ 1,338. If we do accept the truth of the Rule, the full solution with Julian Date will be:

**Pos 27 = V 31 = DOY 175 = ✸Jan 16, 345 BCE**

## Multiple Equations

We are in a much better situation when we have multiple equations, since we can try to find solutions that fit together and support each other. There are two equations for the year 324/3 BCE, Agora XVI 91 and IG II³,1 372, that we can use as an example.

### Agora XVI 91 (=IG II³,1 374)

The restorations in [Agora XVI 91](https://epigraphy.packhum.org/text/232860) are Meritt's (Meritt 1961, 104-105). [IG II³,1 374](https://epigraphy.packhum.org/text/347231) is much more conservative. With the restorations this inscription is, like IG XII,6 1,261, dated on Prytany V 31, towards the end of Posideiṓn, but one day later in the month:

    [ἐπὶ Ἡγησίου ἄρχοντος, ἐπ]ὶ τῆς Α-
    [ἰαντίδος πέμπτης πρυτα]νείας
    [ἧι Εὐφάνης Φρύνωνος Ῥαμ]ν̣ούσι-
    [ος ἐγραμμάτευεν· Ποσιδε]ῶνος v
    [τρίτηι μετ’ εἰκάδας, μιᾶι κ]αὶ τρ-
    [ιακοστῆι τῆς πρυτανείας

τρίτηι μετ’ εἰκάδας is a later style of "backward count" (third from the end) like τετράδι φθίνοντος (fourth from the end). In full month, this will be the 28th, in a hollow the 27th, so the equation is: 

**Pos 27/28 = V 31**


We can again give the date to `calendar-equation` in the format `Pos 27/28` to test both.

    > calendar_equation.py -p 10    -e Pos 27/28 V 31
    Pos 27 ( 6-) =    V 31 =  DOY 172 (O) [HHHHH, LSSS]
    Pos 27 ( 6-) =    V 31 =  DOY 173 (O) [FHHHH, LLSS]
    Pos 28 ( 6-) =    V 31 =  DOY 173 (O) [HHHHH, LLSS]
    Pos 27 ( 6-) =    V 31 =  DOY 174 (O) [FFHHH, LLLS]
    Pos 28 ( 6-) =    V 31 =  DOY 174 (O) [FHHHH, LLLS]
    Pos 27 ( 6-) =    V 31 =  DOY 175 (O) [FFFHH, LLLL]
    Pos 28 ( 6-) =    V 31 =  DOY 175 (O) [FFHHH, LLLL]
    
These solutions all require an ordinary year, which is what `heniautos` calculates for this year (324/3 BCE):
 
    > heniautos 324 -y
         Year     | Y |      Start      | Days
    --------------|---|-----------------|-----
    BCE 324/323   | O | BCE 0324-Jul-23 |  354
    
As we saw above, `calendar-equations` will output solutions that are mathematically possible but astronomically unlikely or impossible. We can exclude the first and third solutions simply on the grounds that they require all five months before Posideiṓn to be hollow which would never happen (we saw a similar combination for Pos 26/27 = V 31).  The second solution requires four hollow months (FHHHH) but _not_ in a row. It is important to remember that this represents a _count_ of four hollow months. The actual _order_ could be two hollow, full, two hollow (that is `HHFHH`) with the same count.

For the prytany counts the order may be important. If we want to observe the Rule of Aristotle, we need the conciliar year to begin with four "long" prytanies. Since there are only four prytanies preceding this equation they must _all_ be long (or the Rule of Aristotle must not be a rule). Two of the solutions satisfy the rule one implying a hollow Posideiṓn (Pos 27 = V 31 = DOY 175) one a full Posideiṓn (Pos 28 = V 31 = DOY 175). We can show the count requirements graphically

![324/3 BCE](img/324-1.png)

The dotted lines represent the "horizon" of the equation--the solutions give us a count of full and hollow months for the first five months, to the left of the line. Since first solution requires a hollow month and second a full we can fill in this month to the right of the line. We cannot say anything yet about the rest of the festival months so they are empty.  Since the first four prytanies are long, we know the remaining six _must_ be short. We can color them accordingly but leave them with the diagonal hash marks to indicate that they are still hypothetical.

### IG II³,1 372

[IG II³,1 372](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20II_III%C2%B3%201,%20372) (Meritt 1961, 105)
	
    [ἐ]φ’ Ἡγησίου ἄρχ[οντος, ἐπὶ τῆς Ἀκαμα]-
    [ν]τ̣ίδος ἐνάτης [πρυτανείας, ἧι Εὐφά]-
    [νη]ς Φρύνωνος Ῥ[αμνούσιος ἐγραμμά]-
    [τ]ευε· Θαργηλι̣[ῶνος ὀγδόηι ἐπὶ δέκα]·
    [ἐ]νάτει καὶ ε[ἰκοστῆι τῆς πρυτανεία]-
    [ς] 
    
IG II³ leaves the festival date unrestored, but we will accept Meritt's ὀγδόηι ἐπὶ δέκα.

    > calendar_equation.py -p 10    -e Tha 18 IX 29
    Tha 18 (11-) =   IX 29 =  DOY 312 (O) [FFFFHHHHHH, LLLSSSSS]
    Tha 18 (11-) =   IX 29 =  DOY 313 (O) [FFFFFHHHHH, LLLLSSSS]

Both solutions require an ordinary year, so they are consistent with the Agora XVI 91 solutions. Only the second satisfies the Rule of Aristotle so lets focus on that one for simplicity. If we want to combine the solutions for the two equations we have to look for a way that combines them so that the second solution "contains" the first solution.

The two solutions for Agora XVI 91 that satisfied the Rule of Aristotle required the festival month counts `FFFHH` or `FFHHH`. We first "subtract" `FFFHH` from `FFFFFHHHHH` (the count required by IG II³,1 372)--that is, take three full and two hollow months out and see what the "remainder" is: `FFFFFHHHHH` - `FFFHH` = `FFHHH`. Put another way, `FFFHHFFFHH` is a rearrangement of the IG II³,1 372 solution that also satisfies the Agora XVI 91 solution.

`calendar-equation` can help with this. You can provide multiple equations with multiple `-e` options.

    > calendar_equation.py -p 10 -e Pos 27/28 V 31 -e Tha 18 IX 29
    Pos 27 ( 6-) =    V 31 =  DOY 172 (O) [HHHHH, LSSS]
    Pos 27 ( 6-) =    V 31 =  DOY 173 (O) [FHHHH, LLSS]
    Pos 28 ( 6-) =    V 31 =  DOY 173 (O) [HHHHH, LLSS]
    Pos 27 ( 6-) =    V 31 =  DOY 174 (O) [FFHHH, LLLS]
    Pos 28 ( 6-) =    V 31 =  DOY 174 (O) [FHHHH, LLLS]
    Pos 27 ( 6-) =    V 31 =  DOY 175 (O) [FFFHH, LLLL]
    Pos 28 ( 6-) =    V 31 =  DOY 175 (O) [FFHHH, LLLL]
    Tha 18 (11-) =   IX 29 =  DOY 312 (O) [FFFFHHHHHH, LLLSSSSS]
    Tha 18 (11-) =   IX 29 =  DOY 313 (O) [FFFFFHHHHH, LLLLSSSS]

This will simply output solutions for each equation in turn. If you add `-c` or `--collate` to command though, it will generate all the possible "collations" of the two equations together:

    > calendar_equation -p 10 -e Pos 27/28 V 31 -e Tha 18 IX 29 -c
    Pos 27 ( 6-) =    V 31 =  DOY 172 (O) [HHHHH, LSSS]
    Pos 27 ( 6-) =    V 31 =  DOY 173 (O) [FHHHH, LLSS]
    Pos 28 ( 6-) =    V 31 =  DOY 173 (O) [HHHHH, LLSS]
    Pos 27 ( 6-) =    V 31 =  DOY 174 (O) [FFHHH, LLLS]
    Pos 28 ( 6-) =    V 31 =  DOY 174 (O) [FHHHH, LLLS]
    Pos 27 ( 6-) =    V 31 =  DOY 175 (O) [FFFHH, LLLL]
    Pos 28 ( 6-) =    V 31 =  DOY 175 (O) [FFHHH, LLLL]
    Tha 18 (11-) =   IX 29 =  DOY 312 (O) [FFFFHHHHHH, LLLSSSSS]
    Tha 18 (11-) =   IX 29 =  DOY 313 (O) [FFFFFHHHHH, LLLLSSSS]
      1: HHHHH FFFFH   LSSS LLSS
      2: HHHHH FFFFF   LSSS LLLS
      3: FHHHH FFFHH   LLSS LSSS
      4: FHHHH FFFFH   LLSS LLSS
      5: HHHHH FFFFH   LLSS LSSS
      6: HHHHH FFFFF   LLSS LLSS
      7: FFHHH FFHHH   LLLS SSSS
      8: FFHHH FFFHH   LLLS LSSS
      9: FHHHH FFFHH   LLLS SSSS
     10: FHHHH FFFFH   LLLS LSSS
     11: FFFHH FFHHH   LLLL SSSS
     12: FFHHH FFFHH   LLLL SSSS
      1: Pos 27 = V 31 = 172 + Tha 18 = IX 29 = 312
      2: Pos 27 = V 31 = 172 + Tha 18 = IX 29 = 313
      3: Pos 27 = V 31 = 173 + Tha 18 = IX 29 = 312
      4: Pos 27 = V 31 = 173 + Tha 18 = IX 29 = 313
      5: Pos 28 = V 31 = 173 + Tha 18 = IX 29 = 312
      6: Pos 28 = V 31 = 173 + Tha 18 = IX 29 = 313
      7: Pos 27 = V 31 = 174 + Tha 18 = IX 29 = 312
      8: Pos 27 = V 31 = 174 + Tha 18 = IX 29 = 313
      9: Pos 28 = V 31 = 174 + Tha 18 = IX 29 = 312
     10: Pos 28 = V 31 = 174 + Tha 18 = IX 29 = 313
     11: Pos 27 = V 31 = 175 + Tha 18 = IX 29 = 313
     12: Pos 28 = V 31 = 175 + Tha 18 = IX 29 = 313
     
This output could surely be improved, but the first part gives the individual solution (as without the `-c` switch). Next, we have the required counts numbered to corresponding with the combined solutions that follow. The eleventh is the pattern we calculated above and the spacing `FFFHH FFHHH` is to make it easier to distinguish the two "partitions": the five months required by Agora XVI 91 from the five further required by IG II³,1 372 (the "remainder" of "subtracting" the first from the second). Only two collated solutions satisfy the Rule of Aristotle. The first solution only requires two full and three hollow in the second "partition", but since we also know that the interpretation of τρίτηι μετ’ εἰκάδας as Pos 27 requires a hollow Posideiṓn, these months are arranged to show this:

![324/3 BCE](img/324-2.png)

Both solutions require that prytany V 31 is DOY 175 and IX 29 DOY 313. The difference is only whether there are three full months in the first five or two, and two in the next five or three. What is the astronomical prediction? 324/3 turns out to have perfectly alternating full and hollow months:

    > heniautos 324 -m
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 324/323   | Hekatombaiṓn          | BCE 0324-Jul-23 |   30
    BCE 324/323   | Metageitniṓn          | BCE 0324-Aug-22 |   29
    BCE 324/323   | Boēdromiṓn            | BCE 0324-Sep-20 |   30
    BCE 324/323   | Puanopsiṓn            | BCE 0324-Oct-20 |   29
    BCE 324/323   | Maimaktēriṓn          | BCE 0324-Nov-18 |   30
    BCE 324/323   | Posideiṓn             | BCE 0324-Dec-18 |   29
    BCE 324/323   | Gamēliṓn              | BCE 0323-Jan-16 |   30
    BCE 324/323   | Anthestēriṓn          | BCE 0323-Feb-15 |   29
    BCE 324/323   | Elaphēboliṓn          | BCE 0323-Mar-16 |   30
    BCE 324/323   | Mounuchiṓn            | BCE 0323-Apr-15 |   29
    BCE 324/323   | Thargēliṓn            | BCE 0323-May-14 |   30
    BCE 324/323   | Skirophoriṓn          | BCE 0323-Jun-13 |   29
    
In order to fit with the astronomical data, a solution to these two equations must have three full and two hollow months before Posideiṓn, Posideiṓn must be hollow, and two more full and two more hollow months must precede Thargēliṓn. This is exactly the Pos 27 solution. The counts in the calendar equation solutions, independent of their order, match the counts derived from the order calculated astronomically:

![324/3 BCE](img/324-3.png)

Note that of the twelve "collated" solutions, this is the _only_ solution that fits the astronomical data. None of the others call for three full months in the first five. While we used the Rule of Aristotle simply to reduce the number of possibilities for the purposes of illustration, in the end we got it as the part of the unique solution. We can now state the complete solutions to the two calendar equations:

**Pos 27 = V 31 = DOY 175 = ✸Jan 13, 323 BCE**

**Tha 18 = IX 29 = DOY 313 = ✸May 31, 323 BCE**

## 336/5 BCE

Meritt's interpretation of the evidence for this year (Meritt 1961, 10-15) was briefly discussed under the Rule of Aristotle. We can now examine it in more detail and follow some of the process by which successive generations of scholars worked through the problems posed by these texts. There are two inscriptions recording dated decrees for 336/5 BCE: IG II² 328 (=IG II² 328) and IG II³,1 327 (=IG II² 330) with two decrees on separate dates.

IG II³,1 329 (Meritt's IG II² 328) is very conservative:

    [․․․․․․․․․․20․․․․․․․․․․ ἐπ]ὶ τῆς Α[․]
    [․․․․․․․․17․․․․․․․․․ πρυτ]ανείας, ἧ-
    [ι ․․․․․․․․․19․․․․․․․․․․ ἐ]γραμμάτ-
    [ευεν· ․․․․․․․14․․․․․․․ τετ]ράδι φθί-
    [νοντος· ․․․․․․․15․․․․․․․․]ει τῆς πρ-
    [υτανείας]
    
This inscription has a "rich" history of restorations, but let us at least accept the restoration of Pythodelos as the archon (IG II² 328) in line one. 

    [ἐπὶ Πυθοδήλου ἄρχοντος ἐπ]ὶ τῆς Ἀ[.]-

Kirchner, in IG II², specified **Mai 27 = IV 31**, restoring the following for lines 2-6.  

    [......... τετάρτης πρυτ]ανείας ἧ-
    [ι ․․․․․․․․19․․․․․․․․․ ἐ]γραμμάτ-
    [ευεν· Μαιμακτηριῶνος τετ]ράδι φθί-
    [νοντος, μιᾶι καὶ τριακοστ]εῖ τῆς πρ-
    [υτανείας

The interpretion of τετράδι φθίνοντος as the 27th shows that Kirchner assumed Maimaktēriṓn was full (since it would be the 26th of a hollow month). The equation of Mai 27 with IV 31, and the restoration of μιᾶι καὶ τριακοστεῖ for the prytany day rest on the assumption of alternating full and hollow months and years that mostly begin with a full Hekatombaiṓn. Thus Mai 27 = DOY 145 (30 + 29 + 30 + 29 + 27). To make the equation work, the first three pytanies must be 38 days long (38 + 38 + 38 + 31 = 145)

Translated into Heniautos terms, Kirchner's solution for this equation is the only one that accommodates this alternation (by virtue of having an even number of full and hollow months).


    > calendar_equation.py -e Mai 27 IV 31
    Mai 27 ( 5-) =   IV 31 =  DOY 145 (I) [FFHH, SSS]
    Mai 27 ( 5-) =   IV 31 =  DOY 146 (I) [FFFH, LSS]
    Mai 27 ( 5-) =   IV 31 =  DOY 147 (I) [FFFF, LLS]

Therefore, his **[Mai] 27 = [IV] [31]** looks like this:

![324/3 BCE](img/kirchner-year-336.png)

Dinsmoor looked at this inscription next (Dinsmoor 1931, 356). He noted that all festival dates in IG II² 328 and 330 require restoring, but "In the first instance [IG II² 328] it was clearly the longest name Maimakterion so that the day must have been 144/145th of the year." He thus reopens the possibility of a hollow Maimaktēriṓn in which τετράδι φθίνοντος means the 26th. He then pursues this, again with the assumption of regularly alternating months: "Beginning the year with Hekatombaion and Maimakterion also being hollow it is probably that the first equation was Maim. 26 = Pryt. IV,29." That is, reading lines 4-5 as:

           [Μαιμακτηριῶνος τετ]ράδι φθί-
    [νοντος, ἐνάτηι καὶ εἰκοστ]εῖ

Plugging **Mai 26 = IV 29** into `calendar-equation` we have:

    > calendar_equation.py -e Mai 26 IV 29
    Mai 26 ( 5-) =   IV 29 =  DOY 143 (I) [FHHH, SSS]
    Mai 26 ( 5-) =   IV 29 =  DOY 144 (I) [FFHH, LSS]
    Mai 26 ( 5-) =   IV 29 =  DOY 145 (I) [FFFH, LLS]
    Mai 26 ( 5-) =   IV 29 =  DOY 146 (I) [FFFF, LLL]

Like Kirchner, Dinsmoor settled on the only solution (DOY 144) that worked with alternating full and hollow months (albeit the reverse alternation from Kirchner's), including the fact that "Pryt. I had 39 days, II-III had 38."

![324/3 BCE](img/dinsmoor-year-336.png)

Pritchett and Neugebaur were the first to take Aristotle's statment about prytanies to heart. They disagreed with the previous practice of making restorations "in conformity with this assumption of rigid [sic] sequence of months and days in the civic calendar" since this led to "prytanies of varying lengths" being "interspersed at random thoughout the prytany year." Instead, they proposed that we "reverse the method by positing a rule of regularity in the length and sequence of prytanies" (Pritchett and Neugebauer 1947, 34-35). They thus restored the prytany date of IG II² 328 as the 28th (Pritchett and Neugebauer 1947, 43):

           [Μαιμακτηριῶνος τετ]ράδι φθί-
    [νοντος, ὀγδόηι καὶ εἰκοστ]εῖ
    
Returning to a full Maimaktēriṓn, this gives us an equation **Mai 27 = IV 28** 

    > calendar_equation.py -e Mai 27 IV 28
    Mai 27 ( 5-) =   IV 28 =  DOY 143 (I) [HHHH, LSS]
    Mai 27 ( 5-) =   IV 28 =  DOY 144 (I) [FHHH, LLS]
    Mai 27 ( 5-) =   IV 28 =  DOY 145 (I) [FFHH, LLL]

The DOY 145 solution allows for the Rule of Aristotle.

![324/3 BCE](img/pritchett-year-336.png)

This clearly also still accomodates a regular alternation, but it does not assume it. The difference between Pritchet and Neugebauer's equation and Dinsmoor is that Dinsmoor, beginning with an assumption about the festival year settled on a solution that would only accomodate the Rule of Aristotle if the first four months were full (the DOY 146 solution for Mai 26 = IV 29, above, and astronomically improbable if not impossible). Pritchett and Neugebauer, on the other, begin with an assumption about the conciliar calendar and arrive at a solution that allows for regularity in the prytanies (the Rule) without excluding regularity in the festival months. 

IG II³,1 327 (= IG II² 330) contains two dates, one in lines 29-30:

    [ἐπ]ὶ Πυθοδήλου ἄρχοντος, ἐ[πὶ τῆς ․․․․8․․․․ ἐνάτης πρυτανεί]-
    [ας]· τετράδι ἐπὶ δέκα· δευτέ[ραι τῆς πρυτανείας
    
and another in lines 47-49:

    [ἐπ]ὶ Πυθοδήλου ἄρχοντος, ἐπ[ὶ τῆς ․․․․․10․․․․․ δεκάτης πρυτα]-
    [ν]είας· ἕνει καὶ νέαι· ἑβδόμη[ι καὶ τριακοστῆι τῆς πρυτανεία]-
    [ς]

The festival month is omitted in both, and since the prytany must be restored much relies on one's theories about the calendar. Kirchner was very much in the early days of calendar research and reconstructed of the lengths of the prytanies for this year (given in his commentary on IG II² 330) as 39, 38, 38, 38, 38, 38, 39, 39, 40, 37 days. Dinsmoor's statement that "The second equation, with the 14th of a month falling on the second of a prytany could be either the sixth or the ninth prytany; the third with the last day of a month falling on the 37th of a prytany, could be either the seventh or the tenth prytany" we can check with `calendar-equations`, starting with the first equation, **? 14 = ? 2**: 

    > calendar_equation.py -e any 14 any 2 --no-ordinary
    Pos 14 ( 7+) =   VI  2 =  DOY 192 (I) [FFFFHH, SSSSS]
    Gam 14 ( 7-) =   VI  2 =  DOY 192 (I) [FFFFHH, SSSSS]
    Pos 14 ( 7+) =   VI  2 =  DOY 193 (I) [FFFFFH, LSSSS]
    Gam 14 ( 7-) =   VI  2 =  DOY 193 (I) [FFFFFH, LSSSS]
    Pos 14 ( 7+) =   VI  2 =  DOY 194 (I) [FFFFFF, LLSSS]
    Gam 14 ( 7-) =   VI  2 =  DOY 194 (I) [FFFFFF, LLSSS]
    Mou 14 (11+) =   IX  2 =  DOY 308 (I) [FFFFHHHHHH, LLSSSSSS]
    Tha 14 (11-) =   IX  2 =  DOY 308 (I) [FFFFHHHHHH, LLSSSSSS]
    Mou 14 (11+) =   IX  2 =  DOY 309 (I) [FFFFFHHHHH, LLLSSSSS]
    Tha 14 (11-) =   IX  2 =  DOY 309 (I) [FFFFFHHHHH, LLLSSSSS]
    Mou 14 (11+) =   IX  2 =  DOY 310 (I) [FFFFFFHHHH, LLLLSSSS]
    Tha 14 (11-) =   IX  2 =  DOY 310 (I) [FFFFFFHHHH, LLLLSSSS] 

We can simplify this by (manually) combining the alternatives for the festival months

    Pos/Gam 14 (7)  =  VI  2 =  DOY 192 (I) [FFFFHH, SSSSS]
    Pos/Gam 14 (7)  =  VI  2 =  DOY 193 (I) [FFFFFH, LSSSS]
    Pos/Gam 14 (7)  =  VI  2 =  DOY 194 (I) [FFFFFF, LLSSS]
    Mou/Tha 14 (11) =  IX  2 =  DOY 308 (I) [FFFFHHHHHH, LLSSSSSS]
    Mou/Tha 14 (11) =  IX  2 =  DOY 309 (I) [FFFFFHHHHH, LLLSSSSS]
    Mou/Tha 14 (11) =  IX  2 =  DOY 310 (I) [FFFFFFHHHH, LLLLSSSS]

And if we do the same simplification for **? 29/30 = ? 37** of the output from `calendar_equation.py -e any last any 37 --no-ordinary` we have:

    Ant/Ela 29 (9) =  VII 37 =  DOY 265 (I) [FFFFHHHH, SSSSSS]
    Ant/Ela 30 (9) =  VII 37 =  DOY 265 (I) [FFFHHHHH, SSSSSS]
    Ant/Ela 29 (9) =  VII 37 =  DOY 266 (I) [FFFFFHHH, LSSSSS]
    Ant/Ela 30 (9) =  VII 37 =  DOY 266 (I) [FFFFHHHH, LSSSSS]
    Ant/Ela 29 (9) =  VII 37 =  DOY 267 (I) [FFFFFFHH, LLSSSS]
    Ant/Ela 30 (9) =  VII 37 =  DOY 267 (I) [FFFFFHHH, LLSSSS]
    Ant/Ela 29 (9) =  VII 37 =  DOY 268 (I) [FFFFFFFH, LLLSSS]
    Ant/Ela 30 (9) =  VII 37 =  DOY 268 (I) [FFFFFFHH, LLLSSS]
    Ant/Ela 30 (9) =  VII 37 =  DOY 269 (I) [FFFFFFFH, LLLLSS]
    Ski 29 (13+)   =    X 37 =  DOY 382 (I) [FFFFFHHHHHHH, LLLSSSSSS]
    Ski 29 (13+)   =    X 37 =  DOY 383 (I) [FFFFFFHHHHHH, LLLLSSSSS]
    Ski 30 (13+)   =    X 37 =  DOY 383 (I) [FFFFFHHHHHHH, LLLLSSSSS]

In both the prytany VI and VII solutions those that fit the Rule of Aristotle require an impossible count of festival months while those that are more realistic solutions for the festival months have the worst violations of the Rule. The consensus since Kirchner has been to restore the prytanies as IX and X, and to supply Mounuchiṓn and Skirophoriṓn (assuming that the intercalation came earlier in the year). The second date is very likely to be the last day of the year, so any solution should take into account that the DOY probably also represents the length of the year. 

Collation does not help much in this situation. We can check all the above possibilities with the `calendar-equation` command 

    > calendar_equation.py -e Mai 26/27 iv 28/29/31 -e any 14 any 2 -e any last any 37 --no-ordinary -c
    
But in this case it only serves to multiply the possibilities (289 mathematically valid collations!) rather than narrow them. For simplicity's sake we can highlight the solutions that best fit the two extremes. First those that allow for a perfect alternation of full and hollow months:

     54: FFHH FFFHHH FH   LLS LSSSS L
     64: FFHH FFFHHH FH   LSS LLSSS L
    150: FFHH FFFHHH FH   LLL SSSSS L
    160: FFHH FFFHHH FH   LLS LSSSS L
    185: FFHH FFFHHH FH   SSS LLLSS L
     54: Mai 26 = IV 28 = 144 + Mou 14 = IX 2 = 309 + Ski 29 = X 37 = 383
     64: Mai 26 = IV 29 = 144 + Mou 14 = IX 2 = 309 + Ski 29 = X 37 = 383
    150: Mai 27 = IV 28 = 145 + Mou 14 = IX 2 = 309 + Ski 29 = X 37 = 383
    160: Mai 27 = IV 29 = 145 + Mou 14 = IX 2 = 309 + Ski 29 = X 37 = 383
    185: Mai 27 = IV 31 = 145 + Mou 14 = IX 2 = 309 + Ski 29 = X 37 = 383
    
Second those that fit the Rule of Aristotle:

     97: FFFH FFFHHH HH   LLL LSSSS S
    155: FFHH FFFFHH HH   LLL LSSSS S
    198: FFFF FFHHHH HH   LLL LSSSS S
    242: FFFH FFFHHH HH   LLL LSSSS S

     97: Mai 26 = IV 28 = 145 + Mou 14 = IX 2 = 310 + Ski 29 = X 37 = 383
    155: Mai 27 = IV 28 = 145 + Mou 14 = IX 2 = 310 + Ski 29 = X 37 = 383
    198: Mai 26 = IV 29 = 146 + Mou 14 = IX 2 = 310 + Ski 29 = X 37 = 383
    242: Mai 27 = IV 29 = 146 + Mou 14 = IX 2 = 310 + Ski 29 = X 37 = 383

 Pritchett and Neugebaur settled on these three equations as indications that the Rule of Aristotle should be followed:

* **[Mai] 27 = [IV] [28] = DOY 145**
* **<Mou> 14 = [IX] 2 = DOY 310**
* **<Ski> 29 = [X] 37 = DOY 383**
 
Among the `calendar-equations` collations, this is #155, with the counts and partitions: `FFHH FFFFHH HH`, `LLL LSSSS S`. Far from assuming a regular alternation of festival months, it assumes that "the months Mounichion, Thargelion, and Skirophion were each of 29 days duration."

![324/3 BCE](img/pritchett-year-336-2.png)

One consequence of the equation **<Ski> 29 = [X] 37 = DOY 383** that should be noted is that the last prytany is short by a day (37 rather than 38 days) to accomodate a 383 rather than 384 day intercalary year.

Meritt, who did not believe that the festival months were regulated by lunar observations, accepted all of Pritchett and Neugebaur's restorations, but argued that three hollow months in a row should present something of a difficulty for Pritchett and Neugebaur and others who do (Meritt 1961, 13). While three hollow months is more astronomically probable than Meritt makes it seem, it does offer a check against another line of evidence for which he turned to the best astronomical data available to him at the time, calculations published by Parker and Dubberstein (1942, 35-36). Their dates for visible new moons in 336/5 BCE are very close to those from Heniautos:

| Month | P&D Start | P&D Days | Hen. Start | Hen. Days |
|-------|-----------|----------|------------|-----------|
| Hek   | Jul-06    | 30       | Jul-06     | 29        |
| Met   | Aug-05    | 29       | Aug-04     | 30        |
| Boe   | Sep-03    | 30       | Sep-03     | 29        |
| Pua   | Oct-03    | 29       | Oct-02     | 30        |
| Mai   | Nov-01    | 30       | Nov-01     | 29        |
| Pos   | Dec-01    | 29       | Nov-30     | 30        |
| Pos₂  | Dec-30    | 30       | Dec-30     | 30        |
| Gam   | Jan-29    | 30       | Jan-29     | 29        |
| Ant   | Feb-28    | 29       | Feb-27     | 30        |
| Ela   | Mar-29    | 30       | Mar-29     | 30        |
| Mou   | Apr-28    | 29       | Apr-28     | 29        |
| Tha   | May-27    | 30       | May-27     | 30        |
| Ski   | Jun-26    | 29       | Jun-26     | 29        | 

Meritt's only appeals to astronomy to weaken Pritchett and Neugebaur's reconstruction of a year ending with three hollow months. His purpose is to show that the Rule of Aristotle is not a requirement and that a sensible reconstruction of the year can be without it while improving on those of Kirchner and Dinsmoor. To this end he settles on these three equations:

* **[Mai] 26 = [IV] [28] = DOY 144**
* **<Mou> 14 = Prytany [IX] 2 = DOY 309**
* **<Ski> 29 = [X] [3]7 = DOY 383**

This is #54 from our solutions, above, which has the partitions `FFHH FFFHHH FH` and `LLS LSSSS L`. For τετράδι φθίνοντος to be the 27th, Maimaktēriṓn must be hollow. Assuming a regular alternation of months, as Meritt does, this makes all the odd-numbered months hollow, so Meritt reconstructs this as beginning with a hollow Hekatombaiṓn, and prytanies I, II, VIII and IX with 39 days:

![324/3 BCE](img/meritt-year-336-with-schematic.png)

His one departure from perfectly regular alternation is, after the last day of Skirophoriṓn (29 = X 37), to posit an "intercalated last day of Skirophoriṓn" so that there is a Ski 29₂ = X 38 which fills out the prytany and brings the year to 384 days rather than Pritchett and Neubegauer's 383.

As we said before, this is mathematically possible but Meritt offers no mechanism by which the Athenians might have decided on this arrangement. It would be very characteristic of them to draw lots for the lengths of prytanies (as the did for the _phulaí_ holding the prytanies), but there is no historical evidence they did so and no one has ever reconstructed conciliar years that random--many of Meritt's reconstructions do fit the decidedly non-random Rule of Aristotle but those that do not usually have some long prytanies at the beginning with the rest coming at or near the end. Lots would require more years that looked like `LSLSLSSSLS` or `LSSSSLLSLS` than `LLSSSSSSLL` or `LLSSSSSLLS`. Without that, what motivation could they have had?

Pritchett and Neubegaur did not have Parker and Dubberstein's calculations of ancient visible moons. With the even better data, from NASA's Jet Propulsion Laboratory, that Heniautos relies on, is their a better solution that fits the Rule of Aristotle? Here is the Heniautos view of 336/5 BCE

    > heniautos -m 336
         Year     |        Month          |      Start      | Days
    --------------|-----------------------|-----------------|-----
    BCE 336/335   | Hekatombaiṓn          | BCE 0336-Jul-06 |   29
    BCE 336/335   | Metageitniṓn          | BCE 0336-Aug-04 |   30
    BCE 336/335   | Boēdromiṓn            | BCE 0336-Sep-03 |   29
    BCE 336/335   | Puanopsiṓn            | BCE 0336-Oct-02 |   30
    BCE 336/335   | Maimaktēriṓn          | BCE 0336-Nov-01 |   29
    BCE 336/335   | Posideiṓn             | BCE 0336-Nov-30 |   30
    BCE 336/335   | Posideiṓn hústeros    | BCE 0336-Dec-30 |   30
    BCE 336/335   | Gamēliṓn              | BCE 0335-Jan-29 |   29
    BCE 336/335   | Anthestēriṓn          | BCE 0335-Feb-27 |   30
    BCE 336/335   | Elaphēboliṓn          | BCE 0335-Mar-29 |   30
    BCE 336/335   | Mounuchiṓn            | BCE 0335-Apr-28 |   29
    BCE 336/335   | Thargēliṓn            | BCE 0335-May-27 |   30
    BCE 336/335   | Skirophoriṓn          | BCE 0335-Jun-26 |   29
    
This fits one of the `calendar-equations` solutions very well--#155, the same as match Pritchett and Neugebaur's equations. It can fit both becuase the collation of the three equations does not say anything about the length of Skirophoriṓn. Above we made hollow in the schematic representation, below we make it full.

![324/3 BCE](img/possible-solution-336.png)

Parker and Duberstein's calculations fit this solution equally well (P&D). It terms of counts, Heniautos and P&D are exactly equivalent and differ only in the arragment of months. The only reason to prefer Heniautos' dates over Parker and Duberstein's is that Heniautos data comes from computer calculations made by an agency that successfully sends probes to Pluto. The only problem (for both) is on the last three months. The collation requires Mounuchiṓn and Thargēliṓn to be hollow, which we can accommodate by moving up the first day of Skirophoriṓn to June 25. This gives us a hollow Thargēliṓn but now the last day, ἕνει καὶ νέαι, of Skirophoriṓn should by Ski 30 = X 38. Perhaps Meritt is correct to posit a Ski 29 = X 37 followed by Ski 29₂ = X 38?

There is a way around this complication. Unfortunately, it requires that we recognize the fact that we cannot put much trust in the recorded festival dates. As cases where there is no good solution for an equation show, Athenians made many silent manipulations of the festival calendar.

## It Doesn't Always Work Out

It is frequently the case that you have a perfectly clear calendar equation that has no good solution. Take for instance [IG II³,1 917](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20II_III%C2%B3%201,%20917) from 266/5

    [ἐπ]ὶ Νικίου ἄρχοντος [Ὀτρυνέ]ως ἐπὶ τῆς Ἀκαμαντίδος τρίτ-
    [ης] πρυτανείας, ἧι Ἰσο[κράτ]ης Ἰσοκράτου Ἀλωπεκῆθεν ἐγρα-
    [μμ]άτευεν· Βοηδρομιῶ[νος ἕκτ]ει μετ’ εἰκάδας, ἕκτει καὶ εἰκ-
    [οσ]τεῖ τῆς πρυτανεία[ς
    
This is from the [period of twelve _phulaí_](conciliar-calendar.md#307-224-bce) and is a normal year so we would the prytanies to be 30 or 29 days, following the festival calendar. Ἕκτει μετ’ εἰκάδας, however, is the 24th or 25th of the month and the prytany date is the 26th (ἕκτει καὶ εἰκοστεῖ) so it seems one or two days off. There are mathematically _possible_ solutions but they require odd arrangements of months and prytanies: 

    > calendar_equation.py -p 12 -e Boe 24/25 III 26
    Boe 24 ( 3-) =  III 26 =  DOY  84 (O) [FF, SS]
    Boe 25 ( 3-) =  III 26 =  DOY  84 (O) [FH, SS]
    Boe 25 ( 3-) =  III 26 =  DOY  85 (O) [FF, LS]
    
It is hard to imagine, for instance, why anyone would start a year with two 30-day months (FF) but two 29-day prytanies (SS). You might hypothesize an error on the part of the letter-carver, since the backward count of festival month, ἕκτει μετ’ εἰκάδας, is very similar to the forward count of the prytany, ἕκτει καὶ εἰκοστεῖ, but that would not explain another dated decree from later in the year, [IG II³,1 918](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20II_III%C2%B3%201,%20918)

    [ἐπὶ Νικίου] ἄρ[χοντο]ς Ὀτρυνέω̣[ς, ἐπὶ τῆς – –c.6–8– –δος ἕκτ]–
    ης πρυτανείας, ἧι Ἰσοκράτης Ἰσοκράτ̣ο̣[υ Ἀλωπε]κῆ̣θεν ἐ[γ]–
    ραμμάτευεν· Ποσιδεῶνος ἑν[δε]κ̣άτει· δωδ[εκά]τει τῆς π[ρ]–
    υτανείας
    
We would expect Pos 11 = VI 11 or Pos 12 = VI 12. Inscribing ἑνδεkάτει for δωδεκάτει or vice versa, is not an obvious mistake to make. 

An even more troublesome scenario is in [IG II³,1 352](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20II_III%C2%B3%201,%20352) (=IG II² 351). This inscription has a prefectly clear date, requiring no important restorations **Tha 11 = IX 19** but, as `calendar-equation` will tell us, there is no solution for this equation:

    > calendar_equation -e Tha 11 IX 19
    No solutions for ((<Months.THA: 11>, 11),) = ((<Prytanies.IX: 9>, 19),
    
There is another inscription from the same year, [IG II³,1 353](http://telota.bbaw.de/ig/digitale-edition/inschrift/IG%20II_III%C2%B3%201,%20353) (=IG II² 352) with equally certain equation **Tha 14 = IX 32**. This equation does have solutions, all for an intercalary year which we expect this year (330/29) to be astronomically:

    > calendar_equation.py -p 10 -e Tha 14 IX 32
    Tha 14 (12+) =   IX 32 =  DOY 338 (I) [FFFFFHHHHHH, LLSSSSSS]
    Tha 14 (12+) =   IX 32 =  DOY 339 (I) [FFFFFFHHHHH, LLLSSSSS]
    Tha 14 (12+) =   IX 32 =  DOY 340 (I) [FFFFFFFHHHH, LLLLSSSS]
    
The festival dates, Tha 11 and Tha 14, are only three days apart while the prytany dates, IX 11 and IX 32, are 13 days apart. This has led to many hypotheses of errors on the part of the inscriber in IG II³,1 352 (Meritt 1961, 91-94). There is another possibility, though.

### Triple Dating

[IG II² 1006](https://epigraphy.packhum.org/text/3226) (122/1 BCE) is one of a handful of inscriptions with what is known as a triple date:

    ἐπὶ Νικ[ο]δήμου ἄρχοντος ἐπὶ τῆς Αἰγεῖδος τρίτης πρυτανείας, ᾗ Ἐπιγένης Ἐπιγένου Οἰναῖος ἐγραμ-
    μάτευε[ν]· Βοιηδρομιῶνος ὀγδόῃ ἱσταμένου ἐμβολίμωι κατ’ ἄρχοντα, κατὰ θεὸν δὲ ἐνάτῃ ἱσταμένου,
    ἐνάτῃ τῆς πρυτανείας
    
Here we have one prytany date III 9, and two festival dates: Βοιηδρομιῶνος ὀγδόῃ ἱσταμένου ἐμβολίμωι κατ’ ἄρχοντα and κατὰ θεὸν δὲ ἐνάτῃ ἱσταμένου, "the intercalary (ἐμβολίμωι) eighth of Boēdromiṓn according to the archon (κατ’ ἄρχοντα), according to the god (κατὰ θεὸν) the ninth." Ὀγδόῃ ἱσταμένου ἐμβολίμωι shows that the Athenians not only intercalated months, but even _days_. For a short time in the second century BCE, they also made a practice of sometimes distinguishing dates that are κατ’ ἄρχοντα from those that are κατὰ θεὸν, as is done here.

Many interpretations of these two terms were offered in the course of the 19th and 20th centuries, but the simplest was finally the one agreed on (see Meritt and Traill 1974, 23-24). Κατὰ θεὸν indicates a "natural" lunar date, the equivalent of κατὰ σελήνην "according to the moon" (or κατὰ Σελήνην, "according the goddess Selene") which is found elsewhere.  κατ’ ἄρχοντα indicates a date that is the result of some adjustment on the part of the archon. We are not sure why this was done, but it is likely that it was to manage the times of festivals. Since certain dates were considered holu, rather than rescheduling a festival, the calendar was adjusted so that the regular date of the festival fell where it was desired. It seems, though, that the prytany dates are never adjusted.

We would expect, Boe 9 to correspond to III 9. Instead, this inscription shows us that in September of 122 BCE, this stretch of the Athenian calendar was "adjusted" by adding a repeating Boe 8 (which we will represent as Boe 8₂): 

| κατὰ θεὸν | κατ’ ἄρχοντα | Prytany | DOY | Julian |
|-----------|--------------|---------|----:|--------|
| Boe 6     | Boe 6        | III 6   | 65  | Sep 13 |
| Boe 7     | Boe 7        | III 7   | 66  | Sep 14 |
| Boe 8     | Boe 8        | III 8   | 67  | Sep 15 |
| Boe 9     | **Boe 8₂**       | III 9 | 68   | Sep 16 |
| Boe 10    | Boe 9        | III 10  | 69  | Sep 17 |
| Boe 11    | Boe 10       | III 11  | 70  | Sep 18 |

There are three possible solutions for **Boe 9 = III 9**

    > calendar_equation -p 12 -e Boe 9 III 9
    Boe  9 ( 3-) =  III  9 =  DOY  67 (O) [HH, SS]
    Boe  9 ( 3-) =  III  9 =  DOY  68 (O) [FH, LS]
    Boe  9 ( 3-) =  III  9 =  DOY  69 (O) [FF, LL]
    
The Julian dates above are assigned according to the DOY 68 solution, which fits Heniautos' calculation that Hekatombaiṓn is full and Metageitniṓn is hollow for this year. To give a full, if provisional, equation, we will use the abbreviations κΑ and κΘ for the κατ’ ἄρχοντα and κατὰ θεὸν dates, give the κατ’ ἄρχοντα adjustment in parentheses after that date, and use the star symbol (✸) as above for dates made by astronomical calculation:

**Boe 8₂ κΑ (+1) = Boe 9 κΘ = ✸DOY 68 = ✸Sept. 16, 122 BCE**


This would seem to explain IG II³,1 917 and 918 as well. In those inscriptions, wehad Boe 25 = III 26 where whe would expect it to equal II 25 and Pos 11 = VI 12 where we would expect it to equal VI 11. The obvious hypothesis is that an itercalary day anytime before Boe 25 put the κατὰ θεὸν and κατ’ ἄρχοντα calendars out od sync by one day. This further indicates that any impossible or suspicious  calendar equation is possibly the result of an adjustment like this one. 

[Agora XV 238](https://epigraphy.packhum.org/text/231109) (= IG II² 967) is another example with a much greater adjustment:

    [ἐπ]ὶ Μητροφάνου ἄρχοντος ἐπὶ τῆς Ἀκαμαντίδος δεκάτης πρυτα-
    νείας, ἧι Ἐπιγένης Μοσχίωνος Λαμπτρεὺς ἐγραμμάτευεν· ἀντι-
    γραφεὺς Δημοκράτης Δημοκράτου Κυδαθηναιεύς· Ἐλ̣αφηβολιῶνο[ς]
    ἐνάτει μετ’ εἰκάδας κατ’ ἄρχοντα, κατὰ θεὸν [δ]ὲ Μ̣ουνιχιῶνος δωδε[κά]-
    τει, δωδεκάτει τῆς πρυτανείας
    
The κατὰ θεὸν date equates the festival and prytany days as we wold expect in an ordinary year in this period (145/4 BCE), Mou 12 = X 12. ἐνάτει μετ’ εἰκάδας is probably the 22nd of a full or 21st of a hollow month, so this represent 20 or 21 intercalary days. `calendar-equation` gives us four possibilities for the κατὰ θεὸν date:

    > calendar_equation -p 12 -e Mou 12 X 12
    Mou 12 (10-) =    X 12 =  DOY 277 (O) [FFFFHHHHH, LLLLSSSSS]
    Mou 12 (10-) =    X 12 =  DOY 278 (O) [FFFFFHHHH, LLLLLSSSS]
    Mou 12 (10-) =    X 12 =  DOY 279 (O) [FFFFFFHHH, LLLLLLSSS]
    Mou 12 (10-) =    X 12 =  DOY 280 (O) [FFFFFFFHH, LLLLLLLSS] 

and the DOY 279 solution matches the 6 full months that Heniautos calculates before Mounuchiṓn 145/4 BCE. We can give a provisional solution, where the date in Elaphēboliṓn as marked with a star because it is based on the calculation that the month is full rather than hollow so that ἐνάτει μετ’ εἰκάδας is the 22nd:

**Ela ✸22 κΑ (+20) = Mou 12 κΘ = X 12 = ✸DOY 279 = ✸Apr 27, 144 BCE**

Intercalary years in the 3rd century BCE and later are especially useful for understanding the calendar because the prytanies are all the same length (32 days) and avoid any complications due to accepting or rejecting the rule of Aristotle. Triple dated inscriptions from intercalary years would be that much more useful becuase the contain one date that should be that of a true lunar month. Unfortunately there are no examples free of complications from restoration or uncertainty of the date of the archon.

### Implications

These calendar adjustments were not limited to the years when triple dating was in use. In an oft-cited passage in Aristophanes' _Clouds_, the chorus reports the complaints of the moon to the Athenians that "you do not manage the days at all correctly but make a jumble all up and down" (615-616); it ends by saying that Hyperbolus "ought to manage the days of his life according to the moon (κατὰ σελήνην)" (626). This is usually interpreted to mean that the kinds of adjustments explicit in the κατ’ ἄρχοντα/κατὰ θεὸν dates were common as early as the 5th century BCE (van der Waerden 1960, 179; Dunn 1998, 228).

On the positive side, when a calendar equation seems to have no solution, such as IG II³,1 352 **Tha 11 = IX 19** the evidence from triple dating gives us the hypothesis that dates are κατ’ ἄρχοντα, and reflect intercalary days previously added to the calendar. In 330/29, it seems, 10 days added before IG II³,1 352 had been "taken back" before  IG II³,1 353 **Tha 14 = IX 32**, which has solutions as an intercalary year (one of which satisfies the Rule of Aristotle).


| κατὰ θεὸν | κατ’ ἄρχοντα | Prytany | DOY | Julian |
|-----------|--------------|---------|-----|--------|
| Tha 1     | Tha 11       | IX 19   | 327 | May 21 |
| Tha 2     | ?            | IX 20   | 328 | May 22 |
| Tha 3     | ?            | IX 21   | 329 | May 23 |
| Tha 4     | ?            | IX 22   | 330 | May 24 |
| Tha 5     | ?            | IX 23   | 331 | May 25 |
| Tha 6     | ?            | IX 24   | 332 | May 26 |
| Tha 7     | ?            | IX 25   | 333 | May 27 |
| Tha 8     | ?            | IX 26   | 334 | May 28 |
| Tha 19    | ?            | IX 27   | 335 | May 29 |
| Tha 10    | ?            | IX 28   | 336 | May 30 |
| Tha 11    | ?            | IX 29   | 337 | May 31 |
| Tha 12    | ?            | IX 30   | 338 | Jun  1 |
| Tha 13    | ?            | IX 31   | 339 | Jun  2 |
| Tha 14    | Tha 14       | IX 32   | 340 | Jun  3 |

This, of course, assumes that IG II³,1 352 and 353 are both reporting κατ’ ἄρχοντα dates that by the middle of Thargēliṓn coincided with the κατὰ θεὸν rather than, say, a κατ’ ἄρχοντα in 352 and a κατὰ θεὸν in 353.

On the negative side any equation must be treated with suspicion. It is possible for a κατ’ ἄρχοντα date to have solutions. If the decree recorded in IG II² 1006, above, had been passed one date later, Boe 9 (κΑ) rather than Boe 8₂, if it it was double- rather than triple-dated, we would be trying to make sense of an equation **Boe 9 = III 10**. Mathematically, this _has_ solutions:

    > calendar_equation -p 12 -e Boe 9 iii 10
    Boe  9 ( 3-) =  III 10 =  DOY  68 (O) [FH, SS]
    Boe  9 ( 3-) =  III 10 =  DOY  69 (O) [FF, LS]

These are just misleading about the lengths of months and prytanies.

The Athenian calendar is a fascinating and frustrating puzzle. The clues provided by these calendar equations are open to multiple interpretations and, while the efforts of epigraphers in the last hundred years have done much to clarify the data, their disagreements were many and interpretations changed a great deal as more information became available. In the end, this may have left more smoke than fire for any who comes to this topic now. I ony hope that Heniautos makes it easier for anytone to explore the evidence, to examine it in different ways, and come up with new and better conclusions.
 

## Works Cited

* Agora XV = Meritt, Benjamin Dean, and John S. Traill, eds. 1974. _Inscriptions: The Athenian Councillors_. The Athenian Agora 15. Princeton, N.J: American School of Classical Studies at Athens.
* Agora XVI = Woodhead, A. G. 1997. _Inscriptions: The Decrees_. The Athenian Agora, v. 16. Princeton: American School of Classical Studies at Athens.
* Dinsmoor, William Bell. 1931. _The Archons of Athens in the Hellenistic Age_. Cambridge: Harvard University Press.
* Dunn, Francis M. 1998. “Tampering with the Calendar.” Zeitschrift für Papyrologie Und Epigraphik 123: 213–31.
* Hansen, Mogens Herman. 1982. “When Did the Athenian Ecclesia Meet?” _GRBS_ 23 (4): 331–50.
* Meritt, Benjamin D. 1938. “Greek Inscriptions.” _Hesperia_ 7 (1): 77–160.
* ----------. 1947. “Greek Inscriptions.” _Hesperia_ 16 (3): 147–83.
* ----------. 1964. “Greek Inscriptions.” _Hesperia_ 33 (2): 168–227.
* ----------. 1968. “Calendar Studies.” _Αρχαιολογική Εφημερίς_, 77–115.
* ----------. 1974. “The Count of Days at Athens.” _American Journal of Philology_ 95 (3): 268–79.
* ----------. 1977. “Athenian Archons 347/6-48/7 B.C.” Historia 26 (2): 161–91.
* ----------. 1977. “The Hollow Month at Athens.” _Mnemosyne_ 30 (3): 217–42.
* Meritt, Benjamin D., Margaret Larson Lethen, and George A. Stamires. 1957. “Greek Inscriptions.” _Hesperia_ 26 (1): 24–97.
* Osborne, Michael. 2008. “The Date of the Athenian Archon Thrasyphon.” _Zeitschrift Für Papyrologie und Epigraphik_ 164: 85–89.
* Parker, Richard Anthony, and Waldo H. Dubberstein. 1942. _Babylonian Chronology 626 B. C.-45._ Studies in Ancient Oriental Civilization 24. Chicago: The University of Chicago Press.
* Pritchett, W. Kendrick, and Benjamin D. Meritt. 1940. _The Chronology of Hellenistic Athens_. Cambridge: Harvard University Press.
* Pritchett, W. Kendrick. 1970. “The Name of the Game Is Restoration.” _California Studies in Classical Antiquity_ 3: 199–214.
* Waerden, B. L. van der. 1960. “Greek Astronomical Calendars and Their Relation to the Athenian Civil Calendar.” _Journal of Hellenic Studies_ 80: 168–80.


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.