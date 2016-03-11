# -*- coding: utf-8 -*-

"""
Settings for 'django_survey' app
"""

"""
# deault consts
DS_SURVEYS_QUESTION_TYPE_TEXT = 'text' # se la risposta è campo libero
DS_SURVEYS_QUESTION_TYPE_BOOLEAN = 'boolean' # se la risposta è si/no

DS_SURVEYS_CODE_ABOUT_USER = 'about_user'
DS_SURVEYS_CODE_ABOUT_USER = 'about_fashion_user'
DS_SURVEYS_CODE_IS_MODEL = 'is_model'
DS_SURVEYS_CODE_IS_NOT_MODEL = 'is_not_model'

# surveys list
DS_SURVEYS_LIST = [
    { 'survey_code' : DS_SURVEYS_CODE_ABOUT_USER, 'survey_description' : 'Questionario generico su un utente', },
    { 'survey_code' : DS_SURVEYS_CODE_IS_MODEL, 'survey_description' : "Questionario se l'utente è già modella/o", },
    { 'survey_code' : DS_SURVEYS_CODE_IS_NOT_MODEL, 'survey_description' : "Questionario se l'utente non è ancora modella/o", },
]

# questions list
DS_SURVEYS_QUESTIONS = [
    # survey about_user
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_000',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 1,
        'order' : 0,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_050',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 50,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_100',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 100,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_200',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 200,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_300',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 300,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_400',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 400,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_500',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 500,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_600',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 600,
        'default_hidden' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_700',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_BOOLEAN,
        'required' : 0,
        'order' : 700,
        'default_hidden' : 0,
	'case_1_survey_code' : DS_SURVEYS_CODE_IS_MODEL,
	'case_2_survey_code' : DS_SURVEYS_CODE_IS_NOT_MODEL,
    },
    # survey is_model
    {
        'survey_code' : DS_SURVEYS_CODE_IS_MODEL,
        'question_code' : 'is_model_000',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_IS_MODEL,
        'question_code' : 'is_model_100',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 900,
        'default_hidden' : 1,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_IS_MODEL,
        'question_code' : 'is_model_200',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 1000,
        'default_hidden' : 1,
    },
    # survey is_not_model
    {
        'survey_code' : DS_SURVEYS_CODE_IS_NOT_MODEL,
        'question_code' : 'is_not_model_000',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 1100,
        'default_hidden' : 1,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_IS_NOT_MODEL,
        'question_code' : 'is_not_model_100',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 1200,
        'default_hidden' : 1,
    },
]

# questions label
DS_SURVEYS_QUESTIONS_LABEL = {
    # survey about_user
    'about_user_000' : {
        'question_text_woman' : 'Dicci qualcosa di te',
        'question_text_man' : 'Dicci qualcosa di te',
        'question_hint_woman' : 'Descrivi dove sei nata, chi sei e le tue passioni',
        'question_hint_man' : 'Descrivi dove sei nato, chi sei e le tue passioni',
    },
    'about_user_050' : {
        'question_text_woman' : 'Lavori o ti appassiona il settore della moda?',
        'question_text_man' : 'Lavori o ti appassiona il settore della moda?',
        'question_hint_woman' : '',
        'question_hint_man' : '',
    },
    'about_user_100' : {
        'question_text_woman' : "Qual'è il tuo motto?",
        'question_text_man' : "Qual'è il tuo motto?",
        'question_hint_woman' : "Scrivi qual'è il tuo motto preferito",
        'question_hint_man' : "Scrivi qual'è il tuo motto preferito",
    },
    'about_user_200' : {
        'question_text_woman' : 'La tua giornata tipo?',
        'question_text_man' : 'La tua giornata tipo?',
        'question_hint_woman' : 'Descrivici la tua giornata tipo',
        'question_hint_man' : 'Descrivici la tua giornata tipo',
    },
    'about_user_300' : {
        'question_text_woman' : 'Il tuo pregio più grande?',
        'question_text_man' : 'Il tuo pregio più grande?',
        'question_hint_woman' : 'Scrivi quello che secondo te è il tuo pregio migliore',
        'question_hint_man' : 'Scrivi quello che secondo te è il tuo pregio migliore',
    },
    'about_user_400' : {
        'question_text_woman' : 'Il tuo "peggior" difetto?',
        'question_text_man' : 'Il tuo "peggior" difetto?',
        'question_hint_woman' : 'Scrivi quello che secondo te è il tuo peggior difetto',
        'question_hint_man' : 'Scrivi quello che secondo te è il tuo peggior difetto',
    },
    'about_user_500' : {
        'question_text_woman' : 'Il tuo hobby?',
        'question_text_man' : 'Il tuo hobby?',
        'question_hint_woman' : 'Scrivi quello che ti piace fare nel tuo tempo libero',
        'question_hint_man' : 'Scrivi quello che ti piace fare nel tuo tempo libero',
    },
    'about_user_600' : {
        'question_text_woman' : 'Una causa in cui credi?',
        'question_text_man' : 'Una causa in cui credi?',
        'question_hint_woman' : 'Scrivi una causa in cui credi',
        'question_hint_man' : 'Scrivi una causa in cui credi',
    },
    'about_user_700' : {
        'question_text_woman' : 'Sei una modella?',
        'question_text_man' : 'Sei un modello?',
        'question_hint_woman' : '',
        'question_hint_man' : '',
    },
    # survey is_model
    'is_model_000' : {
        'question_text_woman' : 'Come hai iniziato a fare la modella?',
        'question_text_man' : 'Come hai iniziato a fare il modello?',
        'question_hint_woman' : "Descrivi cosa ti ha portato a fare la modella",
        'question_hint_man' : "Descrivi cosa ti ha portato a fare il modello",
    },
    'is_model_100' : {
        'question_text_woman' : 'Lo/la stilista per cui vorresti sfilare?',
        'question_text_man' : 'Lo/la stilista per cui vorresti sfilare?',
        'question_hint_woman' : "Scrivi il nome dello/a stilista per cui vorresti sfilare",
        'question_hint_man' : "Scrivi il nome dello/a stilista per cui vorresti sfilare",
    },
    'is_model_200' : {
        'question_text_woman' : 'Cosa vorresti fare dopo la tua carriera di modella?',
        'question_text_man' : 'Cosa vorresti fare dopo la tua carriera di modello?',
        'question_hint_woman' : "Scrivi quello che ti piacerebbe fare in futuro",
        'question_hint_man' : "Scrivi quello che ti piacerebbe fare in futuro",
    },
    # survey is_not_model
    'is_not_model_000' : {
        'question_text_woman' : 'Cosa trovi di interessante nel settore della moda?',
        'question_text_man' : 'Cosa trovi di interessante nel settore della moda?',
        'question_hint_woman' : "Scrivi quello che più ti piace nel settore della moda",
        'question_hint_man' : "Scrivi quello che più ti piace nel settore della moda",
    },
    'is_not_model_100' : {
        'question_text_woman' : "Facciamo finta che tu stia per essere assunta da un'agenzia di moda, cosa diresti per convincerli?",
        'question_text_man' : "Facciamo finta che tu stia per essere assunto da un'agenzia di moda, cosa diresti per convincerli?",
        'question_hint_woman' : "Scrivi qualcosa di convincente per essere contattata",
        'question_hint_man' : "Scrivi qualcosa di convincente per essere contattato",
    },
}

Ciao <nome_utente>, parliamo un po' di te!
D: Dicci dove sei nata e le tue passioni
D: Descrivici la tua giornata tipo
D: Il tuo pregio più grande e il tuo "peggior" difetto?

D: Qual'è il marchio che ami di più indossare?
if (Hai qualche hobby?) {
    D: Qual'è il tuo hobby?
}

D: Definisci il tuo concetto di "bellezza"?

D: Una massima in cui ti rispecchi?

if (Lavori nel settore fotografico e/o della moda?) {
    if (Sei una modella?) {
        D: Come hai iniziato a fare la modella?
        D: Lo/la stilista per cui vorresti sfilare?
        D: Cosa vorresti fare dopo la tua carriera di modella?
        D: Alcuni nomi con cui hai lavorato?
        D: Alcuni nomi con cui non hai mai lavorato ma ti piacerebbe?
    } else {
	D: Spiegagi meglio il tuo lavoro
        D: Con chi ti piacerebbe lavorare?
        D: 
    }
} else {
    if (Vorresti lavorare nel settore fotografico o della moda?) {
	D: Cosa ti piacerebbe fare di preciso?
    } else {

    }
}




--- V" ---
Ciao <nome_utente>, parliamo un po' di te!
D: Dicci dove sei nata e le tue passioni
D: Descrivici la tua giornata tipo
D: Il tuo pregio più grande e il tuo "peggior" difetto?

if (Hai qualche hobby?) {
    D: Qual'è il tuo hobby?
}

D: Definisci il tuo concetto di "bellezza"?

D: Una massima in cui ti rispecchi?

D: Le tue marche preferite?

if (Sei già una modella affermata?) {
        D: Come è iniziata la tua avventura nel mondo della moda?
        D: Lo/la stilista per cui vorresti sfilare?
        D: Cosa vorresti fare dopo la tua carriera di modella?
        D: Alcuni nomi con cui hai lavorato?
        D: Qualche consiglio per chi vorrebbe entrare nel mondo della moda?
} else {
        D: Lo/la stilista con cui vorresti lavorare?
        D: Com'è nata la tua passione per il mondo della moda?
        D: La modella a cui ti ispiri?
}




-----v3
<nome, quando nasce la tua passione per il mondo della moda, e quando la tua prima sfilata?
Dopo quella prima esperienza, quali i progetti e gli eventi principali a cui hai partecipato sinora?
Quali obiettivi ti poni per il medio termine?
Quali i tuoi hobby oltre al mondo della moda?
E’ difficile conciliare studio e la passione per la moda?
Per concludere,  e quale è il messaggio che vorresti dare alle ragazze della tua età che si avvicinano al mondo della moda?


Ciao <nome_utente>, parliamo un po' di te!

D: Seleziona la categoria che più ti rispecchia
if(sono una modella affermata) {

} else if (sono un'aspirante modella) {

} else if (sono un'appassionata di moda) {
    Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    Come è nata la passione per la moda?
    Cosa ti appassiona più della moda?
    Il tuo stile preferito durante il giorno?
    Il tuo stile preferito la sera?
} else if (sono un'appassionata di fotografia) {
    Quando e come hai scoperto la fotografia?
    La tua prima foto?
    Qual è stato il tuo percorso di crescita e apprendimento dell'arte fotografica?
    Secondo te fotografare è...?
    Fotografi per lavoro o per diletto?
    Qual è il tuo soggetto preferito?
    Qual è il tuo genere fotografico preferito?
} else if (sono una make up artist) {
    Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    Mi piacerebbe iniziare proprio dal momento in cui è nato il desiderio di diventare una truccatrice
    Quale percorso formativo hai intrapreso
    Cosa ti piace o ami del tuo lavoro in particolare?
    truccatrice/truccatore preferita/o?
    colore che dona a tutte?
    colore più difficile?
    di cosa non puoi fare a meno nel tuo lavoro?
} else if (sono una hair stylist) {
    Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    Cosa significa essere una hair stylist?
    Quale percorso formativo hai intrapreso
    Dove nasce la sua ispirazione nel creare nuove acconciature e nuovi stili?
    A proposito di stile, come definirebbe il suo?
    Secondo te, quali saranno le tendenze della prossima stagione?
} else if (sono una stilista) {
    Come nasce questa tua passione per la moda?
    Quale percorso formativo hai intrapreso
    Quali sono i tuoi look preferiti?
    Quali sono stati gli abbinamenti più difficili?
    A cosa ti ispiri per le tue creazioni?
    Raccontaci della tua ultima collezione
    Secondo te, quali saranno le tendenze della prossima stagione?
} else if (partecipo solo per divertimento) {
    Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    Convinci la gente a darti un voto
}

----- v5 (forse la finale?)
question types
    - select
    - text
    - boolean
    - radio

user_identify
model_pro
model_beginner
fashion_passionate
just_for_fun

if (sono una modella/indossatrice/ragazza immagine professionista) {
    D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    D: Come è iniziata la tua avventura nel mondo della moda?
    D: Definisci quello che secondo te è la "bellezza"?
    D: Il tuo pregio più grande e il tuo "peggior" difetto?
    D: Quali sono i tuoi look preferiti?
    D: Una massima o un motto in cui ti rispecchi?
    if (Nutri altre passioni oltre al mondo della moda?) {
        D: Quali altre passioni nutri oltre al mondo della moda?
    }
    D: La tua giornata tipo?
    if (Hai già partecipato a sfilate?) {
        D: A quali sfilate hai partecipato?
        D: Cos'hai provato durante la tua prima sfilata?
    } else {
        if (C'è qualche stilista particolare per cui vorresti sfilare?) {
            D: per quale stilista vorresti sfilare?
        }
    }
    if (Hai già partecipato a qualche concorso/evento?) {
        D: A quali concorsi/eventi hai partecipato?
        if (Hai già vinto qualche titolo?) {
            D: Quale o quali titoli hai vinto?
        }
    } else {
        if (C'è qualche concorso/evento a cui vorresti partecipare?) {
            D: A quale concorso/evento vorresti partecipare?
        }
    }
    D: Alcune persone che ritieni importanti con cui hai lavorato?
    D: E' stata dura arrivare ai tuoi risultati?
    D: Qualche consiglio per chi vorrebbe entrare nel mondo della moda?
} else if (sono una modella/indossatrice/ragazza immagine esordiente) {
    D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    D: Com'è nata la tua passione per il mondo della moda?
    D: La ragione principale per cui ti piacerebbe lavorare nel mondo della moda?
    D: Definisci quello che secondo te è la "bellezza"?
    D: Ti piacerebbe diventare la nuova Miss...
    if (Nutri altre passioni oltre al mondo della moda?) {
        D: Quali altre passioni nutri oltre al mondo della moda?
    }
    D: La tua giornata tipo?
    D: Lo/la stilista per cui vorresti sfilare?
    D: La tua modella ispiratrice?
    D: Quali sono i tuoi look preferiti?
    D: Colore preferito
    D: Convinci la gente a darti un voto
} else if (sono un'appassionata di fotografia) {
    Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    D: La tua giornata tipo?
    D: Quali sono i tuoi look preferiti?
    D: Cosa ti appassiona di più della fotografia?
    D: Definisci quello che secondo te è la "bellezza"?
    D: Qual è il tuo genere fotografico preferito?
    if (Hai qualche hobby oltre alla fotografia?) {
        D: Qual'è il tuo hobby?
    }
    D: Convinci la gente a darti un voto
} else if (sono un'appassionata di moda) {
    D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    D: Come è nata questa tua passione per il mondo della moda?
    D: Cosa ti appassiona più nel mondo della moda?
    if (Nutri altre passioni oltre al mondo della moda?) {
        D: Quali altre passioni nutri oltre al mondo della moda?
    }
    D: Il tuo pregio più grande e il tuo "peggior" difetto?
    D: Definisci quello che secondo te è la "bellezza"?
    D: Il tuo stile preferito "giornaliero"?
    D: Il tuo stile preferito "serale"?
    D: Convinci la gente a darti un voto
} else if (partecipo solo per divertimento/altro) {
    D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
    D: Il tuo pregio più grande e il tuo "peggior" difetto?
    D: Quali sono i tuoi look preferiti?
    if (Hai qualche hobby?) {
        D: Qual'è il tuo hobby?
    }
    D: Una massima in cui ti rispecchi?
    D: Convinci la gente a darti un voto
}

question types
    - select
    - text
    - boolean
    - radio

user_identify
model_pro
model_beginner
photo_passionate
fashion_passionate
just_for_fun
"""
# gruppi di domande
DS_QUESTIONS_GROUPS = [
    'user_interview',
]

