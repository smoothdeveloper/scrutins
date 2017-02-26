import csv
import urllib

def download_page(url, destination):
    file = urllib.URLopener()
    file.retrieve(url, destination)

with open('data/communes', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if len(row) < 1:
            continue

        insee = row[0]
        dpt = "0" + row[0][0:2]
        print insee, dpt

        download_page("http://www.interieur.gouv.fr/Elections/Les-resultats/Referendums/elecresult__referendum_2005/(path)/referendum_2005/082/" + dpt + "/" + insee + ".html", "data/2005/" + insee)



