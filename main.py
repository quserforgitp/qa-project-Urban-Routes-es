import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # LOCATORS
    from_field_locator = (By.ID, 'from')
    to_field_locator = (By.ID, 'to')
    call_a_taxi_btn_locator = (By.XPATH, '//button[@type="button" and text()="Pedir un taxi"]')
    comfort_tariff_card_locator = (By.XPATH, '//img[@alt="Comfort"]')
    phone_number_btn_locator = (By.XPATH, '//div[@class="np-button"]/div[@class="np-text" and text()="Número de teléfono"]')
    phone_number_field_locator = (By.XPATH, '//div[@class="input-container"]/input[@id="phone" and @placeholder="+1 xxx xxx xx xx"]')
    phone_number_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Siguiente"]')
    phone_code_field_locator = (By.XPATH, '//div[@class="input-container"]/input[@id="code" and @placeholder="xxxx"]')
    phone_code_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Confirmar"]')

    payment_method_btn_locator = (By.XPATH, '//div[contains(@class, "pp-button")]/div[@class="pp-text" and text()="Método de pago"]')
    add_card_btn_locator = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    card_number_field_locator = (By.XPATH, '//div[@class="card-number-input"]/input[@id="number" and @placeholder="1234 4321 1408"]')
    card_code_field_locator = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code" and @placeholder="12"]')
    new_card_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Agregar"]')
    close_add_card_modal_btn_locator = (By.XPATH, '//div[@class="head" and text()="Método de pago"]/preceding-sibling::button[contains(@class, "close-button")]')

    message_for_the_driver_field_locator = (By.XPATH, '//input[@id="comment" and @placeholder="Traiga un aperitivo"]')

    blanket_n_handkerchiefs_checkbox_locator = (By.XPATH, '//div[@class="r-sw-label" and text()="Manta y pañuelos"]/following-sibling::div[@class="r-sw"]//input[@type="checkbox"]/following-sibling::span')

    icecream_increase_counter_btn_locator = (By.XPATH, '//div[@class="r-counter-container"]/div[text()="Helado"]/following-sibling::div[@class="r-counter"]//div[@class="counter-plus" and text()="+"]')

    call_the_vehicle_btn_locator = (By.XPATH, '//button[@type="button"]/span[text()="Pedir un taxi"]')

    searching_vehicle_modal_locator = (By.XPATH, '//div[@class="order-body" and .//div[@class="order-header-title" and text()="Buscar automóvil"]]')


    def __init__(self, driver, search_element_timeout=5, visual_review_timeout=3):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, search_element_timeout)
        self.VISUAL_REVIEW_TIMEOUT = visual_review_timeout

    # INTERACTORS
    def set_from(self, from_address):
        self.__set_element_text(self.from_field_locator, from_address)

    def set_to(self, to_address):
        self.__set_element_text(self.to_field_locator, to_address)

    def get_from(self):
        return  self.__get_element_text(self.from_field_locator)

    def get_to(self):
        return  self.__get_element_text(self.to_field_locator)

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.wait_for_visual_review()
        self.set_to(address_to)
        self.wait_for_visual_review()

    def click_on_call_a_taxi_btn(self):
        self.__click_on_element(self.call_a_taxi_btn_locator)

    def click_on_comfort_tariff_card(self):
        self.__click_on_element(self.comfort_tariff_card_locator)

    def click_on_phone_number_btn(self):
        self.scroll_into_and_click_on_element(self.phone_number_btn_locator)

    def set_phone_number(self, phone_number):
        self.__set_element_text(self.phone_number_field_locator, phone_number)

    def click_on_submit_phone_number_btn(self):
        self.__click_on_element(self.phone_number_submit_btn_locator)

    def click_on_submit_phone_code_btn(self):
        self.__click_on_element(self.phone_code_submit_btn_locator)

    def set_phone_code(self, phone_code):
        self.__set_element_text(self.phone_code_field_locator, phone_code)

    # ADD CARD
    def click_on_payment_method_btn(self):
        self.__click_on_element(self.payment_method_btn_locator)

    def click_on_add_card_btn(self):
        self.__click_on_element(self.add_card_btn_locator)

    def set_card_number(self, card_number):
        self.__set_element_text(self.card_number_field_locator, card_number)

    def set_card_code(self, card_code):
        self.__set_element_text(self.card_code_field_locator, card_code)

    def click_on_submit_new_card_btn(self, send_tab_to_remove_focus=False):
        if send_tab_to_remove_focus:
            self.__set_element_text(self.card_code_field_locator, Keys.TAB)
        self.__click_on_element(self.new_card_submit_btn_locator)

    def click_on_close_add_card_modal_btn(self):
        self.__click_on_element(self.close_add_card_modal_btn_locator)

    def add_new_card(self, card_number, card_code):
        self.click_on_payment_method_btn()
        self.click_on_add_card_btn()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.click_on_submit_new_card_btn(send_tab_to_remove_focus=True)
        self.click_on_close_add_card_modal_btn()

    def set_message_for_the_driver(self, comment):
        self.__set_element_text(self.message_for_the_driver_field_locator, comment)

    def click_on_checkbox_blanket_and_handkerchiefs(self):
        self.scroll_into_and_click_on_element(self.blanket_n_handkerchiefs_checkbox_locator)

    def clicks_on_icecream_increase_counter_btn(self, times=1, clicks_delay=0):
        self.__click_on_element_multiple_times(self.icecream_increase_counter_btn_locator, times, clicks_delay)

    def click_on_call_the_vehicle_btn(self):
        self.__click_on_element(self.call_the_vehicle_btn_locator)

    def check_if_appears_searching_vehicle_modal(self, timeout):
        self.__check_if_appears_element(self.searching_vehicle_modal_locator, timeout)


    # Utility methods
    def __click_on_element(self, element_locator):
        self.wait.until(EC.visibility_of_element_located(element_locator)).click()
        self.wait_for_visual_review()

    def __scroll_into_element(self, element_locator):
        element = self.wait.until(EC.visibility_of_element_located(element_locator))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.wait_for_visual_review()

    def __set_element_text(self, element_locator, text):
        self.wait.until(EC.visibility_of_element_located(element_locator)).send_keys(text)
        self.wait_for_visual_review()

    def __get_element_text(self, element_locator):
        return (self.wait
                    .until(EC.visibility_of_element_located(element_locator))
                    .get_property('value')
                )

    def __click_on_element_multiple_times(self, locator, times=1, clicks_delay=0):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        for _ in range(times):
            element.click()
            time.sleep(clicks_delay)

    def __check_if_appears_element(self, element_locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(element_locator))

    def scroll_into_and_click_on_element(self, element_locator):
        self.__scroll_into_element(element_locator)
        self.__click_on_element(element_locator)

    def wait_for_visual_review(self):
        time.sleep(self.VISUAL_REVIEW_TIMEOUT)


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.maximize_window()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(driver=self.driver, search_element_timeout=5, visual_review_timeout=1)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_call_a_taxi(self):
        self.driver.maximize_window()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(driver=self.driver, search_element_timeout=5, visual_review_timeout=1)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_on_call_a_taxi_btn()
        routes_page.click_on_comfort_tariff_card()
        routes_page.click_on_phone_number_btn()
        routes_page.set_phone_number(data.phone_number)
        routes_page.click_on_submit_phone_number_btn()
        phone_code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(phone_code)
        routes_page.click_on_submit_phone_code_btn()
        routes_page.add_new_card(data.card_number, data.card_code)
        routes_page.set_message_for_the_driver(data.message_for_driver)
        routes_page.click_on_checkbox_blanket_and_handkerchiefs()
        routes_page.clicks_on_icecream_increase_counter_btn(times=2, clicks_delay=1)
        routes_page.click_on_call_the_vehicle_btn()
        routes_page.check_if_appears_searching_vehicle_modal(timeout=10)





    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
