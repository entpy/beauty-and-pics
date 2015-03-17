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
