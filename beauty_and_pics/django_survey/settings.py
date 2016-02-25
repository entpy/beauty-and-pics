# -*- coding: utf-8 -*-

"""
Settings for 'django_survey' app
"""

# deault consts
DS_SURVEYS_QUESTION_TYPE_TEXT = 'text' # se la risposta è campo libero
DS_SURVEYS_QUESTION_TYPE_BOOLEAN = 'boolean' # se la risposta è si/no

DS_SURVEYS_CODE_ABOUT_USER = 'about_user'
DS_SURVEYS_CODE_IS_MODEL = 'is_model'
DS_SURVEYS_CODE_IS_NOT_MODEL = 'is_not_model'

# surveys list
DS_SURVEYS_LIST = [
    { 'survey_code' : DS_SURVEYS_CODE_ABOUT_USER, 'survey_description' : 'Questionario generico su un utente', },
    { 'survey_code' : 'is_model', 'survey_description' : "Questionario se l'utente è già modella/o", },
    { 'survey_code' : 'is_not_model', 'survey_description' : "Questionario se l'utente non è ancora modella/o", },
]

# questions list
DS_SURVEYS_QUESTIONS = [
    # survey about_user
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_informazioni_generali',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 1,
        'order' : 0,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_motto',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 10,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_giornata_tipo',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 20,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_pregio',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 30,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_difetto',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 40,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_hobby',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 50,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_causa_in_cui_credo',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 60,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_ABOUT_USER,
        'question_code' : 'about_user_gia_modella',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_BOOLEAN,
        'required' : 0,
        'order' : 70,
    },
    # survey is_model
    {
        'survey_code' : DS_SURVEYS_CODE_IS_MODEL,
        'question_code' : 'is_model_inizio',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 80,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_IS_MODEL,
        'question_code' : 'is_model_stilista',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 90,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_IS_MODEL,
        'question_code' : 'is_model_dopo_carriera',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 100,
    },
    # survey is_not_model
    {
        'survey_code' : DS_SURVEYS_CODE_IS_NOT_MODEL,
        'question_code' : 'is_not_model_moda_interessante',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 110,
    },
    {
        'survey_code' : DS_SURVEYS_CODE_IS_NOT_MODEL,
        'question_code' : 'is_not_model_convinci',
        'question_type' : DS_SURVEYS_QUESTION_TYPE_TEXT,
        'required' : 0,
        'order' : 120,
    },
]

# questions label
DS_SURVEYS_QUESTIONS_LABEL = {
    # survey about_user
    'about_user_informazioni_generali' : {
        'question_text_woman' : 'Qualcosa su di te?',
        'question_text_man' : 'Qualcosa su di te?',
        'question_hint_woman' : 'Descrivi in poche righe dove sei nata, chi sei e le tue passioni',
        'question_hint_man' : 'Descrivi in poche righe dove sei nato, chi sei e le tue passioni',
    },
    'about_user_motto' : {
        'question_text_woman' : "Qual'è il tuo motto?",
        'question_text_man' : "Qual'è il tuo motto?",
        'question_hint_woman' : "Scrivi qual'è il tuo motto preferito",
        'question_hint_man' : "Scrivi qual'è il tuo motto preferito",
    },
    'about_user_giornata_tipo' : {
        'question_text_woman' : 'La tua giornata tipo?',
        'question_text_man' : 'La tua giornata tipo?',
        'question_hint_woman' : 'Descrivici la tua giornata tipo',
        'question_hint_man' : 'Descrivici la tua giornata tipo',
    },
    'about_user_pregio' : {
        'question_text_woman' : 'Il tuo pregio più grande?',
        'question_text_man' : 'Il tuo pregio più grande?',
        'question_hint_woman' : 'Scrivi quello che secondo te è il tuo pregio migliore',
        'question_hint_man' : 'Scrivi quello che secondo te è il tuo pregio migliore',
    },
    'about_user_difetto' : {
        'question_text_woman' : 'Il tuo "peggior" difetto?',
        'question_text_man' : 'Il tuo "peggior" difetto?',
        'question_hint_woman' : 'Scrivi quello che secondo te è il tuo peggior difetto',
        'question_hint_man' : 'Scrivi quello che secondo te è il tuo peggior difetto',
    },
    'about_user_hobby' : {
        'question_text_woman' : 'Il tuo hobby?',
        'question_text_man' : 'Il tuo hobby?',
        'question_hint_woman' : 'Scrivi quello che ti piace fare nel tuo tempo libero',
        'question_hint_man' : 'Scrivi quello che ti piace fare nel tuo tempo libero',
    },
    'about_user_causa_in_cui_credo' : {
        'question_text_woman' : 'Una causa in cui credi?',
        'question_text_man' : 'Una causa in cui credi?',
        'question_hint_woman' : 'Scrivi una causa in cui credi',
        'question_hint_man' : 'Scrivi una causa in cui credi',
    },
    'about_user_gia_modella' : {
        'question_text_woman' : 'Sei già una modella?',
        'question_text_man' : 'Sei già un modello?',
        'question_hint_woman' : '',
        'question_hint_man' : '',
    },
    # survey is_model
    'is_model_inizio' : {
        'question_text_woman' : 'Come hai iniziato a fare la modella?',
        'question_text_man' : 'Come hai iniziato a fare il modello?',
        'question_hint_woman' : "Descrivi cosa ti ha portato a fare la modella",
        'question_hint_man' : "Descrivi cosa ti ha portato a fare il modello",
    },
    'is_model_stilista' : {
        'question_text_woman' : 'Lo/la stilista per cui vorresti sfilare?',
        'question_text_man' : 'Lo/la stilista per cui vorresti sfilare?',
        'question_hint_woman' : "Scrivi il nome dello/a stilista per cui vorresti sfilare",
        'question_hint_man' : "Scrivi il nome dello/a stilista per cui vorresti sfilare",
    },
    'is_model_dopo_carriera' : {
        'question_text_woman' : 'Cosa vorresti fare dopo la tua carriera di modella?',
        'question_text_man' : 'Cosa vorresti fare dopo la tua carriera di modello?',
        'question_hint_woman' : "Scrivi quello che ti piacerebbe fare in futuro",
        'question_hint_man' : "Scrivi quello che ti piacerebbe fare in futuro",
    },
    # survey is_not_model
    'is_not_model_moda_interessante' : {
        'question_text_woman' : 'Cosa trovi di interessante nel settore della moda?',
        'question_text_man' : 'Cosa trovi di interessante nel settore della moda?',
        'question_hint_woman' : "Scrivi quello che più ti piace nel settore della moda",
        'question_hint_man' : "Scrivi quello che più ti piace nel settore della moda",
    },
    'is_not_model_convinci' : {
        'question_text_woman' : "Facciamo finta che tu stia per essere assunta da un'agenzia di moda, cosa diresti per convincerli?",
        'question_text_man' : "Facciamo finta che tu stia per essere assunto da un'agenzia di moda, cosa diresti per convincerli?",
        'question_hint_woman' : "Scrivi qualcosa di convincente per essere contattata",
        'question_hint_man' : "Scrivi qualcosa di convincente per essere contattato",
    },
}
