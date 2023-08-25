Function Reference
==================

.. module:: heniautos

:py:mod:`heniautos`
----------------------

Exceptions
^^^^^^^^^^

.. autoexception:: HeniautosError
.. autoexception:: HeniautosNoMatchError
.. autoexception:: HeniautosNoDataError
.. autoexception:: HeniautosNoDayInYearError
.. autoexception:: HeniautosDateNotFoundError

Enums and Classes
^^^^^^^^^^^^^^^^^

.. autoenum:: GenericMonths
.. autoenum:: ArgiveMonths
.. autoenum:: AthenianMonths
.. autoenum:: CorinthianMonths
.. autoenum:: DelianMonths
.. autoenum:: DelphianMonths
	       
		  
.. autoenum:: Seasons
.. autoenum:: TZOptions
.. autoenum:: MonthNameOptions

.. autoclass:: FestivalDay
.. autoclass:: PrytanyDay
	      

Calendar Functions
^^^^^^^^^^^^^^^^^^

.. autofunction:: festival_calendar
.. autofunction:: athenian_festival_calendar
.. autofunction:: argive_festival_calendar
.. autofunction:: corinthian_festival_calendar
.. autofunction:: delian_festival_calendar
.. autofunction:: delphian_festival_calendar
.. autofunction:: spartan_festival_calendar
.. autofunction:: by_months
.. autofunction:: jdn_to_festival_day
.. autofunction:: julian_to_festival_day
.. autofunction:: gregorian_to_festival_day


Date Formatting
^^^^^^^^^^^^^^^

.. autofunction:: bce_as_negative

.. py:function:: negative_as_bce(year)

    Inverse of :py:func:`bce_as_negative`. Treats a negative integer
    as astronomical year numbering as converts to a positive integer
    to be understood as a year BCE
   
.. autofunction:: arkhon_year
.. autofunction:: month_name
.. autofunction:: as_julian
		  
.. autofunction:: as_gregorian
.. autofunction:: to_jdn
.. autofunction:: tz_offset


Astronomical Dates
^^^^^^^^^^^^^^^^^^

.. autofunction:: solar_event
.. autofunction:: observed_solar_event
.. autofunction:: new_moons
.. autofunction:: visible_new_moons

		  


:py:mod:`heniautos.prytanies`
-----------------------------

.. autoenum:: heniautos.prytanies.Prytanies

.. autofunction:: heniautos.prytanies.prytany_calendar
.. autofunction:: heniautos.prytanies.by_prytanies
.. autofunction:: heniautos.prytanies.prytany_label
.. autofunction:: heniautos.prytanies.prytany_type
.. autofunction:: heniautos.prytanies.prytany_to_julian
.. autofunction:: heniautos.prytanies.jdn_to_prytany_day
.. autofunction:: heniautos.prytanies.julian_to_prytany_day
.. autofunction:: heniautos.prytanies.gregorian_to_prytany_day


:py:mod:`heniautos.equations`
-----------------------------

.. autoclass:: heniautos.equations.FestivalDOY
.. autoclass:: heniautos.equations.PrytanyDOY


.. autofunction:: heniautos.equations.festival_doy
.. autofunction:: heniautos.equations.prytany_doy
.. autofunction:: heniautos.equations.equations
.. autofunction:: heniautos.equations.collations
