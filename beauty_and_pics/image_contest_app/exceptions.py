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
