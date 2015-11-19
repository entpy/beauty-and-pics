# -*- coding: utf-8 -*-

from django.db.models.signals import post_delete
from django.dispatch import receiver
from image_contest_app.models import ImageContestImage
import logging, uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ImageContestImage post_delete callback
@receiver(post_delete, sender=ImageContestImage)
def post_delete_callback(sender, **kwargs):
    logger.info("ImageContestImage -> post_delete_callback: elemento rimosso con successo: " + str(kwargs['instance'].__dict__))

# @receiver(post_delete)
# post_delete.connect(post_delete_callback, sender=ImageContestImage, dispatch_uid=str(uuid.uuid1()))
