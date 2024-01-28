from app.factories.notifier_enums import NotifierEnum
from app.notifications.base_notifier import BaseNotifier
from app.notifications.discord_notifier import DiscordNotifier
from app.notifications.email_notifier import EmailNotifier


class NotifierFactory:
    @staticmethod
    def get_notifier(notifier_type: NotifierEnum) -> BaseNotifier:
        if notifier_type == NotifierEnum.EMAIL:
            return EmailNotifier()
        elif notifier_type == NotifierEnum.DISCORD:
            return DiscordNotifier()

        raise ValueError("Unknown site")
