from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers.util_helpers import parse_to_seconds
from helpers.pom_helpers import (scroll_into_and_click_on_element,
                                 set_element_text,
                                 get_element_text,
                                 click_on_element,
                                 click_on_element_multiple_times,
                                 check_if_appears_element)


class UrbanRoutesPage:
    # Localizadores de elementos en la página mediante diferentes estrategias
    # Localizadores del formulario para establecer ruta
    from_field_locator = (By.ID, 'from')
    to_field_locator = (By.ID, 'to')
    call_a_taxi_btn_locator = (By.XPATH, '//button[@type="button" and text()="Pedir un taxi"]')

    # Localizadores de las tarifas
    comfort_tariff_card_img_locator = (By.XPATH, '//div[@class="tcard-icon"]/img[@alt="Comfort"]')
    setted_tariff_card_text_locator = (
    By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-icon"]/following-sibling::div[@class="tcard-title"]')

    # Localizadores del campo para agregar numero telefonico
    #TODO class selector
    phone_number_btn_locator = (By.XPATH, '//div[contains(@class,"np-button")]/div[@class="np-text"]')
    phone_number_input_field_on_modal_locator = (
    By.XPATH, '//div[@class="input-container"]/input[@id="phone" and @placeholder="+1 xxx xxx xx xx"]')
    phone_number_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Siguiente"]')
    #TODO css selector por id
    phone_code_field_locator = (By.XPATH, '//div[@class="input-container"]/input[@id="code" and @placeholder="xxxx"]')
    phone_code_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Confirmar"]')

    # Localizadores del campo para agregar metodo de pago
    payment_method_btn_locator = (By.XPATH, '//div[contains(@class, "pp-button")]/div[@class="pp-text"]')
    payment_method_setted_on_payment_method_btn = (
    By.XPATH, '//div[contains(@class, "pp-value")]/div[@class="pp-value-text"]')
    add_card_btn_locator = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    card_number_field_locator = (
    By.XPATH, '//div[@class="card-number-input"]/input[@id="number" and @placeholder="1234 4321 1408"]')
    card_code_field_locator = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code" and @placeholder="12"]')
    new_card_submit_btn_locator = (By.XPATH, '//button[@type="submit" and text()="Agregar"]')
    close_add_card_modal_btn_locator = (By.XPATH,
                                        '//div[@class="head" and text()="Método de pago"]/preceding-sibling::button[contains(@class, "close-button")]')

    # Localizadores del campo para agregar un comentario para el conductor
    message_for_the_driver_field_locator = (By.XPATH, '//input[@id="comment" and @placeholder="Traiga un aperitivo"]')

    # Localizadores de los checkbox y los contadores para pedir mantas, panuelos y helados
    blanket_n_handkerchiefs_slider_locator = (By.XPATH,
                                              '//div[@class="r-sw-label" and text()="Manta y pañuelos"]/following-sibling::div[@class="r-sw"]//input[@type="checkbox"]/following-sibling::span')
    icecream_counter_field_locator = (By.XPATH,
                                      '//div[@class="r-counter-container"]/div[text()="Helado"]/following-sibling::div[@class="r-counter"]//div[@class="counter-value"]')
    icecream_increase_counter_btn_locator = (By.XPATH,
                                             '//div[@class="r-counter-container"]/div[text()="Helado"]/following-sibling::div[@class="r-counter"]//div[@class="counter-plus" and text()="+"]')

    # Localizadores del boton que inicia la busqueda de un conductor
    call_the_vehicle_btn_locator = (By.XPATH, '//button[@type="button"]/span[text()="Pedir un taxi"]')

    # Localizadores del modal que contiene informacion de la busqueda del conductor
    searching_vehicle_modal_locator = (
    By.XPATH, '//div[@class="order-body" and .//div[@class="order-header-title" and text()="Buscar automóvil"]]')

    # Localizadores para la informacion del conductor
    driver_arrival_time_label_locator = (By.XPATH,
                                         '//div[@class="order-header-title" and text()="Buscar automóvil"]/following-sibling::div[@class="order-header-time"]')
    driver_rating_field_locator = (
    By.XPATH, '//div[@class="order-buttons"]/div[@class="order-btn-group"]//div[@class="order-btn-rating"]')
    driver_img_field_locator = (By.XPATH,
                                '//div[@class="order-buttons"]/div[@class="order-btn-group"]//div[@class="order-btn-rating"]/following-sibling::img')
    driver_name_field_locator = (By.XPATH,
                                 '//div[@class="order-buttons"]/div[@class="order-btn-group"]/div[@class="order-button" and ./div[@class="order-btn-rating"]]/following-sibling::div')

    # Constructor de la clase, inicializa el controlador, y establace los tiempos de espera para recuperar elementos de la pagina y para inspeccion visual
    def __init__(self, driver, search_element_timeout=5, visual_review_timeout=3):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, search_element_timeout)
        self.VISUAL_REVIEW_TIMEOUT = visual_review_timeout

    # Métodos para interactuar con los elementos de la página
    # Métodos para interactuar con el formulario para establecer la ruta (Desde y Hasta)
    def set_from(self, from_address):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.from_field_locator, from_address)
    def set_to(self, to_address):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.to_field_locator, to_address)
    def get_from(self):
        return get_element_text(self.wait, self.from_field_locator)
    def get_to(self):
        return get_element_text(self.wait, self.to_field_locator)
    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)
    def click_on_call_a_taxi_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.call_a_taxi_btn_locator)

    # Métodos para intecarctuar con las tarifas
    def click_on_comfort_tariff_card(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.comfort_tariff_card_img_locator)
    def get_selected_tariff(self):
        return get_element_text(self.wait, self.setted_tariff_card_text_locator)

    # Métodos para agregar el numero de telefono
    def click_on_phone_number_btn(self):
        scroll_into_and_click_on_element(self.wait, self.driver, self.VISUAL_REVIEW_TIMEOUT,
                                         self.phone_number_btn_locator)
    def set_phone_number(self, phone_number):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.phone_number_input_field_on_modal_locator,
                           phone_number)
    def get_phone_number_from_field_on_modal(self):
        return get_element_text(self.wait, self.phone_number_input_field_on_modal_locator)
    def get_phone_number_from_btn(self):
        return get_element_text(self.wait, self.phone_number_btn_locator)
    def click_on_submit_phone_number_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.phone_number_submit_btn_locator)
    def click_on_submit_phone_code_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.phone_code_submit_btn_locator)
    def set_phone_code(self, phone_code):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.phone_code_field_locator, phone_code)

    # Métodos para interactuar con los elementos de la tarjeta
    def click_on_payment_method_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.payment_method_btn_locator)
    def get_type_of_setted_payment_method_from_payment_method_btn(self):
        return get_element_text(self.wait, self.payment_method_setted_on_payment_method_btn)
    def click_on_add_card_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.add_card_btn_locator)
    def set_card_number(self, card_number):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.card_number_field_locator, card_number)
    def get_card_number(self):
        return get_element_text(self.wait, self.card_number_field_locator)
    def set_card_code(self, card_code):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.card_code_field_locator, card_code)
    def get_card_code(self):
        return get_element_text(self.wait, self.card_code_field_locator)
    def click_on_submit_new_card_btn(self, send_tab_to_remove_focus=False):
        if send_tab_to_remove_focus:
            set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.card_code_field_locator, Keys.TAB)
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.new_card_submit_btn_locator)
    def click_on_close_add_card_modal_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.close_add_card_modal_btn_locator)
    def add_new_card(self, card_number, card_code):
        self.click_on_payment_method_btn()
        self.click_on_add_card_btn()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.click_on_submit_new_card_btn(send_tab_to_remove_focus=True)
        self.click_on_close_add_card_modal_btn()

    # Métodos para agregar un comentario para el conductor
    def set_message_for_the_driver(self, comment):
        set_element_text(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.message_for_the_driver_field_locator, comment)
    def get_message_for_the_driver(self):
        return get_element_text(self.wait, self.message_for_the_driver_field_locator)

    # Métodos para interactuar con el checkbox de manta y panuelos, y el contador de helados
    def click_on_checkbox_blanket_and_handkerchiefs(self):
        scroll_into_and_click_on_element(self.wait, self.driver, self.VISUAL_REVIEW_TIMEOUT,
                                         self.blanket_n_handkerchiefs_slider_locator)
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
        return get_element_text(self.wait, self.icecream_counter_field_locator)
    def clicks_on_icecream_increase_counter_btn(self, times=1):
        click_on_element_multiple_times(self.wait, self.VISUAL_REVIEW_TIMEOUT,
                                          self.icecream_increase_counter_btn_locator, times)

    # Métodos para iniciar la busqueda de un conductor
    def click_on_call_the_vehicle_btn(self):
        click_on_element(self.wait, self.VISUAL_REVIEW_TIMEOUT, self.call_the_vehicle_btn_locator)

    # Métodos para comprobar que el modal de busqueda de vehiculo aparece
    def check_if_appears_searching_vehicle_modal(self, search_timeout=5, minimum_visibility_time=1):
        # El minimum_element_visibility_time es para comprobar que el elemento se muestre en pantalla como minimo x segundos,
        # ya que hay casos en los que el elemento aparece, pero desaparece inmediatamente,
        # ocasionando que selenium lo detecte y lo marque como que si esta presente
        # cuando en realidad puede que lo querramos presente mas tiempo
        return check_if_appears_element(self.driver, self.searching_vehicle_modal_locator, search_timeout,
                                          minimum_visibility_time)

    # Métodos para obtener la informacion del conductor encontrado
    def wait_for_driver_info(self, additional_secs=1):
        time_str = get_element_text(self.wait, self.driver_arrival_time_label_locator)
        arrival_time_in_seconds = parse_to_seconds(time_str)
        total_timeout = arrival_time_in_seconds + additional_secs
        WebDriverWait(self.driver, total_timeout).until(
            EC.visibility_of_element_located(self.driver_name_field_locator))
    def get_driver_rating(self):
        return get_element_text(self.wait, self.driver_rating_field_locator)
    def get_driver_img_url(self):
        return self.wait.until(EC.visibility_of_element_located(self.driver_img_field_locator)).get_attribute('src')
    def get_driver_name(self):
        return get_element_text(self.wait, self.driver_name_field_locator)