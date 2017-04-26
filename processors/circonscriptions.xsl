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

    <xsl:variable name="nuances" select="document('../circonscriptions/nuances.xml')" />
    <xsl:for-each select="$nuances//nuance">
      \definecolor{<xsl:value-of select="." />}{HTML}{<xsl:value-of select="upper-case(./@color)" />}
    </xsl:for-each>
    
    
    \title{\bf Revue des circonscriptions}    % Supply information
    \author{}              %   for the title page.
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
        \begin{tabular}{|c|l|r|}
          \hline
          \hphantom &amp; \textbf{Candidat} &amp; \textbf{Score} \\
          \hline
         <xsl:for-each select="./fn:number[ends-with(./@key, 'PRES_2012') and string-length(./@key)=14]">
             <xsl:sort data-type="number" order="descending" select="."/>
            \cellcolor{<xsl:value-of select="substring-before(./@key, '_PRES_2012')" />} \hphantom &amp; <xsl:value-of select="substring-before(./@key, '_PRES_2012')" /> &amp; <xsl:value-of select="format-number(.,'#.##')" /> \% \\
          </xsl:for-each>
          \hline
          \hphantom &amp; \textbf{Abstention} &amp; <xsl:value-of select="format-number(./fn:number[@key='ABSTENTION_PRES_2012'],'#.##')" /> \% \\
          \hline
        \end{tabular}

        \subsubsection*{Législatives 2012}
        \begin{figure}[hptb]
          \begin{subfigure}[t]{.225\textwidth}
            \begin{tabular}{|c|l|r|}
            \hline
            \hphantom &amp; \textbf{Nuance} &amp; \textbf{Score} \\
            \hline
           <xsl:for-each select="./fn:number[ends-with(./@key, 'LEGI1_2012') and string-length(./@key) &lt;= 15]"><xsl:sort data-type="number" order="descending" select="."/><xsl:if test=". &gt; 0">\cellcolor{<xsl:value-of select="substring-before(./@key, '_LEGI1_2012')" />} \hphantom &amp; <xsl:value-of select="substring-before(./@key, '_LEGI1_2012')" /> &amp; <xsl:value-of select="format-number(.,'#.##')" /> \% \\</xsl:if></xsl:for-each>
            \hline
            \hphantom &amp; \textbf{Abstention} &amp; <xsl:value-of select="format-number(./fn:number[@key='ABSTENTION_LEGI1_2012'],'#.##')" /> \% \\
            \hline
            \end{tabular} 
            \caption{1er tour}
            \label{fig:1}
          \end{subfigure}%
<xsl:if test="count(./fn:number[ends-with(./@key, 'LEGI2_2012') and string-length(./@key) &lt;= 15]) &gt; 0">\begin{subfigure}[t]{.225\textwidth}
              \begin{tabular}{|c|l|r|}
                \hline
                \hphantom &amp; \textbf{Nuance} &amp; \textbf{Score} \\
                \hline
               <xsl:for-each select="./fn:number[ends-with(./@key, 'LEGI2_2012') and string-length(./@key) &lt;= 15]">
                   <xsl:sort data-type="number" order="descending" select="."/>
                  <xsl:if test=". &gt; 0">
                    \cellcolor{<xsl:value-of select="substring-before(./@key, '_LEGI2_2012')" />} \hphantom &amp; <xsl:value-of select="substring-before(./@key, '_LEGI2_2012')" /> &amp; <xsl:value-of select="format-number(.,'#.##')" /> \% \\
                  </xsl:if>
                </xsl:for-each>
                \hline
                \hphantom &amp; \textbf{Abstention} &amp; <xsl:value-of select="format-number(./fn:number[@key='ABSTENTION_LEGI2_2012'],'#.##')" /> \% \\
                \hline
              \end{tabular}
            \caption{2nd tour}
            \label{fig:2}
          \end{subfigure}</xsl:if>
        \end{figure}
    
    </xsl:for-each>
    
    
    \end{document}                          % The required last line
    
</xsl:template>
</xsl:stylesheet>
