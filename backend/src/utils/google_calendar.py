import datetime
from logging import getLogger
import logging
import os

import pytz
from dateutil import parser
from fastapi import HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core.config import SCOPES_, SERVICE_ACC_FILE, NURB_CALENDAR_ID
from models.booking import Booking
from models.car import Car

# PATH to my Service Account JSON File
SERVICE_ACCOUNT_FILE = SERVICE_ACC_FILE
SCOPES = [SCOPES_]

# ID of my Nurburgring calendar
NURBURGRING_CALENDAR_ID = NURB_CALENDAR_ID

logger = logging.getLogger(__name__)

# Check if the file exists
if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
    raise FileNotFoundError(
        f"Service Account file does not exist: {SERVICE_ACCOUNT_FILE}"
    )

try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build("calendar", "v3", credentials=credentials)
    print("Google API client successfully created")
except Exception as e:
    print(f"Error initializing Google API client: {e}")
    raise

bulgaria_tz = pytz.timezone("Europe/Sofia")


def format_datetime_to_local(iso_datetime_str):
    """Converts ISO datetime string to local timezone (Bulgaria)"""
    if not iso_datetime_str:
        return ""

    dt = parser.parse(iso_datetime_str)

    # Convert to Bulgaria/Sofia timezone
    local_dt = dt.astimezone(bulgaria_tz)

    # New date and hour format for better reading
    return local_dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def get_events():
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        one_month_later = (
            datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ).isoformat() + "Z"

        # Fetch events from Nürburgring calendar
        events_result = (
            service.events()
            .list(
                calendarId=NURBURGRING_CALENDAR_ID,
                timeMin=now,
                timeMax=one_month_later,
                maxResults=100,
                singleEvents=True,
                orderBy="startTime",
                timeZone="Europe/Berlin",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return {"message": "No upcoming events found."}

        event_list = []
        for event in events:
            start_datetime = event["start"].get("dateTime")
            end_datetime = event["end"].get("dateTime")

            if not start_datetime:
                start = event["start"].get("date")
                end = event["end"].get("date")
                is_all_day = True
            else:
                start = format_datetime_to_local(start_datetime)
                end = format_datetime_to_local(end_datetime)
                is_all_day = False

            # Check if the track is closed for public session or not
            is_closed = "Nürburgring Closed" in event.get("summary", "")

            event_list.append(
                {
                    "title": event["summary"],
                    "start": start,
                    "end": end,
                    "description": event.get("description", ""),
                    "location": event.get("location", ""),
                    "isClosed": is_closed,
                    "isAllDay": is_all_day,
                    "color": "#FF0000"
                    if is_closed
                    else "#00FF00",  # red for closed, green for opened
                }
            )

        return {"events": event_list}

    except HttpError as error:
        print(f"Error fetching events: {error}")
        raise HTTPException(
            status_code=500, detail=f"Google Calendar API error: {error}"
        ) from e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error processing the request: {e}"
        ) from e


def check_date_availability(date: str):
    """
    Checks if a specific date is open or closed.
    Date format: YYYY-MM-DD
    """
    try:
        # Create start/end of the day in UTC
        dt_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        start_date = dt_obj.replace(hour=0, minute=0, second=0).isoformat() + "Z"
        end_date = dt_obj.replace(hour=23, minute=59, second=59).isoformat() + "Z"

        # Fetch events for this day
        events_result = (
            service.events() # type ignore
            .list(
                calendarId=NURBURGRING_CALENDAR_ID,
                timeMin=start_date,
                timeMax=end_date,
                singleEvents=True,
                timeZone="Europe/Berlin",  # Set timezone for fetching
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            return {
                "date": date,
                "status": "unknown",
                "message": "No information available for this date.",
            }

        # Check for closed days
        closed_events = [
            event
            for event in events
            if "Nürburgring Closed" in event.get("summary", "")
        ]

        if closed_events:
            return {
                "date": date,
                "status": "closed",
                "message": "The track is closed on this date.",
            }

        # Extract times for open days
        open_events = [
            event for event in events if "Tourist Drives" in event.get("summary", "")
        ]

        if open_events:
            open_times = []
            for event in open_events:
                start_datetime = event["start"].get("dateTime", "")
                end_datetime = event["end"].get("dateTime", "")

                if start_datetime and end_datetime:
                    start_dt = parser.parse(start_datetime).astimezone(bulgaria_tz)
                    end_dt = parser.parse(end_datetime).astimezone(bulgaria_tz)

                    start_time = start_dt.strftime("%H:%M")
                    end_time = end_dt.strftime("%H:%M")

                    open_times.append(f"{start_time}-{end_time}")

            return {
                "date": date,
                "status": "open",
                "times": open_times,
                "message": f"The track is open during the following hours: {', '.join(open_times)}",
            }

        return {
            "date": date,
            "status": "unknown",
            "message": "No clear information available for this date.",
        }

    except Exception as e:
        print(f"Error checking the date: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error checking the date: {e}"
        ) from e #FIXME

def _add_to_calendar(self, booking: Booking):
    """Add the booking as an event in Google Calendar"""
    try:
        # Get car details
        car = self.db.query(Car).filter(Car.id == booking.car_id).first()
        car_name = f"{car.make} {car.model}" if car else "Unknown Car"

        # Create event
        event = {
            "summary": f"Booking: {car_name} - {booking.full_name}",
            "description": f"Laps: {booking.laps}\nPackage: {booking.package.value}\nContact: {booking.email}, {booking.phone_number}",
            "start": {
                "dateTime": booking.booking_time.isoformat(),
                "timeZone": "Europe/Berlin",
            },
            "end": {
                "dateTime": (
                    booking.booking_time + datetime.timedelta(hours=2)
                ).isoformat(),
                "timeZone": "Europe/Berlin",
            },
            "colorId": "11",  # A distinct color for bookings
        }
        service.events().insert(
            calendarId=NURBURGRING_CALENDAR_ID, body=event
        ).execute()
        return True
    except Exception as e: #FIXME
        logger.error("Failed to add booking to calendar: %s", e)
        return False