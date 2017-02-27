<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:doc="http://jlm2017.fr"
    xmlns:fn="http://www.w3.org/2005/xpath-functions"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   inkscape:version="0.48.2 r9819"
   sodipodi:docname="circonscriptions.svg"
    exclude-result-prefixes="xs doc">
    <xsl:output method="xml" indent="yes"/>

    <xsl:param name="communes" select="document('../communes.xml')"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="svg:polygon">
       <xsl:variable name="insee" select="substring-before(./@id, ' ')" />
       <xsl:variable name="red" select="$communes//fn:map[@key=$insee]/fn:number[@key='HOLL_PRES']" />
        <xsl:copy>
            <xsl:attribute name="fill">rgb(255, <xsl:value-of select="255-round(255 * $red div 100)" />, <xsl:value-of select="255-round(255 * $red div 100)" />)</xsl:attribute>
          <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
