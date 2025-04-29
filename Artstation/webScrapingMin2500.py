from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os


def scrape_until_min_links(url, stil_adi, min_links=2500):
    
    # Tarayıcı ayarları
    options = Options()
    #options.add_argument("--headless")  # Arka plan
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)  

    prev_count = 0         # Önceki link sayısp
    scroll_count = 0       # scroll sayısı
    links = set()          # tüm linkler

    while len(links) < min_links:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        scroll_count += 1

        try:
            WebDriverWait(driver, 10).until(        ## 10 saniye bekler
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.gallery-grid-link")) 
            )
        except:
            print("Bittii.")
            break

        elements = driver.find_elements(By.CSS_SELECTOR, "a.gallery-grid-link")
        for el in elements:
            href = el.get_attribute("href")
            if href and "/artwork/" in href:  # Sadece artwork 
                links.add(href)

        print(f"{scroll_count}: {len(links)} toplandı")

        if len(links) == prev_count:
            print(" YENİ LİNK YOK BİTTİİİİİİİ.")
            break
        prev_count = len(links)

    driver.quit()  

    # json
    os.makedirs("linkler", exist_ok=True)
    safe_name = stil_adi.lower()  
    with open(f"linkler/artstation_links_{safe_name}.json", "w", encoding="utf-8") as f:
        json.dump(list(links), f, indent=2) 

    print(f"[{stil_adi}] için  {len(links)} görsel.")

stil_linkleri = {
    "anime": "https://www.artstation.com/search?sort_by=likes&query=anime&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&medium_ids_include=1&category_ids_include=38",
    "pixel_art": "https://www.artstation.com/search?sort_by=likes&query=pixel%20art&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&category_ids_include=52&medium_ids_include=1",
    "abstract_digital": "https://www.artstation.com/search?sort_by=likes&query=abstract%20digital&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&category_ids_include=35&medium_ids_include=1",
    "digital_realism": "https://www.artstation.com/search?sort_by=likes&query=digital%20realism&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&category_ids_include=54&medium_ids_include=1",
    "simple_illustration": "https://www.artstation.com/search?sort_by=likes&query=Simple%20Illustration&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&category_ids_include=27&medium_ids_include=1",
    "comic": "https://www.artstation.com/search?sort_by=likes&query=comic&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&category_ids_include=14&medium_ids_include=1",
    "fantasy": "https://www.artstation.com/search?sort_by=likes&query=fantasy&tags_exclude=CreatedWithAI&software_ids_exclude=193982,187754,205467&category_ids_include=2&medium_ids_include=1"
}

#  MAIN
for stil, url in stil_linkleri.items():
    print(f"\n🔍 [{stil}] verisi toplanıyor...")
    scrape_until_min_links(url, stil, min_links=1000)
