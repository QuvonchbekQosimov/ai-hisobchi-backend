import requests

# ==========================================
# 🚀 SIZNING SHAXSIY GEMINI API KALITINGIZ:
# ==========================================
API_KEY = "AIzaSyAfePKH_zVcwXO_j53eR6VGz8PLRcPD4MU"  # O'zingizning kalitingiz

def check_available_models():
    print("⏳ Google Gemini serverlariga ulanmoqda...\n")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        response = requests.get(url)
        
        # Agar kalit to'g'ri bo'lsa va server javob bersa
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            print(f"✅ Muvaffaqiyatli! Kalitingiz orqali {len(models)} ta modelga ruxsat bor:\n")
            print("=" * 60)
            
            for model in models:
                name = model.get("name").replace("models/", "") # 'models/gemini-1.5-flash' ni tozalaymiz
                display_name = model.get("displayName")
                methods = model.get("supportedGenerationMethods", [])
                
                # Bizga asosan chat/matn uchun "generateContent" metodi kerak
                if "generateContent" in methods:
                    print(f"📌 Model ID (Kodga yoziladigani): {name}")
                    print(f"📖 Rasmiy nomi: {display_name}")
                    print("-" * 60)
                    
        else:
            print(f"❌ Xatolik yuz berdi! Status kod: {response.status_code}")
            print(f"Sababi: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Internet yoki tarmoq xatoligi: {e}")
        print("VPN yoqib tekshirib ko'ring (O'zbekistonda ba'zan bloklanadi).")

if __name__ == "__main__":
    check_available_models()