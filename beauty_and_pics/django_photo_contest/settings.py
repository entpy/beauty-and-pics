# -*- coding: utf-8 -*-

"""
Settings for 'django_photo_contest' app
"""

SECONDS_BETWEEN_VOTATION = 604800 # 604800 seconds = 7 days

# photo contest list
DPC_PHOTO_CONTEST_LIST = [
    'bianco-e-nero',
    'selfie',
    'spiaggia',
    'retro',
    'graffiti',
]

DPC_PHOTO_CONTEST_INFO = {
    'bianco-e-nero' : {
        'name' : 'Bianco e nero',
        'description' : "Concorso a tema che permette di scoprire la foto più d'effetto in bianco e nero.",
        'rules' : ['Valide solo foto in bianco e nero'],
        'like_limit' : 20,
        'order' : 1000,
    },
    'selfie' : {
        'name' : 'Selfie',
        'description' : "Quale sarà il selfie più apprezzato? Scoprilo con questo concorso dedicato ai selfie.",
        'rules' : ['Valide solo foto di selfie'],
        'like_limit' : 25,
        'order' : 2000,
    },
    'spiaggia' : {
        'name' : 'Spiaggia',
        'description' : "Se ami le location marine questo è il posto giusto per te.",
        'rules' : ['Valide solo foto in prossimità di mare e spiaggia'],
        'like_limit' : 20,
        'order' : 3000,
    },
    'retro' : {
        'name' : 'Rétro',
        'description' : "Per gli amanti del rétro. Il bello non passa mai di moda? Qui puoi dimostrarlo!",
        'rules' : ['Valide solo foto in abiti rétro'],
        'like_limit' : 20,
        'order' : 4000,
    },
    'graffiti' : {
        'name' : 'Graffiti',
        'description' : "Solo per gente underground. Paesaggi cittadini.",
        'rules' : ['Valide solo foto che hanno come location la metropoli', 'Nella foto deve essere presente un graffito'],
        'like_limit' : 20,
        'order' : 5000,
    },
}
