#saxonb-xslt -s:maps/circonscriptions.svg -xsl:processors/circo.xsl -o:data/circo -ext:on
#saxonb-xslt -s:maps/communes.svg -xsl:processors/communes.xsl -o:data/communes -ext:on

.PHONY: maps

maps: communes.xml
	saxonb-xslt -s:maps/communes.svg -xsl:processors/non_2005.xsl -o:output/non_2005.svg -ext:on
	saxonb-xslt -s:maps/communes.svg -xsl:processors/hollande.xsl -o:output/hollande.svg -ext:on

	for f in output/*.svg; do \
		inkscape -f $$f -e "$f$.png"; \
	done

communes.xml:
	python get_election_data.py
	basex -q "let \$$file := \"communes.json\" return json-to-xml(file:read-text(\$$file))" > communes.xml

clean:
	rm -rf communes.xml
