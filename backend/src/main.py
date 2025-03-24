from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import api_router
import uvicorn
from database.session import init_db

app = FastAPI(
    title="NURBURGRING-EXPERIENCE API",
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

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized")

app.include_router(api_router, prefix="/api/v1")

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
