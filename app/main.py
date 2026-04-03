from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Loyiha modullarini chaqirish
from app.database import engine, Base
from app.models import users, finance
from app.routers import auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth # o'zingizning routerlaringiz

app = FastAPI()

# Barcha saytlardan keladigan so'rovlarga ruxsat berish (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Kelajakda bu yerga faqat Vercel linkini yozasiz, hozircha hamma kirsin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
# 1. Ma'lumotlar bazasi jadvallarini yaratish
# Ushbu kod server ishga tushganda PostgreSQL/SQLite bazangizda 
# jadvallar yo'q bo'lsa, ularni avtomatik yaratib beradi.
Base.metadata.create_all(bind=engine)

# 2. FastAPI obyektini yaratish
# Dasturning asosiy "yuragi". Swagger UI hujjatlarida shu ma'lumotlar ko'rinadi.
app = FastAPI(
    title="BAIS - Moliya va Logistika Tizimi",
    description="BAIS loyihasi uchun xavfsiz va tezkor backend API tizimi",
    version="1.0.0"
)

# 3. CORS SOZLAMALARI (MUHIM!)
# Brauzer blokirovkalarini (CORS ERR_FAILED) oldini olish uchun 
# vaqtincha barcha manzillarga ruxsat berildi.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Barcha frontend manzillariga (localhost, 127.0.0.1, Vercel va h.k.) ruxsat
    allow_credentials=True,      # Cookie va xavfsizlik tokenlari o'tishiga ruxsat
    allow_methods=["*"],         # GET, POST, PUT, DELETE, OPTIONS - barchasiga ruxsat
    allow_headers=["*"],         # Barcha turdagi HTTP header'larga ruxsat (Authorization, Content-Type)
)

# 4. Routerlarni ulash
# Auth (avtentifikatsiya) uchun yozilgan barcha yo'llarni (endpointlarni) dasturga qo'shamiz
app.include_router(auth.router)

# 5. Asosiy sahifa (Sog'lomlikni tekshirish / Health Check)
# Tizim ishlayotganini bilish uchun oddiy test yo'li
@app.get("/", tags=["Asosiy Sahifa"])
def read_root():
    return {
        "xabar": "Salom! BAIS backend tizimi muvaffaqiyatli ishga tushdi va aloqaga tayyor!",
        "status": "online",
        "version": "1.0.0"
    }