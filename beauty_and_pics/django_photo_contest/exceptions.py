# -*- coding: utf-8 -*-

# list of custom exceptions with error code
class PhotocontestMissingConfiguration(Exception):
    """Il codice specificato non è presente nel file di configurazione"""
    get_error_code = "001"
    pass

class LikeAlreadyAssigned(Exception):
    """Il like all'immagine è già stato dato"""
    get_error_code = "002"
    pass
