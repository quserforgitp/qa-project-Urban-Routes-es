import data
from selenium import webdriver

from helpers.pom_helpers import clear_local_storage
from urban_routes_page import UrbanRoutesPage
from helpers.util_helpers import retrieve_phone_code

class TestUrbanRoutes:

    driver = None

    SEARCH_TIMEOUT = 5 # tiempo de espera maximo para localizar elementos (por lo menos VISUAL_TIMEOUT + 1)
    VISUAL_TIME0UT = 0 # tiempo para visualizacion de acciones en pantalla

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
        assert routes_page.get_from() == address_from, f'La direccion en el campo "Desde" deberia ser "{address_from}"'
        assert routes_page.get_to() == address_to, f'La direccion en el campo "Hasta" deberia ser "{address_from}"'

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
        clear_local_storage(routes_page.driver)

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
        clear_local_storage(routes_page.driver)

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

        # Recupera el numero de telefono que aparece en el input dentro del modal
        setted_phone_number_on_modal_input_field = routes_page.get_phone_number_from_field_on_modal()

        assert setted_phone_number_on_modal_input_field == data.phone_number, f'El numero de telefono en el input dentro del modal deberia ser "{data.phone_number}"'

        # Hace clic en el botón de envío del número de teléfono.
        routes_page.click_on_submit_phone_number_btn()

        # Recupera el código de verificación del teléfono desde el sitio web.
        phone_code = retrieve_phone_code(self.driver)

        # Establece el código de teléfono obtenido anteriormente.
        routes_page.set_phone_code(phone_code)

        # Hace clic en el botón de envío del código de teléfono.
        routes_page.click_on_submit_phone_code_btn()

        # Recupera el numero de telefono que aparece en el campo del numero de telefono del panel de configuracion del viaje
        setted_phone_number_on_button = routes_page.get_phone_number_from_btn()


        assert setted_phone_number_on_button == data.phone_number, f'El numero de telefono en el campo del numero de telefono del panel de configuracion del viaje deberia ser "{data.phone_number}"'

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
        clear_local_storage(routes_page.driver)

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
        # Recupera el numero de la tarjeta que aparece en el campo
        actual_card_number = routes_page.get_card_number()
        assert actual_card_number == data.card_number, f'El numero de la tarjeta en el input del modal para agregar tarjetas deberia ser "{data.card_number}"'

        routes_page.set_card_code(data.card_code)
        # Recupera el codigo (CVV) de la tarjeta que aparece en el campo
        actual_card_code = routes_page.get_card_code()
        assert actual_card_code == data.card_code, f'El codigo (CVV) de la tarjeta en el input del modal para agregar tarjetas deberia ser "{data.card_code}"'

        # Click en el boton Confirmar del modal para agregar en tarjetas
        routes_page.click_on_submit_new_card_btn(send_tab_to_remove_focus=True)
        # Click en la equis para cerrar el modal para agregar tarjetas
        routes_page.click_on_close_add_card_modal_btn()

        setted_text_on_payment_method_btn = routes_page.get_type_of_setted_payment_method_from_payment_method_btn()

        assert setted_text_on_payment_method_btn == 'Tarjeta' , f'El metodo de pago establecido en el campo de Metodo de Pago del panel de configuracion del viaje deberia de ser "Tarjeta"'


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
        clear_local_storage(routes_page.driver)

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
        clear_local_storage(routes_page.driver)

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
        clear_local_storage(routes_page.driver)

        # Establece la ruta de la prueba, con la dirección de origen y destino proporcionadas en los datos.
        routes_page.set_route(data.address_from, data.address_to)

        # Hace clic en el botón "Llamar un taxi".
        routes_page.click_on_call_a_taxi_btn()

        # Hace clic en la tarjeta de tarifa "comfort" para seleccionar el tipo de tarifa.
        routes_page.click_on_comfort_tariff_card()

        # Hace clic en el botón para aumentar el contador de helados dos veces, sin retraso entre clics.
        routes_page.clicks_on_icecream_increase_counter_btn(times=2)

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
        clear_local_storage(routes_page.driver)

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

        # Verifica si aparece el modal de "buscando vehículo", con un tiempo de espera máximo de 2 segundos y comprobando que siga presente por al menos 2 seg.
        modal_is_present = routes_page.check_if_appears_searching_vehicle_modal(search_timeout=2, minimum_visibility_time=2)

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
        clear_local_storage(routes_page.driver)

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

        # Verifica si aparece el modal de "buscando vehículo", con un tiempo de espera máximo de 2 segundos y comprobando que siga presente por al menos 2 seg.
        modal_is_present = routes_page.check_if_appears_searching_vehicle_modal(search_timeout=2, minimum_visibility_time=2)

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
        clear_local_storage(routes_page.driver)

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
        routes_page.clicks_on_icecream_increase_counter_btn(times=2)

        # Hace clic en el botón para llamar al vehículo.
        routes_page.click_on_call_the_vehicle_btn()

        # Verifica si aparece el modal de "buscando vehículo", con un tiempo de espera máximo de 2 segundos y comprobando que siga presente por al menos 2 seg.
        modal_is_present = routes_page.check_if_appears_searching_vehicle_modal(search_timeout=2, minimum_visibility_time=2)

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