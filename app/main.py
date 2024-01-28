import argparse
import logging

from dotenv import load_dotenv

from configuration.logger import setup_logger
from factories.notifier_enums import NotifierEnum
from factories.notifier_factory import NotifierFactory
from factories.scraper_enums import ScraperEnum
from factories.scraper_factory import ScraperFactory
from items.scraped_item import ScrapedItem
from items.base_item import BaseItem
from items.error_item import ErrorItem
from notifications.base_notifier import BaseNotifier
from scrapers.base_scraper import BaseScraper
from sqlitedb import SQLiteDB

logger = logging.getLogger(__name__)
load_dotenv()


def main(scraper_enums: list[ScraperEnum], notifier_enums: list[NotifierEnum]) -> None:
    logger.info("Starting main application")

    scrapers = [ScraperFactory.get_scraper(scraper_enum) for scraper_enum in scraper_enums]
    scraped_data = execute_scrapers(scrapers)

    if scraped_data:
        notifiers = [NotifierFactory.get_notifier(notifier_enum) for notifier_enum in notifier_enums]
        execute_notifiers(notifiers, scraped_data)
    else:
        logger.info("No new data found")

    logger.info("Ending main application\n")


def execute_scrapers(scrapers: list[BaseScraper]) -> dict[type[BaseScraper], list[BaseItem]]:
    new_scraped_data = {}
    for scraper in scrapers:
        scraper_name = scraper.__class__.__name__
        logger.info(f"Executing: {scraper_name}")
        try:
            items_scraped = scraper.scrape()
            new_items = filter_new_items(items_scraped)

            if new_items:
                logger.info(f"New data scraped from {scraper_name}: {len(new_items)} items")
                add_items_to_db(new_items)
                new_scraped_data[scraper.__class__] = new_items

        except Exception as e:
            logger.exception(f"Error during scraping from {scraper_name}: {e}")
            new_items = [ErrorItem(scraper=type(scraper), message=str(e))]
            add_items_to_db(new_items)
            new_scraped_data[scraper.__class__] = new_items

    return new_scraped_data


def add_items_to_db(new_items):
    db = SQLiteDB()

    for item in new_items:
        if isinstance(item, ScrapedItem):
            db.add_scraped_item(item)


def filter_new_items(items_scraped: list[BaseItem]) -> list[BaseItem]:
    db = SQLiteDB()

    return [
        item
        for item in items_scraped
        if (isinstance(item, ScrapedItem) and not db.item_already_sent(item)) or isinstance(item, ErrorItem)
    ]


def execute_notifiers(notifiers: list[BaseNotifier], scraped_data: dict[type[BaseScraper], list[BaseItem]]):
    db = SQLiteDB()

    for notifier in notifiers:
        notifier_name = notifier.__class__.__name__
        logger.info(f"Sending notification via {notifier_name}")
        try:
            notifier.notify(scraped_data)
            for scraper_class, items in scraped_data.items():
                for item in items:
                    if isinstance(item, ScrapedItem):
                        db.mark_item_as_sent(item)

        except Exception as e:
            logger.exception(f"Error sending notification via {notifier_name}: {e}", exc_info=True)
            raise


if __name__ == "__main__":
    setup_logger()

    parser = argparse.ArgumentParser(description="Web Scraper Application")
    parser.add_argument(
        "--scrapers",
        nargs="*",
        choices=[scraper.value for scraper in ScraperEnum],
        help="List of scrapers to use",
        required=True,
    )
    parser.add_argument(
        "--notifiers",
        nargs="*",
        choices=[notifier.value for notifier in NotifierEnum],
        help="List of notifiers to use",
        default=[NotifierEnum.EMAIL.value],
    )

    args = parser.parse_args()
    scrapers = [ScraperEnum(scraper) for scraper in args.scrapers]
    notifiers = [NotifierEnum(notifier) for notifier in args.notifiers]
    main(scrapers, notifiers)
