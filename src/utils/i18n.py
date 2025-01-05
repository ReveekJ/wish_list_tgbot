from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator
import os


def list_files_in_directory(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru")
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=list_files_in_directory('./locales/ru/LC_MESSAGES'))),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US",
                    filenames=list_files_in_directory('./locales/en/LC_MESSAGES')))
        ],
        root_locale="ru"
    )
    return translator_hub
