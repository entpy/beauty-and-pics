# -*- coding: utf-8 -*-

"""
Settings for 'django_survey' app
"""

"""
user_identify
model_pro
model_beginner
fashion_passionate
just_for_fun

### interview_block1
if (sono una modella/indossatrice/ragazza immagine professionista)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview_block1_block1
        D: Come è iniziata la tua avventura nel mondo della moda? ### interview_block1_block1
        D: Definisci quello che secondo te è la "bellezza"? ### interview_block1_block1
        D: Il tuo pregio più grande e il tuo "peggior" difetto? ### interview_block1_block1
        D: Quali sono i tuoi look preferiti? ### interview_block1_block1
        D: Una massima o un motto in cui ti rispecchi? ### interview_block1_block1
        if (Nutri altre passioni oltre al mondo della moda?) ### interview_block1_block2
            {
                D: Quali altre passioni nutri oltre al mondo della moda? ### interview_block1_block2_block1
            }
        D: La tua giornata tipo? ### interview_block1_block1
        if (Hai già partecipato a sfilate?) ### interview_block1_block3
            {
                D: A quali sfilate hai partecipato? ### interview_block1_block3_block1
                D: Il ricordo più bello della tua prima sfilata? ### interview_block1_block3_block1
        } else {
            if (C'è qualche stilista particolare per cui vorresti sfilare?) ### interview_block1_block3_block2
                {
                    D: per quale stilista vorresti sfilare? ### interview_block1_block3_block2_block1
                }
        }
        if (Hai già partecipato a qualche concorso/evento?) ### interview_block1_block4
            {
                D: A quali concorsi/eventi hai partecipato? ### interview_block1_block4_block1
                if (Hai già vinto qualche titolo?) ### interview_block1_block4_block2
                    {
                        D: Quale o quali titoli hai vinto? ### interview_block1_block4_block2_block1
                    }
        } else {
            if (C'è qualche concorso/evento a cui vorresti partecipare?) ### interview_block1_block4_block3
                {
                    D: A quale concorso/evento vorresti partecipare? ### interview_block1_block4_block3_block1
                }
        }
        D: Alcune persone che ritieni importanti con cui hai lavorato? ### interview_block1_block1
        D: E' stata dura arrivare ai tuoi risultati? ### interview_block1_block1
        D: Qualche consiglio per chi vorrebbe entrare nel mondo della moda? ### interview_block1_block1
    } else if (sono una modella/indossatrice/ragazza immagine esordiente)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview_block1_block200
        D: Com'è nata la tua passione per il mondo della moda? ### interview_block1_block200
        D: La ragione principale per cui ti piacerebbe lavorare nel mondo della moda? ### interview_block1_block200
        D: Definisci quello che secondo te è la "bellezza"? ### interview_block1_block200
        D: Ti piacerebbe diventare la nuova Miss... ### interview_block1_block200
        if (Nutri altre passioni oltre al mondo della moda?) { ### interview_block1_block300
            D: Quali altre passioni nutri oltre al mondo della moda? ### interview_block1_block300_block1
        }
        D: La tua giornata tipo? ### interview_block1_block200
        D: Lo/la stilista per cui vorresti sfilare? ### interview_block1_block200
        D: La tua modella ispiratrice? ### interview_block1_block200
        D: Quali sono i tuoi look preferiti? ### interview_block1_block200
        D: Colore preferito ### interview_block1_block200
        D: Convinci la gente a darti un voto ### interview_block1_block200
    } else if (sono un'appassionata di fotografia)
    {
        Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview_block1_block400
        D: La tua giornata tipo? ### interview_block1_block400
        D: Quali sono i tuoi look preferiti? ### interview_block1_block400
        D: Cosa ti appassiona di più della fotografia? ### interview_block1_block400
        D: Definisci quello che secondo te è la "bellezza"? ### interview_block1_block400
        D: Qual è il tuo genere fotografico preferito? ### interview_block1_block400
        if (Hai qualche hobby oltre alla fotografia?) { ### interview_block1_block500
            D: Qual'è il tuo hobby? ### interview_block1_block500_block1
        }
        D: Convinci la gente a darti un voto ### interview_block1_block400
    } else if (sono un'appassionata di moda)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview_block1_block600
        D: Come è nata questa tua passione per il mondo della moda? ### interview_block1_block600
        D: Cosa ti appassiona più nel mondo della moda? ### interview_block1_block600
        if (Nutri altre passioni oltre al mondo della moda?) { ### interview_block1_block700
            D: Quali altre passioni nutri oltre al mondo della moda? ### interview_block1_block700_block1
        }
        D: Il tuo pregio più grande e il tuo "peggior" difetto? ### interview_block1_block600
        D: Definisci quello che secondo te è la "bellezza"? ### interview_block1_block600
        D: Il tuo stile preferito "giornaliero"? ### interview_block1_block600
        D: Il tuo stile preferito "serale"? ### interview_block1_block600
        D: Convinci la gente a darti un voto ### interview_block1_block600
    } else if (partecipo solo per divertimento/altro)
    {
        D: Parlaci un po' di te, dove sei nata e quali sono le tue passioni ### interview_block1_block800
        D: Il tuo pregio più grande e il tuo "peggior" difetto? ### interview_block1_block800
        D: Quali sono i tuoi look preferiti? ### interview_block1_block800
        if (Hai qualche hobby?) { ### interview_block1_block900
            D: Qual'è il tuo hobby? ### interview_block1_block900_block1
        }
        D: Una massima in cui ti rispecchi? ### interview_block1_block800
        D: Convinci la gente a darti un voto ### interview_block1_block800
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

# pubblicazione
DS_CONST_NOT_PUBLISHED = 0
DS_CONST_PUBLISHED = 1

# approvazione
DS_CONST_MUST_BE_APPROVED = 3
DS_CONST_PENDING_APPROVAL = 2
DS_CONST_APPROVED = 1
DS_CONST_NOT_APPROVED = 0

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
        'not_to_show' : 1,
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
                'answer_code' : 'interview__block1__q1__a3',
                'next_question_block_1' : 'interview__block1__block400', # children flat block questions
                'next_question_block_2' : 'interview__block1__block500', # Nutri altre passioni oltre al mondo della moda?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 20,
            },
            {
                # Sono appassionata di moda
                'answer_code' : 'interview__block1__q1__a4',
                'next_question_block_1' : 'interview__block1__block600', # children flat block questions
                'next_question_block_2' : 'interview__block1__block700', # Nutri altre passioni oltre al mondo della moda?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 30,
            },
            {
                # Solo per divertimento/altro
                'answer_code' : 'interview__block1__q1__a5',
                'next_question_block_1' : 'interview__block1__block800', # children flat block questions
                'next_question_block_2' : 'interview__block1__block900', # Hai qualche hobby?
                'next_question_block_3' : False,
                'next_question_block_4' : False,
                'next_question_block_5' : False,
		'order' : 40,
            },
        ],
    },
    ## question_block: user_interview_model_pro
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
    # interview_block1_block2 {{{
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
    # interview_block1_block2 }}}
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
    # interview_block1_block3 {{{
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
                    'answer_code' : 'interview_block1__block3__block1__q1__a1',
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
                'answer_code' : 'interview__block1__block4__q1__a2',
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
		# Qual è il tuo hobby?
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
		# Qual è il tuo hobby?
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

DS_QUESTIONS_ANSWERS_LABEL = {
    # user_interview__model_pro
    'interview__block1__q1' : {
        'question_text_woman' : "Seleziona la tua categoria",
        'question_text_man' : "Seleziona la tua categoria",
        'question_hint_woman' : False,
        'question_hint_man' : False,
    },
	'interview__block1__q1__a1' : {
	    'question_text_woman' : "Sono una modella/indossatrice/ragazza immagine professionista",
	    'question_text_man' : "Sono un modello/indossatrice/ragazzo immagine professionista",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__q1__a2' : {
	    'question_text_woman' : "Sono una modella/indossatrice/ragazza immagine esordiente",
	    'question_text_man' : "Sono un modello/indossatrice/ragazzo immagine esordiente",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__q1__a3' : {
	    'question_text_woman' : "Sono un'appassionata di fotografia",
	    'question_text_man' : "Sono un appassionato di fotografia",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__q1__a4' : {
	    'question_text_woman' : "Sono un'appassionata di moda",
	    'question_text_man' : "Sono un appassionato di moda",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__q1__a5' : {
	    'question_text_woman' : "Partecipo solo per divertimento/Altro",
	    'question_text_man' : "Partecipo solo per divertimento/Altro",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block1__q1' : {
	'question_text_woman' : "Parlaci un po' di te, dove sei nata e quali sono le tue passioni",
	'question_text_man' : "Parlaci un po' di te, dove sei nato e quali sono le tue passioni",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q2' : {
	'question_text_woman' : "Come è iniziata la tua avventura nel mondo della moda?",
	'question_text_man' : "Come è iniziata la tua avventura nel mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q3' : {
	'question_text_woman' : 'Definisci quello che secondo te è la "bellezza"',
	'question_text_man' : 'Definisci quello che secondo te è la "bellezza"',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q4' : {
	'question_text_woman' : 'Il tuo pregio più grande e il tuo "peggior" difetto?',
	'question_text_man' : 'Il tuo pregio più grande e il tuo "peggior" difetto?',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q5' : {
	'question_text_woman' : "Quali sono i tuoi look preferiti?",
	'question_text_man' : "Quali sono i tuoi look preferiti?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q6' : {
	'question_text_woman' : "Una massima o un motto in cui ti rispecchi?",
	'question_text_man' : "Una massima o un motto in cui ti rispecchi?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block2__q7' : {
	'question_text_woman' : "Nutri altre passioni oltre al mondo della moda?",
	'question_text_man' : "Nutri altre passioni oltre al mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block2__q7__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block2__q7__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block2__block1__q1' : {
	'question_text_woman' : "Quali altre passioni nutri oltre al mondo della moda?",
	'question_text_man' : "Quali altre passioni nutri oltre al mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q8' : {
	'question_text_woman' : "La tua giornata tipo?",
	'question_text_man' : "La tua giornata tipo?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block3__q1' : {
	'question_text_woman' : "Hai già partecipato a qualche sfilata?",
	'question_text_man' : "Hai già partecipato a qualche sfilata?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block3__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block3__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block3__block1__q1' : {
	'question_text_woman' : "A quali sfilate hai partecipato?",
	'question_text_man' : "A quali sfilate hai partecipato?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block3__block1__q2' : {
	'question_text_woman' : "Il ricordo più bello della tua prima sfilata?",
	'question_text_man' : "Il ricordo più bello della tua prima sfilata?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block3__block2__q1' : {
	'question_text_woman' : "C'è qualche stilista particolare per cui vorresti sfilare?",
	'question_text_man' : "C'è qualche stilista particolare per cui vorresti sfilare?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block3__block2__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block3__block2__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block3__block2__block1__q1' : {
	'question_text_woman' : "Per quale stilista vorresti sfilare?",
	'question_text_man' : "Per quale stilista vorresti sfilare?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block4__q1' : {
	'question_text_woman' : "Hai già partecipato a qualche concorso/evento?",
	'question_text_man' : "Hai già partecipato a qualche concorso/evento?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block4__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block4__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block4__block1__q1' : {
	'question_text_woman' : "A quali concorsi/eventi hai partecipato?",
	'question_text_man' : "A quali concorsi/eventi hai partecipato?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block4__block2__q1' : {
	'question_text_woman' : "Hai già vinto qualche titolo?",
	'question_text_man' : "Hai già vinto qualche titolo?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block4__block2__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block4__block2__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block4__block2__block1__q1' : {
	'question_text_woman' : "Quale o quali titoli hai vinto?",
	'question_text_man' : "Quale o quali titoli hai vinto?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block4__block3__q1' : {
	'question_text_woman' : "C'è qualche concorso/evento a cui vorresti partecipare?",
	'question_text_man' : "C'è qualche concorso/evento a cui vorresti partecipare?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block4__block3__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block4__block3__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block4__block3__block1__q1' : {
	'question_text_woman' : "A quale concorso/evento vorresti partecipare?",
	'question_text_man' : "A quale concorso/evento vorresti partecipare?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q11' : {
	'question_text_woman' : "Alcune persone che ritieni importanti con cui hai lavorato?",
	'question_text_man' : "Alcune persone che ritieni importanti con cui hai lavorato?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q12' : {
	'question_text_woman' : "E' stata dura arrivare ai tuoi risultati?",
	'question_text_man' : "E' stata dura arrivare ai tuoi risultati?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block1__q13' : {
	'question_text_woman' : "Qualche consiglio per chi vorrebbe entrare nel mondo della moda?",
	'question_text_man' : "Qualche consiglio per chi vorrebbe entrare nel mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    # user_interview__model_beginner
    'interview__block1__block200__q1' : {
	'question_text_woman' : "Parlaci un po' di te, dove sei nata e quali sono le tue passioni",
	'question_text_man' : "Parlaci un po' di te, dove sei nato e quali sono le tue passioni",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q2' : {
	'question_text_woman' : "Com'è nata la tua passione per il mondo della moda?",
	'question_text_man' : "Com'è nata la tua passione per il mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q3' : {
	'question_text_woman' : "La ragione principale per cui ti piacerebbe lavorare nel mondo della moda?",
	'question_text_man' : "La ragione principale per cui ti piacerebbe lavorare nel mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q4' : {
	'question_text_woman' : 'Definisci quello che secondo te è la "bellezza"',
	'question_text_man' : 'Definisci quello che secondo te è la "bellezza"',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q5' : {
	'question_text_woman' : "Ti piacerebbe diventare la nuova Miss...",
	'question_text_man' : "Ti piacerebbe diventare il nuovo Mister...",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q6' : {
	'question_text_woman' : "La tua giornata tipo?",
	'question_text_man' : "La tua giornata tipo?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block300__q1' : {
	'question_text_woman' : "Nutri altre passioni oltre al mondo della moda?",
	'question_text_man' : "Nutri altre passioni oltre al mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block300__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block300__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block300__block1__q1' : {
	'question_text_woman' : "Quali altre passioni nutri oltre al mondo della moda?",
	'question_text_man' : "Quali altre passioni nutri oltre al mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q7' : {
	'question_text_woman' : "Lo/la stilista per cui vorresti sfilare?",
	'question_text_man' : "Lo/la stilista per cui vorresti sfilare?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q8' : {
	'question_text_woman' : "La tua modella ispiratrice?",
	'question_text_man' : "Il tuo modello ispiratore?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q9' : {
	'question_text_woman' : "Quali sono i tuoi look preferiti?",
	'question_text_man' : "Quali sono i tuoi look preferiti?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q10' : {
	'question_text_woman' : "Il tuo colore preferito?",
	'question_text_man' : "Il tuo colore preferito?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block200__q11' : {
	'question_text_woman' : "Convinci il pubblico a darti un voto",
	'question_text_man' : "Convinci il pubblico a darti un voto",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    # user_interview__photo_passionate
    'interview__block1__block400__q1' : {
	'question_text_woman' : "Parlaci un po' di te, dove sei nata e quali sono le tue passioni",
	'question_text_man' : "Parlaci un po' di te, dove sei nato e quali sono le tue passioni",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block400__q2' : {
	'question_text_woman' : "La tua giornata tipo?",
	'question_text_man' : "La tua giornata tipo?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block400__q3' : {
	'question_text_woman' : "Quali sono i tuoi look preferiti?",
	'question_text_man' : "Quali sono i tuoi look preferiti?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block400__q4' : {
	'question_text_woman' : "Cosa ti appassiona di più del mondo della fotografia?",
	'question_text_man' : "Cosa ti appassiona di più del mondo della fotografia?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block400__q5' : {
	'question_text_woman' : 'Definisci quello che secondo te è la "bellezza"?',
	'question_text_man' : 'Definisci quello che secondo te è la "bellezza"?',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block400__q6' : {
	'question_text_woman' : "Qual è il tuo genere fotografico preferito?",
	'question_text_man' : "Qual è il tuo genere fotografico preferito?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block500__q1' : {
	'question_text_woman' : "Hai qualche hobby oltre alla fotografia?",
	'question_text_man' : "Hai qualche hobby oltre alla fotografia?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block500__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block500__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block500__block1__q1' : {
	'question_text_woman' : "Qual è il tuo hobby?",
	'question_text_man' : "Qual è il tuo hobby?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    # user_interview__fashion_passionate
    'interview__block1__block600__q1' : {
	'question_text_woman' : "Parlaci un po' di te, dove sei nata e quali sono le tue passioni",
	'question_text_man' : "Parlaci un po' di te, dove sei nato e quali sono le tue passioni",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q2' : {
	'question_text_woman' : "Come è nata questa tua passione per il mondo della moda?",
	'question_text_man' : "Come è nata questa tua passione per il mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q3' : {
	'question_text_woman' : "Cosa ti appassiona nel mondo della moda?",
	'question_text_man' : "Cosa ti appassiona nel mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q4' : {
	'question_text_woman' : 'Il tuo pregio più grande e il tuo "peggior" difetto?',
	'question_text_man' : 'Il tuo pregio più grande e il tuo "peggior" difetto?',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q5' : {
	'question_text_woman' : 'Definisci quello che secondo te è la "bellezza"',
	'question_text_man' : 'Definisci quello che secondo te è la "bellezza"',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block700__q1' : {
	'question_text_woman' : "Nutri altre passioni oltre al mondo della moda?",
	'question_text_man' : "Nutri altre passioni oltre al mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block700__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block700__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block700__block1__q1' : {
	'question_text_woman' : "Quali altre passioni nutri oltre al mondo della moda?",
	'question_text_man' : "Quali altre passioni nutri oltre al mondo della moda?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q6' : {
	'question_text_woman' : 'Il tuo stile preferito "giornaliero"',
	'question_text_man' : 'Il tuo stile preferito "giornaliero"',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q7' : {
	'question_text_woman' : 'Il tuo stile preferito "serale"?',
	'question_text_man' : 'Il tuo stile preferito "serale"?',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block600__q8' : {
	'question_text_woman' : "Convinci il pubblico a darti un voto",
	'question_text_man' : "Convinci il pubblico a darti un voto",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    # user_interview__just_for_fun
    'interview__block1__block800__q1' : {
	'question_text_woman' : "Parlaci un po' di te, dove sei nata e quali sono le tue passioni",
	'question_text_man' : "Parlaci un po' di te, dove sei nato e quali sono le tue passioni",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block800__q2' : {
	'question_text_woman' : 'Il tuo pregio più grande e il tuo "peggior" difetto?',
	'question_text_man' : 'Il tuo pregio più grande e il tuo "peggior" difetto?',
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block800__q3' : {
	'question_text_woman' : "Quali sono i tuoi look preferiti?",
	'question_text_man' : "Quali sono i tuoi look preferiti?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block900__q1' : {
	'question_text_woman' : "Hai qualche hobby?",
	'question_text_man' : "Hai qualche hobby?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
	'interview__block1__block900__q1__a1' : {
	    'question_text_woman' : "Si",
	    'question_text_man' : "Si",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
	'interview__block1__block900__q1__a2' : {
	    'question_text_woman' : "No",
	    'question_text_man' : "No",
	    'question_hint_woman' : False,
	    'question_hint_man' : False,
	},
    'interview__block1__block900__block1__q1' : {
	'question_text_woman' : "Qual è il tuo hobby?",
	'question_text_man' : "Qual è il tuo hobby?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block800__q4' : {
	'question_text_woman' : "Una massima o un motto in cui ti rispecchi?",
	'question_text_man' : "Una massima o un motto in cui ti rispecchi?",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
    'interview__block1__block800__q5' : {
	'question_text_woman' : "Convinci il pubblico a darti un voto",
	'question_text_man' : "Convinci il pubblico a darti un voto",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
}


"""
    'question_code' : {
	'question_text_woman' : "",
	'question_text_man' : "",
	'question_hint_woman' : False,
	'question_hint_man' : False,
    },
"""
