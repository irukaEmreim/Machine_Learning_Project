"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

stil_linkleri = {
    "anime": "https://www.deviantart.com/search?q=anime",
    "pixel_art": "https://www.deviantart.com/search?q=pixel+art",
    "comic": "https://www.deviantart.com/search?q=comic",
    "fantasy": "https://www.deviantart.com/search?q=fantasy",
    "simple_illustration": "https://www.deviantart.com/search?q=simple+illustration",
    "abstract_digital": "https://www.deviantart.com/search?q=abstract+digital",
    "digital_realism": "https://www.deviantart.com/search?q=digital+realism"
}

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def collect_links_from_page(driver):
    time.sleep(3)
    elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/art/"]')
    links = set()
    for el in elements:
        href = el.get_attribute("href")
        if href:
            clean_link = href.split("#")[0]  # '#comments' gibi fragment'leri temizle
            links.add(clean_link)
    return links

def go_to_next_page(driver):
    try:
        next_link = driver.find_element(By.XPATH, '//a[text()="Next"]')
        href = next_link.get_attribute("href")
        if href:
            driver.get(href)
            time.sleep(3)  # Yeni sayfa yüklenmesini bekle
            return True
    except Exception as e:
        print("🚫 'Next' linki bulunamadı:", e)
    return False


def scrape_deviantart_links(base_url, max_pages=5, output_filename="deviantart_links.json"):
    driver = setup_driver()
    driver.get(base_url)
    time.sleep(5)

    all_links = set()
    page = 1

    while page <= max_pages:
        print(f"🔎 Sayfa {page} işleniyor...")
        new_links = collect_links_from_page(driver)
        print(f"✅ {len(new_links)} yeni link bulundu.")
        all_links.update(new_links)

        if not go_to_next_page(driver):
            break
        page += 1

    driver.quit()

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(list(all_links), f, ensure_ascii=False, indent=2)

    print(f"🎉 Toplam {len(all_links)} link kaydedildi: {output_filename}")

# Örnek kullanım:
if __name__ == "__main__":
    scrape_deviantart_links("https://www.deviantart.com/search?q=anime", max_pages=5, output_filename="deviantart_anime_links.json")
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
import os

stil_linkleri = {
    "anime": "https://www.deviantart.com/search?q=anime",
    "pixel_art": "https://www.deviantart.com/search?q=pixel+art",
    "comic": "https://www.deviantart.com/search?q=comic",
    "fantasy": "https://www.deviantart.com/search?q=fantasy",
    "simple_illustration": "https://www.deviantart.com/search?q=simple+illustration",
    "abstract_digital": "https://www.deviantart.com/search?q=abstract+digital",
    "digital_realism": "https://www.deviantart.com/search?q=digital+realism"
}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

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
            time.sleep(random.uniform(1.0, 2.5))
            return True
    except Exception as e:
        print("➡️ Sonraki sayfa bulunamadı:", e)
    return False

def scrape_deviantart_links(stil_adi, stil_url, min_links=1500):
    print(f"\n🔍 Stil işleniyor: {stil_adi}")
    options = Options()
    options.add_argument("--headless=new")
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
        print(f"📄 Sayfa {page_num}: {len(page_links)} link bulundu. Toplam: {len(all_links)}")
        all_links.update(page_links)
        page_num += 1

        if not go_to_next_page(driver):
            print(f"⚠️ Sonraki sayfa yok. {len(all_links)} link ile durduruldu.")
            break

    driver.quit()

    # Kayıt klasörü
    output_dir = os.path.join("deviantart_images", "linkler")
    os.makedirs(output_dir, exist_ok=True)

    # Dosya yolu
    json_path = os.path.join(output_dir, f"deviantart_links_{stil_adi}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(list(all_links), f, ensure_ascii=False, indent=2)

    print(f"💾 {stil_adi} için toplam {len(all_links)} link kaydedildi: {json_path}\n")


# 🔁 Tüm stiller için çalıştır
for stil, link in stil_linkleri.items():
    scrape_deviantart_links(stil, link, min_links=2000)
