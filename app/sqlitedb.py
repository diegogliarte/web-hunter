import sqlite3
import logging
from typing import Optional

from configuration import settings
from items.scraped_item import ScrapedItem

logger = logging.getLogger(__name__)


class SQLiteDB:
    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(settings.DATABASE_PATH)
            self.create_table()
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def create_table(self):
        if not self.conn:
            return
        try:
            query = """
                CREATE TABLE IF NOT EXISTS scraped_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    scraper TEXT NOT NULL,
                    url TEXT,
                    price REAL,
                    expiration_date TIMESTAMP,
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
            raise

    def item_exists(self, item: ScrapedItem) -> bool:
        if not self.conn:
            return False
        try:
            query = """
                SELECT 1 FROM scraped_items
                WHERE name = ? AND scraper = ? AND url = ? 
                AND (price = ? OR (price IS NULL AND ? IS NULL))
                AND (expiration_date = ? OR (expiration_date IS NULL AND ? IS NULL));
            """
            cursor = self.conn.execute(
                query,
                (
                    item.name,
                    item.scraper.__name__,
                    item.url,
                    item.price,
                    item.price,
                    item.expiration_date,
                    item.expiration_date,
                ),
            )
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Error checking if item exists in database: {e}")
            raise

    def add_scraped_item(self, item: ScrapedItem) -> Optional[bool]:
        if not self.conn:
            return None
        try:
            query = """
                INSERT INTO scraped_items (name, scraper, url, price, expiration_date)
                VALUES (?, ?, ?, ?, ?);
            """
            self.conn.execute(
                query,
                (
                    item.name,
                    item.scraper.__name__,
                    item.url,
                    item.price,
                    item.expiration_date,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Error adding item to database: {e}")
            raise
