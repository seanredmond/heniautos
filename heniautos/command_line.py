#!/usr/bin/env python3

# heniautos. Ancient Athenian calendar generator
# Copyright (C) 2021 Sean Redmond

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import csv
from datetime import datetime
import juliandate as jd
import heniautos as ha
import heniautos.prytanies
from sys import stdout, stderr, exit

ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI",
         "XII", "XIII")

SOLAR = {ha.Seasons.SPRING_EQUINOX: "SpEq",
         ha.Seasons.SUMMER_SOLSTICE: "SuSo",
         ha.Seasons.AUTUMN_EQUINOX: "AuEq",
         ha.Seasons.WINTER_SOLSTICE: "WiSo"}


def julian_fmt(d):
    return " ".join((bce_as_bce(tuple(d.utc)[0]), d.utc_strftime("%b %d")))


def years(start, end, ce):
    """ Return a list of years from START to END inclusive."""
    if end is None:
        # Single year, return a range
        if ce:
            return range(start, start + 1)
        return range(ha.bce_as_negative(start), ha.bce_as_negative(start) + 1)
    if ce:
        if end > start:
            return range(start, end + 1)
    else:
        if end <= start:
            # multiple years, return as range
            return range(ha.bce_as_negative(start),
                         ha.bce_as_negative(end) + 1)

    raise ValueError("End year must be later than the start year")


def get_rule(r):
    if r == "0":
        return ha.Visible.CONJUNCTION

    if r == "1":
        return ha.Visible.NEXT_DAY

    if r == "d":
        return ha.Visible.DINSMOOR

    return ha.Visible.SECOND_DAY


def month_n(m, int_m, abbrev, greek=False):
    if abbrev:
        n = month_name(m, int_m, greek).split(" ")
        if len(n) > 1:
            return f"{n[0][0:3]} II"

        return n[0][0:3]

    return month_name(m, int_m, greek)


def arkhon_year(y):
    eet = ha.as_eet(y)
    epoch = eet[:3]
    year1 = int(eet[4:8])
    year2 = year1 - 1 if epoch == "BCE" else year1 + 1
    return f"{epoch} {year1}/{year2}"


def day_filter(day, args):
    if args.day:
        return day.day == args.day

    return True


def doy_filter(day, doy):
    if doy:
        return day.doy == doy

    return True


def month_filter(month, args):
    # if type(month) == ha.Prytanies and args.prytany:
    #     return ROMAN.index(args.prytany) + 1 == month

    # if type(month) == ha.Months and args.month:
    #     return ha.MONTH_ABBREVS.index(args.month) + 1 == month

    return True


def display_month(month, args):
    if type(month) is ha.prytanies.PrytanyDay:
        if not args.arabic:
            return ROMAN[month.prytany-1]

    return month.month_name


def yearly_table(year, writer, args):
    writer.writerow((
        f"{arkhon_year(year[0].jdn):13} ",
        " I " if len(year) > 355 else " O ",
        f" {ha.as_eet(year[0].jdn)} ",
        f"{len(year):>5}"))


def yearly_tsv(year, writer, args):
    writer.writerow((
        arkhon_year(year[0].jdn),
        "I" if len(year) > 355 else "O",
        ha.as_eet(year[0].jdn),
        len(year)))


def monthly_table(year, writer, args):
    ay = arkhon_year(year[0][0].jdn)
    for month in year:
        writer.writerow((
            f"{ay:13} ",
            f" {display_month(month[0], args):22}",
            f" {ha.as_eet(month[0].jdn)} ",
            f"{len(month):>5}"))


def monthly_tsv(year, writer, args):
    ay = arkhon_year(year[0][0].jdn)
    for month in year:
        writer.writerow((
            ay,
            display_month(month[0], args),
            ha.as_eet(month[0].jdn),
            len(month)))


def daily_table(year, writer, args):
    ay = arkhon_year(year[0].jdn)
    for day in year:
        writer.writerow((
            f"{ay:13} ",
            f" {display_month(day, args):22}",
            f"{day.day:>4} ",
            f" {ha.as_eet(day.jdn)} ",
            f"{day.doy:>4}"))


def daily_tsv(year, writer, args):
    ay = arkhon_year(year[0].jdn)
    for day in year:
        writer.writerow((
            ay,
            display_month(day, args),
            day.day,
            ha.as_eet(day.jdn),
            day.doy))


