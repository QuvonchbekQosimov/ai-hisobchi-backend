from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import requests
import random
import smtplib
from email.mime.text import MIMEText

router = APIRouter()

GOOGLE_CLIENT_ID = "932175888025-3t33bu8c5627jpu0j329pfu05sme46go.apps.googleusercontent.com"

# --- Vaqtinchalik Baza (Foydalanuvchilar va Email OTP uchun) ---
# Format: {"quvonchbek": {"password": "123", "email": "qosimovquvonc@gmail.com"}}
fake_users_db = {}
email_otp_storage = {}

# --- Ma'lumot turlari (Pydantic modellari) ---
class UserAuth(BaseModel):
    username: str
    password: str

class GoogleTokenRequest(BaseModel):
    token: str

class EmailOTPRequest(BaseModel):
    email: str

class VerifyEmailRequest(BaseModel):
    username: str
    email: str
    otp: str

# --- Endpointlar (Marshrutlar) ---

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserAuth):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Bu login band! Boshqa login tanlang.")
    
    # Yangi foydalanuvchini bazaga qo'shish (Email hozircha bo'sh)
    fake_users_db[user.username] = {"password": user.password, "email": None}
    print(f"Backend: Yangi foydalanuvchi - {user.username}")
    return {"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz"}

@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login(user: UserAuth):
    user_data = fake_users_db.get(user.username)
    if not user_data or user_data["password"] != user.password:
        raise HTTPException(status_code=400, detail="Login yoki parol noto'g'ri!")

    return {
        "access_token": "AI_HISOBCHI_SECURE_JWT_TOKEN_2026",
        "token_type": "bearer",
        "user": {"username": user.username, "email": user_data["email"]}
    }

@router.post("/auth/google", status_code=status.HTTP_200_OK)
async def google_auth(data: GoogleTokenRequest):
    """Google orqali kirish (Faqat email ulangan bo'lsa ruxsat beriladi)"""
    try:
        google_api_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={data.token}"
        response = requests.get(google_api_url)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Google tokenni tasdiqlay olmadi.")
        
        user_info = response.json()
        google_email = user_info.get("email")

        # 1-QADAM: Bazadan shu emailga ega foydalanuvchini qidiramiz
        found_username = None
        for uname, udata in fake_users_db.items():
            if udata.get("email") == google_email:
                found_username = uname
                break
        
        # 2-QADAM: Agar topilmasa, TIZIMGA KIRITILMAYDI!
        if not found_username:
            raise HTTPException(
                status_code=403, 
                detail="Bu Google hisob ro'yxatdan o'tmagan! Avval oddiy login orqali kiring va profilingizdan emailni ulang."
            )

        # Muvaffaqiyatli kirish
        return {
            "access_token": "AI_HISOBCHI_SECURE_JWT_TOKEN_2026",
            "token_type": "bearer",
            "user": {"username": found_username, "email": google_email}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- EMAIL TASDIQLASH QISMI (SMTP) ---

@router.post("/auth/send-email-otp", status_code=status.HTTP_200_OK)
async def send_email_otp(data: EmailOTPRequest):
    """Foydalanuvchining Gmailiga tasdiqlash kodini yuborish"""
    try:
        otp_code = str(random.randint(100000, 999999))
        email_otp_storage[data.email] = otp_code
        
        # --- DIQQAT! Hozircha terminalga chiqaramiz. Haqiqiy xat yuborish uchun pastdagi kodni ochishingiz kerak ---
        print("\n" + "="*40)
        print("📧 GMAILGA XABAR KETDI")
        print(f"Manzil: {data.email}")
        print(f"Tasdiqlash kodi: {otp_code}")
        print("="*40 + "\n")

        # Haqiqiy Email yuborish mantiqi (Kelajakda ochib ishlating):
        """
        SENDER_EMAIL = "sizning_pochtangiz@gmail.com"
        SENDER_APP_PASSWORD = "16_talik_maxsus_app_parol" # Googledan olinadi
        
        msg = MIMEText(f"AI Hisobchi tizimida pochtangizni tasdiqlash kodi: {otp_code}")
        msg['Subject'] = 'Tasdiqlash kodi'
        msg['From'] = SENDER_EMAIL
        msg['To'] = data.email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, data.email, msg.as_string())
        """

        return {"message": "Tasdiqlash kodi elektron pochtangizga yuborildi!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email yuborishda xatolik: {str(e)}")

@router.post("/auth/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(data: VerifyEmailRequest):
    """Emailga borgan kodni tekshirish va profilga saqlash"""
    saved_otp = email_otp_storage.get(data.email)
    
    if not saved_otp or saved_otp != data.otp:
        raise HTTPException(status_code=400, detail="Tasdiqlash kodi noto'g'ri yoki eskirgan!")
    
    # Kod to'g'ri. Endi emailni foydalanuvchining bazasiga saqlaymiz
    if data.username in fake_users_db:
        fake_users_db[data.username]["email"] = data.email
        del email_otp_storage[data.email] # Xavfsizlik uchun kodni o'chiramiz
        print(f"Backend: {data.username} hisobiga {data.email} muvaffaqiyatli ulandi!")
        return {"message": "Email muvaffaqiyatli ulandi!"}
    
    raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi!")