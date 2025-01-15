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
    from_field_locator = (By.ID, 'from')
    to_field_locator = (By.ID, 'to')
    call_a_taxi_btn_locator = (By.XPATH, '//button[@type="button" and text()="Pedir un taxi"]')
    comfort_tariff_card_locator = (By.XPATH, '//img[@alt="Comfort"]')

    #DEBUG
    DEBUG_TIMEOUT = 1
    
    #DEBUG
    def wait_for_visual_review(self):
        time.sleep(self.DEBUG_TIMEOUT)

    def __init__(self, driver, wait_timeout=5):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait_timeout)

    def set_from(self, from_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field_locator)).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(EC.visibility_of_element_located(self.to_field_locator)).send_keys(to_address)

    def get_from(self):
        return  self.wait.until(EC.visibility_of_element_located(self.from_field_locator)).get_property('value')

    def get_to(self):
        return  self.wait.until(EC.visibility_of_element_located(self.to_field_locator)).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.wait_for_visual_review()
        self.set_to(address_to)
        self.wait_for_visual_review()

    def click_on_call_a_taxi_btn(self):
        self.wait.until(EC.visibility_of_element_located(self.call_a_taxi_btn_locator)).click()
        self.wait_for_visual_review()

    def click_on_comfort_tariff_card(self):
        self.wait.until(EC.visibility_of_element_located(self.comfort_tariff_card_locator)).click()
        self.wait_for_visual_review()



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
        routes_page = UrbanRoutesPage(self.driver, 5)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_call_a_taxi(self):
        self.driver.maximize_window()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(driver=self.driver, wait_timeout=5)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_on_call_a_taxi_btn()
        routes_page.click_on_comfort_tariff_card()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
