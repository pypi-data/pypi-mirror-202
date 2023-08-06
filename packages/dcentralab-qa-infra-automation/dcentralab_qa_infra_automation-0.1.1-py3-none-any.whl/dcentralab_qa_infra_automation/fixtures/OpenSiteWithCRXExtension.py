import pytest
from dcentralab_qa_infra_automation.infra.CustomEventListener import CustomEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dcentralab_qa_infra_automation.drivers import ChromeDriver, BraveDriver

"""
open site with extension via CRX. to any browser type.

@Author: Efrat Cohen
@Date: 12.2022
"""


def before_test(request):
    """
    get crx extension file, setup driver - open the site with extension.
    store the driver to use him in different fixtures and pages.
    if brave browser injected - add the option to driver initialization
    :param request: the requesting test context
    """
    pytest.logger.info("Test: " + request.node.nodeid + " is started ")
    # chrome_options = ChromeOptions()
    # # In metamask wallet type
    # if pytest.data_driven.get("wallet_type") == 'MetaMask':
    #     chrome_options.add_extension(pytest.user_dir + pytest.properties.get("metamask.extension.crx"))
    # elif pytest.data_driven.get("wallet_type") == 'Coinbase':
    #     chrome_options.add_extension(pytest.user_dir + pytest.properties.get("coinbase.extension.crx"))

    # Init driver with extension based on injected driver type
    if pytest.data_driven.get("browser") == "brave":
        pytest.logger.info("brave browser type injected, initialize brave browser")
        driver = BraveDriver.initBraveDriverWithExtension()
    elif pytest.data_driven.get("browser") == "chrome":
        pytest.logger.info("chrome driver type injected, initialize chrome browser")
        driver = ChromeDriver.initChromeDriverWithExtension()

    # If no driver type injected - chrome is the default
    else:
        pytest.logger.info("no browser type injected, initialize default chrome browser")
        driver = ChromeDriver.initChromeDriverWithExtension()


        # # On macOS - use mac brave path
        # if pytest.data_driven.get("OS") == "windows":
        #     chrome_options.binary_location = pytest.properties.get("brave.windows.path")
        #     # On windowsOS - use windows brave path
        # elif pytest.data_driven.get("OS") == "mac":
        #     chrome_options.binary_location = pytest.properties.get("brave.mac.path")
        #     # If no OS injected
        # else:
        #     pytest.logger.info("no OS type injected, brave did not add to chrome.")

    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # Add event listener
    event_listener = CustomEventListener()
    event_firing_driver = EventFiringWebDriver(driver, event_listener)

    pytest.logger.info("driver :" + event_firing_driver.name + " had installed successfully")
    driver.maximize_window()
    pytest.logger.info("window had maximize")

    # Store driver in cls object
    request.cls.driver = driver
    pytest.driver = driver