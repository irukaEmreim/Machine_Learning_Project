"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, json, requests
from tqdm import tqdm

def download_artstation_images(json_path, stil_adi):
    # JSON'dan proje linklerini oku
    with open(json_path, "r", encoding="utf-8") as f:
        links = json.load(f)

    # Klasör oluştur
    os.makedirs(f"gorseller/{stil_adi}", exist_ok=True)

    # Selenium başlat
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    for i, url in enumerate(tqdm(links[:50], desc=stil_adi)):  # test amaçlı ilk 50
        try:
            driver.get(url)
            time.sleep(2)  # sayfanın yüklenmesi için

            # Tüm <source> elementlerini al
            sources = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "picture source"))
            )

            for j, src in enumerate(sources):
                srcset = src.get_attribute("srcset")
                if srcset and srcset.startswith("https://cdna.artstation.com/"):
                    img_data = requests.get(srcset).content
                    with open(f"gorseller/{stil_adi}/{stil_adi}_{i}_{j}.jpg", "wb") as f:
                        f.write(img_data)
            time.sleep(0.5)

        except Exception as e:
            print(f"⚠️ {i}. görselde hata: {e}")
            continue

    driver.quit()
    print(f"✅ {stil_adi} için görsel indirme tamamlandı.")


# Örnek kullanım:
download_artstation_images("veri/artstation_links_anime.json", "anime")
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import os
import json
import time
import requests
def download_artstation_images(json_path, style_name, max_images=50):
    # JSON yolunu projeye göre ayarla
    json_full_path = os.path.join("linkler", json_path)

    # Görsellerin kaydedileceği klasör
    save_dir = os.path.join("gorseller", style_name)
    os.makedirs(save_dir, exist_ok=True)

    with open(json_full_path, "r", encoding="utf-8") as f:
        links = json.load(f)

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    for idx, url in enumerate(tqdm(links[:max_images], desc=style_name)):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "picture img"))
            )
            time.sleep(1)

            img_element = driver.find_element(By.CSS_SELECTOR, "picture img")
            img_url = img_element.get_attribute("src")

            if img_url:
                ext = img_url.split("?")[0].split(".")[-1]
                file_path = os.path.join(save_dir, f"{style_name}_{idx+1}.{ext}")
                r = requests.get(img_url)
                with open(file_path, "wb") as f:
                    f.write(r.content)
            else:
                print(f"⚠️ Görsel URL bulunamadı: {url}")

        except Exception as e:
            print(f"⚠️ {idx+1}. görselde hata: {e}")
            continue

    driver.quit()
    print(f"✅ {style_name} için görsel indirme tamamlandı.")

# Kullanım örneği
download_artstation_images("artstation_links_anime.json", "anime", max_images=50)
download_artstation_images("artstation_links_comic.json", "comic", max_images=50)
download_artstation_images("artstation_links_digital_realism.json", "digital_realism", max_images=30)
download_artstation_images("artstation_links_fantasy.json", "fantasy", max_images=30)
download_artstation_images("artstation_links_pixel_art.json", "pixel_art", max_images=50)
download_artstation_images("artstation_links_simple_illustration.json", "simple_illustration", max_images=50)
download_artstation_images("artstation_links_abstract_digital.json", "abstract_digital", max_images=50)
