from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.parents import router as parents_router
from routes.providers import router as providers_router
from routes.children import router as children_router
from routes.activities import router as activities_router
from routes.bookings import router as bookings_router

app = FastAPI(
    title="Saifi Backend",
    version="1.0.0",
    description="Backend API for Saifi Platform"
)

# =========================
# ✅ CORS CONFIG (IMPORTANT FOR FLUTTER)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقًا يمكنكِ تحديد دومين التطبيق فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ✅ ROUTERS
# =========================
app.include_router(parents_router, prefix="/parents", tags=["Parents"])
app.include_router(providers_router, prefix="/providers", tags=["Providers"])
app.include_router(children_router, prefix="/children", tags=["Children"])
app.include_router(activities_router, prefix="/activities", tags=["Activities"])
app.include_router(bookings_router, prefix="/bookings", tags=["Bookings"])

# =========================
# ✅ ROOT CHECK
# =========================
@app.get("/")
def home():
    return {
        "message": "Saifi API is live 🔥",
        "status": "ok"
    }

# =========================
# ✅ HEALTH CHECK (FOR RENDER + DEBUGGING)
# =========================
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "saifi-backend"
    }
