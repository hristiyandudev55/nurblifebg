import datetime
import logging
from abc import ABC, abstractmethod
import secrets
import string
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from schemas.vouchers import VoucherDetails
from utils.transaction_context import transaction_context
from utils.voucher_utils import get_voucher_by_id

logger = logging.getLogger(__name__)
now_utc = datetime.datetime.now(datetime.timezone.utc)


class BaseRepository(ABC):
    @abstractmethod
    def generate(self, length: int):
        pass

    @abstractmethod
    def get(self, voucher_id):
        pass

    @abstractmethod
    def validate(self, voucher_code: str):
        pass

    @abstractmethod
    def delete(self, voucher_id):
        pass


class VoucherRepository(BaseRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def generate(self, length: int = 10) -> str:
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

    def get(self, voucher_id: str) -> VoucherDetails:
        db_voucher = get_voucher_by_id(voucher_id, self.db)

        return VoucherDetails.model_validate(db_voucher)

    def delete(self, voucher_id) -> dict:
        try:
            with transaction_context(self.db):
                db_voucher = get_voucher_by_id(voucher_id, db=self.db)

                self.db.delete(db_voucher)
            return {"detail": f"Voucher with ID {voucher_id} deleted successfully."}

        except SQLAlchemyError as e:
            logger.error("Database error deleting voucher: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error.",
            ) from e
