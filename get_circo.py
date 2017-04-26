#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals

import pandas as pd
import json
from json import encoder

encoder.FLOAT_REPR = lambda o: format(o, '.2f')


def calculer_totaux(df):
    stats_index = ['departement', 'circo', 'tour']
    choix_index = stats_index + ['choix']

    # on vérifie que le nombre d'inscrits, votants et exprimes est le même à chaque ligne d'un même bureau
    verif_unique = df.groupby(stats_index + ['commune_code', 'bureau']).agg({
        'inscrits': 'nunique',
        'votants': 'nunique',
        'exprimes': 'nunique',
    })
    assert (verif_unique == 1).all().all()

    stats = (
        df
            # on a vérifié que les stats étaient les mêmes pour chaque bureau, donc on déduplique en prenant
            # la première valeur
            .groupby(stats_index + ['commune_code', 'bureau']).agg({
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


def calculer_scores(stats, choix, tour, gauche, droite, nonistes_gauche, nonistes_droite):
    print(choix)
    scores = 100 * choix[tour].divide(stats[tour]['exprimes'], axis=0)
    if gauche and droite and nonistes_gauche and nonistes_droite:
        scores['DROITE'] = scores[droite].sum(axis=tour)
        scores['GAUCHE'] = scores[gauche].sum(axis=tour)
        scores['NONISTES_DROITE'] = scores[nonistes_droite].sum(axis=tour)
        scores['NONISTES_GAUCHE'] = scores[nonistes_gauche].sum(axis=tour)
        scores['NONISTES'] = scores['NONISTES_DROITE'] + scores['NONISTES_GAUCHE']

    scores['ABSTENTION'] = 100-100 * stats[tour]['exprimes'] / stats[tour]['inscrits']
    scores['INSCRITS'] = stats[tour]['inscrits']
    return scores


use_columns = [
    'tour', 'departement', 'circo', 'commune_code', 'bureau',
    'inscrits', 'votants', 'exprimes',
    'choix', 'voix'
]


df_pres_2012 = pd.read_csv(
    'data/pres_2012.csv',
    sep=';',
    encoding='cp1252',
    names=['tour', 'departement', 'commune_code', 'commune_nom', 'circo', 'canton', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str},
    usecols=use_columns
)


df_legi_2012 = pd.read_csv(
    'data/legi_2012.csv',
    sep=';',
    skiprows=18,
    names=['tour', 'departement', 'commune_code', 'commune_nom', 'circo', 'canton', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'choix': str, 'commune_code': str, 'bureau': str},
    usecols=use_columns
)

stats_2012, choix_2012 = calculer_totaux(df_pres_2012)
stats_legi_2012, choix_legi_2012 = calculer_totaux(df_legi_2012)


# statistiques présidentielles 2012

droite_2012 = [ "LEPE", "DUPO", "SARK" ]
gauche_2012 = [ "MELE", "ARTH", "POUT" ]
nonistes_droite_2012 = ["LEPE", "DUPO"]
nonistes_gauche_2012 = ["MELE", "ARTH", "POUT"]
scores_pres_2012 = calculer_scores(stats_2012, choix_2012, 1,
                                   droite=droite_2012, gauche=gauche_2012,
                                   nonistes_droite=nonistes_droite_2012, nonistes_gauche=nonistes_gauche_2012)


# statistiques législatives 2012
# qui des divers droite ? Beaucoup doivent être nonistes
# sans doute moins le cas pour les divers gauche.
droite_legislatives_2012 = [ 'FN', 'EXD', 'DVD', 'UMP' ]
gauche_legislatives_2012 = [ 'FG', 'EXG', 'DVG', 'SOC' ]
nonistes_droite_legislatives_2012 = ['FN', 'EXD']
nonistes_gauche_legislatives_2012 = ['FG', 'EXG']
scores_legi1_2012 = calculer_scores(stats_legi_2012, choix_legi_2012, 1,
                                   droite=droite_legislatives_2012,
                                   gauche=gauche_legislatives_2012,
                                   nonistes_droite=nonistes_droite_legislatives_2012,
                                   nonistes_gauche=nonistes_gauche_legislatives_2012)

scores_legi2_2012 = calculer_scores(stats_legi_2012, choix_legi_2012, 2,
                                   droite=[],
                                   gauche=[],
                                   nonistes_droite=[],
                                   nonistes_gauche=[])


df_circonscriptions = pd.concat([
    scores_pres_2012.rename(columns=lambda c: c + '_PRES_2012'),
    scores_legi1_2012.rename(columns=lambda c: c + '_LEGI1_2012'),
    scores_legi2_2012.rename(columns=lambda c: c + '_LEGI2_2012')
], axis=1)


# a améliorer, on pourrait sortir directement du XML par exemple
circonscriptions = {dep+'{:02d}'.format(circo): scores[scores.notnull()].to_dict() for (dep, circo), scores in df_circonscriptions.iterrows()}

open("circos.json", 'w').write(json.dumps(circonscriptions, indent=4))
