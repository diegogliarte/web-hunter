from factories.notifier_enums import NotifierEnum
from notifications.base_notifier import BaseNotifier
from notifications.discord_notifier import DiscordNotifier
from notifications.email_notifier import EmailNotifier


class NotifierFactory:
    @staticmethod
    def get_notifier(notifier_type: NotifierEnum) -> BaseNotifier:
        if notifier_type == NotifierEnum.EMAIL:
            return EmailNotifier()
        elif notifier_type == NotifierEnum.DISCORD:
            return DiscordNotifier()

        raise ValueError("Unknown site")
