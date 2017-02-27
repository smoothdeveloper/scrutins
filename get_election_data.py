import csv
import urllib
import os.path
import shutil
import json

def download_page(url, destination):
    if os.path.isfile(destination):
        return

    file = urllib.URLopener()
    file.retrieve(url, destination)

def fix_csv(file, original_delim, desired_delim):
    newLogFile = open("tmp", 'w')
    textFile = open(file, 'rb')
    for row in textFile:
        row.replace(original_delim, desired_delim)
        newLogFile.write(row)

    shutil.copy2("tmp", file)

download_page("https://www.data.gouv.fr/s/resources/election-presidentielle-2012-resultats-par-bureaux-de-vote-1/20150925-102751/PR12_Bvot_T1T2.txt", "data/pres_2012.csv")
download_page("https://www.data.gouv.fr/s/resources/referendum-de-2005-resultats-par-bureaux-de-vote/20150925-112918/RF05_BVot.txt", "data/2005.csv")

fix_csv("data/2005.csv", ",", ";")
fix_csv("data/pres_2012.csv", ",", ";")

def init_res():
    c = {}
    c["exprimes_2005"] = 0
    c["votants_2005"] = 0
    c["abstention_2005"] = 0
    c["inscrits_2005"] = 0
    c["exprimes_2012"] = 0
    c["votants_2012"] = 0
    c["inscrits_2012"] = 0
    return c

bureaux = []
communes = {}

with open('data/2005.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        if len(row) != 16:
            print "ignored", ','.join(row)
            continue

        dpt = row[2]
        insee = row[2] + row[6]
        resultat = row[14].strip()

        if not insee in communes:
            communes[insee] = init_res()

        if not resultat + "_2005" in communes[insee]:
            communes[insee][resultat + "_2005"] = 0

        communes[insee][resultat + "_2005"] = communes[insee][resultat + "_2005"] + int(row[15])

        if resultat == "OUI":
            communes[insee]["exprimes_2005"] = communes[insee]["exprimes_2005"] + int(row[13])
            communes[insee]["votants_2005"] = communes[insee]["votants_2005"] + int(row[11])
            communes[insee]["abstention_2005"] = communes[insee]["abstention_2005"] + int(row[12])

with open('data/pres_2012.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        if len(row) != 15:
            print "ignored", ','.join(row)
            continue

        if int(row[0]) != 1:
            continue

        dpt = row[1]
        insee = row[1] + row[2]
        resultat = row[13].strip()

        if not insee in communes:
            communes[insee] = init_res()

        if not resultat + "_2012" in communes[insee]:
            communes[insee][resultat + "_2012"] = 0

        communes[insee][resultat + "_2012"] = communes[insee][resultat + "_2012"] + int(row[14])

        if resultat == "HOLL":
            communes[insee]["exprimes_2012"] = communes[insee]["exprimes_2012"] + int(row[9])
            communes[insee]["votants_2012"] = communes[insee]["votants_2012"] + int(row[8])
            communes[insee]["inscrits_2012"] = communes[insee]["inscrits_2012"] + int(row[7])

        #print insee, dpt
for insee,commune in communes.iteritems():
    print insee

open("communes.json", 'w').write(json.dumps(communes, indent=4))
