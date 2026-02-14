# Release History

## 2.2.2 (2026-02-13, Gamēliṓn 26 2025/2026)

* Switch package management to uv
* Change spelling of Ποσιδεών/Posideṓn

## 2.2.1 (skipped)

## 2.2.0 (2024-09-29, Boēdromiṓn 26 2024/2025)

Apply ΔT to dates

## 2.1.0 (2024-09-27, Boēdromiṓn 24 2024/2025)

Add function to generate octaeteric calendars

## 2.0.2 (2024-09-21, Boēdromiṓn 18 2024/2025)

Make _moon_phases more generic so that it can be used to generate
dates for phases other than the new moon

## 2.0.1 (2024-02-21, Anthestēriṓn 12 2023/2024)

Added missing TSV data files and manifest

## 2.0.0 (2024-02-21, Anthestēriṓn 12 2023/2024)

Complete refactor with many, many changes

* Removed hard dependency on Skyfield (but can be optionally used)
* Changed default approximation of visible new moon. Now 1 day after conjunction rather than 2 days
* Added calendars for other poleis (Corinth, Delphi, Delos, Sparta) and generation of generic calendars based on several parameters
* Some functions moved to sub-modules
* Documentation moved to sphinx and readthedocs.io

## 1.3.0 (2021-12-03, Maimaktēriṓn 29 2021/2022)

* Add `--full-moons` option to `heniautos` command to output full moon dates

## 1.2.0 (2021-11-21, Maimaktēriṓn 17 2021/2022)

* Add option to `heniautos` command to output Julian year with
  indications of solar events and new moons

## 1.1.0 (2021-11-20, Maimaktēriṓn 16 2021/2022)

* Add options for all solar events (solstices, equinoxes) to `heniautos` command

## 1.0.0 (2021-06-15, Skirophoriṓn 5 2020/2021)

Initial release
