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

ROMAN = (
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
    "XIII",
)

SOLAR = {
    ha.Seasons.SPRING_EQUINOX: "SpEq",
    ha.Seasons.SUMMER_SOLSTICE: "SuSo",
    ha.Seasons.AUTUMN_EQUINOX: "AuEq",
    ha.Seasons.WINTER_SOLSTICE: "WiSo",
}


def adj_time(args):
    """Return tz keyword parameter if requested"""
    if args.alt:
        return {"tz": ha.TZOptions.ALT}

    if args.longitude:
        return {"tz": args.longitude}

    return {}


def julian_fmt(d):
    return " ".join((bce_as_bce(tuple(d.utc)[0]), d.utc_strftime("%b %d")))


def years(start, end, ce):
    """Return a list of years from START to END inclusive."""
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
            return range(ha.bce_as_negative(start), ha.bce_as_negative(end) + 1)

    raise ValueError("End year must be later than the start year")


def month_n(m, int_m, abbrev, greek=False):
    if abbrev:
        n = month_name(m, int_m, greek).split(" ")
        if len(n) > 1:
            return f"{n[0][0:3]} II"

        return n[0][0:3]

    return month_name(m, int_m, greek)


def display_month(month, args):
    if type(month) is ha.PrytanyDay:
        if not args.arabic:
            return ROMAN[month.prytany - 1]

    return month.month_name


def yearly_table(year, writer, args):
    writer.writerow(
        (
            f"{year[0].year:13} ",
            " I " if len(year) > 355 else " O ",
            f" {ha.as_julian(year[0].jdn)} ",
            f"{len(year):>5}",
        )
    )


def yearly_tsv(year, writer, args):
    writer.writerow(
        (
            year[0].year,
            "I" if len(year) > 355 else "O",
            ha.as_julian(year[0].jdn),
            len(year),
        )
    )


def monthly_table(year, writer, args):
    for month in year:
        writer.writerow(
            (
                f"{month[0].year:13} ",
                f" {display_month(month[0], args):22}",
                f" {ha.as_julian(month[0].jdn)} ",
                f"{len(month):>5}",
            )
        )


def monthly_tsv(year, writer, args):
    for month in year:
        writer.writerow(
            (
                month[0].year,
                display_month(month[0], args),
                ha.as_julian(month[0].jdn),
                len(month),
            )
        )


def daily_table(year, writer, args):
    for day in year:
        writer.writerow(
            (
                f"{day.year:13} ",
                f" {display_month(day, args):22}",
                f"{day.day:>4} ",
                f" {ha.as_julian(day.jdn)} ",
                f"{day.doy:>4}",
            )
        )


def daily_tsv(year, writer, args):
    for day in year:
        writer.writerow(
            (
                day.year,
                display_month(day, args),
                day.day,
                ha.as_julian(day.jdn),
                day.doy,
            )
        )


def get_solar_event(start):
    if start == "fall":
        return {"event": ha.Seasons.AUTUMN_EQUINOX}

    if start == "winter":
        return {"event": ha.Seasons.WINTER_SOLSTICE}

    if start == "spring":
        return {"event": ha.Seasons.SPRING_EQUINOX}

    if start == "summer":
        return {"event": ha.Seasons.SUMMER_SOLSTICE}

    return {}


def needs_before(before, after):
    if before:
        return {"before_event": True}

    if after:
        return {"before_event": False}

    return {}


def name_as(abbrev, greek):
    if greek:
        return {"name_as": ha.MonthNameOptions.GREEK}

    if abbrev:
        return {"name_as": ha.MonthNameOptions.ABBREV}

    return {}  # ha.MonthNameOptions.TRANSLITERATION


def festival_func(cal):
    if cal == "argos":
        return ha.argive_festival_calendar

    if cal == "corinth":
        return ha.corinthian_festival_calendar

    if cal == "delos":
        return ha.delian_festival_calendar

    if cal == "delphi":
        return ha.delphian_festival_calendar

    if cal == "sparta":
        return ha.spartan_festival_calendar

    if cal == "macedon":
        return ha.macedonian_festival_calendar

    if cal == "generic":
        return ha.festival_calendar

    return ha.athenian_festival_calendar


def one_kwarg(args, argk, argn=None):
    if vars(args).get(argk, None) is not None:
        if argn is not None:
            return {argn: vars(args).get(argk, None)}

        return {argk: vars(args).get(argk, None)}

    return {}


def cal_kwargs(args, astro_data):
    return {
        **name_as(args.abbreviations, args.greek_names),
        **get_solar_event(args.calendar_start),
        **needs_before(args.before_solar_event, args.after_solar_event),
        **one_kwarg(args, "intercalate"),
        **one_kwarg(args, "visibility_offset", "v_off"),
        **one_kwarg(args, "solar_offset", "s_off"),
        **{"data": astro_data()},
    }

    raise ValueError()


