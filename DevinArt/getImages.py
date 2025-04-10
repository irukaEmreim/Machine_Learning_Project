import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Stil dosyaları listesi
style_files = [
    "deviantart_links_anime.json",
    "deviantart_links_pixel_art.json",
    "deviantart_links_comic.json",
    "deviantart_links_fantasy.json",
    "deviantart_links_simple_illustration.json",
    "deviantart_links_abstract_digital.json",
    "deviantart_links_digital_realism.json"
]

# Stil ismini dosya adından çıkar
def get_style_name(filename):
    return filename.replace("deviantart_links_", "").replace(".json", "")

# Görsel indirme fonksiyonu
def download_image(url, path):
    try:
        img_data = requests.get(url).content
        with open(path, "wb") as f:
            f.write(img_data)
    except Exception as e:
        print(f"❌ {url} indirilemedi: {e}")

# Tarayıcı ayarları
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Her dosya için işlemi uygula
for file in style_files:
    style = get_style_name(file)
    os.makedirs(f"deviantart_images/{style}", exist_ok=True)

    with open(file, "r", encoding="utf-8") as f:
        links = json.load(f)

    for i, link in enumerate(links):
        try:
            driver.get(link)
            time.sleep(3)

            container = driver.find_element(By.CLASS_NAME, "_2Rewc")
            img = container.find_element(By.TAG_NAME, "img")
            src = img.get_attribute("src")

            if src:
                filename = f"deviantart_images/{style}/{style}_{i}.jpg"
                download_image(src, filename)
                print(f"✅ Kaydedildi: {filename}")
        except Exception as e:
            print(f"⚠️ Hata ({link}): {e}")

driver.quit()
print("🎉 Tüm görseller indirildi.")
