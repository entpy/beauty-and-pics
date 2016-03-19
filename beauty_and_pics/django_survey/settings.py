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

### interview__block1
if (sono una modella/indossatrice/ragazza immagine professionista)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview__block1__block1
        D: Come è iniziata la tua avventura nel mondo della moda? ### interview__block1__block1
        D: Definisci quello che secondo te è la "bellezza"? ### interview__block1__block1
        D: Il tuo pregio più grande e il tuo "peggior" difetto? ### interview__block1__block1
        D: Quali sono i tuoi look preferiti? ### interview__block1__block1
        D: Una massima o un motto in cui ti rispecchi? ### interview__block1__block1
        if (Nutri altre passioni oltre al mondo della moda?) ### interview__block1__block2
            {
                D: Quali altre passioni nutri oltre al mondo della moda? ### interview__block1__block2__block1
            }
        D: La tua giornata tipo? ### interview__block1__block1
        if (Hai già partecipato a sfilate?) ### interview__block1__block3
            {
                D: A quali sfilate hai partecipato? ### interview__block1__block3__block1
                D: Il ricordo più bello della tua prima sfilata? ### interview__block1__block3__block1
        } else {
            if (C'è qualche stilista particolare per cui vorresti sfilare?) ### interview__block1__block3__block2
                {
                    D: per quale stilista vorresti sfilare? ### interview__block1__block3__block2__block1
                }
        }
        if (Hai già partecipato a qualche concorso/evento?) ### interview__block1__block4
            {
                D: A quali concorsi/eventi hai partecipato? ### interview__block1__block4__block1
                if (Hai già vinto qualche titolo?) ### interview__block1__block4__block2
                    {
                        D: Quale o quali titoli hai vinto? ### interview__block1__block4__block2__block1
                    }
        } else {
            if (C'è qualche concorso/evento a cui vorresti partecipare?) ### interview__block1__block4__block3
                {
                    D: A quale concorso/evento vorresti partecipare? ### interview__block1__block4__block3__block1
                }
        }
        D: Alcune persone che ritieni importanti con cui hai lavorato? ### interview__block1__block1
        D: E' stata dura arrivare ai tuoi risultati? ### interview__block1__block1
        D: Qualche consiglio per chi vorrebbe entrare nel mondo della moda? ### interview__block1__block1
    } else if (sono una modella/indossatrice/ragazza immagine esordiente)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview__block1__block200
        D: Com'è nata la tua passione per il mondo della moda? ### interview__block1__block200
        D: La ragione principale per cui ti piacerebbe lavorare nel mondo della moda? ### interview__block1__block200
        D: Definisci quello che secondo te è la "bellezza"? ### interview__block1__block200
        D: Ti piacerebbe diventare la nuova Miss... ### interview__block1__block200
        if (Nutri altre passioni oltre al mondo della moda?) { ### interview__block1__block300
            D: Quali altre passioni nutri oltre al mondo della moda? ### interview__block1__block300__block1
        }
        D: La tua giornata tipo? ### interview__block1__block200
        D: Lo/la stilista per cui vorresti sfilare? ### interview__block1__block200
        D: La tua modella ispiratrice? ### interview__block1__block200
        D: Quali sono i tuoi look preferiti? ### interview__block1__block200
        D: Colore preferito ### interview__block1__block200
        D: Convinci la gente a darti un voto ### interview__block1__block200
    } else if (sono un'appassionata di fotografia)
    {
        Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview__block1__block400
        D: La tua giornata tipo? ### interview__block1__block400
        D: Quali sono i tuoi look preferiti? ### interview__block1__block400
        D: Cosa ti appassiona di più della fotografia? ### interview__block1__block400
        D: Definisci quello che secondo te è la "bellezza"? ### interview__block1__block400
        D: Qual è il tuo genere fotografico preferito? ### interview__block1__block400
        if (Hai qualche hobby oltre alla fotografia?) { ### interview__block1__block500
            D: Qual'è il tuo hobby? ### interview__block1__block500__block1
        }
        D: Convinci la gente a darti un voto ### interview__block1__block400
    } else if (sono un'appassionata di moda)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview__block1__block600
        D: Come è nata questa tua passione per il mondo della moda? ### interview__block1__block600
        D: Cosa ti appassiona più nel mondo della moda? ### interview__block1__block600
        if (Nutri altre passioni oltre al mondo della moda?) { ### interview__block1__block700
            D: Quali altre passioni nutri oltre al mondo della moda? ### interview__block1__block700__block1
        }
        D: Il tuo pregio più grande e il tuo "peggior" difetto? ### interview__block1__block600
        D: Definisci quello che secondo te è la "bellezza"? ### interview__block1__block600
        D: Il tuo stile preferito "giornaliero"? ### interview__block1__block600
        D: Il tuo stile preferito "serale"? ### interview__block1__block600
        D: Convinci la gente a darti un voto ### interview__block1__block600
    } else if (partecipo solo per divertimento/altro)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview__block1__block800
        D: Il tuo pregio più grande e il tuo "peggior" difetto? ### interview__block1__block800
        D: Quali sono i tuoi look preferiti? ### interview__block1__block800
        if (Hai qualche hobby?) { ### interview__block1__block900
            D: Qual'è il tuo hobby? ### interview__block1__block900__block1
        }
        D: Una massima in cui ti rispecchi? ### interview__block1__block800
        D: Convinci la gente a darti un voto ### interview__block1__block800
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
DS_SURVEY = [
    {
	'survey_code' : 'interview',
	'validation_required' : True,
    }
]

# elenco di domande per ogni blocco
DS_QUESTIONS_AND_SELECTABLE_ANSWERS = {
    'interview' : [
    {
        # D: Seleziona una categoria
        'question_block' : 'interview__block1',
        'question_code' : 'interview__block1__q1',
	'block_level' : 1,
	# massimo 5 livelli di profondità
	'block_code_level_1': False,
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'select',
        'required' : 1,
        'order' : 0,
        'default_hidden' : 0,
        'answers' : [
            {
                # Sono una modella/ragazza immagine/indossatrice professionista
                'answer_code' : 'interview__block1__q1__a1',
                'next_question_block_1' : 'interview__block1__block1', # children flat block questions
                'next_question_block_2' : 'interview__block1__block2', # Nutri altre passioni oltre al mondo della moda?
                'next_question_block_3' : 'interview__block1__block3', # Hai già partecipato a sfilate?
                'next_question_block_4' : 'interview__block1__block4', # Hai già partecipato a qualche concorso/evento?
                'next_question_block_5' : False,
		'order' : 0,
            },
            {
                # Sono una modella/ragazza immagine/indossatrice emergente
                'answer_code' : 'interview__block1__q1__a2',
                'next_question_block_1' : 'interview__block1__block200', # children flat block questions
                'next_question_block_2' : 'interview__block1__block300', # Nutri altre passioni oltre al mondo della moda?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 10,
            },
            {
                # Sono appassionata di foto
                'answer_code' : 'user_interview__block1__q1__a3',
                'next_question_block_1' : 'interview__block1__block400', # children flat block questions
                'next_question_block_2' : 'interview__block1__block500', # Nutri altre passioni oltre al mondo della moda?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 20,
            },
            {
                # Sono appassionata di moda
                'answer_code' : 'user_interview__block1__q1__a4',
                'next_question_block_1' : 'interview__block1__block600', # children flat block questions
                'next_question_block_2' : 'interview__block1__block700', # Nutri altre passioni oltre al mondo della moda?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 30,
            },
            {
                # Solo per divertimento/altro
                'answer_code' : 'user_interview__block1__q1__a5',
                'next_question_block_1' : 'interview__block1__block800', # children flat block questions
                'next_question_block_2' : 'interview__block1__block900', # Hai qualche hobby?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 40,
            },
        ],
    },
    ## question_block: user_interview__model_pro
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q1',
	'block_level' : 2,
	# massimo 5 livelli di profondità
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q1__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Come è iniziata la tua avventura nel mondo della moda?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q2',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q2__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q3',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q3__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Il tuo pregio più grande e il tuo "peggior" difetto?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q4',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q4__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q5',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q5__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Una massima o un motto in cui ti rispecchi?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q6',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q6__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block2 {{{
    {
	# Nutri altre passioni oltre al mondo della moda?
        'question_block' : 'interview__block1__block2',
        'question_code' : 'interview__block1__block2__q7',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'select',
        'required' : 0,
        'order' : 650,
        'default_hidden' : 1,
        'answers' : [
            {
                # Si
                'answer_code' : 'interview__block1__block2__q7__a1',
                'next_question_block_1' : 'interview__block1__block2__block1',
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
            {
                # No
                'answer_code' : 'interview__block1__block2__q7__a2',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 10,
            },
        ],
    },
    {
        # Quali altre passioni nutri oltre al mondo della moda?
        'survey' : 'interview',
        'question_block' : 'interview__block1__block2__block1',
        'question_code' : 'interview__block1__block2__block1__q1',
        'block_level' : 3,
        'block_code_level_1': 'interview__block1',
        'block_code_level_2': 'interview__block1__block2',
        'block_code_level_3': False, 
        'block_code_level_4': False,
        'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 651,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block2__block1__q1__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block2 }}}
    {
        # D: La tua giornata tipo?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q8',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 700,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q8__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block3 {{{
    {
	# Hai già partecipato a sfilate?
        'survey' : 'interview',
        'question_block' : 'interview__block1__block3',
        'question_code' : 'interview__block1__block3__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'select',
        'required' : 0,
        'order' : 653,
        'default_hidden' : 1,
        'answers' : [
            {
                # Si
                'answer_code' : 'interview__block1__block3__q1__a1',
                'next_question_block_1' : 'interview__block1__block3__block1', # A quali sfilate hai partecipato? / Il ricordo più bello della tua prima sfilata?
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
            {
                # No
                'answer_code' : 'interview__block1__block3__q1__a2',
                'next_question_block_1' : 'interview__block1__block3__block2', # C'è qualche stilista particolare per cui vorresti sfilare?
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 10,
            },
        ],
    },
        # Si {{{
        {
            # A quali sfilate hai partecipato?
            'survey' : 'interview',
            'question_block' : 'interview__block1__block3__block1',
            'question_code' : 'interview__block1__block3__block1__q1',
            'block_level' : 3,
            'block_code_level_1': 'interview__block1',
            'block_code_level_2': 'interview__block1__block3',
            'block_code_level_3': False, 
            'block_code_level_4': False,
            'block_code_level_5': False,
            'question_type' : 'text',
            'required' : 0,
            'order' : 654,
            'default_hidden' : 1,
            'answers' : [
                {
                    'answer_code' : 'interview__block1__block3__block1__q1__a1',
                    'next_question_block_1' : False,
                    'next_question_block_2' : False,
                    'next_question_block_3' : False,
                    'next_question_block_4' : False,
                    'next_question_block_5' : False,
		    'order' : 0,
                },
            ],
        },
        {
            # Il ricordo più bello della tua prima sfilata?
            'survey' : 'interview',
            'question_block' : 'interview__block1__block3__block1',
            'question_code' : 'interview__block1__block3__block1__q2',
            'block_level' : 3,
            'block_code_level_1': 'interview__block1',
            'block_code_level_2': 'interview__block1__block3',
            'block_code_level_3': False, 
            'block_code_level_4': False,
            'block_code_level_5': False,
            'question_type' : 'text',
            'required' : 0,
            'order' : 655,
            'default_hidden' : 1,
            'answers' : [
                {
                    'answer_code' : 'interview__block1__block3__block1__q2__a1',
                    'next_question_block_1' : False,
                    'next_question_block_2' : False,
                    'next_question_block_3' : False,
                    'next_question_block_4' : False,
                    'next_question_block_5' : False,
		    'order' : 0,
                },
            ],
        },
        # Si }}}
        # No {{{
            {
                # C'è qualche stilista particolare per cui vorresti sfilare?
                'survey' : 'interview',
                'question_block' : 'interview__block1__block3__block2',
                'question_code' : 'interview__block1__block3__block2__q1',
                'block_level' : 3,
                'block_code_level_1': 'interview__block1',
                'block_code_level_2': 'interview__block1__block3',
                'block_code_level_3': False, 
                'block_code_level_4': False,
                'block_code_level_5': False,
                'question_type' : 'select',
                'required' : 0,
                'order' : 656,
                'default_hidden' : 1,
                'answers' : [
                    {
                        # Si
                        'answer_code' : 'interview__block1__block3__block2__q1__a1',
                        'next_question_block_1' : 'interview__block1__block3__block2__block1',
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 0,
                    },
                    {
                        # No
                        'answer_code' : 'interview__block1__block3__block2__q1__a2',
                        'next_question_block_1' : False,
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 10,
                    },
                ],
            },
            # Si {{{
                {
                    # Per quale stilista vorresti sfilare?
                    'survey' : 'interview',
                    'question_block' : 'interview__block1__block3__block2__block1',
                    'question_code' : 'interview__block1__block3__block2__block1__q1',
                    'block_level' : 4,
                    'block_code_level_1': 'interview__block1',
                    'block_code_level_2': 'interview__block1__block3',
                    'block_code_level_3': 'interview__block1__block3__block2', 
                    'block_code_level_4': False,
                    'block_code_level_5': False,
                    'question_type' : 'text',
                    'required' : 0,
                    'order' : 657,
                    'default_hidden' : 1,
                    'answers' : [
                        {
                            'answer_code' : 'interview__block1__block3__block2__block1__q1__a1',
                            'next_question_block_1' : False,
                            'next_question_block_2' : False,
                            'next_question_block_3' : False,
                            'next_question_block_4' : False,
                            'next_question_block_5' : False,
			    'order' : 0,
                        },
                    ],
                },
            # Si }}}
        # No }}}
    # interview__block1__block3 }}}

    # interview__block1__block4 {{{
    {
	# Hai già partecipato a qualche concorso/evento?
        'survey' : 'interview',
        'question_block' : 'interview__block1__block4',
        'question_code' : 'interview__block1__block4__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'select',
        'required' : 0,
        'order' : 658,
        'default_hidden' : 1,
        'answers' : [
            {
                # Si
                'answer_code' : 'interview__block1__block4__q1__a1',
                'next_question_block_1' : 'interview__block1__block4__block1',
                'next_question_block_2' : 'interview__block1__block4__block2',
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
            {
                # No
                'answer_code' : 'interview__block1__block1__block4__q1__a2',
                'next_question_block_1' : 'interview__block1__block4__block3',
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 10,
            },
        ],
    },
    # Si {{{
        {
            # A quali concorsi/eventi hai partecipato?
            'survey' : 'interview',
            'question_block' : 'interview__block1__block4__block1',
            'question_code' : 'interview__block1__block4__block1__q1',
            'block_level' : 3,
            'block_code_level_1': 'interview__block1',
            'block_code_level_2': 'interview__block1__block4',
            'block_code_level_3': False, 
            'block_code_level_4': False,
            'block_code_level_5': False,
            'question_type' : 'text',
            'required' : 0,
            'order' : 659,
            'default_hidden' : 1,
            'answers' : [
                {
                    'answer_code' : 'interview__block1__block4__block1__q1__a1',
		    'next_question_block_1' : False,
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 0,
                },
            ],
        },
        # interview__block1__block4__block2 {{{
            {
                # Hai già vinto qualche titolo?
                'survey' : 'interview',
                'question_block' : 'interview__block1__block4__block2',
                'question_code' : 'interview__block1__block4__block2__q1',
                'block_level' : 3,
                'block_code_level_1': 'interview__block1',
                'block_code_level_2': 'interview__block1__block4',
                'block_code_level_3': False, 
                'block_code_level_4': False,
                'block_code_level_5': False,
                'question_type' : 'select',
                'required' : 0,
                'order' : 660,
                'default_hidden' : 1,
                'answers' : [
                    {
                        # Si
                        'answer_code' : 'interview__block1__block4__block2__q1__a1',
                        'next_question_block_1' : 'interview__block1__block4__block2__block1', # Quale o quali titoli hai vinto?
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 0,
                    },
                    {
                        # No
                        'answer_code' : 'interview__block1__block4__block2__q1__a2',
                        'next_question_block_1' : False,
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 10,
                    },
                ],
            },
            # Si {{{
                {
                    # Quale o quali titoli hai vinto?
                    'survey' : 'interview',
                    'question_block' : 'interview__block1__block4__block2__block1',
                    'question_code' : 'interview__block1__block4__block2__block1__q1',
                    'block_level' : 4,
                    'block_code_level_1': 'interview__block1',
                    'block_code_level_2': 'interview__block1__block4',
                    'block_code_level_3': 'interview__block1__block4__block2', 
                    'block_code_level_4': False,
                    'block_code_level_5': False,
                    'question_type' : 'text',
                    'required' : 0,
                    'order' : 661,
                    'default_hidden' : 1,
                    'answers' : [
                        {
                            'answer_code' : 'interview__block1__block4__block2__block1__q1__a1',
                            'next_question_block_1' : False,
                            'next_question_block_2' : False,
                            'next_question_block_3' : False,
                            'next_question_block_4' : False,
                            'next_question_block_5' : False,
			    'order' : 0,
                        },
                    ],
                },
            # Si }}}
        # interview__block1__block4__block2 }}}
    # Si }}}
    # No {{{
        # interview__block1__block4__block3 {{{ C'è qualche concorso/evento a cui vorresti partecipare?
            {
                # C'è qualche concorso/evento a cui vorresti partecipare?
                'survey' : 'interview',
                'question_block' : 'interview__block1__block4__block3',
                'question_code' : 'interview__block1__block4__block3__q1',
                'block_level' : 3,
                'block_code_level_1': 'interview__block1',
                'block_code_level_2': 'interview__block1__block4',
                'block_code_level_3': False, 
                'block_code_level_4': False,
                'block_code_level_5': False,
                'question_type' : 'select',
                'required' : 0,
                'order' : 662,
                'default_hidden' : 1,
                'answers' : [
                    {
                        # Si
                        'answer_code' : 'interview__block1__block4__block3__q1__a1',
                        'next_question_block_1' : 'interview__block1__block4__block3__block1',
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 0,
                    },
                    {
                        # No
                        'answer_code' : 'interview__block1__block4__block3__q1__a2',
                        'next_question_block_1' : False,
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 10,
                    },
                ],
            },
            # Si {{{
                {
                    # A quale concorso/evento vorresti partecipare?
                    'survey' : 'interview',
                    'question_block' : 'interview__block1__block4__block3__block1',
                    'question_code' : 'interview__block1__block4__block3__block1__q1',
                    'block_level' : 4,
                    'block_code_level_1': 'interview__block1',
                    'block_code_level_2': 'interview__block1__block4',
                    'block_code_level_3': 'interview__block1__block4__block3', 
                    'block_code_level_4': False,
                    'block_code_level_5': False,
                    'question_type' : 'text',
                    'required' : 0,
                    'order' : 663,
                    'default_hidden' : 1,
                    'answers' : [
                        {
                            'answer_code' : 'interview__block1__block4__block3__block1__q1__a1',
                            'next_question_block_1' : False,
                            'next_question_block_2' : False,
                            'next_question_block_3' : False,
                            'next_question_block_4' : False,
                            'next_question_block_5' : False,
			    'order' : 0,
                        },
                    ],
                },
            # Si }}}
        # interview__block1__block4__block3 }}}
    # No }}}
    # interview__block1__block4 }}}
    {
        # D: Alcune persone che ritieni importanti con cui hai lavorato?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q11',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q11__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: E' stata dura arrivare ai tuoi risultati?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q12',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 900,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q12__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Qualche consiglio per chi vorrebbe entrare nel mondo della moda?
        'question_block' : 'interview__block1__block1',
        'question_code' : 'interview__block1__block1__q13',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 1000,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block1__q13__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    ## question_block: user_interview__model_beginner
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q1__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Com'è nata la tua passione per il mondo della moda?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q2',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q2__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: La ragione principale per cui ti piacerebbe lavorare nel mondo della moda?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q3',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q3__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q4',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q4__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Ti piacerebbe diventare la nuova Miss...
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q5',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q5__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: La tua giornata tipo?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q6',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q6__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block300 {{{
    {
	# Nutri altre passioni oltre al mondo della moda?
        'question_block' : 'interview__block1__block300',
        'question_code' : 'interview__block1__block300__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'select',
        'required' : 0,
        'order' : 650,
        'default_hidden' : 1,
        'answers' : [
            {
                # Si
                'answer_code' : 'interview__block1__block300__q1__a1',
                'next_question_block_1' : 'interview__block1__block300__block1',
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
            {
                # No
                'answer_code' : 'interview__block1__block300__q1__a2',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 10,
            },
        ],
    },
        # Si {{{
            {
                # Quali altre passioni nutri oltre al mondo della moda?
                'question_block' : 'interview__block1__block300__block1',
                'question_code' : 'interview__block1__block300__block1__q1',
                'block_level' : 3,
                'block_code_level_1': 'interview__block1',
                'block_code_level_2': 'interview__block1__block300',
                'block_code_level_3': False, 
                'block_code_level_4': False,
                'block_code_level_5': False,
                'question_type' : 'text',
                'required' : 0,
                'order' : 651,
                'default_hidden' : 1,
                'answers' : [
                    {
                        'answer_code' : 'interview__block1__block300__block1__q1__a1',
                        'next_question_block_1' : False,
                        'next_question_block_2' : False,
                        'next_question_block_3' : False,
                        'next_question_block_4' : False,
                        'next_question_block_5' : False,
			'order' : 0,
                    },
                ],
            },
        # Si }}}
    # interview__block1__block300 }}}
    {
        # D: Lo/la stilista per cui vorresti sfilare?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q7',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 700,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q7__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: La tua modella ispiratrice?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q8',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q8__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q9',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 900,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q9__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Colore preferito?
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q10',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 1000,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q10__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Convinci la gente a darti un voto
        'question_block' : 'interview__block1__block200',
        'question_code' : 'interview__block1__block200__q11',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 1100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block200__q11__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    ## question_block: user_interview__photo_passionate
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'interview__block1__block400',
        'question_code' : 'interview__block1__block400__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block400__q1__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: La tua giornata tipo?
        'question_block' : 'interview__block1__block400',
        'question_code' : 'interview__block1__block400__q2',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block400__q2__a2',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'interview__block1__block400',
        'question_code' : 'interview__block1__block400__q3',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block400__q3__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Cosa ti appassiona di più della fotografia?
        'question_block' : 'interview__block1__block400',
        'question_code' : 'interview__block1__block400__q4',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block400__q4__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"?
        'question_block' : 'interview__block1__block400',
        'question_code' : 'interview__block1__block400__q5',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block400__q5__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Qual è il tuo genere fotografico preferito?
        'question_block' : 'interview__block1__block400',
        'question_code' : 'interview__block1__block400__q6',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block400__q6__a1',
                'next_question_block_1' : False,
                'next_question_block_2' : False,
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block500 {{{
	{
	    # Hai qualche hobby oltre alla fotografia?
	    'question_block' : 'interview__block1__block500',
	    'question_code' : 'interview__block1__block500__q1',
	    'block_level' : 2,
	    'block_code_level_1': 'interview__block1',
	    'block_code_level_2': False,
	    'block_code_level_3': False, 
	    'block_code_level_4': False,
	    'block_code_level_5': False,
	    'question_type' : 'select',
	    'required' : 0,
	    'order' : 650,
	    'default_hidden' : 1,
	    'answers' : [
		{
		    # Si
		    'answer_code' : 'interview__block1__block500__q1__a1',
		    'next_question_block_1' : 'interview__block1__block500__block1',
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 0,
		},
		{
		    # No
		    'answer_code' : 'interview__block1__block500__q1__a2',
		    'next_question_block_1' : False,
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 10,
		},
	    ],
	},
	# Si {{{
	    {
		# Qual'è il tuo hobby?
		'question_block' : 'interview__block1__block500__block1',
		'question_code' : 'interview__block1__block500__block1__q1',
		'block_level' : 3,
		'block_code_level_1': 'interview__block1',
		'block_code_level_2': 'interview__block1__block500',
		'block_code_level_3': False, 
		'block_code_level_4': False,
		'block_code_level_5': False,
		'question_type' : 'text',
		'required' : 0,
		'order' : 651,
		'default_hidden' : 1,
		'answers' : [
		    {
			'answer_code' : 'interview__block1__block500__block1__q1__a1',
			'next_question_block_1' : False,
			'next_question_block_2' : False,
			'next_question_block_3' : False,
			'next_question_block_4' : False,
			'next_question_block_5' : False,
			'order' : 0,
		    },
		],
	    },
	# Si }}}
    # interview__block1__block500 }}}
    ## question_block: user_interview__fashion_passionate
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q1__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Come è nata questa tua passione per il mondo della moda?
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q2',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q2__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Cosa ti appassiona più nel mondo della moda?
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q3',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q3__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Il tuo pregio più grande e il tuo "peggior" difetto?
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q4',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q4__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Definisci quello che secondo te è la "bellezza"?
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q5',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q5__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block700 {{{
	{
	    # Nutri altre passioni oltre al mondo della moda?
	    'question_block' : 'interview__block1__block700',
	    'question_code' : 'interview__block1__block700__q1',
	    'block_level' : 2,
	    'block_code_level_1': 'interview__block1',
	    'block_code_level_2': False,
	    'block_code_level_3': False, 
	    'block_code_level_4': False,
	    'block_code_level_5': False,
	    'question_type' : 'select',
	    'required' : 0,
	    'order' : 650,
	    'default_hidden' : 1,
	    'answers' : [
		{
		    # Si
		    'answer_code' : 'interview__block1__block700__q1__a1',
		    'next_question_block_1' : 'interview__block1__block700__block1',
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 0,
		},
		{
		    # No
		    'answer_code' : 'interview__block1__block700__q1__a2',
		    'next_question_block_1' : False,
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 10,
		},
	    ],
	},
	# Si {{{
	    {
		# Quali altre passioni nutri oltre al mondo della moda?
		'question_block' : 'interview__block1__block700__block1',
		'question_code' : 'interview__block1__block700__block1__q1',
		'block_level' : 3,
		'block_code_level_1': 'interview__block1',
		'block_code_level_2': 'interview__block1__block700',
		'block_code_level_3': False, 
		'block_code_level_4': False,
		'block_code_level_5': False,
		'question_type' : 'text',
		'required' : 0,
		'order' : 651,
		'default_hidden' : 1,
		'answers' : [
		    {
			'answer_code' : 'interview__block1__block700__block1__q1',
			'next_question_block_1' : False,
			'next_question_block_2' : False,
			'next_question_block_3' : False,
			'next_question_block_4' : False,
			'next_question_block_5' : False,
			'order' : 0,
		    },
		],
	    },
	# Si }}}
    # interview__block1__block700 }}}
    {
        # D: Il tuo stile preferito "giornaliero"?
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q6',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 600,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q6__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Il tuo stile preferito "serale"?
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q7',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 700,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q7__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Convinci la gente a darti un voto
        'question_block' : 'interview__block1__block600',
        'question_code' : 'interview__block1__block600__q8',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 800,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block600__q8__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    ## question_block: user_interview__just_for_fun
    {
        # D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni
        'question_block' : 'interview__block1__block800',
        'question_code' : 'interview__block1__block800__q1',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 100,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block800__q1__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Il tuo pregio più grande e il tuo "peggior" difetto?
        'question_block' : 'interview__block1__block800',
        'question_code' : 'interview__block1__block800__q2',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 200,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block800__q2__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Quali sono i tuoi look preferiti?
        'question_block' : 'interview__block1__block800',
        'question_code' : 'interview__block1__block800__q3',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 300,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block800__q3__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    # interview__block1__block900 {{{
	{
	    # Hai qualche hobby?
	    'question_block' : 'interview__block1__block900',
	    'question_code' : 'interview__block1__block900__q1',
	    'block_level' : 2,
	    'block_code_level_1': 'interview__block1',
	    'block_code_level_2': False,
	    'block_code_level_3': False, 
	    'block_code_level_4': False,
	    'block_code_level_5': False,
	    'question_type' : 'select',
	    'required' : 0,
	    'order' : 350,
	    'default_hidden' : 1,
	    'answers' : [
		{
		    # Si
		    'answer_code' : 'interview__block1__block900__q1__a1',
		    'next_question_block_1' : 'interview__block1__block900__block1',
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 0,
		},
		{
		    # No
		    'answer_code' : 'interview__block1__block900__q1__a2',
		    'next_question_block_1' : False,
		    'next_question_block_2' : False,
		    'next_question_block_3' : False,
		    'next_question_block_4' : False,
		    'next_question_block_5' : False,
		    'order' : 10,
		},
	    ],
	},
	# Si {{{
	    {
		# Qual'è il tuo hobby?
		'question_block' : 'interview__block1__block900__block1',
		'question_code' : 'interview__block1__block900__block1__q1',
		'block_level' : 3,
		'block_code_level_1': 'interview__block1',
		'block_code_level_2': 'interview__block1__block900',
		'block_code_level_3': False, 
		'block_code_level_4': False,
		'block_code_level_5': False,
		'question_type' : 'text',
		'required' : 0,
		'order' : 351,
		'default_hidden' : 1,
		'answers' : [
		    {
			'answer_code' : 'interview__block1__block900__block1__q1__a1',
			'next_question_block_1' : False,
			'next_question_block_2' : False,
			'next_question_block_3' : False,
			'next_question_block_4' : False,
			'next_question_block_5' : False,
			'order' : 0,
		    },
		],
	    },
	# Si }}}
    # interview__block1__block900 }}}
    {
        # D: Una massima in cui ti rispecchi?
        'question_block' : 'interview__block1__block800',
        'question_code' : 'interview__block1__block800__q4',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 400,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block800__q4__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
    {
        # D: Convinci la gente a darti un voto
        'question_block' : 'interview__block1__block800',
        'question_code' : 'interview__block1__block800__q5',
	'block_level' : 2,
	'block_code_level_1': 'interview__block1',
	'block_code_level_2': False,
	'block_code_level_3': False, 
	'block_code_level_4': False,
	'block_code_level_5': False,
        'question_type' : 'text',
        'required' : 0,
        'order' : 500,
        'default_hidden' : 1,
        'answers' : [
            {
                'answer_code' : 'interview__block1__block800__q5__a1',
		'next_question_block_1' : False,
		'next_question_block_2' : False,
		'next_question_block_3' : False,
		'next_question_block_4' : False,
		'next_question_block_5' : False,
		'order' : 0,
            },
        ],
    },
]}

"""
### questions
"interview__block1__q1"
"interview__block1__block1__q1"
"interview__block1__block1__q2"
"interview__block1__block1__q3"
"interview__block1__block1__q4"
"interview__block1__block1__q5"
"interview__block1__block1__q6"
"interview__block1__block2__q7"
"interview__block1__block2__block1__q1"
"interview__block1__block1__q8"
"interview__block1__block3__q1"
"interview__block1__block3__block1__q1"
"interview__block1__block3__block1__q2"
"interview__block1__block3__block2__q1"
"interview__block1__block3__block2__block1__q1"
"interview__block1__block4__q1"
"interview__block1__block4__block1__q1"
"interview__block1__block4__block2__q1"
"interview__block1__block4__block2__block1__q1"
"interview__block1__block4__block3__q1"
"interview__block1__block4__block3__block1__q1"
"interview__block1__block1__q11"
"interview__block1__block1__q12"
"interview__block1__block1__q13"
"interview__block1__block200__q1"
"interview__block1__block200__q2"
"interview__block1__block200__q3"
"interview__block1__block200__q4"
"interview__block1__block200__q5"
"interview__block1__block200__q6"
"interview__block1__block300__q1"
"interview__block1__block300__block1__q1"
"interview__block1__block200__q7"
"interview__block1__block200__q8"
"interview__block1__block200__q9"
"interview__block1__block200__q10"
"interview__block1__block200__q11"
"interview__block1__block400__q1"
"interview__block1__block400__q2"
"interview__block1__block400__q3"
"interview__block1__block400__q4"
"interview__block1__block400__q5"
"interview__block1__block400__q6"
"interview__block1__block500__q1"
"interview__block1__block500__block1__q1"
"interview__block1__block600__q1"
"interview__block1__block600__q2"
"interview__block1__block600__q3"
"interview__block1__block600__q4"
"interview__block1__block600__q5"
"interview__block1__block700__q1"
"interview__block1__block700__block1__q1"
"interview__block1__block600__q6"
"interview__block1__block600__q7"
"interview__block1__block600__q8"
"interview__block1__block800__q1"
"interview__block1__block800__q2"
"interview__block1__block800__q3"
"interview__block1__block900__q1"
"interview__block1__block900__block1__q1"
"interview__block1__block800__q4"
"interview__block1__block800__q5"
### answers
"interview__block1__q1__a1"
"interview__block1__q1__a2"
"user_interview__block1__q1__a3"
"user_interview__block1__q1__a4"
"user_interview__block1__q1__a5"
"interview__block1__block1__q1__a1"
"interview__block1__block1__q2__a1"
"interview__block1__block1__q3__a1"
"interview__block1__block1__q4__a1"
"interview__block1__block1__q5__a1"
"interview__block1__block1__q6__a1"
"interview__block1__block2__q7__a1"
"interview__block1__block2__q7__a2"
"interview__block1__block2__block1__q1__a1"
"interview__block1__block1__q8__a1"
"interview__block1__block3__q1__a1"
"interview__block1__block3__q1__a2"
"interview__block1__block3__block1__q1__a1"
"interview__block1__block3__block1__q2__a1"
"interview__block1__block3__block2__q1__a1"
"interview__block1__block3__block2__q1__a2"
"interview__block1__block3__block2__block1__q1__a1"
"interview__block1__block4__q1__a1"
"interview__block1__block1__block4__q1__a2"
"interview__block1__block4__block1__q1__a1"
"interview__block1__block4__block2__q1__a1"
"interview__block1__block4__block2__q1__a2"
"interview__block1__block4__block2__block1__q1__a1"
"interview__block1__block4__block3__q1__a1"
"interview__block1__block4__block3__q1__a2"
"interview__block1__block4__block3__block1__q1__a1"
"interview__block1__block1__q11__a1"
"interview__block1__block1__q12__a1"
"interview__block1__block1__q13__a1"
"interview__block1__block200__q1__a1"
"interview__block1__block200__q2__a1"
"interview__block1__block200__q3__a1"
"interview__block1__block200__q4__a1"
"interview__block1__block200__q5__a1"
"interview__block1__block200__q6__a1"
"interview__block1__block300__q1__a1"
"interview__block1__block300__q1__a2"
"interview__block1__block300__block1__q1__a1"
"interview__block1__block200__q7__a1"
"interview__block1__block200__q8__a1"
"interview__block1__block200__q9__a1"
"interview__block1__block200__q10__a1"
"interview__block1__block200__q11__a1"
"interview__block1__block400__q1__a1"
"interview__block1__block400__q2__a2"
"interview__block1__block400__q3__a1"
"interview__block1__block400__q4__a1"
"interview__block1__block400__q5__a1"
"interview__block1__block400__q6__a1"
"interview__block1__block500__q1__a1"
"interview__block1__block500__q1__a2"
"interview__block1__block500__block1__q1__a1"
"interview__block1__block600__q1__a1"
"interview__block1__block600__q2__a1"
"interview__block1__block600__q3__a1"
"interview__block1__block600__q4__a1"
"interview__block1__block600__q5__a1"
"interview__block1__block700__q1__a1"
"interview__block1__block700__q1__a2"
"interview__block1__block700__block1__q1"
"interview__block1__block600__q6__a1"
"interview__block1__block600__q7__a1"
"interview__block1__block600__q8__a1"
"interview__block1__block800__q1__a1"
"interview__block1__block800__q2__a1"
"interview__block1__block800__q3__a1"
"interview__block1__block900__q1__a1"
"interview__block1__block900__q1__a2"
"interview__block1__block900__block1__q1__a1"
"interview__block1__block800__q4__a1"
"interview__block1__block800__q5__a1"

DS__QUESTIONS_ANSWERS_LABEL = {
    # survey about_user
    'about_user_000' : {
        'question_text_woman' : 'Dicci qualcosa di te',
        'question_text_man' : 'Dicci qualcosa di te',
        'question_hint_woman' : 'Descrivi dove sei nata, chi sei e le tue passioni',
        'question_hint_man' : 'Descrivi dove sei nato, chi sei e le tue passioni',
    },
"""
