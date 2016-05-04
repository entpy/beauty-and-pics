# -*- coding: utf-8 -*-

"""
Settings for 'django_photo_contest' app
"""

DPC_SECONDS_BETWEEN_VOTATION = 604800 # 604800 seconds = 7 days
DPC_ADD_WINNER_POINTS = True # indica se al vincitore devono essere assegnati i punti
DPC_WRITE_WINNER_NOTIFY = True # indica se scrivere la notifica al vincitore

# photocontest list
DPC_PHOTO_CONTEST_LIST = [
    'bianco-e-nero',
    'selfie',
    'spiaggia',
    'retro',
    'graffiti',
]

# info per ogni photocontest
DPC_PHOTO_CONTEST_INFO = {
    'bianco-e-nero' : {
        'name' : 'Bianco e nero',
        'description' : "La fotografia in bianco e nero ha sempre il suo fascino. Scopri con questo concorso a tema quale sarà la foto in bianco e nero più apprezzata.",
        'rules' : ['Valide solo foto in bianco e nero'],
        'like_limit' : 20,
        'order' : 1000,
    },
    'selfie' : {
        'name' : 'Selfie',
        'description' : "Quale sarà il selfie più apprezzato? Scoprilo con questo divertente concorso a tema dedicato ai selfie.",
        'rules' : ['Valide solo foto di selfie'],
        'like_limit' : 25,
        'order' : 2000,
    },
    'spiaggia' : {
        'name' : 'Spiaggia',
        'description' : "Scopri la suggestiva scenografia che offre il mare. Se ami le location marine questo è il posto giusto per te.",
        'rules' : ['Valide solo foto in prossimità di mare e spiaggia'],
        'like_limit' : 20,
        'order' : 3000,
    },
    'retro' : {
        'name' : 'Rétro',
        'description' : "Per gli amanti del rétro. Sei dell'idea che l'old school non passi mai di moda? Questo concorso a tema racchiude le foto che conservano l'anima e le emozioni del passato.",
        'rules' : ['Valide solo foto in abiti e ambientazioni rétro'],
        'like_limit' : 20,
        'order' : 4000,
    },
    'graffiti' : {
        'name' : 'Graffiti',
        'description' : "Solo per gente underground. Il concorso a tema si prefigge di evidenziare in maniera artistica alcuni elementi della città.",
        'rules' : ['Valide solo foto che hanno come location la metropoli', 'Nella foto deve essere presente almeno un graffito'],
        'like_limit' : 20,
        'order' : 5000,
    },
}