# blocchi di domande per ogni gruppo
DS_QUESTIONS_BLOCK = [
    # block_code	= identificativo del blocco di domande
    # path_code		= comune a tutte le domande di questo livello
    # child_path_code	= il path_code che avranno i "figli" di questo bivio
    # order		= ordinamento dei macroblocchi
    { 'block_code' : 'user_interview__user_identify', 'path_code' : 'path001', 'child_path_code' : 'path002', 'order' : 0, }, # bivio
	{ 'block_code' : 'user_interview__model_pro', 'path_code' : 'path002', 'child_path_code' : False, 'order' : 100, },
	{ 'block_code' : 'user_interview__model_pro__hobby', 'path_code' : 'path002', 'child_path_code' : 'path002_002', 'order' : 125, }, # bivio
	    { 'block_code' : 'user_interview__model_pro__write_hobby', 'path_code' : 'path002_001', 'child_path_code' : False, 'order' : 150, },
	{ 'block_code' : 'user_interview__model_beginner', 'path_code' : 'path003', 'child_path_code' : False, 'order' : 200, },
	{ 'block_code' : 'user_interview__photo_passionate', 'path_code' : 'path004', 'child_path_code' : False, 'order' : 300, },
	{ 'block_code' : 'user_interview__fashion_passionate', 'path_code' : 'path005', 'child_path_code' : False, 'order' : 400, },
	{ 'block_code' : 'user_interview__just_for_fun', 'path_code' : 'path006', 'child_path_code' : False, 'order' : 500, },
]

