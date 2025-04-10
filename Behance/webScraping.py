from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Profil bilgileri
profile_path = r"C:\Users\iruka\AppData\Local\Google\Chrome\User Data"
profile_directory = "Default"  # Eğer farklı profil kullanıyorsan değiştir

options = Options()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")  # Ekransız mod için, şimdilik kapalı

# Tarayıcıyı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Behance ana sayfasına git
driver.get("https://www.behance.net")

# Giriş yapıldığından emin olmak için biraz bekle
time.sleep(5)

print("✅ Giriş yapılmış profil ile bağlantı kuruldu!")



behance_stil_linkleri = {
    "anime": "https://www.behance.net/search/projects/anime%20digital%20art?tracking_source=typeahead_nav_suggestion&field=illustration",
    "pixel_art": "https://www.behance.net/search/projects/pixel%20art%20?tracking_source=typeahead_search_direct&field=illustration",
    "abstract_digital": "https://www.behance.net/search/projects/abstract%20illustration?tracking_source=typeahead_search_direct",
    "Realistic Portrait": "https://www.behance.net/search/projects/realistic%20portrait%20illustration?tracking_source=typeahead_search_suggestion",
    "simple_illustration":"https://www.behance.net/search/projects/simple%20illustration?tracking_source=typeahead_search_direct&field=illustration" ,
    "comic": "" ,
    "fantasy": 
}
