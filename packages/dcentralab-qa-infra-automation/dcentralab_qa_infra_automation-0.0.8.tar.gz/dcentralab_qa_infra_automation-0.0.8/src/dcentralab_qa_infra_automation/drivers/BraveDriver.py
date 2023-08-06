import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

"""
init brave browser driver

@Author: Efrat Cohen
@Date: 12.2022
"""


def addBraveToChrome():
    """
    add brave to chrome based on OS type
    :return: binary_location
    """
    binary_location = None
    # On macOS - use mac brave path
    if pytest.data_driven.get("OS") == "windows":
        binary_location = pytest.properties.get("brave.windows.path")
    # On windowsOS - use windows brave path
    elif pytest.data_driven.get("OS") == "mac":
        binary_location = pytest.properties.get("brave.mac.path")
    # If no OS injected
    else:
        pytest.logger.info("no OS type injected, brave did not add to chrome.")

    return binary_location


def addExtensionToChrome():
    """
    add CRX extension to chrome
    :return: add_extension - current extension crx file
    """
    add_extension = None
    # In metamask wallet type
    if pytest.data_driven.get("wallet_type") == 'MetaMask':
        add_extension = pytest.user_dir + pytest.properties.get("metamask.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Coinbase':
        add_extension = pytest.user_dir + pytest.properties.get("coinbase.extension.crx")

    return add_extension


def initBraveDriver():
    """
    init brave driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = addBraveToChrome()

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


def initBraveDriverWithExtension():
    """
    init brave driver with CRX extension, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = addBraveToChrome()
    options.add_extension(addExtensionToChrome())
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver
