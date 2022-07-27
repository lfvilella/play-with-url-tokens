import pyotp


def _otp() -> pyotp.TOTP:
    # otp_secret = pyotp.random_base32()
    return pyotp.TOTP("JHWCS43RCPO5YQLUH3GHM75J52HYECYW")


def get_otp_time_code() -> str:
    return _otp().now()


def verify_otp_time_code(code: str, valid_window: int = None) -> bool:
    if not code:
        return False

    # each window is 30s so by default code will be valid for 1min
    valid_window = valid_window or 2

    return _otp().verify(code, valid_window=valid_window)
