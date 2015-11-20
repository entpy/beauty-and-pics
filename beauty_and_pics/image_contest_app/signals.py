# -*- coding: utf-8 -*-

from django.db.models.signals import post_delete
from django.dispatch import receiver
from image_contest_app.models import ImageContestImage
from datetime import datetime
from .settings import ICA_CONTEST_TYPE_CLOSED
import logging, uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ImageContestImage post_delete callback
@receiver(post_delete, sender=ImageContestImage)
def post_delete_callback(sender, instance, using, **kwargs):
    """Se è l'immagine vincitrice del photoboard e la elimino, allora termino anche il relativo contest"""
    logger.info("ImageContestImage -> post_delete_callback: elemento rimosso con successo: " + str(instance.__dict__))
    # se il contest relativo all'immagine è chiuso:
    # allora metto come data di scadenza now
    if instance.image_contest.status == ICA_CONTEST_TYPE_CLOSED:
	instance.image_contest.expiring = datetime.now()
	instance.image_contest.save()

    return True
