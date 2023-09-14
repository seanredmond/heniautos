# Requires an environment variable EPH containing the path to an ephemeris file

.PHONY: lunar solar

bce_start := -631
bce_end := 1
ce_start := 1900
ce_end := 2151

lunar_tsv := ../heniautos/new_moons.tsv
solar_tsv := ../heniautos/solstices.tsv

lunar:
	python gen_astro_data.py $(bce_start) $(bce_end) ${EPH} -t lunar > $(lunar_tsv)
	python gen_astro_data.py $(ce_start) $(ce_end) ${EPH} -t lunar >> $(lunar_tsv)


solar:
	python gen_astro_data.py $(bce_start) $(bce_end) ${EPH} -t solar > $(solar_tsv)
	python gen_astro_data.py $(ce_start) $(ce_end) ${EPH} -t solar >> $(solar_tsv)

all: lunar solar
