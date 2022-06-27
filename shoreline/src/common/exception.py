class ShorelineException(Exception):
    faultstring = "An unknown exception occurred, please check REST-API logs"
    code = 500

    def __init__(self, faultstring=None, **kwargs):
        self.kwargs = kwargs
        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass
        if faultstring:
            self.faultstring = faultstring

        try:
            if 'user_id' in kwargs.keys():
                self.faultstring = self.faultstring + f' {kwargs["user_id"]}'
        except Exception as e:
            raise e
        super(ShorelineException, self).__init__(self.faultstring)


class InvalidRequestData(ShorelineException):
    code = 400
    faultstring = "Invalid Request data"


class InvalidCredentials(ShorelineException):
    code = 401
    faultstring = "User Email/Password is invalid"


class UserAlreadyLoggedIn(ShorelineException):
    code = 400
    faultstring = "User already Logged-In with different device."


class UserAlreadyExists(ShorelineException):
    code = 400
    faultstring = "Email-ID already registered with Numeronix."


class FaildToRegisterUser(ShorelineException):
    code = 409
    faultstring = "Failed to Register User"


class FaildToResendOTP(ShorelineException):
    code = 409
    faultstring = "Failed to Resend OTP to registered user"


class ForgetPasswordFailed(ShorelineException):
    code = 409
    faultstring = "Forget Password failed for user:"


class UserNotFound(ShorelineException):
    code = 400
    faultstring = "User Not Found:"


class GameNotFound(ShorelineException):
    code = 400
    faultstring = "Game Not Found with provided game id"


class InvalidGameSetup(ShorelineException):
    code = 400
    faultstring = "Invalid Game Setup detected"


class EmailAlreadyVerified(ShorelineException):
    code = 400
    faultstring = "Email-ID already registered and verified with Numeronix."


class WalletInfoNotFound(ShorelineException):
    code = 400
    faultstring = "Wallet info does not exists for provided user id:"


class InsufficientWalletBalance(ShorelineException):
    code = 409
    faultstring = "Insufficient wallet balance for user with user_id:"


class FinishedGame(ShorelineException):
    code = 400
    faultstring = "Game stats can't be updated as the wallet is already updated for this game."


class InvalidAuthToken(ShorelineException):
    code = 401
    faultstring = "Invalid Auth-Token"
