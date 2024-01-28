from factories.scraper_enums import ScraperEnum
from scrapers.base_scraper import BaseScraper
from scrapers.fanatical_scraper import FanaticalScraper
from scrapers.humble_bundle_scraper import HumbleBundleScraper
from scrapers.steamdb_scraper import SteamDBScraper
from scrapers.humble_choice_scraper import HumbleChoiceScraper


class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_enum: ScraperEnum) -> BaseScraper:
        if scraper_enum == ScraperEnum.HUMBLE_BUNDLE:
            return HumbleBundleScraper()
        elif scraper_enum == ScraperEnum.FANATICAL:
            return FanaticalScraper()
        elif scraper_enum == ScraperEnum.STEAM_DB:
            return SteamDBScraper()
        elif scraper_enum == ScraperEnum.HUMBLE_CHOICE:
            return HumbleChoiceScraper()

        raise ValueError("Unknown scraper")
