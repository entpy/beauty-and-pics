# -*- coding: utf-8 -*-

"""
Settings for 'django_photo_contest' app
"""

# photo contest list
DPC_PHOTO_CONTEST_LIST = [
    'back-and-white',
    'selfie',
]

DPC_PHOTO_CONTEST_INFO = {
    'back-and-white' : {
        'name' : 'Bianco e nero',
        'description' : "Concorso a tema che permette di scoprire la foto più d'effetto in bianco e nero.",
        'rules' : ['Valide solo foto in bianco e nero'],
        'like_limit' : 20,
    },
    'selfie' : {
        'name' : 'Selfie',
        'description' : "Quale sarà il selfie più apprezzato? Scoprilo con questo concorso dedicato ai selfie.",
        'rules' : ['Valide solo foto di selfie'],
        'like_limit' : 25,
    },
    # TODO
    'selfie' : {
        'name' : "Giochi d'ombre",
        'description' : "Quale sarà il selfie più apprezzato? Scoprilo con questo concorso dedicato ai selfie.",
        'rules' : ['Valide solo foto di selfie'],
        'like_limit' : 25,
    },
}
