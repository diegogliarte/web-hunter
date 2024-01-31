import datetime
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from items.base_item import BaseItem
from items.error_item import ErrorItem
from items.scraped_item import ScrapedItem
from notifications.base_notifier import BaseNotifier
from notifications.smtp_parameters import SMTPParameters
from scrapers.base_scraper import BaseScraper

from scrapers.humble_choice_scraper import HumbleChoiceScraper

logger = logging.getLogger(__name__)


class EmailNotifier(BaseNotifier):
    def notify(self, scraped_data: dict[type[BaseScraper], list[BaseItem]]):
        smtp_parameters = self.create_smtp_parameters()
        bundles_count, errors_count = self.get_counts(scraped_data)
        body = self.create_email_body(scraped_data, bundles_count, errors_count)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "WebHunter Scraping Report"
        msg["From"] = smtp_parameters.username
        msg["To"] = ", ".join(smtp_parameters.to)
        part1 = MIMEText(body, "html")
        msg.attach(part1)

        self.send_email(smtp_parameters, msg.as_string())

    @staticmethod
    def create_email_body(scraped_data, bundles_count, errors_count) -> str:
        body = "<html><body>"
        body += "<h2 style='color: navy;'>🌍 WebHunter Daily Digest 🌍</h2>"

        if bundles_count > 0:
            body += f"<h3 style='color: green;'>🎉 Total Bundles Discovered: {bundles_count}</h3>"
        if errors_count > 0:
            body += f"<h3 style='color: red;'>❌ Total Errors: {errors_count}</h3>"

        if bundles_count > 0:
            body += "<h4>🎁 <u>Bundles:</u></h4>"
            body += "<ul>"
            for scraper, items in scraped_data.items():
                bundle_items = [item for item in items if isinstance(item, ScrapedItem)]
                bundle_items = sorted(bundle_items,
                                      key=lambda item: (item.expiration_date is None, item.expiration_date))
                if bundle_items:
                    if scraper == HumbleChoiceScraper:
                        body += f"<li><a href='{bundle_items[0].url}'><strong>{scraper.__name__}</strong></a>:<ul>"
                        for item in bundle_items:
                            body += f"<li>{item.name}</li>"
                    else:
                        body += f"<li><strong>{scraper.__name__}</strong>:<ul>"
                        for item in bundle_items:
                            time_left = EmailNotifier.get_time_left(item.expiration_date)
                            body += f"<li><a href='{item.url}'>{item.name}</a> {time_left}</li>"
                    body += "</ul></li><br>"
            body += "</ul>"

        if errors_count > 0:
            body += "<h4>🐛 <u>Error Log:</u></h4>"
            body += "<ul>"
            for scraper, items in scraped_data.items():
                error_items = [item for item in items if isinstance(item, ErrorItem)]
                if error_items:
                    body += f"<li><strong>{scraper.__name__} Issues:</strong><ul>"
                    for item in error_items:
                        body += f"<li style='color: crimson;'>Error: {item.message} (Code: {item.code})</li>"
                    body += "</ul></li>"
            body += "</ul>"

            body += "<p style='font-size: 16px;'>Until tomorrow! 🚀</p>"
            body += "</body></html>"

        return body

    @staticmethod
    def get_counts(scraped_data: dict[type[BaseScraper], list[BaseItem]]) -> (int, int):
        bundles_count = 0
        errors_count = 0

        for items in scraped_data.values():
            bundles_count += sum(1 for item in items if isinstance(item, ScrapedItem))
            errors_count += sum(1 for item in items if isinstance(item, ErrorItem))

        return bundles_count, errors_count

    @staticmethod
    def get_time_left(expiration_date_str: str) -> str:
        if not expiration_date_str:
            return ""
        expiration_date = datetime.datetime.fromisoformat(expiration_date_str)
        now = datetime.datetime.now()
        time_delta = expiration_date - now
        days, seconds = time_delta.days, time_delta.seconds
        hours = seconds // 3600
        return f"{days} days, {hours} hours left" if days >= 0 else "Expired"

    @staticmethod
    def send_email(smtp_parameters: SMTPParameters, message: str):
        try:
            with smtplib.SMTP(smtp_parameters.host, smtp_parameters.port) as server:
                server.starttls()
                server.login(smtp_parameters.username, smtp_parameters.password)
                server.sendmail(smtp_parameters.username, smtp_parameters.to, message)
        except smtplib.SMTPException as e:
            logger.error(f"Error sending email: {e}")

    @staticmethod
    def create_smtp_parameters() -> SMTPParameters:
        return SMTPParameters(
            host=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT")),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            to=os.getenv("SMTP_TO").split(","),
        )
