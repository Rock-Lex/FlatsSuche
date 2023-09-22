from telegram.ext import Updater
import logging
from geopy.geocoders import Nominatim
import handlers
geolocator = Nominatim(user_agent="geoapiExercises")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class BOT:
    def __init__(self, TOKEN, databaseManager, helpers, parser, url, *args):
        """python telegram bot vars"""
        self.updater = Updater(TOKEN, use_context=True)
        self.dp = self.updater.dispatcher

        """parser"""
        self.parser = parser
        self.url = url

        """database manager"""
        self.databaseManager = databaseManager

        """setting up configurations"""
        self.helper = helpers
        self.handler_config()

    def run(self):
        self.updater.start_polling()

    def handler_config(self):
        """
        Setting handlers for conversational talks here
        """
        """/start command handler"""
        start_handler = handlers.StartHandler(self.url, self.parser, self.updater, self.dp, self.databaseManager, self.helper)
        self.dp.add_handler(start_handler.return_handler())

        settings_handler = handlers.SettingsHandler(self.updater, self.dp, self.databaseManager, self.helper)
        self.dp.add_handler(settings_handler.return_handler())

        language_handler = handlers.ChangeLanguageHandler(self.updater, self.dp, self.databaseManager, self.helper)
        self.dp.add_handler(language_handler.return_handler())
        donation_handler = handlers.DonateHandler(self.updater, self.dp, self.databaseManager, self.helper)
        self.dp.add_handler(donation_handler.return_handler())

