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
import heniautos as ha
from sys import stdout, stderr, exit

ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI",
         "XII", "XIII")


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
        return day["day"] == args.day

    return True


def doy_filter(day, doy):
    if doy:
        return day["doy"] == doy

    return True


def month_filter(month, args):
    if args.conciliar:
        if args.prytany:
            return ROMAN.index(args.prytany) + 1 == month["prytany"]

    if (not args.conciliar) and args.month:
        return ha.MONTH_ABBREVS.index(args.month) + 1 == month["constant"]

    return True


def display_month(month, args):
    if args.conciliar:
        if not args.arabic:
            return ROMAN[month-1]

    return month


def yearly_table(year, writer, args):
    writer.writerow((
        f"{arkhon_year(year[0]['days'][0]['date']):13} ",
        " I " if year[-1]["days"][-1]["doy"] > 355 else " O ",
        f" {ha.as_eet(year[0]['days'][0]['date'])} ",
        f"{sum(len(m['days']) for m in year):>5}"))


def yearly_tsv(year, writer, args):
    writer.writerow((
        arkhon_year(year[0]["days"][0]["date"]),
        "I" if year[-1]["days"][-1]["doy"] > 355 else "O",
        ha.as_eet(year[0]["days"][0]["date"]),
        sum(len(m["days"]) for m in year)))


def monthly_table(year, writer, month_key, args):
    ay = arkhon_year(year[0]["days"][0]["date"])
    for month in year:
        if month_filter(month, args):
            writer.writerow((
                f"{ay:13} ",
                f" {display_month(month[month_key], args):22}",
                f" {ha.as_eet(month['days'][0]['date'])} ",
                f"{len(month['days']):>5}"))


def monthly_tsv(year, writer, month_key, args):
    ay = arkhon_year(year[0]["days"][0]["date"])
    for month in year:
        if month_filter(month, args):
            writer.writerow((
                ay,
                display_month(month[month_key], args),
                ha.as_eet(month["days"][0]["date"]),
                len(month["days"])))


def daily_table(year, writer, month_key, args):
    ay = arkhon_year(year[0]["days"][0]["date"])
    for month in year:
        if month_filter(month, args):
            for day in month["days"]:
                if day_filter(day, args) and doy_filter(day, args.doy):
                    writer.writerow((
                        f"{ay:13} ",
                        f" {display_month(month[month_key], args):22}",
                        f"{day['day']:>4} ",
                        f" {ha.as_eet(day['date'])} ",
                        f"{day['doy']:>4}"))


def daily_tsv(year, writer, month_key, args):
    ay = arkhon_year(year[0]["days"][0]["date"])
    for month in year:
        if month_filter(month, args):
            for day in month["days"]:
                if day_filter(day, args) and doy_filter(day, args.doy):
                    writer.writerow((
                        ay,
                        display_month(month[month_key], args),
                        day["day"],
                        ha.as_eet(day["date"]),
                        day["doy"]))


def output_years(args, writer, tabs):
    if not tabs:
        m_or_p = "Prytany" if args.conciliar else "Month  "
        if args.year_summary:
            print(f"{'Year':^14}| Y |{'Start':^17}| Days")
            print("|".join(["-"*n for n in (14, 3, 17, 5)]))
        elif args.month_summary:
            print(f"{'Year':^14}|{m_or_p:^23}|{'Start':^17}| Days")
            print("|".join(["-"*n for n in (14, 23, 17, 5)]))
        else:
            print(f"{'Year':^14}|{m_or_p:^23}| Day |{'Start':^17}| DOY")
            print("|".join(["-"*n for n in (14, 23, 5, 17, 4)]))

    for year in years(args.start_year, args.end_year, args.as_ce):
        if args.conciliar:
            cal = ha.prytany_calendar(year, rule=get_rule(args.rule))
            month_key = "prytany"

        else:
            cal = ha.festival_calendar(year,
                                       abbrev=args.abbreviations,
                                       greek=args.greek_names,
                                       intercalate=ha.MONTH_ABBREVS.index(
                                           args.intercalate) + 1,
                                       rule=get_rule(args.rule))
            month_key = "month"

        if args.year_summary:
            if tabs:
                yearly_tsv(cal, writer, args)
            else:
                yearly_table(cal, writer, args)
        elif args.month_summary:
            if tabs:
                monthly_tsv(cal, writer, month_key, args)
            else:
                monthly_table(cal, writer, month_key, args)
        else:
            if tabs:
                daily_tsv(cal, writer, month_key, args)
            else:
                daily_table(cal, writer, month_key, args)


def get_writer(tabs):
    if tabs:
        return csv.writer(stdout, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)

    return csv.writer(stdout, delimiter="|", quoting=csv.QUOTE_NONE)


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
    parser.add_argument("-c", "--conciliar", action="store_true",
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
    parser.add_argument("--solstices", action="store_true",
                        help="Only list dates of solstices")
    parser.add_argument("--gmt", action="store_true",
                        help="Format times as GMT (rather than EET)")
    parser.add_argument("-r", "--rule", choices=["0", "1", "2", "d"],
                        default="2", type=str,
                        help="Rule for determining date of new moon. "
                        "0, 1, 2 days after astronomical conjunction, or "
                        "d for Dinsmoor"
                        "(default: 2)")
    parser.add_argument("-e", "--ephemeris", metavar="FILE", type=str,
                        help="Use existing ephemeris FILE (if it cannot "
                        "automatically be found)", default=None)
    parser.add_argument("--tab", action="store_true",
                        help="Output in tab-delimited format")
    parser.add_argument("--version", action="version",
                        version=f"heniautos {ha.version()}",
                        help="Print version and exit")
    args = parser.parse_args()

    ha.init_data(args.ephemeris)

    writer = get_writer(args.tab)

    if args.new_moons:
        for year in years(args.start_year, args.end_year, args.as_ce):
            for nm in ha.new_moons(year):
                if args.gmt:
                    print(ha.as_gmt(nm, True))
                else:
                    print(ha.as_eet(nm, True))
        exit()

    if args.solstices:
        for year in years(args.start_year, args.end_year, args.as_ce):
            if args.gmt:
                print(ha.as_gmt(ha.summer_solstice(year), True))
            else:
                print(ha.as_eet(ha.summer_solstice(year), True))
        exit()

    try:
        output_years(args, writer, args.tab)
    except ha.HeniautosError as e:
        print(e, file=stderr)
        exit(1)