# elenco di domande per ogni blocco
DS_QUESTIONS_AND_SELECTABLE_ANSWERS = [
    {
        # D: Seleziona una categoria
        'question_block' : 'user_interview__user_identify',
        'question_code' : 'user_interview__user_identify__q1',
        'question_type' : 'select',
        'required' : 1,
        'order' : 0,
        'default_hidden' : 0,
        'answers' : [
            {
                # Sono una modella/ragazza immagine/indossatrice professionista
                'answer_code' : 'user_interview__user_identify__q1__model_pro',
                'next_question_block' : 'user_interview__model_pro',
            },
            {
                # Sono una modella/ragazza immagine/indossatrice emergente
                'answer_code' : 'user_interview__user_identify__q1__model_beginner',
                'next_question_block' : 'user_interview__model_beginner',
            },
            {
                # Sono appassionata di foto
                'answer_code' : 'user_interview__user_identify__q1__photo_passionate',
                'next_question_block' : 'user_interview__photo_passionate',
            },
            {
                # Sono appassionata di moda
                'answer_code' : 'user_interview__user_identify__q1__fashion_passionate',
                'next_question_block' : 'user_interview__fashion_passionate',
            },
            {
                # Solo per divertimento/altro
                'answer_code' : 'user_interview__user_identify__q1__just_for_fun',
                'next_question_block' : 'user_interview__just_for_fun',
            },
        ],
    },
    ## question_block: user_interview__model_pro
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q1',
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q1__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Come è iniziata la tua avventura nel mondo della moda?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q2',
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q2__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q3',
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q3__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Il tuo pregio più grande e il tuo "peggior" difetto?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q4',
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q4__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q5',
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q5__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Una massima o un motto in cui ti rispecchi?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q6',
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q6__answer',
                'next_question_block' : False,
            },
        ],
    },

    # TODO
    {
	# Nutri altre passioni oltre al mondo della moda?
        'question_block' : 'user_interview__model_pro__hobby',
        'question_code' : 'user_interview__user_identify__q6_5',
        'question_type' : 'select',
        'required' : 0,
        'order' : 650,
        'default_hidden' : 1,
        'answers' : [
            {
                # Si
                'answer_code' : 'user_interview__user_identify__q6_5__yes',
                'next_question_block' : 'user_interview__model_pro__write_hobby',
            },
            {
                # No
                'answer_code' : 'user_interview__user_identify__q6_5__no',
                'next_question_block' : False,
            },
        ],
    },
    {
	# Quali altre passioni nutri oltre al mondo della moda?
        'question_block' : 'user_interview__model_pro__write_hobby',
        'question_code' : 'user_interview__model_pro__write_hobby__q1',
        'question_type' : 'text',
        'required' : 0,
        'order' : 675,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__write_hobby__q1__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: La tua giornata tipo?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q7',
        'question_type' : 'text',
        'required' : 0,
        'order' : 700,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q7__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Alcune persone che ritieni importanti con cui hai lavorato?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q8',
        'question_type' : 'text',
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q8__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: E' stata dura arrivare ai tuoi risultati?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q9',
        'question_type' : 'text',
        'required' : 0,
        'order' : 900,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q9__answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Qualche consiglio per chi vorrebbe entrare nel mondo della moda?
        'question_block' : 'user_interview__model_pro',
        'question_code' : 'user_interview__model_pro__q10',
        'question_type' : 'text',
        'required' : 0,
        'order' : 1000,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_pro__q10__answer',
                'next_question_block' : False,
            },
        ],
    },
    ## question_block: user_interview__model_beginner
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q1',
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q1_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Com'è nata la tua passione per il mondo della moda?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q2',
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q2_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: La ragione principale per cui ti piacerebbe lavorare nel mondo della moda?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q3',
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q3_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q4',
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q4_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Ti piacerebbe diventare la nuova Miss...
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q5',
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q5_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: La tua giornata tipo?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q6',
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q6_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Lo/la stilista per cui vorresti sfilare?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q7',
        'question_type' : 'text',
        'required' : 0,
        'order' : 700,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q7_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: La tua modella ispiratrice?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q8',
        'question_type' : 'text',
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q8_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q9',
        'question_type' : 'text',
        'required' : 0,
        'order' : 900,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q9_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Colore preferito?
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q10',
        'question_type' : 'text',
        'required' : 0,
        'order' : 1000,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q10_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Convinci la gente a darti un voto
        'question_block' : 'user_interview__model_beginner',
        'question_code' : 'user_interview__model_beginner__q11',
        'question_type' : 'text',
        'required' : 0,
        'order' : 1100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__model_beginner__q11_answer',
                'next_question_block' : False,
            },
        ],
    },
    ## question_block: user_interview__photo_passionate
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'user_interview__photo_passionate',
        'question_code' : 'user_interview__photo_passionate__q1',
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__photo_passionate__q1_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: La tua giornata tipo?
        'question_block' : 'user_interview__photo_passionate',
        'question_code' : 'user_interview__photo_passionate__q2',
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__photo_passionate__q2_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'user_interview__photo_passionate',
        'question_code' : 'user_interview__photo_passionate__q3',
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__photo_passionate__q3_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Cosa ti appassiona di più della fotografia?
        'question_block' : 'user_interview__photo_passionate',
        'question_code' : 'user_interview__photo_passionate__q4',
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__photo_passionate__q4_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"?
        'question_block' : 'user_interview__photo_passionate',
        'question_code' : 'user_interview__photo_passionate__q5',
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__photo_passionate__q5_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Qual è il tuo genere fotografico preferito?
        'question_block' : 'user_interview__photo_passionate',
        'question_code' : 'user_interview__photo_passionate__q6',
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__photo_passionate__q6_answer',
                'next_question_block' : False,
            },
        ],
    },
    ## question_block: user_interview__fashion_passionate
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q1',
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q1_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Come è nata questa tua passione per il mondo della moda?
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q2',
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q2_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Cosa ti appassiona più nel mondo della moda?
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q3',
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q3_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Il tuo pregio più grande e il tuo "peggior" difetto?
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q4',
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q4_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"?
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q5',
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q5_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Il tuo stile preferito "giornaliero"?
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q6',
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q6_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Il tuo stile preferito "serale"?
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q7',
        'question_type' : 'text',
        'required' : 0,
        'order' : 700,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q7_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Convinci la gente a darti un voto
        'question_block' : 'user_interview__fashion_passionate',
        'question_code' : 'user_interview__fashion_passionate__q8',
        'question_type' : 'text',
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__fashion_passionate__q8_answer',
                'next_question_block' : False,
            },
        ],
    },
    ## question_block: user_interview__just_for_fun
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'user_interview__just_for_fun',
        'question_code' : 'user_interview__just_for_fun__q1',
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__just_for_fun__q1_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Il tuo pregio più grande e il tuo "peggior" difetto?
        'question_block' : 'user_interview__just_for_fun',
        'question_code' : 'user_interview__just_for_fun__q2',
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__just_for_fun__q2_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'user_interview__just_for_fun',
        'question_code' : 'user_interview__just_for_fun__q3',
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__just_for_fun__q3_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Una massima in cui ti rispecchi?
        'question_block' : 'user_interview__just_for_fun',
        'question_code' : 'user_interview__just_for_fun__q4',
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__just_for_fun__q4_answer',
                'next_question_block' : False,
            },
        ],
    },
    {
        # D: Convinci la gente a darti un voto
        'question_block' : 'user_interview__just_for_fun',
        'question_code' : 'user_interview__just_for_fun__q5',
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'user_interview__just_for_fun__q5_answer',
                'next_question_block' : False,
            },
        ],
    },
]
