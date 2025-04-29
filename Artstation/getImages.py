from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
import requests

def download_artstation_images(json_path, style_name, max_images=50):
    json_full_path = os.path.join("linkler", json_path)

    save_dir = os.path.join("gorseller", style_name)
    os.makedirs(save_dir, exist_ok=True)

    with open(json_full_path, "r", encoding="utf-8") as f:
        links = json.load(f)

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    #options.add_argument("--headless")  # Şu an tarayıcı açılacak

    driver = webdriver.Chrome(options=options)

    for idx, url in enumerate(links[:max_images]):
        try:
            print(f"{style_name} [{idx+1}/{max_images}] → {url}")
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
                print(f"Görsel Yok: {url}")

        except Exception as e:
            print(f"{idx+1}. HATA : {e}")
            continue

    driver.quit()
    print(f"{style_name} tamamlandı.")

# download_artstation_images("artstation_links_anime.json", "anime", max_images=1000)
# download_artstation_images("artstation_links_comic.json", "comic", max_images=950)
# download_artstation_images("artstation_links_digital_realism.json", "digital_realism", max_images=300)
# download_artstation_images("artstation_links_fantasy.json", "fantasy", max_images=200)
download_artstation_images("artstation_links_pixel_art.json", "pixel_art", max_images=900)
download_artstation_images("artstation_links_simple_illustration.json", "simple_illustration", max_images=100)
download_artstation_images("artstation_links_abstract_digital.json", "abstract_digital", max_images=300)
