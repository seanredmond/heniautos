# Heniautos

Naive ancient Attic calendar generator and calendar equation explorer.

## Installation

    pip install heniautos
    
## Usage

### Command Line

Generate a calendar for 416 BCE:

    heniautos 416
        
### In a Program

Generate a calendar for 416 BCE

    import heniautos as ha
    ha.athenian_festival_calendar(ha.bce_as_negative(416))

## The Basics

Heniautos (ἐνιαυτός, Greek for ”the span of a year”) generates
examples of possible Greek calendars, ancient or modern, and has
features for exploring the calendar and working with calendar
equations. It is hopefully useful for:

* Learning about and teaching the ancient Athenian and other Greek calendars
* Following along with often complex discussions of dating events in ancient Greek history
* Just having fun with questions like ”When would the City Dionysia be this year, if it was still being held.”

Heniautos also comes with a command-line application, `heniautos`, for
generating calendars without any programming required.


Read the full documentation on [Read the
Docs](https://heniautos.readthedocs.io/en/latest/)


