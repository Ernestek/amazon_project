import re

from selenium.common import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

from modules.load_django import *
from parser_app.models import ReviewsInfo, Links


class AamazonReviewsParser:
    BASE_URL = 'https://www.amazon.fr/SPYRA-SpyraLX-WaterBlaster-Red-%C3%A9lectronique/dp/B09YHS514R/ref=sr_1_1?crid=2ITHD6Y15ZF9E&keywords=spyra&qid=1689239683&sprefix=spyra%2Caps%2C376&sr=8-1'

    def __init__(self):
        browser_options = ChromeOptions()
        service_args = [
            '--start-maximized',
            '--no-sandbox',
            '--disable-web-security',
            '--allow-running-insecure-content',
            '--hide-scrollbars',
            '--disable-setuid-sandbox',
            '--profile-directory=Default',
            '--ignore-ssl-errors=true',
            '--disable-dev-shm-usage',
        ]
        for arg in service_args:
            browser_options.add_argument(arg)

        browser_options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
        browser_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        })

        self.driver = Chrome(options=browser_options)

    def placer_amazon_reviews_parser(self):
        links = Links.objects.filter(status=False)
        for link in links:
            self.open_site(link.link)
            while True:
                self.get_review_info()
                try:
                    self._wait_and_choose_element('[class="a-disabled a-last"]', timeout=0)
                    break
                except TimeoutException:
                    self.next_page()
            link.status = True
            link.save()

    def open_site(self, link):
        self.driver.get(link)
        self._wait_and_choose_element('#acrCustomerReviewLink').click()
        try:
            self._wait_and_choose_element('[name="accept"]').click()
        except TimeoutException:
            ...
        elem = self._wait_and_choose_element('.a-link-emphasis.a-text-bold')
        actions = ActionChains(self.driver)
        actions.click(elem).perform()

    def get_review_info(self):
        self._wait_and_choose_element('[class="a-section review aok-relative"]')
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        items = soup.select('[class="a-section review aok-relative"]')
        for i in items:

            try:
                user_id = i['id']
            except AttributeError:
                user_id = None
            try:
                name = i.select_one('#cm_cr-review_list .a-profile-name').text.strip()
            except AttributeError:
                name = None
            try:
                count_stars = i.select_one('#cm_cr-review_list .a-icon-alt').text.strip()[:3]
            except AttributeError:
                count_stars = None
            try:
                date = i.select_one('#cm_cr-review_list .review-date').text
                date = re.findall(r'\d.*\d', date)
            except AttributeError:
                date = None
            try:
                text = i.select_one('#cm_cr-review_list .review-text-content').text.strip()
            except AttributeError:
                text = None

            defaults = {
                # 'user_id': user_id,
                'name': name,
                'text': text,
                'date': date,
                'count_stars': count_stars,
            }
            print(defaults)
            ReviewsInfo.objects.get_or_create(
                user_id=user_id,
                defaults=defaults
            )

    def next_page(self):
        self._wait_and_choose_element('.a-last').click()

    def _wait_and_choose_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 10) -> WebElement:
        condition = EC.presence_of_element_located((by, selector))
        element = WebDriverWait(self.driver, timeout).until(condition)
        return element

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()


if __name__ == '__main__':
    with AamazonReviewsParser() as placer:
        placer.placer_amazon_reviews_parser()
