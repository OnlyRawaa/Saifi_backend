from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.parents import router as parents_router
from routes.providers import router as providers_router
from routes.children import router as children_router
from routes.activities import router as activities_router
from routes.bookings import router as bookings_router
from routes.ai_router import router as ai_router   # <<=== NEW

app = FastAPI(
    title="Saifi Backend",
    version="1.0.0",
    description="Backend API for Saifi Platform"
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================
app.include_router(parents_router)
app.include_router(providers_router)
app.include_router(children_router)
app.include_router(activities_router)
app.include_router(bookings_router)
app.include_router(ai_router)  # <<=== NEW

# =========================
# ROOT CHECK
# =========================
@app.get("/")
def home():
    return {"message": "Saifi API is live 🔥", "status": "ok"}

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "healthy", "service": "saifi-backend"}
