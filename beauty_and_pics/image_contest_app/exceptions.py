# list of custom exceptions with error code

class AddImageContestImageFieldMissignError(Exception):
    """Error in add new image contest image, one or more fields are missing"""
    get_error_code = "001"
    pass

class AddImageContestIntegrityError(Exception):
    """Error in add new image contest image, eg. duplicate elements"""
    get_error_code = "002"
    pass

class RemoveImageContestImageError(Exception):
    """Error in remove image contest image, row not found"""
    get_error_code = "003"
    pass

class ImageAlreadyVotedError(Exception):
    """Error in image voting, image already voted"""
    get_error_code = "004"
    pass

class AddImageContestVoteIntegrityError(Exception):
    """Error in add new image contest vote, eg. duplicate elements"""
    get_error_code = "005"
    pass

class ImageContestClosedError(Exception):
    """
    Error in get image contest, eg. status not matches (ex. try to retrieve
    an element in open contest but the constest was already closed)
    """
    get_error_code = "006"
    pass
