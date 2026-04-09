import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By  # noqa: F401
    from needle.cases import NeedleTestCase
    from needle.driver import (NeedleFirefox, NeedleChrome, NeedleIe, NeedleOpera,
                               NeedleSafari, NeedlePhantomJS)
    from pyvirtualdisplay import Display
    HAS_VISUAL_DEPS = True
    _visual_bases = (NeedleTestCase, StaticLiveServerTestCase)
    HAS_VISUAL_DEPS = True
except ImportError:
    _visual_bases = (StaticLiveServerTestCase,)
    HAS_VISUAL_DEPS = False


@unittest.skipUnless(HAS_VISUAL_DEPS and 'VISUAL' in os.environ, 'Visual tests are not enabled')
class VisualTest(*_visual_bases):
    engine_class = 'needle.engines.perceptualdiff_engine.Engine'
    viewport_width = 1280
    viewport_height = 1024

    @classmethod
    def setUpClass(cls):
        cls.display = None
        if 'NODISPLAY' not in os.environ:
            cls.display = Display(visible=0, size=(cls.viewport_width, cls.viewport_height))
            cls.display.start()
        super().setUpClass()

    @classmethod
    def set_viewport_size(cls, width, height):
        cls.driver.set_window_size(width, height)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if cls.display is not None:
            cls.display.stop()

    @classmethod
    def get_web_driver(cls):
        """Return the WebDriver instance to be used."""
        browser_name = os.environ.get('NEEDLE_BROWSER')
        browser_map = {
            'firefox': NeedleFirefox,
            'chrome': NeedleChrome,
            'ie': NeedleIe,
            'opera': NeedleOpera,
            'safari': NeedleSafari,
            'phantomjs': NeedlePhantomJS,
        }
        browser_class = browser_map.get(browser_name, NeedleFirefox)
        browser_kwargs = {}
        if browser_class == NeedleFirefox:
            options = webdriver.FirefoxOptions()
            options.set_preference("browser.startup.homepage", "about:blank")
            options.set_preference("startup.homepage_welcome_url", "about:blank")
            options.set_preference("startup.homepage_welcome_url.additional", "about:blank")
            browser_kwargs = {'options': options}
        return browser_class(**browser_kwargs)

    def assertScreenshot(self, element_or_selector, file, threshold=0.02):
        super().assertScreenshot(element_or_selector, file, threshold=threshold)
