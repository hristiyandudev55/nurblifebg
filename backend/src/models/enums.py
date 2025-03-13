from enum import Enum


class Extras(str, Enum):
    GUIDANCE_LAP = "guidance_lap"
    VIDEO_RECORD = "video_record"
    DMG_EXCESS_REDUCTION = "dmg_excess_reduction"
    EXTRA_DRIVER = (
        "extra_driver"  # up to 2 drivers is free, the 3rd is paying 50 euro additional
    )


class BookingStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    PENDING = "pending"


class Package(str, Enum):
    BASE_PACKAGE = "base_package"
    PREMIUM_PACKAGE = "premium_package"


class Trace(str, Enum):
    PUBLIC_SESSION = "public_session"
    TRACKDAY = "trackday"
    GP_TRACK = "gp_track"
    SPA_FRANCOCHAMPS = "spa_francochamps"


class CarGearboxEnum(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SEMI_AUTOMATIC = "Semi-Automatic"
    CVT = "CVT"


class DriveTypeEnum(str, Enum):
    AWD = "awd"
    FWD = "fwd"
    RWD = "rwd"


class RollcageTypeEnum(str, Enum):
    NO_CAGE = "no_cage"
    FOUR_POINT = "four_point"
    SIX_POINT = "six_point"
    EIGHT_POINT = "eight_point"


class SeatsCountEnum(int, Enum):
    ONE_SEAT = 1
    TWO_SEATS = 2
    THREE_SEATS = 3
