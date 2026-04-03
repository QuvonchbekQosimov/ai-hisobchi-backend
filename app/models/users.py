from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    """
    Foydalanuvchi modeli - Tizimga kirish, profil va 
    Google autentifikatsiya ma'lumotlarini saqlaydi.
    """
    __tablename__ = "users"

    # --- ASOSIY ID VA IDENTIFIKATSIYA ---
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Telefon raqami - Asosiy login sifatida ishlatiladi
    phone_number = Column(String, unique=True, index=True, nullable=False)
    
    # Shifrlangan parol (bcrypt orqali saqlanadi)
    hashed_password = Column(String, nullable=False)
    
    # --- PROFIL MA'LUMOTLARI ---
    full_name = Column(String, nullable=True)
    
    # Profil rasmi (URL manzili yoki fayl nomi saqlanadi)
    profile_picture = Column(String, nullable=True, default="default_profile.png")
    
    # Foydalanuvchi haqida qisqacha ma'lumot (ixtiyoriy)
    bio = Column(Text, nullable=True)

    # --- GOOGLE AUTHENTICATION ---
    # Google orqali ro'yxatdan o'tganda to'ldiriladi
    google_email = Column(String, unique=True, index=True, nullable=True)
    google_id = Column(String, unique=True, index=True, nullable=True)

    # --- TIZIM HOLATI VA VAQT ---
    # Foydalanuvchi faolligi (bloklangan yoki yo'qligini tekshirish uchun)
    is_active = Column(Boolean, default=True)
    
    # Admin huquqi (kelajakda kerak bo'lishi mumkin)
    is_superuser = Column(Boolean, default=False)
    
    # Ro'yxatdan o'tgan vaqti (UTC bo'yicha)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Ma'lumotlar oxirgi marta yangilangan vaqti
    updated_at = Column(
        DateTime, 
        default=datetime.datetime.utcnow, 
        onupdate=datetime.datetime.utcnow
    )

    # --- MUNOSABATLAR (RELATIONSHIPS) ---
    # Foydalanuvchiga tegishli barcha moliya yozuvlari (Daromad/Xarajat)
    # Bu qator 'Finance' modeli yaratilganda u bilan bog'lanishni ta'minlaydi
    finances = relationship("Finance", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone_number}, name={self.full_name})>"