def festival_filters(cal, args):
    """Apply festival filters."""
    return [d for d in cal if month_filter(d.month, args) and day_filter(d, args) and doy_filter(d, args.doy)]


def prytany_filters(cal, args):
    """Apply prytany filters."""
    return [d for d in cal if month_filter(d.prytany, args) and day_filter(d, args) and doy_filter(d, args.doy)]


def get_calendar(cal):
    if cal == "athenian":
        return ha.Cal.ATHENIAN

    if cal == "corinthian":
        return ha.Cal.CORINTHIAN

    if cal == "delian":
        return ha.Cal.DELIAN

    if cal == "delphian":
        return ha.Cal.DELPHIAN
    

    if cal == "spartan":
        return ha.Cal.SPARTAN

    return None


def get_solar_event(cal):
    if cal in ("athenian", "delphian"):
        return ha.Seasons.SUMMER_SOLSTICE

    if cal in ("corinthian", "spartan"):
        return ha.Seasons.AUTUMN_EQUINOX

    if cal == "delian":
        return ha.Seasons.WINTER_SOLSTICE


def needs_before(cal):
    if cal in ("corinthian", "spartan"):
        return True

    return False


def filtered_festival_calendar(year, args, astro_data):
    """Filter festival calendar to requested scope."""
    return festival_filters(
        ha.festival_calendar(year,
                             #abbrev=args.abbreviations,
                             #greek=args.greek_names,
                             calendar=get_calendar(args.calendar),
                             event=get_solar_event(args.calendar),
                             before_event=needs_before(args.calendar),
                             intercalate=6,
                             rule=get_rule(args.rule),
                             data=astro_data()
                             ),
        args)
        

def filtered_prytany_calendar(year, args, astro_data):
    """Filter prytany calendar to requested scope."""
    return prytany_filters(
        ha.prytany_calendar(year, rule=get_rule(args.rule), data=astro_data())
        , args)


def filtered_calendar(year, args, astro_data):
    """Return a calendar with requested filters."""
    if args.conciliar:
        return filtered_prytany_calendar(year, args, astro_data)

    return filtered_festival_calendar(year, args, astro_data)         


def by_group(year):
    """Group by months or prytanies depending on type of calendar."""
    if type(year[0]) is ha.prytanies.PrytanyDay:
        return ha.by_prytanies(year)

    return ha.by_months(year)


def output_years(args, writer, tabs, astro_data):
    if not tabs:
        m_or_p = "Prytany" if args.conciliar else "Month  "
        if args.year_summary:
            output_header(("Year", "Y", "Start", "Days"), (14, 3, 17, 6),
                          writer)
        elif args.month_summary:
            output_header(("Year", m_or_p, "Start", "Days"), (14, 23, 17, 6),
                          writer)
        else:
            output_header(("Year", m_or_p, "Day", "Start", "DOY"),
                          (14, 23, 5, 17, 5),
                          writer)

    for year in years(args.start_year, args.end_year, args.as_ce):
        cal = filtered_calendar(year, args, astro_data)

        if args.year_summary:
            if tabs:
                yearly_tsv(cal, writer, args)
            else:
                yearly_table(cal, writer, args)
        elif args.month_summary:
            if tabs:
                monthly_tsv(by_group(cal), writer, args)
            else:
                monthly_table(by_group(cal), writer, args)
        else:
            if tabs:
                daily_tsv(cal, writer, args)
            else:
                daily_table(cal, writer, args)


def get_julian_half_year(year1, year2):
    """ Get the days of (Attic) year1 that are in (Julian) year2. """
    return [d["date"] for d in [a for b in [m for m in [y["days"] for y in ha.festival_calendar(year1)]] for a in b] if d["date"].ut1_calendar()[0] == year2]


def get_julian_year(year):
    """ Combine two parts of Julian year that span Attic year. """
    jan1 = int(jd.from_julian(year, 1, 1) + 0.5)
    dec31 = int(jd.from_julian(year, 12, 31) + 0.5)
    return range(jan1, dec31+1)
    # print(jan1)
    # print(dec31)
    # return get_julian_half_year(year - 1, year) + \
    #     get_julian_half_year(year, year)
    

