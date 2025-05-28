from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import time
import requests
import csv
import sys

#### CONFIGURACIÓ I PREPARACIÓ ####

if len(sys.argv) != 2:
    print("Ús: python crawler.py <url>")
    sys.exit(1)

start_url = sys.argv[1]
domain = urlparse(start_url).netloc

# Inicialitza Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Llistes de control
to_visit = [start_url]
visited_urls = set()
errors_4xx = []

#### FUNCIONS PRINCIPALS ####

def check_url_status(url, origin):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if 400 <= response.status_code < 500:
            errors_4xx.append({
                'url': url,
                'status': response.status_code,
                'origin': origin
            })
    except requests.RequestException:
        errors_4xx.append({
            'url': url,
            'status': 'Request Failed',
            'origin': origin
        })

def crawl_page(url):
    if url in visited_urls:
        return

    visited_urls.add(url)
    try:
        driver.get(url)
        time.sleep(1)
        check_url_status(url, origin='Direct Access')

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href:
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                if parsed.netloc == domain:
                    if full_url not in visited_urls and full_url not in to_visit:
                        to_visit.append(full_url)
                        check_url_status(full_url, origin=url)
    except Exception as e:
        print(f"Error carregant {url}: {e}")

#### BUCLE PRINCIPAL ####

while to_visit:
    current_url = to_visit.pop(0)
    crawl_page(current_url)
    print(f"Processat: {current_url}")

#### EXPORTACIÓ D'ERRORS A CSV ####

def export_errors_to_csv(errors, filename="errors.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["url", "status", "origin"])
            writer.writeheader()
            for error in errors:
                writer.writerow(error)
        print(f"Informe exportat correctament a {filename}.")
    except Exception as e:
        print(f"Error exportant CSV: {e}")

export_errors_to_csv(errors_4xx)

#### TANCAMENT DEL DRIVER ####

driver.quit()
