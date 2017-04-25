#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals

import pandas as pd
import json
from json import encoder

encoder.FLOAT_REPR = lambda o: format(o, '.2f')

def attribuer_circo(df_source, df):
    
    return df


def calculer_totaux(df):
    stats_index = ['departement', 'circo_code', 'tour' ]
    choix_index = stats_index + ['choix']

    # on vérifie que le nombre d'inscrits, votants et exprimes est le même à chaque ligne d'un même bureau
    verif_unique = df.groupby(stats_index + ['bureau']).agg({
        'inscrits': 'nunique',
        'votants': 'nunique',
        'exprimes': 'nunique',
    })
    assert (verif_unique == 1).all().all()

    stats = (
        df
            # on a vérifié que les stats étaient les mêmes pour chaque bureau, donc on déduplique en prenant
            # la première valeur
            .groupby(stats_index + ['bureau']).agg({
            'inscrits': 'first',
            'votants': 'first',
            'exprimes': 'first',
        })
            # puis on somme par commune
            .groupby(level=stats_index).sum()
            # puis on dépile le numéro de tour et on le met en premier index de colonne
            .unstack(['tour']).swaplevel(0, 1, axis=1).sortlevel(axis=1)
            # enfin, on remplace les valeurs manquantes avec des 0 (pour les élections sans second tour)
            .fillna(0, downcast='infer')
    )
    stats.columns = stats.columns.set_names(['tour', 'statistique'])

    # le fillna est utilisé pour les législatives : toutes les nuances ne sont pas présentes dans toutes
    # les circos, donc il faut remplacer les valeurs manquantes par des 0, et recaster en int
    choix = df.groupby(choix_index)['voix'].sum().unstack(['tour', 'choix']).fillna(0, downcast='infer').sortlevel(axis=1)

    # on vérifie que le nombre de suffrages exprimés est égal à la somme des votes pour chaque choix, et ce pour chaque
    # tour de l'élection
    assert (
       stats.swaplevel(0, 1, axis=1)['exprimes'] == choix.sum(axis=1, level=0)
    ).all().all()

    return stats, choix


def calculer_scores(stats, choix, gauche, droite, nonistes_gauche, nonistes_droite):
    scores = 100 * choix[1].divide(stats[1]['inscrits'], axis=0)
    scores['DROITE'] = scores[droite].sum(axis=1)
    scores['GAUCHE'] = scores[gauche].sum(axis=1)
    scores['NONISTES_DROITE'] = scores[nonistes_droite].sum(axis=1)
    scores['NONISTES_GAUCHE'] = scores[nonistes_gauche].sum(axis=1)
    scores['NONISTES'] = scores['NONISTES_DROITE'] + scores['NONISTES_GAUCHE']
    scores['ABSTENTION'] = 100-100 * stats[1]['exprimes'] / stats[1]['inscrits']
    scores['INSCRITS'] = stats[1]['inscrits']
    return scores


use_columns = [
    'tour', 'departement', 'commune_code', 'bureau',
    'inscrits', 'votants', 'exprimes',
    'choix', 'voix'
]


# Pour 2005

df_2005 = pd.read_csv(
    'data/2005.csv',
    sep=';',
    skiprows=20,
    encoding='cp1252',
    names=['tour', 'region', 'departement', 'arrondissement', 'circo', 'canton', 'commune_code', 'ref_inscrits',
           'commune_nom', 'bureau', 'inscrits', 'votants', 'abstentions', 'exprimes', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str},
    usecols=use_columns
)
# attention aux espaces en trop dans la réponse
df_2005['choix'] = df_2005.choix.str.strip()
df_2005['circo_code'] = df_2005.departement+"_"+df_2005.circo

# 2007 maintenant

df_2007 = pd.read_csv(
    'data/pres_2007.csv',
    sep=';',
    skiprows=17,
    encoding='cp1252',
    names=['tour', 'departement', 'commune_code', 'commune_nom', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str},
    usecols=use_columns
)

