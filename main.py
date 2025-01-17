import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


# Funciones Útiles
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

def parse_to_seconds(time_str):
    minutes, seconds = time_str.split(":")
    total_seconds = int(seconds) + int(minutes) * 60
    return total_seconds


class UrbanRoutesPage:
    # Localizadores de elementos en la página mediante diferentes estrategias
    # Localizadores del formulario para establecer ruta
    from_field_locator = (By.ID, 'from')
    to_field_locator = (By.ID, 'to')
    call_a_taxi_btn_locator = (By.XPATH, '//button[@type="button" and text()="Pedir un taxi"]')

    # Localizadores de las tarifas
    comfort_tariff_card_img_locator = (By.XPATH, '//div[@class="tcard-icon"]/img[@alt="Comfort"]')
    setted_tariff_card_text_locator = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-icon"]/following-sibling::div[@class="tcard-title"]')

    # Localizadores del campo para agregar numero telefonico
    phone_number_btn_locator = (By.XPATH, '//div[@class="np-button"]/div[@class="np-text" and text()="Número de teléfono"]')
    phone_number_field_locator = (By.XPATH, '//div[@class="input-container"]/input[@id="phone" and @placeholder="+1 xxx xxx xx xx"]')
    phone_number_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Siguiente"]')
    phone_code_field_locator = (By.XPATH, '//div[@class="input-container"]/input[@id="code" and @placeholder="xxxx"]')
    phone_code_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Confirmar"]')

    # Localizadores del campo para agregar metodo de pago
    payment_method_btn_locator = (By.XPATH, '//div[contains(@class, "pp-button")]/div[@class="pp-text" and text()="Método de pago"]')
    add_card_btn_locator = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    card_number_field_locator = (By.XPATH, '//div[@class="card-number-input"]/input[@id="number" and @placeholder="1234 4321 1408"]')
    card_code_field_locator = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code" and @placeholder="12"]')
    new_card_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Agregar"]')
    close_add_card_modal_btn_locator = (By.XPATH, '//div[@class="head" and text()="Método de pago"]/preceding-sibling::button[contains(@class, "close-button")]')

    # Localizadores del campo para agregar un comentario para el conductor
    message_for_the_driver_field_locator = (By.XPATH, '//input[@id="comment" and @placeholder="Traiga un aperitivo"]')

    # Localizadores de los checkbox y los contadores para pedir mantas, panuelos y helados
    blanket_n_handkerchiefs_slider_locator = (By.XPATH, '//div[@class="r-sw-label" and text()="Manta y pañuelos"]/following-sibling::div[@class="r-sw"]//input[@type="checkbox"]/following-sibling::span')
    icecream_counter_field_locator = (By.XPATH, '//div[@class="r-counter-container"]/div[text()="Helado"]/following-sibling::div[@class="r-counter"]//div[@class="counter-value"]')
    icecream_increase_counter_btn_locator = (By.XPATH, '//div[@class="r-counter-container"]/div[text()="Helado"]/following-sibling::div[@class="r-counter"]//div[@class="counter-plus" and text()="+"]')

    # Localizadores del boton que inicia la busqueda de un conductor
    call_the_vehicle_btn_locator = (By.XPATH, '//button[@type="button"]/span[text()="Pedir un taxi"]')

    # Localizadores del modal que contiene informacion de la busqueda del conductor
    searching_vehicle_modal_locator = (By.XPATH, '//div[@class="order-body" and .//div[@class="order-header-title" and text()="Buscar automóvil"]]')

    # Localizadores para la informacion del conductor
    driver_arrival_time_label_locator = (By.XPATH, '//div[@class="order-header-title" and text()="Buscar automóvil"]/following-sibling::div[@class="order-header-time"]')
    driver_rating_field_locator = (By.XPATH, '//div[@class="order-buttons"]/div[@class="order-btn-group"]//div[@class="order-btn-rating"]')
    driver_img_field_locator = (By.XPATH, '//div[@class="order-buttons"]/div[@class="order-btn-group"]//div[@class="order-btn-rating"]/following-sibling::img')
    driver_name_field_locator = (By.XPATH, '//div[@class="order-buttons"]/div[@class="order-btn-group"]/div[@class="order-button" and ./div[@class="order-btn-rating"]]/following-sibling::div')

    # Constructor de la clase, inicializa el controlador, y establace los tiempos de espera para recuperar elementos de la pagina y para inspeccion visual
    def __init__(self, driver, search_element_timeout=5, visual_review_timeout=3):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, search_element_timeout)
        self.VISUAL_REVIEW_TIMEOUT = visual_review_timeout

    # Métodos para interactuar con los elementos de la página
    # Métodos para interactuar con el formulario para establecer la ruta (Desde y Hasta)
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

    # Métodos para intecarctuar con las tarifas
    def click_on_comfort_tariff_card(self):
        self.__click_on_element(self.comfort_tariff_card_img_locator)
    def get_selected_tariff(self):
        return self.__get_element_text(self.setted_tariff_card_text_locator)


    # Métodos para agregar el numero de telefono
    def click_on_phone_number_btn(self):
        self.scroll_into_and_click_on_element(self.phone_number_btn_locator)
    def set_phone_number(self, phone_number):
        self.__set_element_text(self.phone_number_field_locator, phone_number)
    def get_phone_number(self):
        return self.__get_element_text(self.phone_number_field_locator)
    def click_on_submit_phone_number_btn(self):
        self.__click_on_element(self.phone_number_submit_btn_locator)
    def click_on_submit_phone_code_btn(self):
        self.__click_on_element(self.phone_code_submit_btn_locator)
    def set_phone_code(self, phone_code):
        self.__set_element_text(self.phone_code_field_locator, phone_code)

    # Métodos para interactuar con los elementos de la tarjeta
    def click_on_payment_method_btn(self):
        self.__click_on_element(self.payment_method_btn_locator)
    def click_on_add_card_btn(self):
        self.__click_on_element(self.add_card_btn_locator)
    def set_card_number(self, card_number):
        self.__set_element_text(self.card_number_field_locator, card_number)
    def get_card_number(self):
        return self.__get_element_text(self.card_number_field_locator)
    def set_card_code(self, card_code):
        self.__set_element_text(self.card_code_field_locator, card_code)
    def get_card_code(self):
        return self.__get_element_text(self.card_code_field_locator)
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

    # Métodos para agregar un comentario para el conductor
    def set_message_for_the_driver(self, comment):
        self.__set_element_text(self.message_for_the_driver_field_locator, comment)
    def get_message_for_the_driver(self):
        return self.__get_element_text(self.message_for_the_driver_field_locator)

    # Métodos para interactuar con el checkbox de manta y panuelos, y el contador de helados
    def click_on_checkbox_blanket_and_handkerchiefs(self):
        self.scroll_into_and_click_on_element(self.blanket_n_handkerchiefs_slider_locator)
    def check_if_checkbox_blanket_and_handkerchiefs_is_checked(self):
        # es necesario porque selenium no lo encuentra ya que sus dimensiones son 0x0
        checkbox = self.driver.execute_script("""
                                                const expectedLabelText = "Manta y pañuelos"
                                                const containers = document.querySelectorAll('div.r-sw-container');
                                                let checkbox = null;
                                                
                                                containers.forEach( (container) => {
                                                    const label = container.querySelector('.r-sw-label');
                                                    const currentlabelText = label.textContent;
                                                    if (expectedLabelText === currentlabelText) checkbox = container.querySelector('.switch-input');
                                                });
                                                return checkbox;
                                              """)

        return checkbox.get_property('checked')
    def get_icecream_counter_number(self):
        return self.__get_element_text(self.icecream_counter_field_locator)
    def clicks_on_icecream_increase_counter_btn(self, times=1, clicks_delay=0):
        self.__click_on_element_multiple_times(self.icecream_increase_counter_btn_locator, times, clicks_delay)

    # Métodos para iniciar la busqueda de un conductor
    def click_on_call_the_vehicle_btn(self):
        self.__click_on_element(self.call_the_vehicle_btn_locator)

    # Métodos para comprobar que el modal de busqueda de vehiculo aparece
    def check_if_appears_searching_vehicle_modal(self, search_timeout=5, start_search_at=1):
        # El start_search_at es para demorar el inicio de la busqueda x segundos, ya que hay casos en los que el elemento
        # aparece, pero desaparece inmediatamente, ocasionando que selenium lo detecte y lo marque como que si esta presente
        # cuando en realidad puede que lo querramos presente mas tiempo
        return self.__check_if_appears_element(self.searching_vehicle_modal_locator, search_timeout, start_search_at)

    # Métodos para obtener la informacion del conductor encontrado
    def get_driver_rating(self):
        return self.__get_element_text(self.driver_rating_field_locator)
    def get_driver_img_url(self):
        return self.wait.until(EC.visibility_of_element_located(self.driver_img_field_locator)).get_attribute('src')
    def get_driver_name(self):
        return self.__get_element_text(self.driver_name_field_locator)


    # Metodos auxiliares para interactuar con los elementos de la pagina
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
        element = self.wait.until(EC.visibility_of_element_located(element_locator))

        text = element.text
        if text:
            return text

        text = element.get_property('value')

        if text:
            return text

        return ""
    def __click_on_element_multiple_times(self, locator, times=1, clicks_delay=0):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        for _ in range(times):
            element.click()
            time.sleep(clicks_delay)
    def __check_if_appears_element(self, element_locator, search_timeout=5, start_search_at=1):
        # El start_search_at es para demorar el inicio de la busqueda x segundos, ya que hay casos en los que el elemento
        # aparece, pero desaparece inmediatamente, ocasionando que selenium lo detecte y lo marque como que si esta presente
        # cuando en realidad puede que lo querramos presente mas tiempo
        time.sleep(start_search_at)
        try:
            WebDriverWait(self.driver, search_timeout).until(EC.visibility_of_element_located(element_locator))
        except TimeoutException:
            return False
        return True


    def scroll_into_and_click_on_element(self, element_locator):
        self.__scroll_into_element(element_locator)
        self.__click_on_element(element_locator)
    def wait_for_visual_review(self):
        time.sleep(self.VISUAL_REVIEW_TIMEOUT)
    def wait_for_driver_info(self, additional_secs=1):
        time.sleep(additional_secs)

        time_str = self.__get_element_text(self.driver_arrival_time_label_locator)
        arrival_time_in_seconds = parse_to_seconds(time_str)
        time.sleep(arrival_time_in_seconds + additional_secs)
    def clear_local_storage(self):
        self.driver.execute_script("window.localStorage.clear();")




