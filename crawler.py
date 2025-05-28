## TEST SELENIUM BÀSIC
# from selenium import webdriver
 
# driver = webdriver.Chrome() 
##

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import time
import requests
import csv
import sys


#### FASE 1 - EXPLORACIÓ DE DOMINIS

driver = webdriver.Chrome()

# --- Configura domini inicial ---
if len(sys.argv) != 2:
    print("Ús: python crawler.py <url>")
    sys.exit(1)

start_url = sys.argv[1]

domain = urlparse(start_url).netloc

# --- Estructures de control ---
to_visit = [start_url]   # cua de URLs per visitar
visited = set()          # conjunt de URLs ja visitades

# --- Inicia l'exploració ---
while to_visit:
    url = to_visit.pop(0)
    if url in visited:
        continue
    visited.add(url)

    try:
        driver.get(url)
        time.sleep(1)  # petit delay per evitar bloquejos

        # Extreu tots els enllaços <a href="...">
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href:
                parsed = urlparse(href)
                if parsed.netloc == "" or parsed.netloc == domain:
                    full_url = urljoin(url, href)
                    if full_url not in visited and full_url not in to_visit:
                        to_visit.append(full_url)

        print(f"Visitat: {url} → {len(links)} enllaços trobats")
    except Exception as e:
        print(f"Error a {url}: {e}")

###################################


#### FASE 2 - DETECCIÓ D'ERRORS 4XX

visited_urls = set()
errors_4xx = []

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

def crawl(driver, url, base_url):
    if url in visited_urls or not url.startswith(base_url):
        return

    visited_urls.add(url)
    driver.get(url)
    time.sleep(1)  # ajusta el temps si cal

    # Comprovar la URL mateixa
    check_url_status(url, origin='Direct Access')

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("http"):
            check_url_status(href, origin=url)
            crawl(driver, href, base_url)

###################################


#### FASE 3 - GENERACIÓ D'INFORME #

def export_errors_to_csv(errors, filename="errors.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["url", "status", "origin"])
        writer.writeheader()
        for error in errors:
            writer.writerow(error)

# Crida aquesta funció un cop hagi acabat el crawler
export_errors_to_csv(errors_4xx)

###################################

driver.quit()