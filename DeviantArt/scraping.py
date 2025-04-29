from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
import os

#user-agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

stil_linkleri = {
    "anime": "https://www.deviantart.com/search?q=anime",
    "pixel_art": "https://www.deviantart.com/search?q=pixel+art",
    "comic": "https://www.deviantart.com/search?q=comic",
    "fantasy": "https://www.deviantart.com/search?q=fantasy",
    "simple_illustration": "https://www.deviantart.com/search?q=simple+illustration",
    "abstract_digital": "https://www.deviantart.com/search?q=abstract+digital",
    "digital_realism": "https://www.deviantart.com/search?q=digital+realism"
}

def get_artwork_links(driver):
    links = set()
    containers = driver.find_elements(By.CSS_SELECTOR, 'div._3Y0hT._3oBlM')  
    for container in containers:
        try:
            a_tag = container.find_element(By.TAG_NAME, "a")  
            href = a_tag.get_attribute("href")  
            if href and "#comments" not in href:  
                links.add(href)
            time.sleep(random.uniform(0.2, 0.6)) 
        except:
            continue
    return list(links)


def go_to_next_page(driver):
    try:
        next_link = driver.find_element(By.XPATH, '//a[text()="Next"]') 
        href = next_link.get_attribute("href")
        if href:
            driver.get(href)
            time.sleep(random.uniform(1.0, 2.5))  # Yükleme bekleme
            return True
    except Exception as e:
        print("SAYFADA HATA ", e)
    return False


 # İLK BURASIIIIIIIIIIIIIIIIIIII
def scrape_deviantart_links(stil_adi, stil_url, min_links=1500):
    print(f"{stil_adi} : Yapiliyor")

    options = Options()
    #options.add_argument("--headless=new")  # Tarayıcı arka planda çalışır
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(stil_url)
    time.sleep(random.uniform(1.0, 3.0))

    all_links = set()
    page_num = 0

    while len(all_links) < min_links:
        page_links = get_artwork_links(driver) 
        print(f"Sayfa {page_num}: {len(page_links)} link. Toplamı: {len(all_links)}")
        all_links.update(page_links)
        page_num += 1

        if not go_to_next_page(driver):  
            print(f"Sayfa Bitti. {len(all_links)} tane link toplandı.")
            break

    driver.quit()  #

    output_dir = os.path.join("deviantart_images", "linkler")
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, f"deviantart_links_{stil_adi}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(list(all_links), f, ensure_ascii=False, indent=2)

    print(f" {stil_adi} için toplam {len(all_links)} link kaydedildi: {json_path}\n")







# MAIN
for stil, link in stil_linkleri.items():
    scrape_deviantart_links(stil, link, min_links=2000)
