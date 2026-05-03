import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://libros-web:5000"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

class LibrosAppTests(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()

    def tearDown(self):
        self.driver.quit()

    # Test 1: Home page loads successfully
    def test_01_home_page_loads(self):
        self.driver.get(BASE_URL)
        self.assertIn("Formulario de Libros", self.driver.page_source)

    # Test 2: Page title is correct
    def test_02_page_title(self):
        self.driver.get(BASE_URL)
        self.assertIn("Formulario de Libros", self.driver.title)

    # Test 3: Form is present on home page
    def test_03_form_present(self):
        self.driver.get(BASE_URL)
        form = self.driver.find_element(By.TAG_NAME, "form")
        self.assertIsNotNone(form)

    # Test 4: Form action points to /registrar_libro
    def test_04_form_action(self):
        self.driver.get(BASE_URL)
        form = self.driver.find_element(By.TAG_NAME, "form")
        self.assertIn("registrar_libro", form.get_attribute("action"))

    # Test 5: Titulo field is present
    def test_05_titulo_field_present(self):
        self.driver.get(BASE_URL)
        field = self.driver.find_element(By.NAME, "titulo")
        self.assertIsNotNone(field)

    # Test 6: Autor field is present
    def test_06_autor_field_present(self):
        self.driver.get(BASE_URL)
        field = self.driver.find_element(By.NAME, "autor")
        self.assertIsNotNone(field)

    # Test 7: Genero field is present
    def test_07_genero_field_present(self):
        self.driver.get(BASE_URL)
        field = self.driver.find_element(By.NAME, "genero")
        self.assertIsNotNone(field)

    # Test 8: Anio publicacion field is present
    def test_08_anio_field_present(self):
        self.driver.get(BASE_URL)
        field = self.driver.find_element(By.NAME, "anio_publicacion")
        self.assertIsNotNone(field)

    # Test 9: Editorial field is present
    def test_09_editorial_field_present(self):
        self.driver.get(BASE_URL)
        field = self.driver.find_element(By.NAME, "editorial")
        self.assertIsNotNone(field)

    # Test 10: Submit button is present
    def test_10_submit_button_present(self):
        self.driver.get(BASE_URL)
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertIsNotNone(button)

    # Test 11: Submit button has correct text
    def test_11_submit_button_text(self):
        self.driver.get(BASE_URL)
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertEqual("Registrar Libro", button.text)

    # Test 12: Bootstrap CSS is loaded
    def test_12_bootstrap_loaded(self):
        self.driver.get(BASE_URL)
        self.assertIn("bootstrap", self.driver.page_source.lower())

    # Test 13: Successfully register a book
    def test_13_register_book_success(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("Selenium Test Book")
        self.driver.find_element(By.NAME, "autor").send_keys("Selenium Author")
        self.driver.find_element(By.NAME, "genero").send_keys("Testing")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2024")
        self.driver.find_element(By.NAME, "editorial").send_keys("Test Publisher")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Libro registrado con", self.driver.page_source)

    # Test 14: Success page shows correct message
    def test_14_success_message(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("Book For Success Test")
        self.driver.find_element(By.NAME, "autor").send_keys("Author Success")
        self.driver.find_element(By.NAME, "genero").send_keys("Drama")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2023")
        self.driver.find_element(By.NAME, "editorial").send_keys("Drama Press")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("xito", self.driver.page_source)

    # Test 15: Success page has back link to home
    def test_15_success_page_back_link(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("Book Back Link Test")
        self.driver.find_element(By.NAME, "autor").send_keys("Author Back")
        self.driver.find_element(By.NAME, "genero").send_keys("Fiction")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2022")
        self.driver.find_element(By.NAME, "editorial").send_keys("Fiction Press")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        link = self.driver.find_element(By.LINK_TEXT, "Volver al formulario")
        self.assertIsNotNone(link)

    # Test 16: Back link on success page navigates to home
    def test_16_back_link_navigates_home(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("Book Nav Test")
        self.driver.find_element(By.NAME, "autor").send_keys("Author Nav")
        self.driver.find_element(By.NAME, "genero").send_keys("History")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2021")
        self.driver.find_element(By.NAME, "editorial").send_keys("History Press")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Volver al formulario").click()
        time.sleep(1)
        self.assertIn("Formulario de Libros", self.driver.page_source)

    # Test 17: Registered book appears in table on home page
    def test_17_book_appears_in_table(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("Unique Selenium Book 12345")
        self.driver.find_element(By.NAME, "autor").send_keys("Unique Author")
        self.driver.find_element(By.NAME, "genero").send_keys("Science")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2020")
        self.driver.find_element(By.NAME, "editorial").send_keys("Science Press")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.driver.get(BASE_URL)
        self.assertIn("Unique Selenium Book 12345", self.driver.page_source)

    # Test 18: Table has correct column headers
    def test_18_table_headers(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("Header Test Book")
        self.driver.find_element(By.NAME, "autor").send_keys("Header Author")
        self.driver.find_element(By.NAME, "genero").send_keys("General")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2019")
        self.driver.find_element(By.NAME, "editorial").send_keys("General Press")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.driver.get(BASE_URL)
        self.assertIn("Título", self.driver.page_source)
        self.assertIn("Autor", self.driver.page_source)
        self.assertIn("Editorial", self.driver.page_source)

    # Test 19: Titulo field accepts text input
    def test_19_titulo_accepts_input(self):
        self.driver.get(BASE_URL)
        field = self.driver.find_element(By.NAME, "titulo")
        field.send_keys("Testing Input")
        self.assertEqual("Testing Input", field.get_attribute("value"))

    # Test 20: All five fields accept input
    def test_20_all_fields_accept_input(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.NAME, "titulo").send_keys("All Fields Book")
        self.driver.find_element(By.NAME, "autor").send_keys("All Fields Author")
        self.driver.find_element(By.NAME, "genero").send_keys("All Fields Genre")
        self.driver.find_element(By.NAME, "anio_publicacion").send_keys("2018")
        self.driver.find_element(By.NAME, "editorial").send_keys("All Fields Press")
        self.assertEqual("All Fields Book", self.driver.find_element(By.NAME, "titulo").get_attribute("value"))
        self.assertEqual("All Fields Author", self.driver.find_element(By.NAME, "autor").get_attribute("value"))
        self.assertEqual("All Fields Genre", self.driver.find_element(By.NAME, "genero").get_attribute("value"))

if __name__ == "__main__":
    unittest.main()
