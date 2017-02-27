#saxonb-xslt -s:maps/circonscriptions.svg -xsl:processors/circo.xsl -o:data/circo -ext:on
#saxonb-xslt -s:maps/communes.svg -xsl:processors/communes.xsl -o:data/communes -ext:on
#python get_election_data.py

#basex -q "let \$file := \"communes.json\" return json-to-xml(file:read-text(\$file))" > communes.xml

#saxonb-xslt -s:maps/communes.svg -xsl:processors/non_2005.xsl -o:maps/non_2005.svg -ext:on
saxonb-xslt -s:maps/communes.svg -xsl:processors/hollande.xsl -o:maps/hollande.svg -ext:on