class TestUrbanRoutes:

    driver = None

    SEARCH_TIMEOUT = 5
    VISUAL_TIME0UT = 0

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    # 1.- Comprobacion de la configuracion de la direccion
    def test_set_route(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        self.driver.maximize_window()
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2.- Comprobacion de la seleccion de la tarifa 'Comfort'
    def test_set_tariff(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)

        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Recupera el texto de la tarifa seleccionada para compararlo
        selected_tariff = routes_page.get_selected_tariff()

        assert selected_tariff == 'Comfort', 'La tarifa seleccionada debería ser "Comfort"'

    # 3.- Comprobacion del numero de telefono introducido
    def test_set_phone_number(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)
        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para ingresar el número de teléfono del pasajero.
        routes_page.click_on_phone_number_btn()

        # Establece el número de teléfono proporcionado en los datos de prueba.
        routes_page.set_phone_number(data.phone_number)

        # Recupera el numero de telefono que aparece en el elemento
        setted_phone_number = routes_page.get_phone_number()

        assert setted_phone_number == data.phone_number, f'El numero de telefono deberia ser "{data.phone_number}"'

    # 4.- Comprobacion de datos introducidos en los campos cuando se agrega una tarjeta nueva
    def test_set_credit_card_data(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)

        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para ingresar el número de teléfono del pasajero.
        routes_page.click_on_phone_number_btn()

        # Establece el número de teléfono proporcionado en los datos de prueba.
        routes_page.set_phone_number(data.phone_number)

        # Hace clic en el botón de envío del número de teléfono.
        routes_page.click_on_submit_phone_number_btn()

        # Recupera el código de verificación del teléfono desde el sitio web.
        phone_code = retrieve_phone_code(self.driver)

        # Establece el código de teléfono obtenido anteriormente.
        routes_page.set_phone_code(phone_code)

        # Hace clic en el botón de envío del código de teléfono.
        routes_page.click_on_submit_phone_code_btn()

        # Añade una nueva tarjeta de pago
        routes_page.click_on_payment_method_btn()
        routes_page.click_on_add_card_btn()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)

        # Recupera el numero de la tarjeta que aparece en el campo
        actual_card_number = routes_page.get_card_number()
        assert actual_card_number == data.card_number, f'El numero de la tarjeta deberia ser "{data.card_number}"'

        # Recupera el codigo (CVV) de la tarjeta que aparece en el campo
        actual_card_code = routes_page.get_card_code()
        assert actual_card_code == data.card_code, f'El codigo (CVV) de la tarjeta deberia ser "{data.card_code}"'

    # 5.- Comprobacion del mensaje introducido para el conductor
    def test_set_message_for_the_driver(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)

        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Establece el mensaje para el conductor, tal como está en los datos de prueba.
        routes_page.set_message_for_the_driver(data.message_for_driver)

        # Recupera el mensaje para el conductor desde el campo
        actual_message = routes_page.get_message_for_the_driver()
        assert actual_message == data.message_for_driver, f'El mensaje para el conductor deberia ser "{data.message_for_driver}"'

    # 6.- Comprobacion de la activacion del checkbox de manta y panuelos
    def test_checkbox_blanket_and_handkerchiefs_activation(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)
        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en la casilla de verificación para manta y pañuelos.
        routes_page.click_on_checkbox_blanket_and_handkerchiefs()

        # Recupera el estado del checkbox de mantas y panuelos
        blanket_and_handkerchiefs_is_checked = routes_page.check_if_checkbox_blanket_and_handkerchiefs_is_checked()

        assert blanket_and_handkerchiefs_is_checked, 'El checkbox de mantas y panuelos deberia estar seleccionado'

    # 7.- Comprobacion de la cantidad de helados pedidos
    def test_set_icecream_quantity(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)
        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para aumentar el contador de helados dos veces, sin retraso entre clics.
        routes_page.clicks_on_icecream_increase_counter_btn(times=2, clicks_delay=0)

        # Recupera el numero que aparece en el campo de contador de helados
        actual_icecream_counter_number = routes_page.get_icecream_counter_number()

        expected_icecream_counter_number = '2'

        assert  expected_icecream_counter_number == actual_icecream_counter_number, f'El numero de helados pedidos deberia ser "{expected_icecream_counter_number}"'

    # 8.- Comprobacion de que aparece el modal donde se muestra la informacion de busqueda del taxi
    def test_searching_taxi_modal_appears(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)

        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para ingresar el número de teléfono del pasajero.
        routes_page.click_on_phone_number_btn()

        # Establece el número de teléfono proporcionado en los datos de prueba.
        routes_page.set_phone_number(data.phone_number)

        # Hace clic en el botón de envío del número de teléfono.
        routes_page.click_on_submit_phone_number_btn()

        # Recupera el código de verificación del teléfono desde el sitio web.
        phone_code = retrieve_phone_code(self.driver)

        # Establece el código de teléfono obtenido anteriormente.
        routes_page.set_phone_code(phone_code)

        # Hace clic en el botón de envío del código de teléfono.
        routes_page.click_on_submit_phone_code_btn()

        # Añade una nueva tarjeta de pago con el número de tarjeta y código proporcionados en los datos de prueba.
        routes_page.add_new_card(data.card_number, data.card_code)

        # Hace clic en el botón para llamar al vehículo.
        routes_page.click_on_call_the_vehicle_btn()

        # Verifica si aparece el modal de "buscando vehículo", con un tiempo de espera máximo de 4 segundos.
        modal_is_present = routes_page.check_if_appears_searching_vehicle_modal(search_timeout=2, start_search_at=2)

        assert modal_is_present, 'El modal que muestra la informacion de buscar un taxi deberia aparecer y permanecer mostrandose hasta que el tiempo de espera expire'

    # 9.- Comprobacion de que aparece la informacion del conductor en el modal
    def test_driver_info_appears(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)
        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para ingresar el número de teléfono del pasajero.
        routes_page.click_on_phone_number_btn()

        # Establece el número de teléfono proporcionado en los datos de prueba.
        routes_page.set_phone_number(data.phone_number)

        # Hace clic en el botón de envío del número de teléfono.
        routes_page.click_on_submit_phone_number_btn()

        # Recupera el código de verificación del teléfono desde el sitio web.
        phone_code = retrieve_phone_code(self.driver)

        # Establece el código de teléfono obtenido anteriormente.
        routes_page.set_phone_code(phone_code)

        # Hace clic en el botón de envío del código de teléfono.
        routes_page.click_on_submit_phone_code_btn()

        # Añade una nueva tarjeta de pago con el número de tarjeta y código proporcionados en los datos de prueba.
        routes_page.add_new_card(data.card_number, data.card_code)

        # Hace clic en el botón para llamar al vehículo.
        routes_page.click_on_call_the_vehicle_btn()

        # Verifica si aparece el modal de "buscando vehículo", con un tiempo de espera máximo de 4 segundos.
        modal_is_present = routes_page.check_if_appears_searching_vehicle_modal(search_timeout=2, start_search_at=2)

        assert modal_is_present, 'El modal que muestra la informacion de buscar un taxi deberia aparecer y permanecer mostrandose hasta que el tiempo de espera expire'

        # Espera la información del conductor con un tiempo adicional de 3 segundos.
        routes_page.wait_for_driver_info(additional_secs=3)

        # Verificación del nombre del conductor
        driver_name = routes_page.get_driver_name()
        assert driver_name != '', "El nombre del conductor no debe estar vacío."

        # Verificación de la URL de la imagen del conductor
        driver_img = routes_page.get_driver_img_url()
        assert driver_img != '', "La URL de la imagen del conductor no debe estar vacía."

        # Verificación de la calificación del conductor
        driver_rating = routes_page.get_driver_rating()
        assert driver_rating != '', "La calificación del conductor no debe estar vacía."

    # 10.- Comprobacion del proceso completo de llamar un taxi
    def test_call_a_taxi(self, search_timeout=SEARCH_TIMEOUT, visual_timeout=VISUAL_TIME0UT):
        # Maximiza la ventana del navegador para una mejor visualización de la prueba.
        self.driver.maximize_window()

        # Abre la página de Urban.Routes desde la URL almacenada en los datos de prueba.
        self.driver.get(data.urban_routes_url)

        # Inicializa la página de Urban.Routes con el tiempo de espera para los elementos de búsqueda y para la revisión visual.
        routes_page = UrbanRoutesPage(driver=self.driver,
                                      search_element_timeout=search_timeout,
                                      visual_review_timeout=visual_timeout)

        # Limpia el almacenamiento local
        routes_page.clear_local_storage()

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para ingresar el número de teléfono del pasajero.
        routes_page.click_on_phone_number_btn()

        # Establece el número de teléfono proporcionado en los datos de prueba.
        routes_page.set_phone_number(data.phone_number)

        # Hace clic en el botón de envío del número de teléfono.
        routes_page.click_on_submit_phone_number_btn()

        # Recupera el código de verificación del teléfono desde el sitio web.
        phone_code = retrieve_phone_code(self.driver)

        # Establece el código de teléfono obtenido anteriormente.
        routes_page.set_phone_code(phone_code)

        # Hace clic en el botón de envío del código de teléfono.
        routes_page.click_on_submit_phone_code_btn()

        # Añade una nueva tarjeta de pago con el número de tarjeta y código proporcionados en los datos de prueba.
        routes_page.add_new_card(data.card_number, data.card_code)

        # Establece el mensaje para el conductor, tal como está en los datos de prueba.
        routes_page.set_message_for_the_driver(data.message_for_driver)

        # Hace clic en la casilla de verificación para manta y pañuelos.
        routes_page.click_on_checkbox_blanket_and_handkerchiefs()

        # Hace clic en el botón para aumentar el contador de helados dos veces, sin retraso entre clics.
        routes_page.clicks_on_icecream_increase_counter_btn(times=2, clicks_delay=0)

        # Hace clic en el botón para llamar al vehículo.
        routes_page.click_on_call_the_vehicle_btn()

        # Verifica si aparece el modal de "buscando vehículo", con un tiempo de espera máximo de 4 segundos.
        modal_is_present = routes_page.check_if_appears_searching_vehicle_modal(search_timeout=2, start_search_at=2)

        assert modal_is_present, 'El modal que muestra la informacion de buscar un taxi deberia aparecer y permanecer mostrandose hasta que el tiempo de espera expire'

        # Espera la información del conductor con un tiempo adicional de 3 segundos.
        routes_page.wait_for_driver_info(additional_secs=3)

        # Verificación del nombre del conductor
        driver_name = routes_page.get_driver_name()
        assert driver_name != '', "El nombre del conductor no debe estar vacío."

        # Verificación de la URL de la imagen del conductor
        driver_img = routes_page.get_driver_img_url()
        assert driver_img != '', "La URL de la imagen del conductor no debe estar vacía."

        # Verificación de la calificación del conductor
        driver_rating = routes_page.get_driver_rating()
        assert driver_rating != '', "La calificación del conductor no debe estar vacía."

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()