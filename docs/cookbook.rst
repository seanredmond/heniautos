.. _cookbook:

Cookbook
========

.. currentmodule:: heniautos

Import the library:

>>> import heniautos as ha

Get the ”astronomical year” for 431 BCE:

>>> ha.bce_as_negative(431)
-430

Get a Calendar
--------------

Get the whole Athenian calendars for 431 and 430 BCE:

>>> year_431 = ha.athenian_festival_calendar(ha.bce_as_negative(431))
>>> year_430 = ha.athenian_festival_calendar(ha.bce_as_negative(430))

Or:

>>> year_431 = ha.athenian_festival_calendar(-430)
>>> year_430 = ha.athenian_festival_calendar(-429)
>>> year_431[0]
FestivalDay(jdn=1564187, month_name='Hekatombaiṓn', month_index=1, month=<AthenianMonths.HEK: 1>, month_length=29, day=1, doy=1, year='BCE 431/430', year_length=383, astronomical_year=-430)
>>> year_431[-1]
FestivalDay(jdn=1564569, month_name='Skirophoriṓn', month_index=13, month=<AthenianMonths.SKI: 12>, month_length=29, day=29, doy=383, year='BCE 431/430', year_length=383, astronomical_year=-430)

Group the calendar by months:

>>> months_431 = ha.by_months(year_431)
>>> len(months_431)
13

Date Conversion
---------------

>>> ha.as_julian(year_431[0])
'BCE 0431-Jul-06'
>>> ha.as_gregorian(year_431[0])
'BCE 0431-Jul-01'

Calendar dates are returned as noon GMT:

>>> ha.as_julian(year_431[0], full=True)
'BCE 0431-Jul-06 12:00:00 GMT'

You can convert this to the imaginary timezone ”Athens Local Time” (94 minutes ahead of Greenwhich, England):

>>> ha.as_julian(year_431[0], full=True, tz=ha.TZOptions.ALT)
'BCE 0431-Jul-06 13:34:54 ALT'


You can use juliandate (which is a dependency of heniautos) to convert a jdn to a tuple for other purposes:

>>> import juliandate as jd
>>> jd.to_julian(year_431[0].jdn)
(-430, 7, 6, 12, 0, 0, 0)



Ordinary and Intercalary Years
------------------------------

Is the year intercalary? Method 1a, judge by the number of days (an ordinary year will have 353, 354, or 355):

>>> len(year_431) > 355
True
>>> len(year_430) > 355
False

Method 1b, every day has a year_length property:

>>> year_431[0].year_length > 355
True
>>> year_430[0].year_length > 355
False

Method 2, look for an intercalary month (it will always have the constant Months.INT):

>>> any([d.month == ha.Months.INT for d in year_431])
True
>>> any([d.month == ha.Months.INT for d in year_430])
False

Method 3, count the months:

>>> len(ha.by_months(year_431)) > 12
True
>>> len(ha.by_months(year_430)) > 12
False

Solstices and New Moons
-----------------------

When was the summer solstice in 431 BCE?

>>> ha.solar_event(-430, ha.Seasons.SUMMER_SOLSTICE)
1564179.2994276646

Thanks, but what does the number (it’s a Julian Date) mean?

>>> ha.as_julian(ha.solar_event(-430, ha.Seasons.SUMMER_SOLSTICE), full=True)
'BCE 0431-Jun-28 19:11:10 GMT'

When were the new moons?

>>> ha.new_moons(-430)
(1564008.0602801414, 1564037.6455186703, 1564067.2763095852, 1564096.9253876545, 1564126.5652702623, 1564156.1786419542, 1564185.7577616004, 1564215.2989305945, 1564244.8006015243, 1564274.2669730457, 1564303.7110831663, 1564333.1512613718, 1564362.6028254696)

So the first new moon after the solstice was?

>>> [m for m in ha.new_moons(-430) if m > ha.solar_event(-430, ha.Seasons.SUMMER_SOLSTICE)][0]
1564185.7577616004

And that means?

>>> ha.as_julian([m for m in ha.new_moons(-430) if m > ha.solar_event(-430, ha.Seasons.SUMMER_SOLSTICE)][0], full=True)
'BCE 0431-Jul-05 06:11:10 GMT'


