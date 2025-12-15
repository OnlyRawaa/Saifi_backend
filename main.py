from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.parents import router as parents_router
from routes.providers import router as providers_router
from routes.children import router as children_router
from routes.activities import router as activities_router
from routes.bookings import router as bookings_router
from routes.ai_router import router as ai_router

from services.ai_service import load_assets_once, refresh_ai_cache
from services.ai_cache import STATE


# =========================
# APP INIT
# =========================
app = FastAPI(
    title="Saifi Backend",
    version="1.0.0",
    description="Backend API for Saifi Platform"
)

# =========================
# STARTUP EVENTS
# =========================
@app.on_event("startup")
async def startup():
    try:
        await refresh_ai_cache(force=True)
    except Exception as e:
        print("AI cache skipped:", e)



# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production if you want
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
app.include_router(ai_router)

# =========================
# ROOT CHECK
# =========================
@app.get("/")
def home():
    return {
        "message": "Saifi API is live 🔥",
        "status": "ok"
    }

# =========================
# GLOBAL HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "saifi-backend",
        "ai_model_loaded": STATE.model is not None,
        "ai_matrix_loaded": STATE.matrix is not None
    }
