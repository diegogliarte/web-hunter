
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.items.base_item import BaseItem
from app.items.scraped_item import ScrapedItem
from app.scrapers.base_scraper import BaseScraper


class FanaticalScraper(BaseScraper):
    def scrape(self) -> list[BaseItem]:
        url = "https://www.fanatical.com/en/bundle"

        # Setup for headless Chrome
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        service = Service(r"chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        scraped_items = []

        try:
            driver.get(url)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "HitCardsRow")))

            bundles = driver.find_elements(By.CLASS_NAME, "HitCardContainer")
            for bundle in bundles:
                a_element = bundle.find_element(By.TAG_NAME, "a")
                href = a_element.get_attribute("href")
                name = href.split("/")[-1]
                name = name.replace("-", " ").title()
                item = ScrapedItem(name=name, scraper=type(self), url=href)
                scraped_items.append(item)

            return scraped_items

        finally:
            driver.quit()
