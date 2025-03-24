from datetime import datetime, timezone
import logging
import secrets
import string
from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
)
from sqlalchemy.orm import Session

from models.enums import VoucherStatusEnum
from models.voucher import Voucher

logger = logging.getLogger(__name__)

def get_voucher_by_id(voucher_id: str, db: Session) -> Voucher:
    db_voucher = db.query(Voucher).filter(Voucher.code == voucher_id).first()

    if not db_voucher:
        error_message = f"Voucher with ID {voucher_id} not found."
        logger.error(error_message)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_message)

    return db_voucher


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

    if voucher.status == VoucherStatusEnum.USED_VOUCHER:
        raise ValueError("This voucher has already been used.")

    if voucher.expiration_date and voucher.expiration_date < datetime.now(timezone.utc):
        raise ValueError("This voucher has expired.")

    return voucher
