#
# Configuration.
#
DAILY_INFECTIONS := COVID-19_aantallen_gemeente_per_dag.csv
COVID_VARIANTS := COVID-19_varianten.csv

DAILY_INFECTIONS_URL := https://data.rivm.nl/covid-19/$(DAILY_INFECTIONS)
COVID_VARIANTS_URL := https://data.rivm.nl/covid-19/$(COVID_VARIANTS)

.PHONY: all clean

all: $(DAILY_INFECTIONS) $(COVID_VARIANTS)

clean:
	rm $(DAILY_INFECTIONS) $(COVID_VARIANTS)

$(DAILY_INFECTIONS):
	wget $(DAILY_INFECTIONS_URL)

$(COVID_VARIANTS):
	wget $(COVID_VARIANTS_URL)
