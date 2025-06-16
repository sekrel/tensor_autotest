import pytest
import os
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.usefixtures("setup")
class TestSaby:
    def test_saby(self, setup):
        driver = setup
        wait = WebDriverWait(driver, 15)
        driver.get("https://saby.ru")

        #Работа с контактами на saby
        wait.until(EC.element_to_be_clickable(("class name", "sbisru-Header-ContactsMenu"))).click()
        wait.until(EC.element_to_be_clickable(("xpath", "//div[@class='sbisru-Header-ContactsMenu__items sbisru-Header-ContactsMenu__items-visible']//a[@class='sbisru-link sbis_ru-link']"))).click()

        #переход по логотипу компании на сайт тензора
        wait.until(EC.element_to_be_clickable(("class name", "sbisru-Contacts__logo-tensor"))).click()
        #переход на другую вкладку
        original_window = driver.current_window_handle
        list_window = driver.window_handles
        list_window.remove(original_window)
        driver.close()
        driver.switch_to.window(list_window[0])

        assert driver.current_url == "https://tensor.ru/", "Не прошел перехд на tensor.ru"

        # Проверка наличия блока сила в людях
        wait.until(EC.presence_of_element_located(("xpath", "//*[text()='Сила в людях']")))

        #Переход в подробнее 
        wait.until(EC.element_to_be_clickable(("xpath", "//div[@class='tensor_ru-Index__block4-content tensor_ru-Index__card']//a"))).click()
        assert driver.current_url == "https://tensor.ru/about", "Не прошел перехд на https://tensor.ru/about"

        lst_img = driver.find_elements("xpath","//div[@class='tensor_ru-container tensor_ru-section tensor_ru-About__block3']//img")
        width = lst_img[0].get_attribute("width")
        height = lst_img[0].get_attribute("height")
        for i in lst_img[1:]:
            assert i.get_attribute("width")== width and i.get_attribute("height") == height, "размер картинок разный"


    def test_saby_second(self, setup):
        driver = setup
        wait = WebDriverWait(driver, 15)
        driver.get("https://saby.ru/contacts/")

        try:
            block = wait.until(EC.presence_of_element_located(("xpath", "//span[@class='sbis_ru-Region-Chooser ml-16 ml-xm-0']//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")))
            assert block.is_displayed(), "Блок с текущим регионом присутствует, но не виден на странице"
        except Exception as e:
            pytest.fail(str(e))

        try:
            partner_block = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='sbisru-Contacts-List__col ws-flex-shrink-1 ws-flex-grow-1']")))
            assert partner_block.is_displayed(), "Блок с партнерами присутствует, но не виден на странице"
        except Exception as e:
            pytest.fail(str(e))

        wait.until(EC.element_to_be_clickable(("xpath", "//span[@class='sbis_ru-Region-Chooser ml-16 ml-xm-0']//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']"))).click()
        reg = "Камчатский край"
        wait.until(EC.element_to_be_clickable(("xpath", f"//span[@title='{reg}']"))).click()

        try:
            block = wait.until(EC.presence_of_element_located(("xpath", f"//span[@class='sbis_ru-Region-Chooser ml-16 ml-xm-0']//span[contains(@class, 'sbis_ru-Region-Chooser__text') and contains(text(), reg)]")))
            assert block.is_displayed(), "Блок присутствует, но не виден на странице"
        except Exception as e:
            pytest.fail(str(e))

        try:
            block = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='sbisru-Contacts-List__col ws-flex-shrink-1 ws-flex-grow-1']")))
            assert block.is_displayed(), "Блок присутствует, но не виден на странице"
            assert block == partner_block, "Блок партнеров не изменился"
            assert "41-kamchatskij-kraj" in driver.current_url, "url не изменился при переходе"
            assert "Камчатский край" in driver.title  , "title не изменился при переходе"
        except Exception as e:
            pytest.fail(str(e))


    def test_saby_download(self, setup):
        driver = setup
        wait = WebDriverWait(driver, 15)
        driver.get("https://saby.ru/")
        wait.until(EC.element_to_be_clickable(("xpath", "//*[text()='Скачать локальные версии']"))).click()
        #скачивание файла плагина
        download = wait.until(EC.element_to_be_clickable(("xpath", "//*[@class='sbis_ru-DownloadNew-flex__child sbis_ru-DownloadNew-flex__child--width-1']")))
        download.click()
        size_download = float(re.search(r'\d+\.\d+', download.text).group()) # получение размера файла с сайта
        file_path = "downloads/saby-setup-web.exe"
        file_size = float(round(os.path.getsize(file_path)/1024/1024, 2)) # Размер в мб
        assert file_size == size_download, f"размер файла не соответствует заявленному {file_size} == {size_download}"
