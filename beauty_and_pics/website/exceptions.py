# list of custom exceptions with error code

class UserCreateError(Exception):
    """Error in create user."""
    get_error_code = "001"
    pass

class UserUpdateDataError(Exception):
    """Error in create update user data after creation."""
    get_error_code = "002"
    pass

class UserNotActiveError(Exception):
    """Error in user login, user not active"""
    get_error_code = "003"
    pass

class UserLoginError(Exception):
    """Error in user login, email and/or password invalid."""
    get_error_code = "004"
    pass

class UserPasswordMatchError(Exception):
    """Error in check password, give password doesn't match the user password."""
    get_error_code = "005"
    pass

class UserEmailPasswordUpdateError(Exception):
    """Error in update user email and password."""
    get_error_code = "006"
    pass

class UserAlreadyVotedError(Exception):
    """Error in voting, user already voted this account."""
    get_error_code = "010"
    pass

class ContestNotActiveError(Exception):
    """Exception in contest active check."""
    get_error_code = "011"
    pass

class imageTypeWrongError(Exception):
    """Exception image type check."""
    get_error_code = "012"
    pass

class croppedImageDoesNotExistError(Exception):
    """Exception cropped image does not exist."""
    get_error_code = "013"
    pass

class bookImageDoesNotExistError(Exception):
    """Exception book image does not exist."""
    get_error_code = "014"
    pass

class deleteImageReferenceError(Exception):
    """Exception on book image delete when user id and image user id are !=."""
    get_error_code = "015"
    pass

class userAlreadyAddedToFavoritesError(Exception):
    """Exception on multiple add to favorite on same user action."""
    get_error_code = "016"
    pass

class UserDeleteIdDoesNotMatchError(Exception):
    """Error in user delete, user id and logged in user id doesn't match."""
    get_error_code = "017"
    pass

class UserDeleteDoesNotExistsError(Exception):
    """Error in user delete, user id doesn't exists."""
    get_error_code = "018"
    pass

class ContestClosedNotExistsError(Exception):
    """Error in get last closed contest, a closed contest not exists yet."""
    get_error_code = "019"
    pass

class ContestTypeRequiredError(Exception):
    """A contest type is required, function called without this param."""
    get_error_code = "020"
    pass

### votes.py {{{
class PerformVotationDataMissingError(Exception):
    """La funzione è stata chiamata senza tutti i parametri richiesti"""
    get_error_code = "021"
    pass
class PerformVotationVoteCodeDataError(Exception):
    """Il vote_code passato non è esistente nel dizionario"""
    get_error_code = "022"
    pass
class PerformVotationFromUserMissingError(Exception):
    """Non è stato possibile prelevare il from_user"""
    get_error_code = "023"
    pass
class PerformVotationToUserMissingError(Exception):
    """Non è stato possibile prelevare il to_user"""
    get_error_code = "024"
    pass
class PerformVotationUserContestMissingError(Exception):
    """Non è stato possibile prelevare il contest relativo all'utente"""
    get_error_code = "025"
    pass
### votes.py }}}
