from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import datetime
from pathlib import Path
from utils import *


class ChromeWebKiosk:
    """Class to handle webkiosk part of PyKiosk"""
    home_folder = str(Path.home())
    state = "active"  # State object
    since = 3600  # This should be set every time the state changes
    last_url_opened = None  # Last opened url

    def __init__(self, json_config):
        """Creates and starts firefox in kiosk mode on main display"""
        # config[KIOSK] is loaded here
        self.config = json_config

        # Load launch arguments
        self.options = ChromeOptions()

        # Load user data folder if 'keep_data' is set in config (This is default behavior)
        if KIOSK_KEEP_DATA in self.config and self.config[KIOSK_KEEP_DATA] is True:
            KIOSK_LAUNCH_ARGUMENTS.append(KIOSK_USER_DIR_ARG + self.home_folder + KIOSK_USER_DIR)

        # Add all launch arguments
        for arg in KIOSK_LAUNCH_ARGUMENTS:
            self.options.add_argument(arg)

        # Disables remote control warning
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)

        # Create driver
        self.browser = webdriver.Chrome(options=self.options)
        self.open_page(self.config[KIOSK_URL])
        self.homepage = self.browser.window_handles

    def open_page(self, url=None, homepage=False):
        """Open url"""
        if url is None and homepage is False:
            return False
        if homepage:
            url = self.config[KIOSK_URL]
        try:
            self.browser.get(url)
            self.browser.fullscreen_window()
            print(" * Webkiosk opened url: {url}".format(url=url))
            self.since = datetime.now().timestamp()
            self.last_url_opened = url
            return True
        except:
            return

    def close_page(self):
        print(" * Closing browser")
        try:
            self.browser.close()
            return True
        except:
            return

    def reset_to_homepage(self):
        for handle in self.browser.window_handles:
            if handle not in self.homepage:
                continue
            self.browser.switch_to.window(handle)
            self.browser.close()
        return True

    def get_current_page(self):
        return self.browser.current_url

    def get_number_of_tabs(self):
        return len(self.browser.window_handles)
