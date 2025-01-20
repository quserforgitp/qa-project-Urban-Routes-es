import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Funciones genericas para interactuar con los elementos de una pagina
def click_on_element(wait, visual_review_timeout, element_locator):
    wait.until(EC.element_to_be_clickable(element_locator)).click()
    confirm_and_trigger_visual_review_timeout(visual_review_timeout)
def click_on_element_multiple_times(wait, visual_review_timeout, locator, times=1):
    element = wait.until(EC.element_to_be_clickable(locator))
    for _ in range(times):
        element.click()

    confirm_and_trigger_visual_review_timeout(visual_review_timeout)
def set_element_text(wait, visual_review_timeout, element_locator, text):
    wait.until(EC.visibility_of_element_located(element_locator)).send_keys(text)
    confirm_and_trigger_visual_review_timeout(visual_review_timeout)
def get_element_text(wait, element_locator):
    element = wait.until(EC.visibility_of_element_located(element_locator))

    text = element.text
    if text:
        return text

    text = element.get_property('value')

    if text:
        return text

    return ""
def scroll_into_element(wait, driver, visual_review_timeout, element_locator):
    element = wait.until(EC.visibility_of_element_located(element_locator))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    confirm_and_trigger_visual_review_timeout(visual_review_timeout)
def scroll_into_and_click_on_element(wait, driver, visual_review_timeout, element_locator):
    scroll_into_element(wait, driver, visual_review_timeout, element_locator)
    click_on_element(wait, visual_review_timeout, element_locator)

# Funciones de espera y comprobacion
def wait_for_visual_review(visual_review_timeout):
    time.sleep(visual_review_timeout)
def confirm_and_trigger_visual_review_timeout(visual_review_timeout):
    if visual_review_timeout > 0:
        wait_for_visual_review(visual_review_timeout)
def check_if_appears_element(driver, element_locator, search_timeout=5, minimum_element_visibility_time=2):
    # El minimum_element_visibility_time es para comprobar que el elemento se muestre en pantalla como minimo x segundos,
    # ya que hay casos en los que el elemento aparece, pero desaparece inmediatamente,
    # ocasionando que selenium lo detecte y lo marque como que si esta presente
    # cuando en realidad puede que lo querramos presente mas tiempo

    # si no requerimos comprobar que el elemento esta presente como minimo x segundos
    if minimum_element_visibility_time == 0:
        try:
            WebDriverWait(driver, search_timeout).until(EC.visibility_of_element_located(element_locator))
        except TimeoutException:
            return False
        return True

    initial_time = time.time()

    # si requerimos comprobar que el elemento este presente como minimo x cantidad de segundos
    try:
        # comprobar permanencia del elemento localizandolo
        while time.time() - initial_time < minimum_element_visibility_time:
            WebDriverWait(driver, search_timeout).until(EC.visibility_of_element_located(element_locator))
    except TimeoutException:
        return False
    return True


# Funciones para manipular LocalStorage y cookies
def clear_local_storage(driver):
    driver.execute_script("window.localStorage.clear();")