<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:doc="http://cosmology.education"
  xmlns:shell="java:java.lang.Runtime"
  xmlns:fn="http://www.w3.org/2005/xpath-functions"
  xmlns:atom="http://www.w3.org/2005/Atom"
  exclude-result-prefixes="xs doc">
  <xsl:output encoding="UTF-8" method="text" omit-xml-declaration="yes" indent="no"/>
  
<xsl:template match="/">
    \documentclass[a4paper,landscape,twocolumn]{article}
    \usepackage[a4paper,margin=1in]{geometry}
    \usepackage[french]{babel}
    \usepackage[utf8]{inputenc} 
    \usepackage[T1]{fontenc}
    \usepackage{import}
    \subimport{.}{header}
    \setsvg{svgpath = ../images/}
    
    
    \title{\bf Histoire de la cosmologie \\
    \ \\
    \large Du développement de la Relativité Générale à la mission Planck
    \\
    \textit{(en cours d'écriture)}}    % Supply information
    \author{Lucas Gautheron}              %   for the title page.
    \date{\today}                           %   Use current date. 
    
    % Note that book class by default is formatted to be printed back-to-back.
    \begin{document}                        % End of preamble, start of text.
    
    \maketitle  
    % Print title page.
    
    \chapter*{Introduction}
    
    
   Blabalh
    
    \tableofcontents                        % Print table of contents
    
    <xsl:for-each select="//fn:map">
        \section{Circonscription n.<xsl:value-of select="./@key" />}
        
        \textbf{Nombre d'inscrits} (2012) : <xsl:value-of select="round(./fn:number[@key='INSCRITS_PRES_2012'])" />
    
        \subsubsection*{Présidentielle 2012}
        \begin{tabular}{|l|r|}
          \hline
          \textbf{Candidat} &amp; \textbf{Score} \\
          \hline
         <xsl:for-each select="./fn:number[ends-with(./@key, 'PRES_2012') and string-length(./@key)=14]">
             <xsl:sort data-type="number" order="descending" select="."/>
            <xsl:value-of select="substring(./@key, 1, 4)" /> &amp; <xsl:value-of select="format-number(.,'#.##')" /> \% \\
          </xsl:for-each>
          \hline
          \textbf{Abstention} &amp; <xsl:value-of select="format-number(./fn:number[@key='ABSTENTION_PRES_2012'],'#.##')" /> \% \\
          \hline
        \end{tabular}
        
    </xsl:for-each>
    
    
    
    
    \end{document}                          % The required last line
    
</xsl:template>
</xsl:stylesheet>
