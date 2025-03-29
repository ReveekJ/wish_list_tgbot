from dishka import Provider, provide, Scope
from fluentogram import TranslatorHub

from src.utils.i18n import create_translator_hub


class ServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def translator_hub(self) -> TranslatorHub:
        return create_translator_hub()