def festival_calendar(year, args, astro_data):
    """Filter festival calendar to requested scope."""

    return festival_func(args.calendar)(year, **cal_kwargs(args, astro_data))


def prytany_calendar(year, args, astro_data):
    """Filter prytany calendar to requested scope."""
    return ha.prytanies.prytany_calendar(
        year, v_off=args.visibility_offset,
        pryt_start=args.quasi_solar_start, data=astro_data()
    )


def selected_calendar(year, args, astro_data):
    """Return a calendar with requested filters."""
    if args.conciliar:
        return prytany_calendar(year, args, astro_data)

    return festival_calendar(year, args, astro_data)


def by_group(year):
    """Group by months or prytanies depending on type of calendar."""
    if type(year[0]) is ha.PrytanyDay:
        return ha.prytanies.by_prytanies(year)

    return ha.by_months(year)


def output_years(args, writer, tabs, astro_data):
    if not tabs:
        m_or_p = "Prytany" if args.conciliar else "Month  "
        if args.year_summary:
            output_header(("Year", "Y", "Start", "Days"), (14, 3, 17, 6), writer)
        elif args.month_summary:
            output_header(("Year", m_or_p, "Start", "Days"), (14, 23, 17, 6), writer)
        else:
            output_header(
                ("Year", m_or_p, "Day", "Start", "DOY"), (14, 23, 5, 17, 5), writer
            )

    for year in years(args.start_year, args.end_year, args.as_ce):
        cal = selected_calendar(year, args, astro_data)

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
    """Get the days of (Attic) year1 that are in (Julian) year2."""
    return [
        d["date"]
        for d in [
            a
            for b in [m for m in [y["days"] for y in ha.festival_calendar(year1)]]
            for a in b
        ]
        if d["date"].ut1_calendar()[0] == year2
    ]


def get_julian_year(year):
    """Combine two parts of Julian year that span Attic year."""
    jan1 = int(jd.from_julian(year, 1, 1) + 0.5)
    dec31 = int(jd.from_julian(year, 12, 31) + 0.5)
    return range(jan1, dec31 + 1)


def is_solar(with_solar, day, solar):
    if not with_solar:
        return tuple()

    event = tuple([s[1] for s in solar if s[0] == ha.as_julian(day)])

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

    event = tuple([s[1] for s in lunar if s[0] == ha.as_julian(day)])

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
            row = (
                (day, ha.as_julian(day))
                + ((solar.get(day, ""),) if with_solar else ())
                + ((lunar.get(day, ""),) if with_nm else ())
            )

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

        eph_cfg = (
            heph.init_ephemeris(eph=args.ephemeris)
            if args.ephemeris
            else heph.init_ephemeris()
        )
        cal_years = list(
            years(
                args.start_year - 2,
                args.end_year + 2 if args.end_year else args.start_year + 2,
                args.as_ce,
            )
        )

        return lambda: heph.get_ephemeris_data(cal_years[0], cal_years[-1], eph_cfg)

    return ha.load_data


