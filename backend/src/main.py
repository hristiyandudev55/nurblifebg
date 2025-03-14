from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(
    title="NURBLIFE-EXPERIENCE API",
    description="Experience the legenedary Green Hell Track with our services.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import functions from google_calendar.py
try:
    from utils.google_calendar import get_events, check_date_availability

    app.get("/events")(get_events)
    app.get("/check-date/{date}")(check_date_availability)

except ImportError as e:
    print(f"ERROR: Failed to import functions from google_calendar.py: {e}")
    # Show more information about the error
    import traceback

    traceback.print_exc()
    raise


if __name__ == "__main__":
    print("Starting the server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
