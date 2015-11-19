"""
# -*- coding: utf-8 -*-
from django.dispatch import receiver

def post_delete_callback(sender, instance, using, **kwargs):
    # se il concorso relativo all'immagine è chiuso lo metto in stato scaduto
    logger.info("--Elemento rimosso con successo: " + str(instance))
"""