def main():
    parser = argparse.ArgumentParser(
        description="Ancient Athenian calendar generator",
        epilog="""
heniautos  Copyright (C) 2021  Sean Redmond
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.""",
    )
    parser.add_argument("start_year", type=int)
    parser.add_argument("end_year", type=int, nargs="?", default=None)
    parser.add_argument(
        "-c",
        "--calendar",
        choices=(
            "argos",
            "athens",
            "corinth",
            "delos",
            "delphi",
            "macedon",
            "sparta",
            "generic",
        ),
        default="athens",
        help="Festival calendar to display",
    ),
    parser.add_argument("-m", "--month-summary", action="store_true")
    parser.add_argument("-y", "--year-summary", action="store_true")
    parser.add_argument(
        "--intercalate",
        choices=tuple(range(1, 13)),
        type=int,
        help="Month after which to intercalate",
    )
    parser.add_argument(
        "-C",
        "--conciliar",
        action="store_true",
        help="Output conciliar calendar (prytanies)",
    )
    parser.add_argument(
        "--arabic",
        action="store_true",
        help="Display prytany numbers as Arabic rather than " "Roman numerals",
    )
    parser.add_argument(
        "--prytany", choices=ROMAN, type=str, help="Only show selected prytany"
    )
    parser.add_argument(
        "--as-ce", action="store_true", help="Treat dates as CE rather than BCE"
    )
    parser.add_argument(
        "-a", "--abbreviations", action="store_true", help="Abbreviate month names"
    )
    parser.add_argument(
        "-g", "--greek-names", action="store_true", help="Use Greek names for months"
    )
    parser.add_argument(
        "--new-moons",
        action="store_true",
        help="Only list times of astronomical new moons",
    )
    parser.add_argument(
        "--summer-solstice", action="store_true", help="Only list dates of solstices"
    )
    parser.add_argument(
        "--spring-equinox",
        action="store_true",
        help="Only list dates of spring equinox",
    )
    parser.add_argument(
        "--autumn-equinox",
        action="store_true",
        help="Only list dates of autumn equinox",
    )
    parser.add_argument(
        "--winter-solstice",
        action="store_true",
        help="Only list dates of winter solstice",
    )
    parser.add_argument(
        "--athens-local-time",
        dest="alt",
        action="store_true",
        help="Show times in Athens Local Time (adjusted for Athens' longitude rather than GMT)",
    )
    parser.add_argument(
        "--longitude",
        type=float,
        help="Adjust new moon and solstice times for longitude (use --athens-local-time for Athens)",
    )
    parser.add_argument(
        "--as-jdn",
        action="store_true",
        help="Show new moon and solstice times as JDN"
    )
    parser.add_argument(
        "-v",
        "--visibility-offset",
        type=int,
        metavar="N",
        default=1,
        help="Offset for determining date of new moon."
        " N days after astronomical conjunction"
        "(default: 1)",
    )
    parser.add_argument(
        "-s",
        "--solar-offset",
        metavar="N",
        type=int,
        default=0,
        help="Offset for determining the date of solstices " "and equinoxes",
    )
    parser.add_argument(
        "--calendar-start",
        choices=("summer", "fall", "winter", "spring"),
        type=str,
        help="Season for beginning of the year (with -c generic, default: summer)",
    )
    parser.add_argument(
        "--before-solar-event",
        action="store_true",
        help="Calendar begins before --calendar-start (with -c generic)",
    )
    parser.add_argument(
        "--after-solar-event",
        action="store_true",
        help="Calendar begins after --calendar-start (with -c generic)",
    )
    parser.add_argument(
        "--quasi-solar-start",
        type=int,
        default=heniautos.prytanies.Prytany.AUTO,
        help="JDN for any Prytany 1.1 for quasi-solar prytanies"
    )
    parser.add_argument(
        "-E", "--use-ephemeris", action="store_true", help="Use ephemeris for data"
    )
    parser.add_argument(
        "-e",
        "--ephemeris",
        metavar="FILE",
        type=str,
        help="Use existing ephemeris FILE (if it cannot " "automatically be found)",
        default=None,
    )
    parser.add_argument(
        "--julian", action="store_true", help="Just output Julian calendar dates"
    ),
    parser.add_argument(
        "--julian-solar-events",
        action="store_true",
        help="Include solstices and equinoxes in Julian " "calendar output",
    ),
    parser.add_argument(
        "--julian-new-moons",
        action="store_true",
        help="Include new moons in Julian calendar output",
    ),
    parser.add_argument(
        "--tab", action="store_true", help="Output in tab-delimited format"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"heniautos {ha.version()}",
        help="Print version and exit",
    )
    args = parser.parse_args()

    astro_data = maybe_load_from_ephemeris(args)

    writer = get_writer(args.tab)

    try:
        if args.new_moons:
            for year in years(args.start_year, args.end_year, args.as_ce):
                for nm in ha.new_moons(year, data=astro_data()):
                    if args.as_jdn:
                        print(f"{ha.tz_offset(nm, **adj_time(args)):0.10f}")
                    else:
                        print(ha.as_julian(nm, True, **adj_time(args)))

            exit()

        # Check for one of the solar events (and take the first one)
        solar = next(
            (
                s
                for s in zip(
                    (
                        args.spring_equinox,
                        args.summer_solstice,
                        args.autumn_equinox,
                        args.winter_solstice,
                    ),
                    ha.Seasons,
                )
                if s[0]
            ),
            None,
        )

        if solar is not None:
            for year in years(args.start_year, args.end_year, args.as_ce):
                if args.as_jdn:
                    print(f"{ha.tz_offset(ha.solar_event(year, solar[1], data=astro_data()), **adj_time(args)):0.10f}")
                else:
                    print(
                        ha.as_julian(
                            ha.solar_event(year, solar[1], data=astro_data()),
                            True,
                            **adj_time(args),
                        )
                    )

                exit()

        if args.julian:
            output_julian(
                args.start_year,
                args.end_year,
                args.julian_solar_events,
                args.julian_new_moons,
                args.as_ce,
                args.tab,
                writer,
            )

            exit()

        output_years(args, writer, args.tab, astro_data)

    except ha.HeniautosError as e:
        print(e, file=stderr)
        exit(1)
