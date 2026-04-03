from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Ma'lumotlar bazasi manzili (PostgreSQL)
# Format: postgresql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Quvonch2006@localhost:5432/ai_hisobchi_db"

# 2. Engine yaratish 
# Bu ma'lumotlar bazasi bilan asosiy aloqa nuqtasi hisoblanadi
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # PostgreSQL uchun qo'shimcha pool sozlamalari (ixtiyoriy lekin tavsiya etiladi)
    pool_pre_ping=True, 
)

# 3. SessionLocal klassini yaratish
# Har bir so'rov uchun alohida ma'lumotlar bazasi sessiyasini yaratadi
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 4. Barcha modellar meros oladigan bazaviy klass
Base = declarative_base()

# 5. Dependency (Yordamchi funksiya)
# FastAPI endpointlarida ma'lumotlar bazasi sessiyasini xavfsiz boshqarish uchun
def get_db():
    """
    Har bir API so'rovi uchun yangi sessiya ochadi va 
    so'rov yakunlangach uni avtomatik yopadi.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()