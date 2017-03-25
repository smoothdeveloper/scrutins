#saxonb-xslt -s:maps/circonscriptions.svg -xsl:processors/circo.xsl -o:data/circo -ext:on
#saxonb-xslt -s:maps/communes.svg -xsl:processors/communes.xsl -o:data/communes -ext:on

SHELL=/bin/bash

# les fichiers et URLS dans le meme ordre
FILES = pres_2012.csv pres_2007.csv 2005.csv
URLS = \
    https://www.data.gouv.fr/s/resources/election-presidentielle-2012-resultats-par-bureaux-de-vote-1/20150925-102751/PR12_Bvot_T1T2.txt \
    https://www.data.gouv.fr/s/resources/election-presidentielle-2007-resultats-par-bureaux-de-vote/20151001-154056/PR07_Bvot_T1T2.txt \
    https://www.data.gouv.fr/s/resources/referendum-de-2005-resultats-par-bureaux-de-vote/20150925-112918/RF05_BVot.txt

RAW_FILES=$(addprefix raw/,$(FILES))
DATA_FILES=$(addprefix data/,$(FILES))

.PHONY: maps download

maps: communes.xml
	saxonb-xslt -s:maps/communes.svg -xsl:processors/non_2005.xsl -o:output/non_2005.svg -ext:on
	saxonb-xslt -s:maps/communes.svg -xsl:processors/hollande.xsl -o:output/hollande.svg -ext:on

	for f in output/*.svg; do \
		inkscape -f $$f -e "$$f.png"; \
	done

communes.xml:
	python get_election_data.py
	basex -q "let \$$file := \"communes.json\" return json-to-xml(file:read-text(\$$file))" > communes.xml

data/2005.csv: raw/2005.csv
	# les numeros de bureau de vote de Caen ont un probleme
	sed 's/Caen;\([0-9]\{2\}\);\([0-9]\);/Caen;\1\2;/' $< > $@

data/%.csv: raw/%.csv
	cp $< $@

raw/%.csv: download

download:
	mkdir -p raw
	files=( $(RAW_FILES) ); urls=( $(URLS) ); \
	for i in $${!files[@]}; do \
	curl -o $${files[$$i]} -z $${files[$$i]} $${urls[$$i]}; \
	done

clean:
	rm -rf communes.xml
	rm -f raw/*.csv
	rm -f data/*.csv
