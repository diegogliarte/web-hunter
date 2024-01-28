from app.factories.scraper_enums import ScraperEnum
from app.scrapers.base_scraper import BaseScraper
from app.scrapers.fanatical_scraper import FanaticalScraper
from app.scrapers.humble_bundle_scraper import HumbleBundleScraper
from app.scrapers.steamdb_scraper import SteamDBScraper


class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_enum: ScraperEnum) -> BaseScraper:
        if scraper_enum == ScraperEnum.HUMBLE_BUNDLE:
            return HumbleBundleScraper()
        elif scraper_enum == ScraperEnum.FANATICAL:
            return FanaticalScraper()
        elif scraper_enum == ScraperEnum.STEAM_DB:
            return SteamDBScraper()

        raise ValueError("Unknown scraper")
