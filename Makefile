#
# INPUTS
#
DAILY_INFECTIONS := COVID-19_aantallen_gemeente_per_dag.csv
COVID_VARIANTS := COVID-19_varianten.csv

DAILY_INFECTIONS_URL := https://data.rivm.nl/covid-19/$(DAILY_INFECTIONS)
COVID_VARIANTS_URL := https://data.rivm.nl/covid-19/$(COVID_VARIANTS)

#
# OUTPUT
#
WEEKLY_VARIANTS := COVID-19_weektotaal_varianten.csv

.PHONY: all clean

all: $(DAILY_INFECTIONS) $(COVID_VARIANTS) $(WEEKLY_VARIANTS)

clean:
	rm -f $(DAILY_INFECTIONS) $(COVID_VARIANTS) $(WEEKLY_VARIANTS)

$(DAILY_INFECTIONS):
	wget $(DAILY_INFECTIONS_URL)

$(COVID_VARIANTS):
	wget $(COVID_VARIANTS_URL)

$(WEEKLY_VARIANTS): $(DAILY_INFECTIONS) $(COVID_VARIANTS)
	python3 scripts/weekly-variant-counts.py --daily-infections $< --variants $(word 2, $^) > $@