def is_solar(with_solar, day, solar):
    if not with_solar:
        return tuple()

    event = tuple([s[1] for s in solar if s[0] == ha.as_eet(day)])

    if event:
        return event

    return ("",)


def solar_events(year, with_solar):
    if with_solar:
        return [(ha.to_jdn(ha.solar_event(year, s)), SOLAR[s]) for s in ha.Seasons]

    return []


def is_lunar(with_nm, day, lunar):
    if not with_nm:
        return tuple()

    event = tuple([s[1] for s in lunar if s[0] == ha.as_eet(day)])

    if event:
        return event

    return ("",)

def is_astro_event(with_event, day, events):
    if not with_event:
        return tuple()

    event = tuple([e[1] for e in events if e[0] == day])

    if event:
        return event

    return ("",)


def lunar_events(year, with_nm):
    if with_nm:
        return [(ha.to_jdn(d), "NM") for d in ha.new_moons(year)]

    return []


def output_julian(start_y, end_y, with_solar, with_nm, as_ce, tabs, writer):
    for year in years(start_y, end_y, as_ce):
        solar = dict(solar_events(year, with_solar))
        lunar = dict(lunar_events(year, with_nm))
        for day in get_julian_year(year):
            row = (day, ha.as_gmt(day), solar.get(day, ""), lunar.get(day, ""))
            
            writer.writerow(row)


def zz_output_julian(start_y, end_y, with_solar, with_nm, as_ce, tabs, writer):
    row_w = [16]  + \
        ([7] if with_solar else []) + \
        ([7] if with_nm else [])

    cent_j = ["^"] * len(row_w)

    if not tabs:
        header = ["Date"] + \
            (["Solar"] if with_solar else []) + \
            (["Lunar"] if with_nm else [])

        writer.writerow([pad_cell(*h) for h in zip(header, cent_j, row_w)])
        writer.writerow(["-" * w for w in row_w])

    for year in years(start_y, end_y, as_ce):
        solar = solar_events(year, with_solar)
        lunar = lunar_events(year, with_nm)
        for x in get_julian_year(year):
            row = (x, ha.as_eet(x),) + \
                is_astro_event(with_solar, x, solar) + \
                is_astro_event(with_nm, x, lunar)

            if not tabs:
                writer.writerow(pad_cell(*r) for r in zip(row, cent_j, row_w))
            else:
                writer.writerow(row)
            

def pad_cell(c, j, w):
    return f"{{:{j}{w}}}".format(c)


def output_header(headers, widths, writer):
    writer.writerow([pad_cell(c, "^", w) for (c, w) in zip(headers, widths)])
    writer.writerow(["-" * w for w in widths])


def get_writer(tabs):
    if tabs:
        return csv.writer(stdout, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)

    return csv.writer(stdout, delimiter="|", quoting=csv.QUOTE_NONE)


def maybe_load_from_ephemeris(args):
    """Return a function to be used to load astronomical data."""
    if args.use_ephemeris:
        import heniautos.ephemeris as heph

        eph_cfg = heph.init_ephemeris(eph=args.ephemeris) if args.ephemeris else heph.init_ephemeris()
        cal_years = list(years(args.start_year, args.end_year, args.as_ce))

        return lambda: heph.get_ephemeris_data(cal_years[0], cal_years[-1], eph_cfg)

    
    return ha.load_data


