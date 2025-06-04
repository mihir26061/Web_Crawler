import logging
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, urljoin
import os
import pandas as pd

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("ProductCrawler")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = RotatingFileHandler(f"{log_dir}/crawler.log", maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def is_product_url(url):
    product_keywords = ['/product/', '/products/', '/item/', '/p/', '/details/', '/shop/', '/pd/', '/collections/', 'cart', 'p-mp']
    return any(k in url for k in product_keywords)

def extract_links(driver, base_url, domain):
    links = set()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(base_url, href)
        if domain in urlparse(full_url).netloc:
            links.add(full_url)
    return links

def crawl_site(start_url, max_pages=100):
    domain = urlparse(start_url).netloc
    visited = set()
    queue = [start_url]
    found_products = set()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/114.0.5735.90 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue

            logger.info(f"Visiting: {url}")
            try:
                driver.get(url)
                time.sleep(0.2)
            except Exception as e:
                logger.error(f"Failed to load {url}: {e}")
                continue

            visited.add(url)
            links = extract_links(driver, url, domain)

            for link in links:
                if link in visited:
                    continue
                if is_product_url(link):
                    logger.debug(f"Found product: {link}")
                    found_products.add(link)
                else:
                    queue.append(link)

    finally:
        driver.quit()

    logger.info(f"Finished crawling {start_url} - Found {len(found_products)} product URLs.")
    return found_products


if __name__ == "__main__":
    sites = [
        "https://nykaafashion.com/",
        "https://www.westside.com/",
        "https://www.virgio.com/",
        "https://www.tatacliq.com/",
    ]

    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    for site in sites:
        logger.info(f"\n--- Crawling {site} ---")
        products = crawl_site(site)
        if not products:
            logger.warning(f"No product URLs found for {site}")
            continue
        
        domain_name = urlparse(site).netloc.replace('www.', '').replace('.', '_')
        df = pd.DataFrame(sorted(products), columns=['product_url'])
        filename = f"{domain_name}_products.xlsx"
        filepath = f'{output_dir}/{filename}'
        df.to_excel(filepath, index=False)
        logger.info(f"Saved {len(df)} product URLs to {filepath}")
