from fastapi import FastAPI

from routes.parents import router as parents_router
from routes.providers import router as providers_router
from routes.children import router as children_router
from routes.activities import router as activities_router
from routes.bookings import router as bookings_router

app = FastAPI(title="Saifi Backend")

app.include_router(parents_router)
app.include_router(providers_router)
app.include_router(children_router)
app.include_router(bookings_router)
app.include_router(activities_router, prefix="/activities", tags=["Activities"])

@app.get("/")
def home():
    return {"message": "Saifi API is live 🔥"}