def main():
    parser = argparse.ArgumentParser(
        description="Ancient Athenian calendar generator",
        epilog="""
heniautos  Copyright (C) 2021  Sean Redmond
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions."""
    )
    parser.add_argument("start_year", type=int)
    parser.add_argument("end_year", type=int, nargs='?', default=None)
    parser.add_argument("-c", "--calendar",
                        choices=("athenian", "delian", "delphian", "spartan", "corinthian", "none"),
                        default="athenian",
                        help="Festival calendar to display"),
    parser.add_argument("--month", choices=ha.MONTH_ABBREVS, type=str,
                        help="Only show selected month")
    parser.add_argument("--day", type=int,
                        help="Only show selected day")
    parser.add_argument("--doy", type=int,
                        help="Only show selected day of year")
    parser.add_argument("-m", "--month-summary", action="store_true")
    parser.add_argument("-y", "--year-summary", action="store_true")
    parser.add_argument("--intercalate", choices=ha.MONTH_ABBREVS,
                        type=str, default="Pos",
                        help="Month after which to intercalate")
    parser.add_argument("-b", "--conciliar", action="store_true",
                        help="Output conciliar calendar (prytanies)")
    parser.add_argument("--arabic", action="store_true",
                        help="Display prytany numbers as Arabic rather than "
                        "Roman numerals")
    parser.add_argument("--prytany", choices=ROMAN, type=str,
                        help="Only show selected prytany")
    parser.add_argument("--as-ce", action="store_true",
                        help="Treat dates as CE rather than BCE")
    parser.add_argument("-a", "--abbreviations", action="store_true",
                        help="Abbreviate month names")
    parser.add_argument("-g", "--greek-names", action="store_true",
                        help="Use Greek names for months")
    parser.add_argument("--new-moons", action="store_true",
                        help="Only list times of astronomical new moons")
    parser.add_argument("--full-moons", action="store_true",
                        help="Only list times of astronomical full moons")
    parser.add_argument("--summer-solstice", action="store_true",
                        help="Only list dates of solstices")
    parser.add_argument("--spring-equinox", action="store_true",
                        help="Only list dates of spring equinox")
    parser.add_argument("--autumn-equinox", action="store_true",
                        help="Only list dates of autumn equinox")
    parser.add_argument("--winter-solstice", action="store_true",
                        help="Only list dates of winter solstice")
    parser.add_argument("--gmt", action="store_true",
                        help="Format times as GMT (rather than EET)")
    parser.add_argument("-r", "--rule", choices=["0", "1", "2", "d"],
                        default="2", type=str,
                        help="Rule for determining date of new moon. "
                        "0, 1, 2 days after astronomical conjunction, or "
                        "d for Dinsmoor"
                        "(default: 2)")
    parser.add_argument("-E", "--use-ephemeris", action="store_true",
                        help="Use ephemeris for data")
    parser.add_argument("-e", "--ephemeris", metavar="FILE", type=str,
                        help="Use existing ephemeris FILE (if it cannot "
                        "automatically be found)", default=None)
    parser.add_argument("--julian", action="store_true",
                        help="Just output Julian calendar dates"),
    parser.add_argument("--julian-solar-events", action="store_true",
                        help="Include solstices and equinoxes in Julian "
                        "calendar output"),
    parser.add_argument("--julian-new-moons", action="store_true",
                        help="Include new moons in Julian calendar output"),
    parser.add_argument("--tab", action="store_true",
                        help="Output in tab-delimited format")
    parser.add_argument("--version", action="version",
                        version=f"heniautos {ha.version()}",
                        help="Print version and exit")
    args = parser.parse_args()

    astro_data = maybe_load_from_ephemeris(args)

    writer = get_writer(args.tab)

    try:
        if args.new_moons:
            for year in years(args.start_year, args.end_year, args.as_ce):
                for nm in ha.new_moons(year, data=astro_data()):
                    if args.gmt:
                        print(ha.as_gmt(nm, True))
                    else:
                        print(ha.as_eet(nm, True))
            exit()

        if args.full_moons:
            for year in years(args.start_year, args.end_year, args.as_ce):
                for nm in ha.moon_phases(year, ha.Phases.FULL, data=astro_data()):
                    if args.gmt:
                        print(ha.as_gmt(nm, True))
                    else:
                        print(ha.as_eet(nm, True))
            exit()

        # Check for one of the solar events (and take the first one)
        solar = next((s for s in zip((args.spring_equinox, args.summer_solstice, args.autumn_equinox, args.winter_solstice), ha.Seasons) if s[0]), None)

        if solar is not None:
            for year in years(args.start_year, args.end_year, args.as_ce):
                if args.gmt:
                    print(ha.as_gmt(
                        ha.solar_event(year, solar[1], data=astro_data()),
                        True))
                else:
                    print(ha.as_eet(
                        ha.solar_event(year, solar[1], data=astro_data()),
                        True))
            exit()
            

        if args.julian:
            output_julian(args.start_year, args.end_year,
                          args.julian_solar_events, args.julian_new_moons,
                          args.as_ce, args.tab, writer)

            exit()
        
        output_years(args, writer, args.tab, astro_data)

    except ha.HeniautosError as e:
        print(e, file=stderr)
        exit(1)
