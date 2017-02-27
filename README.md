# L'objectif

L'objectif est de réaliser une cartographie des communes ou bureaux de vote où la population est susceptible d'être intéressée par notre discours.
Il faut idéalement identifier les transferts suivants :
 * PS -> PG
 * PS -> FN
 * PS -> abstention
 
L'objectif est aussi de répérer les régions avec un fort vote NON "de gauche" au référendum de 2005.


# Comment ?

Le code est assez simple à comprendre, pour qui connait python.
Les cartes sont générées à partir d'un fichier SVG et de feuilles de style XSLT.

```
sudo apt-get install libsaxonb-java basex inkscape
```

```
make maps
```
