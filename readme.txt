test approfonditi upload immagine
testare la votazione
testare il login
leggere i log delle 2 azioni sopra
voti da 49 a 72 ore
modificati alcuni testi delle mail

esempio di left join
        # eseguo una left join di User_Notify in Notify filtrando per data creazione account (il risultato è la query sotto)
        """
	    SELECT "notify_system_app_notify"."notify_id", "notify_system_app_notify"."title", "notify_system_app_notify"."creation_date", "notify_system_app_user_notify"."user_notify_id" 
	    FROM "notify_system_app_notify"
	    LEFT OUTER JOIN "notify_system_app_user_notify" ON ( "notify_system_app_notify"."notify_id" = "notify_system_app_user_notify"."notify_id" )
	    WHERE "notify_system_app_notify"."creation_date" >= '2015-09-21 23:45:00.342532'
	    ORDER BY "notify_system_app_notify"."notify_id" DESC LIMIT 10;
        """
        # return_var = Notify.objects.filter(Q(creation_date__gte=account_creation_date) & (Q(user_notify__user=user_id) | Q(user_notify__user_notify_id__isnull=True))).values('notify_id', 'title', 'creation_date', 'user_notify__user_notify_id').order_by('-notify_id')


I banner
========
Questi strani elementi che compaiono e scompaiono, sono visibili in
diversi punti.
Banner "vai alla passerella", presente in -> (tutte le pagine) | non presente in -> (index passerella)
Banner "vai alla bacheca", presente in -> (index passerella se non ho vincitori, dettaglio photoboard) | non presente in -> (tutte le altre pagine)
Banner "vincitore bacheca", presente in -> (index passerella se ho vincitori) | non presente in -> (tutte le altre pagine)
Banner "vincitore concorso", presente in -> (index passerella) | non presente in -> (tutte le altre pagine)
