from selenium import webdriver                              
from selenium.webdriver.common.by import By                  
from selenium.webdriver.chrome.service import Service       
from selenium.webdriver.chrome.options import Options       
from webdriver_manager.chrome import ChromeDriverManager    
import os                   
import json                
import time                 
import random               
import requests             

json_dir = os.path.join("deviantart_images", "linkler")

style_files = [
    "deviantart_links_anime.json",
    "deviantart_links_pixel_art.json",
    "deviantart_links_comic.json",
    "deviantart_links_fantasy.json",
    "deviantart_links_simple_illustration.json",
    "deviantart_links_abstract_digital.json",
    "deviantart_links_digital_realism.json"
]

def get_style_name(filename: str) -> str:
    return filename.replace("deviantart_links_", "").replace(".json", "")


def download_image(url: str, path: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://www.deviantart.com/',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  
        with open(path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"İNMEDİ : {url} -> {e}")


options = Options()
# options.add_argument("--headless=new")  
options.add_argument("--disable-blink-features=AutomationControlled")  
options.add_argument("--disable-gpu")               
options.add_argument("--window-size=1920,1080")     
options.add_argument("--start-maximized")           
options.add_experimental_option("excludeSwitches", ["enable-automation"])   # Bot engel
options.add_experimental_option('useAutomationExtension', False)            # Bot engel


# Tam yüklemeyi beklemez
options.set_capability("pageLoadStrategy", "eager")

# WebDriver'ı başlat (ChromeDriver otomatik yüklenir)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Tarayıcıya bot olmadığını söyleyen JavaScript kodu (otomasyon algılamasını engellemek için)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    """
})


# MAINNN
for file in style_files:
    style = get_style_name(file) 
    json_path = os.path.join(json_dir, file)

    output_dir = os.path.join("deviantart_images", style)
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        links = json.load(f)

    for i, link in enumerate(links):
        try:
            print(f"Link : {link}")
            driver.get(link)

            time.sleep(random.uniform(2.5, 5.0))

            container = driver.find_element(By.CLASS_NAME, "_2Rewc")
            img = container.find_element(By.TAG_NAME, "img")
            src = img.get_attribute("src")  # Görsel URL

            if src:
                filename = os.path.join(output_dir, f"{style}_{i}.jpg")
                download_image(src, filename)
                print(f"Kaydedildi: {filename}")
            else:
                print(f"Görsel Yok gibi : {link}")

        except Exception as e:
            print(f"Hata ({link}): {e}")
            time.sleep(3)  

driver.quit()
