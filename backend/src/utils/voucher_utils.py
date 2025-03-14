from datetime import datetime, timezone
import secrets
import string
from sqlalchemy.orm import Session

from models.voucher import Voucher

def generate_code_voucher(length: int = 10) -> str:
    """
    Generate a random voucher code of a given length.

    Args:
        length (int): The length of the voucher code to generate. Default is 10.

    Returns:
        str: A randomly generated voucher code consisting of letters and digits.
    """
    characters = string.ascii_letters + string.digits
    voucher_code = "".join(secrets.choice(characters) for _ in range(length))
    return voucher_code


def validate_voucher(code: str, db: Session) -> Voucher:
    """
    Validate a voucher by its code.

    Args:
        code (str): The voucher code to validate.
        db (Session): The SQLAlchemy session used to query the database.

    Raises:
        ValueError: If the voucher doesn't exist, is already used, or is expired.

    Returns:
        Voucher: The valid voucher object.
    """
    voucher = db.query(Voucher).filter(Voucher.code == code).first()

    if not voucher:
        raise ValueError("Invalid voucher code.")

    if voucher.status == "used": # type: ignore
        raise ValueError("This voucher has already been used.")

    # Ако в реалния модел полето е 'expiration_date', коригирайте и тук.
    if voucher.expiration_date is not None and voucher.expiration_date < datetime.now(timezone.utc):
        raise ValueError("This voucher has expired.")

    return voucher
