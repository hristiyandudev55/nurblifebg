from typing import Any, Dict, Union
from uuid import UUID

from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class BaseAppException(HTTPException):
    """Base application exception with additional context capabilities"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,  # type: ignore
        context: Dict[str, Any] = None,  # type: ignore
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.context = context or {}


# Database-related exceptions
class DatabaseOperationException(BaseAppException):
    """Raised when a database operation fails"""

    def __init__(
        self,
        detail: str = "Database operation failed",
        context: Dict[str, Any] = None,  # type: ignore
        error_code: str = "DB_ERROR",
    ):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
            context=context,
        )


class IntegrityConstraintException(BaseAppException):
    """Raised when a database integrity constraint is violated"""

    def __init__(
        self,
        detail: str = "Integrity constraint violation",
        context: Dict[str, Any] = None,  # type: ignore
        error_code: str = "INTEGRITY_ERROR",
    ):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
            context=context,
        )


class ForeignKeyConstraintException(IntegrityConstraintException):
    """Raised when a foreign key constraint is violated"""

    def __init__(
        self,
        detail: str = "Foreign key constraint violation",
        context: Dict[str, Any] = None,  # type: ignore
    ):
        super().__init__(
            detail=detail, context=context, error_code="FK_CONSTRAINT_ERROR"
        )


# Resource-related exceptions
class ResourceNotFoundException(BaseAppException):
    """Raised when a requested resource is not found"""

    def __init__(
        self,
        resource_type: str,
        resource_id: Union[str, int, UUID],
        context: Dict[str, Any] = None,  # type: ignore
    ):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"{resource_type} with ID {resource_id} not found",
            error_code="RESOURCE_NOT_FOUND",
            context=context,
        )


class CarNotFoundException(ResourceNotFoundException):
    """Raised when a car is not found"""

    def __init__(self, car_id: Union[str, int, UUID], context: Dict[str, Any] = None):  # type: ignore
        super().__init__(resource_type="Car", resource_id=car_id, context=context)


class BookingNotFoundException(ResourceNotFoundException):
    """Raised when a booking is not found"""

    def __init__(
        self, booking_id: Union[str, int, UUID], context: Dict[str, Any] = None # type: ignore
    ):  # type: ignore
        super().__init__(
            resource_type="Booking", resource_id=booking_id, context=context
        )


class HotelNotFoundException(ResourceNotFoundException):
    """Raised when a hotel is not found"""

    def __init__(self, hotel_id: Union[str, int, UUID], context: Dict[str, Any] = None):  # type: ignore
        super().__init__(resource_type="Hotel", resource_id=hotel_id, context=context)


class VoucherNotFoundException(ResourceNotFoundException):
    """Raised when a voucher is not found"""

    def __init__(
        self, voucher_id: Union[str, int, UUID], context: Dict[str, Any] = None # type: ignore
    ):  # type: ignore
        super().__init__(
            resource_type="Voucher", resource_id=voucher_id, context=context
        )


# Validation-related exceptions
class ValidationException(BaseAppException):
    """Raised when validation fails"""

    def __init__(
        self,
        detail: str = "Validation error",
        context: Dict[str, Any] = None,  # type: ignore
        error_code: str = "VALIDATION_ERROR",
    ):
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            context=context,
        )


class VoucherValidationException(ValidationException):
    """Raised when voucher validation fails"""

    def __init__(self, detail: str, context: Dict[str, Any] = None):  # type: ignore
        super().__init__(
            detail=detail, context=context, error_code="VOUCHER_VALIDATION_ERROR"
        )


class BookingValidationException(ValidationException):
    """Raised when booking validation fails"""

    def __init__(self, detail: str, context: Dict[str, Any] = None):  # type: ignore
        super().__init__(
            detail=detail, context=context, error_code="BOOKING_VALIDATION_ERROR"
        )


# Service-related exceptions
class ExternalServiceException(BaseAppException):
    """Raised when an external service integration fails"""

    def __init__(
        self,
        service_name: str,
        detail: str = "External service error",
        context: Dict[str, Any] = None,  # type: ignore
    ):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{service_name} service error: {detail}",
            error_code="EXTERNAL_SERVICE_ERROR",
            context=context,
        )


class GoogleCalendarException(ExternalServiceException):
    """Raised when Google Calendar integration fails"""

    def __init__(
        self,
        detail: str = "Calendar operation failed",
        context: Dict[str, Any] = None,  # type: ignore
    ):  # type: ignore
        super().__init__(service_name="Google Calendar", detail=detail, context=context)


# Status-related exceptions
class InvalidStatusTransitionException(BaseAppException):
    """Raised when an invalid status transition is attempted"""

    def __init__(
        self,
        current_status: str,
        target_status: str,
        resource_type: str = "Resource",
        context: Dict[str, Any] = None,  # type: ignore
    ):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition {resource_type} from '{current_status}' to '{target_status}'",
            error_code="INVALID_STATUS_TRANSITION",
            context=context,
        )


class BookingStatusException(InvalidStatusTransitionException):
    """Raised when an invalid booking status transition is attempted"""

    def __init__(
        self,
        current_status: str,
        target_status: str,
        context: Dict[str, Any] = None,  # type: ignore
    ):  # type: ignore
        super().__init__(
            current_status=current_status,
            target_status=target_status,
            resource_type="Booking",
            context=context,
        )


# Availability-related exceptions
class ResourceUnavailableException(BaseAppException):
    """Raised when a resource is unavailable for the requested operation"""

    def __init__(
        self,
        resource_type: str,
        detail: str = "Resource unavailable",
        context: Dict[str, Any] = None,  # type: ignore
    ):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail=f"{resource_type} unavailable: {detail}",
            error_code="RESOURCE_UNAVAILABLE",
            context=context,
        )


class TrackUnavailableException(ResourceUnavailableException):
    """Raised when the track is unavailable for booking"""

    def __init__(self, date: str, context: Dict[str, Any] = None):  # type: ignore
        super().__init__(
            resource_type="Track",
            detail=f"Track is not available on {date}",
            context=context,
        )


class CarUnavailableException(ResourceUnavailableException):
    """Raised when a car is unavailable for booking"""

    def __init__(
        self,
        car_id: Union[str, int, UUID],
        date: str,
        time: str,
        context: Dict[str, Any] = None,
    ):  # type: ignore
        super().__init__(
            resource_type="Car",
            detail=f"Car {car_id} is not available on {date} at {time}",
            context=context,
        )
