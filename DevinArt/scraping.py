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

    # Sadece ilgili div'lerin içindeki <a> tag'lerini al
    containers = driver.find_elements(By.CSS_SELECTOR, 'div._3Y0hT._3oBlM')
    for container in containers:
        a_tag = container.find_element(By.TAG_NAME, "a")
        href = a_tag.get_attribute("href")

        # Yorum sayfalarını filtrele (#comments içerenleri alma)
        if "#comments" not in href:
            links.add(href)

    return list(links)


def go_to_next_page(driver):
    try:
        next_link = driver.find_element(By.XPATH, '//a[text()="Next"]')
        href = next_link.get_attribute("href")
        if href:
            driver.get(href)
            time.sleep(2)
            return True
    except Exception as e:
        print("➡️ Sonraki sayfa bulunamadı:", e)
    return False

def scrape_deviantart_links(stil_adi, stil_url, max_pages=5):
    print(f"🔍 Stil işleniyor: {stil_adi}")
    options = Options()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(stil_url)
    time.sleep(3)

    all_links = []

    for _ in range(max_pages):
        page_links = get_artwork_links(driver)
        print(f"✅ {len(page_links)} link bulundu.")
        all_links.extend(page_links)
        if not go_to_next_page(driver):
            break

    driver.quit()

    # JSON dosyasına kaydet
    with open(f"deviantart_links_{stil_adi}.json", "w", encoding="utf-8") as f:
        json.dump(all_links, f, ensure_ascii=False, indent=2)
    print(f"💾 {stil_adi} için {len(all_links)} link kaydedildi.\n")

# Tüm stiller için çalıştır
for stil, link in stil_linkleri.items():
    scrape_deviantart_links(stil, link, max_pages=2)
