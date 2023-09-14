#!/usr/bin/env python3

import argparse
import csv
import heniautos as ha
import heniautos.ephemeris as heph
import sys


def data_key(t):
    if t == "solar":
        return "solstices"

    if t == "lunar":
        return "new_moons"

    # Just in case--argparse should enforce this validity. Neither of
    # the above options is a good default, though
    raise ValueError(f"Invalid value for data type: {t}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="gen_astro_data.py",
        description="Generate heniautos TSV data files",
    )
    parser.add_argument("start", help="First year for generated data", type=int)
    parser.add_argument("end", help="Last year for generated data", type=int)
    parser.add_argument("ephemeris", help="path to ephemeris file", type=str)
    parser.add_argument(
        "-t",
        "--type",
        choices=("solar", "lunar"),
        help="Kind of data to export",
        required="true",
    )

    args = parser.parse_args()

    e = heph.init_ephemeris(eph=args.ephemeris)
    data = heph.get_ephemeris_data(args.start, args.end, e)

    writer = csv.writer(sys.stdout, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)
    for d in data[data_key(args.type)]:
        writer.writerow(d)