df_pres_2012 = pd.read_csv(
    'data/pres_2012.csv',
    sep=';',
    encoding='cp1252',
    names=['tour', 'departement', 'commune_code', 'commune_nom', '?', '??', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str},
    usecols=use_columns
)



df_legi_2012 = pd.read_csv(
    'data/legi_2012.csv',
    sep=';',
    skiprows=18,
    names=['tour', 'departement', 'commune_code', 'commune_nom', 'circo', '??', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str},
    usecols=use_columns
)

stats_2005, choix_2005 = calculer_totaux(df_2005)
stats_2007, choix_2007 = calculer_totaux(df_2007)
stats_2012, choix_2012 = calculer_totaux(df_pres_2012)
stats_legi_2012, choix_legi_2012 = calculer_totaux(df_legi_2012)

# statistiques tce
scores_tce = pd.DataFrame({
    'OUI_TCE': 100 * choix_2005[1]['OUI'] / stats_2005[1]['inscrits'],
    'NON_TCE': 100 * choix_2005[1]['NON'] / stats_2005[1]['inscrits'],
    'ABSTENTION_TCE': 100-100 * stats_2005[1]['exprimes'] / stats_2005[1]['inscrits']
})

# statistiques présidentielles 2012

droite_2012 = [ "LEPE", "DUPO", "SARK" ]
gauche_2012 = [ "MELE", "ARTH", "POUT" ]
nonistes_droite_2012 = ["LEPE", "DUPO"]
nonistes_gauche_2012 = ["MELE", "ARTH", "POUT"]
scores_pres_2012 = calculer_scores(stats_2012, choix_2012,
                                   droite=droite_2012, gauche=gauche_2012,
                                   nonistes_droite=nonistes_droite_2012, nonistes_gauche=nonistes_gauche_2012)

# statistiques présidentielles 2007
droite_2007 = [ "LEPE", "SARK", "NIHO", "VILL" ]
gauche_2007 = [ "BUFF", "BESA", "SCHI", "ROYA" ]
nonistes_droite_2007 = ["LEPE", "NIHO", "VILL"]
nonistes_gauche_2007 = ["BUFF", "BESA", "SCHI"]
scores_pres_2007 = calculer_scores(stats_2007, choix_2007,
                                   droite=droite_2007, gauche=gauche_2007,
                                   nonistes_droite=nonistes_droite_2007, nonistes_gauche=nonistes_gauche_2007)


# statistiques législatives 2012
# qui des divers droite ? Beaucoup doivent être nonistes
# sans doute moins le cas pour les divers gauche.
droite_legislatives_2012 = [ 'FN', 'EXD', 'DVD', 'UMP' ]
gauche_legislatives_2012 = [ 'FG', 'EXG', 'DVG', 'SOC' ]
nonistes_droite_legislatives_2012 = ['FN', 'EXD']
nonistes_gauche_legislatives_2012 = ['FG', 'EXG']
scores_legi_2012 = calculer_scores(stats_legi_2012, choix_legi_2012,
                                   droite=droite_legislatives_2012,
                                   gauche=gauche_legislatives_2012,
                                   nonistes_droite=nonistes_droite_legislatives_2012,
                                   nonistes_gauche=nonistes_gauche_legislatives_2012)


index = pd.DataFrame({
    'dpt': stats_legi_2012['departement']
})


df_circonscriptions = pd.concat([
    scores_tce,
    scores_pres_2012.rename(columns=lambda c: c + '_PRES_2012'),
    scores_pres_2007.rename(columns=lambda c: c + '_PRES_2007'),
    scores_legi_2012.rename(columns=lambda c: c + '_LEGI_2012')
], axis=1)

print (scores_tce)

# a améliorer, on pourrait sortir directement du XML par exemple
circonscriptions = {dep+circo_code: scores[scores.notnull()].to_dict() for (dep, circo_code), scores in df_circonscriptions.iterrows()}

open("circonscriptions.json", 'w').write(json.dumps(circonscriptions, indent=4))
