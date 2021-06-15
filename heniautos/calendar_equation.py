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
from itertools import product
import sys


# Conversions for argument parameters to Months constants
CMD_MONTHS = {"hek": ha.Months.HEK,
              "met": ha.Months.MET,
              "boe": ha.Months.BOE,
              "pua": ha.Months.PUA,
              "mai": ha.Months.MAI,
              "pos": ha.Months.POS,
              "gam": ha.Months.GAM,
              "ant": ha.Months.ANT,
              "ela": ha.Months.ELA,
              "mou": ha.Months.MOU,
              "tha": ha.Months.THA,
              "ski": ha.Months.SKI}

# Conversions for argument parameters to Prytanies constants
CMD_PRYT = {"i": ha.Prytanies.I,
            "ii": ha.Prytanies.II,
            "iii": ha.Prytanies.III,
            "iv": ha.Prytanies.IV,
            "v": ha.Prytanies.V,
            "vi": ha.Prytanies.VI,
            "vii": ha.Prytanies.VII,
            "viii": ha.Prytanies.VIII,
            "ix": ha.Prytanies.IX,
            "x": ha.Prytanies.X,
            "xi": ha.Prytanies.XI,
            "xii": ha.Prytanies.XII,
            "xiii": ha.Prytanies.XIII}


def abbrev_from_constant(val, dct):
    return [k for k, v in dct.items() if v == val][0]


def month_abbrev_from_constant(m):
    return abbrev_from_constant(m, CMD_MONTHS).title()


def prytany_abbrev_from_constant(p):
    return abbrev_from_constant(p, CMD_PRYT).upper()


def prytany_pattern(p, ph_cnt):
    if len(p) == 0:
        return "∅"

    if ph_cnt == 10:
        return "".join(["L" if d in (36, 39) else "S" for d in p])

    if ph_cnt == 12:
        return "".join(["L" if d in (30, 32) else "S" for d in p])

    return "".join(["L" if d in (28, 20) else "S" for d in p])


def festival_pattern(f):
    if len(f) == 0:
        return "∅"

    return "".join(["F" if d == 30 else "H" for d in f])


def eq_fmt(fest, pryt, ph_cnt):
    m = month_abbrev_from_constant(fest["date"][0])
    m_day = fest["date"][1]

    p = prytany_abbrev_from_constant(pryt["date"][0])
    p_day = pryt["date"][1]

    m_index = len(fest["preceding"]) + 1

    m_int = "+" if fest["intercalation"] else "-"

    p_int = "(I)" if pryt["intercalation"] else "(O)"

    doy = fest["doy"]

    fest_p = "".join(["F" if d == 30 else "H" for d in fest["preceding"]])
    pryt_p = prytany_pattern(pryt["preceding"], ph_cnt)

    patterns = f"[{fest_p}, {pryt_p}]"

    return (f"{m} {m_day:>2} ({m_index:>2}{m_int}) = "
            f"{p:>4} {p_day:>2} = "
            f" DOY {doy:>3} {p_int} {patterns}")


def output_solution(fest, pryt, pryt_type, year, i, cnt, ordinary,
                    intercalary):
    solutions = [e for e
                 in ha.equations(fest, pryt, pryt_type=pryt_type, year=year)
                 if year_type(e, ordinary, intercalary)]

    if len(solutions) == 0:
        print(f"No solutions for {fest} = {pryt}")
        return

    for f, p in solutions:
        print(eq_fmt(f, p, phulai_count(pryt_type, year)))


def phulai_count(pryt_type, year):
    """Return the number of phulai."""
    if year is not None:
        return ha.phulai_count(year)

    if pryt_type == ha.Prytany.ALIGNED_13:
        return 13

    if pryt_type == ha.Prytany.ALIGNED_12:
        return 12

    return 10


def year_type(p, ordinary, intercalary):
    """Test whether type of year is requested type."""
    if ordinary and intercalary:
        return True

    if ordinary:
        return p[1]["intercalation"] is False

    return p[1]["intercalation"] is True


def coll_fmt2(fest, pryt):
    m = month_abbrev_from_constant(fest["date"][0])
    m_day = fest["date"][1]

    p = prytany_abbrev_from_constant(pryt["date"][0])
    p_day = pryt["date"][1]

    doy = fest["doy"]

    return f"{m} {m_day} = {p} {p_day} = {doy}"


def coll_fmt(eq):
    return " + ".join([f"{coll_fmt2(f, p)}" for f, p in eq])


def output_collations(collations, pryt_type, year):
    for i, c in enumerate(collations, 1):
        print(f"{i:>3}:", " ".join([festival_pattern(pat)
                                    for pat in c["partitions"]["festival"]]),
              " ",
              " ".join([prytany_pattern(pat, phulai_count(pryt_type, year))
                        for pat in c["partitions"]["conciliar"]]))

    for i, c in enumerate(collations, 1):
        print(f"{i:>3}:", coll_fmt(c["equations"]))


def cmd_parse_month_or_prytany(month, abbrevs):
    if month.lower() == "any":
        return tuple(abbrevs.values())

    return (abbrevs[month.lower()], )


def cmd_parse_prytany_range(pryt_type, year):
    ph_cnt = phulai_count(pryt_type, year)

    if ph_cnt == 10:
        return range(1, 40)

    if ph_cnt == 12:
        return range(1, 33)

    return range(1, 31)


def cmd_parse_days(day, is_festival, pryt_type, year):
    if day == "any":
        if is_festival:
            return range(1, 31)

        return cmd_parse_prytany_range(pryt_type, year)

    if day == "last":
        if is_festival:
            return (29, 30)

        print("'last' is not a valid value for prytany days", file=sys.stderr)
        sys.exit(-1)

    if "/" in day:
        return tuple([int(d) for d in day.split("/")])

    return (int(day), )


def cmd_parse_abbrevs(month, day, abbrevs, pryt_type=None, year=None):
    try:

        months = cmd_parse_month_or_prytany(month, abbrevs)
        days = cmd_parse_days(day, abbrevs == CMD_MONTHS, pryt_type, year)

        return tuple(product(months, days))
    except KeyError as e:
        if month.lower() in e.__str__():
            print(f"Invalid month or prytany: {month}", file=sys.stderr)
            sys.exit(-1)
        raise e
    except ValueError as e:
        if "invalid literal" in e.__str__():
            print(f"Invalid day '{day}' could not be converted "
                  "to an integer", file=sys.stderr)
            sys.exit(-1)
        raise e


def cmd_parse_festival(month, day):
    return cmd_parse_abbrevs(month, day, CMD_MONTHS)


def cmd_parse_conciliar(prytany, day, pryt_type, year):
    return cmd_parse_abbrevs(prytany, day, CMD_PRYT, pryt_type, year)


def cmd_parse_equations(equation, pryt_type, year):
    try:
        fest = cmd_parse_festival(*equation[:2])
        conc = cmd_parse_conciliar(*equation[2:], pryt_type, year)

        return (fest, conc)
    except TypeError as e:
        print(f"Error parsing equation: '{' '.join(equation)}'",
              file=sys.stderr)

        if "required positional" in e.__str__():
            print("Four elements required: month, month day, "
                  "prytany, prytany day", file=sys.stderr)

        sys.exit(-1)


def prytany_type_year(pryt_cnt, year):
    if year is not None:
        return (ha.Prytany.AUTO, ha.bce_as_negative(year))

    if pryt_cnt == 10:
        return (ha.Prytany.ALIGNED_10, None)

    if pryt_cnt == 12:
        return (ha.Prytany.ALIGNED_12, None)

    return (ha.Prytany.ALIGNED_13, None)


def main():
    parser = argparse.ArgumentParser(
        description="Athenian calendar calendar equation solver",
        epilog="""
heniautos  Copyright (C) 2021  Sean Redmond
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.""")
    parser.add_argument("-e", "--equation", type=str, nargs='+',
                        action="append", required=True)
    parser.add_argument("-c", "--collate", action="store_true")
    parser.add_argument("-p", "--prytanies", type=int, default=10,
                        help="Number of prytanies in equation(s)")
    parser.add_argument("-y", "--year", type=int,
                        help="Year of equation(s). Overrides -p and is only"
                        "used to determine the number of prytanies.")
    parser.add_argument("--ordinary", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="Show solutions for ordinary years")
    parser.add_argument("--intercalary", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="Show solutions for intercalary years")
    parser.add_argument("--version", action="version",
                        version=f"heniautos {ha.version()}",
                        help="Print version and exit")
    args = parser.parse_args()

    pryt_type, year = prytany_type_year(args.prytanies, args.year)

    equations = [cmd_parse_equations(e, pryt_type, year)
                 for e in args.equation]

    [output_solution(fest, pryt, pryt_type, year, i, len(args.equation),
                     args.ordinary, args.intercalary)
     for i, (fest, pryt) in enumerate(equations, 1)]

    if args.collate:
        output_collations(
            ha.collations(
                *[ha.equations(fest, pryt, pryt_type=pryt_type, year=year)
                  for fest, pryt in equations]),
            pryt_type, year)


if __name__ == "__main__":
    main()
