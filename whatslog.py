import os
import logging
import argparse
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

logging.basicConfig(level=logging.INFO)

WHATSAPP_URL = 'https://web.whatsapp.com/'

# CSS identifiers
CONTACT_SEARCH_BOX_CLASS = 'selectable-text'
CONTACT_MATCHED_SEARCH_CLASS = 'matched-text'
MSG_BALOON_CLASS = 'copyable-text'
MSG_PANE_ARIA_LABEL = "[aria-label=\"Message list. Press right arrow key on a message to open message context menu.\""


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('contact_name', type=str, help='Name of the contact to log')
    parser.add_argument('-dest', type=str, help='Where log is incrementally stored', default=None)
    return parser.parse_args()


def access_whatsapp() -> WebDriver:
    driver = webdriver.Firefox()

    # Access whatsapp page, wait it to load and present QR code
    driver.get(WHATSAPP_URL)
    driver.implicitly_wait(15)
    return driver


def find_contact(driver: WebDriver, contact: str) -> None:
    search_box = driver.find_element_by_class_name(CONTACT_SEARCH_BOX_CLASS)
    search_box.send_keys(contact)
    driver.implicitly_wait(2)

    # Click on contact card on the left pane
    driver.find_element_by_class_name(CONTACT_MATCHED_SEARCH_CLASS).click()
    driver.implicitly_wait(10)


def get_messages(driver: WebDriver, filepath: str) -> None:
    def focus_on_msg_pane():
        # Whatsapp use a seemingly random class name, to avoid that resort to aria-label
        driver.implicitly_wait(5)
        return driver.find_element_by_css_selector(MSG_PANE_ARIA_LABEL)

    def get_msgs_from_html(msg_pane):
        # bs4 is way faster than parsing directly on selenium
        soup = BeautifulSoup(msg_pane.get_attribute('innerHTML'), "lxml")
        return soup.find_all('div', {'class': MSG_BALOON_CLASS})

    def parse_msg_from_html(node) -> str:
        try:
            sender = node['data-pre-plain-text'].rstrip()
            message = node.text
            return f'{sender} {message}'
        except KeyError:
            return 'Not a text message'

    def dump_new_msgs(segment: list) -> None:
        with open(filepath, 'a') as dfile:
            dfile.writelines([l + '\n' for l in reversed(segment)])

    def scroll_up(msg_pane) -> None:
        scrollable_window = msg_pane.find_element_by_xpath('..')
        driver.execute_script('arguments[0].scrollTop = 0', scrollable_window)

    already_read = 0
    n_attempts = 0
    while True:
        msg_pane = focus_on_msg_pane()
        nodes = get_msgs_from_html(msg_pane)

        # Count new messages
        n_texts = len(nodes)
        n_new = n_texts - already_read

        # Parse messages in the current tile
        logging.info(f'Found {n_texts} texts ({n_new} new)')
        log_fragment = [parse_msg_from_html(msg) for msg in nodes[:n_new]]

        if n_new != 0:
            n_attempts = 0
        else:
            n_attempts += 1
            logging.warning(f'No new messages found. Attempt {n_attempts}/3')
            if n_attempts == 3:
                break

        already_read += n_new
        dump_new_msgs(log_fragment)

        # Wait new messages loading
        scroll_up(msg_pane)
        sleep(0.5)
    logging.info(f'Done.')


if __name__ == '__main__':
    args = get_args()
    filepath = args.dest or f'log_{args.contact_name}.txt'

    with access_whatsapp() as driver:
        find_contact(driver, args.contact_name)
        get_messages(driver, filepath)
