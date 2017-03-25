#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals

import pandas as pd
import json
from json import encoder

encoder.FLOAT_REPR = lambda o: format(o, '.2f')


def calculer(df):
    stats_index = ['departement', 'commune_code', 'tour']
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
    )
    stats.columns = stats.columns.set_names(['tour', 'statistique'])

    choix = df.groupby(choix_index)['voix'].sum().unstack(['tour', 'choix'])

    # on vérifie que le nombre de suffrages exprimés est égal à la somme des votes pour chaque choix, et ce pour chaque
    # tour de l'élection
    assert (
       stats.swaplevel(0, 1, axis=1)['exprimes'] == choix.sum(axis=1, level=0)
    ).all().all()

    return stats, choix


# Pour 2005

df_2005 = pd.read_csv(
    'data/2005.csv',
    sep=';',
    skiprows=20,
    encoding='cp1252',
    names=['tour', 'region', 'departement', 'arrondissement', 'circo', 'canton', 'commune_code', 'ref_inscrits',
           'commune_nom', 'bureau', 'inscrits', 'votants', 'abstentions', 'exprimes', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str}
)
# attention aux espaces en trop dans la réponse
df_2005['choix'] = df_2005.choix.str.strip()

stats_2005, choix_2005 = calculer(df_2005)

# 2007 maintenant

df_2007 = pd.read_csv(
    'data/pres_2007.csv',
    sep=';',
    skiprows=17,
    encoding='cp1252',
    names=['tour', 'departement', 'commune_code', 'commune_nom', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str}
)

stats_2007, choix_2007 = calculer(df_2007)

df_2012 = pd.read_csv(
    'data/pres_2012.csv',
    sep=';',
    encoding='cp1252',
    names=['tour', 'departement', 'commune_code', 'commune_nom', '?', '??', 'bureau', 'inscrits', 'votants', 'exprimes',
           'numero_candidat', 'nom_candidat', 'prenom_candidat', 'choix', 'voix'],
    dtype={'departement': str, 'commune_code': str, 'bureau': str}
)
stats_2012, choix_2012 = calculer(df_2012)

# statistiques tce
scores_tce = pd.DataFrame({
    'OUI_TCE': 100 * choix_2005[1]['OUI'] / stats_2005[1]['inscrits'],
    'NON_TCE': 100 * choix_2005[1]['NON'] / stats_2005[1]['inscrits']
})
# statistiques 2012
nonistes_droite_2012 = ["LEPE", "DUPO"]
nonistes_gauche_2012 = ["MELE", "ARTH", "POUT"]
scores_pres_2012 = 100 * choix_2012[1].divide(stats_2012[1]['inscrits'], axis=0)
scores_pres_2012['NONISTES_DROITE'] = scores_pres_2012[nonistes_droite_2012].sum(axis=1)
scores_pres_2012['NONISTES_GAUCHE'] = scores_pres_2012[nonistes_gauche_2012].sum(axis=1)
scores_pres_2012['NONISTES'] = scores_pres_2012['NONISTES_DROITE'] + scores_pres_2012['NONISTES_GAUCHE']

# statistiques 2007
nonistes_droite_2007 = ["LEPE", "NIHO", "VILL"]
nonistes_gauche_2007 = ["BUFF", "BESA", "SCHI"]
scores_pres_2007 = 100 * choix_2007[1].divide(stats_2007[1]['inscrits'], axis=0)
scores_pres_2007['NONISTES_DROITE'] = scores_pres_2007[nonistes_droite_2007].sum(axis=1)
scores_pres_2007['NONISTES_GAUCHE'] = scores_pres_2007[nonistes_gauche_2007].sum(axis=1)
scores_pres_2007['NONISTES'] = scores_pres_2007['NONISTES_DROITE'] + scores_pres_2007['NONISTES_GAUCHE']

df_communes = pd.concat([
    scores_tce,
    scores_pres_2012.rename(columns=lambda c: c + '_PRES_2012'),
    scores_pres_2007.rename(columns=lambda c: c + '_PRES_2007')
], axis=1)

# a améliorer, on pourrait sortir directement du XML par exemple
communes = {dep+commune: scores[scores.notnull()].to_dict() for (dep, commune), scores in df_communes.iterrows()}

open("communes.json", 'w').write(json.dumps(communes, indent=4))
